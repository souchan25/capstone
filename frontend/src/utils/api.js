import axios from 'axios';

// Base URLs for the APIs
export const DJANGO_BASE_URL = 'http://localhost:8000';
export const RASA_BASE_URL = 'http://localhost:5005';

// Create API instances with specific base URLs
export const djangoApi = axios.create({
  baseURL: DJANGO_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  // Don't use withCredentials by default to avoid CORS preflight issues
  withCredentials: false,
  timeout: 10000 // 10 seconds timeout
});

export const rasaApi = axios.create({
  baseURL: RASA_BASE_URL,
  timeout: 10000 // 10 seconds timeout
});

// Add a request interceptor to add logging
djangoApi.interceptors.request.use(
  config => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  error => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor for error handling
djangoApi.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // The request was made and the server responded with an error status
      console.error(`API Error ${error.response.status}:`, error.response.data);
      
      // If 401 Unauthorized, clear auth token
      if (error.response.status === 401) {
        console.warn('Unauthorized request detected - clearing auth token');
        localStorage.removeItem('token');
        delete djangoApi.defaults.headers.common['Authorization'];
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('API No Response Error:', error.request);
    } else {
      // Something else caused the error
      console.error('API Setup Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Set auth token for Django API
export const setAuthToken = (token) => {
  if (token) {
    djangoApi.defaults.headers.common['Authorization'] = `Token ${token}`;
    localStorage.setItem('token', token);
  } else {
    delete djangoApi.defaults.headers.common['Authorization'];
    localStorage.removeItem('token');
  }
};

// Initialize token from localStorage
const token = localStorage.getItem('token');
if (token) {
  setAuthToken(token);
}

// Health check functions
export const checkDjangoHealth = async () => {
  try {
    const response = await djangoApi.get('/api/health/');
    return { 
      status: 'online',
      details: response.data
    };
  } catch (error) {
    return { 
      status: 'offline',
      error: error.message
    };
  }
};

export const checkRasaHealth = async () => {
  try {
    const response = await rasaApi.get('/status');
    return { 
      status: 'online',
      details: response.data
    };
  } catch (error) {
    return { 
      status: 'offline',
      error: error.message
    };
  }
};

// Direct disease prediction API
export const predictDisease = async (symptoms) => {
  const response = await djangoApi.post('/api/predict-disease/', { symptoms });
  return response.data;
};

// Rasa chat API
export const sendChatMessage = async (message, senderId = 'user') => {
  const response = await rasaApi.post('/webhooks/rest/webhook', {
    sender: senderId,
    message: message
  });
  return response.data;
};

// User profile API
export const getUserProfile = async () => {
  try {
    console.log('Fetching user profile...');
    const response = await djangoApi.get('/api/profile/');
    console.log('Profile data received:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    if (error.response && error.response.status === 401) {
      // If unauthorized, redirect to login
      window.location.href = '/login';
    }
    throw error;
  }
};

export const updateUserProfile = async (profileData) => {
  const response = await djangoApi.patch('/api/user/profile/', profileData);
  return response.data;
};