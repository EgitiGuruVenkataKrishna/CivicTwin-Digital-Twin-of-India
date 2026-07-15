import os
import time

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CivicTwin PINN Inference API")

# Path to the exported TorchScript model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'pinn_v1.pt')

try:
    if os.path.exists(MODEL_PATH):
        model = torch.jit.load(MODEL_PATH)
        # Set to train mode to keep Dropout active for MC-Dropout uncertainty quantification
        model.train()
    else:
        model = None
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

class InferenceRequest(BaseModel):
    grid_data: list[dict]
    scenario_params: dict
    model_version: str = "latest"

class InferenceResponse(BaseModel):
    predictions: list[dict]
    model_version: str
    inference_time_ms: float

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        start_time = time.time()
        
        # Parse grid inputs to tensor
        inputs = []
        for cell in request.grid_data:
            lat = cell.get("lat", 0.0)
            lon = cell.get("lon", 0.0)
            # Pass lat, lon, and default t=0.5
            inputs.append([lat, lon, 0.5])
            
        if not inputs:
            # Default fallback if empty input
            inputs = [[17.3850, 78.4867, 0.5]]

        # Convert request inputs to tensor of shape [batch_size, 3]
        x_tensor = torch.tensor(inputs, dtype=torch.float32)

        mc_samples = 5
        predictions = []

        # Perform forward passes with dropout active
        with torch.no_grad():
            for _ in range(mc_samples):
                pred = model(x_tensor)
                predictions.append(pred)

        # Stack shape: [mc_samples, batch_size, 2]
        preds_stack = torch.stack(predictions)

        # Calculate mean (prediction) and variance (uncertainty)
        mean_preds = torch.mean(preds_stack, dim=0)
        var_preds = torch.var(preds_stack, dim=0)

        predictions_out = []
        for idx, cell in enumerate(request.grid_data):
            pred_temp = mean_preds[idx, 0].item()
            pred_aqi = mean_preds[idx, 1].item()
            
            # Map predictions to realistic range
            temp_val = 20.0 + pred_temp * 20.0
            aqi_val = 30.0 + pred_aqi * 300.0
            
            # Confidence based on variance
            var_temp = var_preds[idx, 0].item()
            var_aqi = var_preds[idx, 1].item()
            confidence = max(0.1, min(0.99, 1.0 - (var_temp + var_aqi) / 2.0))
            
            predictions_out.append({
                "lat": cell.get("lat", 17.3850),
                "lon": cell.get("lon", 78.4867),
                "predicted_temp": temp_val,
                "predicted_aqi": aqi_val,
                "confidence": confidence
            })

        duration_ms = (time.time() - start_time) * 1000.0

        return InferenceResponse(
            predictions=predictions_out,
            model_version="pinn_v1_torchscript",
            inference_time_ms=duration_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

