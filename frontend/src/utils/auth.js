// Auth helper functions
import { djangoApi } from './api';

/**
 * Set the authentication token in axios and localStorage
 * @param {string} token - The authentication token
 */
export const setAuthToken = (token) => {
  if (token) {
    // Set token in localStorage
    localStorage.setItem('token', token);
    
    // Set authorization header for all future requests
    djangoApi.defaults.headers.common['Authorization'] = `Token ${token}`;
    
    // Log success
    console.log('Auth token set successfully');
    return true;
  } else {
    // Remove token from localStorage
    localStorage.removeItem('token');
    
    // Remove authorization header
    delete djangoApi.defaults.headers.common['Authorization'];
    
    // Log removal
    console.log('Auth token removed');
    return false;
  }
};

/**
 * Check if the user is authenticated
 * @returns {boolean} - True if authenticated, false otherwise
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

/**
 * Get the current token
 * @returns {string|null} - The current token or null
 */
export const getToken = () => {
  return localStorage.getItem('token');
};

/**
 * Initialize authentication from localStorage on app start
 */
export const initAuth = () => {
  const token = localStorage.getItem('token');
  if (token) {
    djangoApi.defaults.headers.common['Authorization'] = `Token ${token}`;
    return true;
  }
  return false;
};

// Initialize on import
initAuth(); 