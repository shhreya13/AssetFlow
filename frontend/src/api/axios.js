import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Navya's backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to all requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;