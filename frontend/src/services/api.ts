import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const api = {
  getItems: () => axios.get(`${API_URL}/items`),
  getItem: (id: string) => axios.get(`${API_URL}/items/${id}`),
  getPriceHistory: (id: string) => axios.get(`${API_URL}/prices/${id}/history`),
};