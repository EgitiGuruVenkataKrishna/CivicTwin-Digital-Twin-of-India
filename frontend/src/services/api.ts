import axios from 'axios';

const getBaseUrl = () => {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const backendHost = isLocal ? `${window.location.hostname}:8000` : window.location.host;
  const protocol = window.location.protocol === 'https:' ? 'https' : 'http';
  return `${protocol}://${backendHost}/api/v1`;
};

const getWsUrl = () => {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const backendHost = isLocal ? `${window.location.hostname}:8000` : window.location.host;
  const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  return `${wsProtocol}://${backendHost}/api/v1`;
};

const API_BASE_URL = getBaseUrl();
const WS_BASE_URL = getWsUrl();

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const runScenario = async (payload: any) => {
  const response = await apiClient.post('/scenarios/run', payload);
  return response.data;
};

export class SimulationWebSocket {
  private ws: WebSocket | null = null;
  private onMessageCallback: ((data: any) => void) | null = null;

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  connect() {
    this.ws = new WebSocket(`${WS_BASE_URL}/simulation/ws`);
    
    this.ws.onopen = () => {
      console.log('WebSocket Connected');
    };

    this.ws.onmessage = (event) => {
      if (this.onMessageCallback) {
        this.onMessageCallback(JSON.parse(event.data));
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket Disconnected');
    };
  }

  onMessage(callback: (data: any) => void) {
    this.onMessageCallback = callback;
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

export const simulationWs = new SimulationWebSocket();
