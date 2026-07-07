import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket connected for simulation streaming.")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket disconnected.")

    async def broadcast_result(self, scenario_id: str, payload: dict):
        message = json.dumps({"scenario_id": scenario_id, "data": payload})
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WS: {e}")

manager = ConnectionManager()

@router.websocket("/ws")
async def simulation_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for live simulation streaming.
    The frontend connects here to receive real-time updates as the PINN
    model converges and produces spatial temperature/AQI deltas.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Wait for any messages from the client (e.g., ping or scenario ID subscription)
            data = await websocket.receive_text()
            logger.debug(f"Received WS message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
