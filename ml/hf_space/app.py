import os

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
    inputs: list[list[float]]

class InferenceResponse(BaseModel):
    predictions: list[list[float]]
    uncertainty: list[list[float]]

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        # Convert request inputs to tensor of shape [batch_size, 3]
        x_tensor = torch.tensor(request.inputs, dtype=torch.float32)

        mc_samples = 5
        predictions = []

        # Perform 5 forward passes with dropout active
        with torch.no_grad():
            for _ in range(mc_samples):
                pred = model(x_tensor)
                predictions.append(pred)

        # Stack shape: [mc_samples, batch_size, 2]
        preds_stack = torch.stack(predictions)

        # Calculate mean (prediction) and variance (uncertainty)
        mean_preds = torch.mean(preds_stack, dim=0)
        var_preds = torch.var(preds_stack, dim=0)

        return InferenceResponse(
            predictions=mean_preds.tolist(),
            uncertainty=var_preds.tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health():
    return {"status": "healthy", "model_loaded": model is not None}
