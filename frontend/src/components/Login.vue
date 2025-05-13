<template>
  <div class="login-container" data-aos="fade-in">
    <div class="login-card animate__animated animate__fadeIn">
      <h2 class="app-title"><i class="fas fa-heartbeat text-primary"></i> Student Health Assistant</h2>
      <h3 class="animate__animated animate__slideInDown">Login</h3>
      
      <div v-if="error" class="error-message animate__animated animate__shakeX">
        <i class="fas fa-exclamation-circle mr-2"></i> {{ error }}
      </div>
      
      <form @submit.prevent="login" class="animate__animated animate__fadeIn animate__delay-1s">
        <div class="form-group">
          <label for="username"><i class="fas fa-user"></i> Username:</label>
          <input 
            type="text" 
            id="username" 
            class="form-control-modern" 
            v-model="username" 
            required 
            placeholder="Enter your username"
          >
        </div>
        <div class="form-group">
          <label for="password"><i class="fas fa-lock"></i> Password:</label>
          <input 
            type="password" 
            id="password" 
            class="form-control-modern" 
            v-model="password" 
            required
            placeholder="Enter your password"
          >
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-modern login-btn" :disabled="isLoading">
            <i class="fas fa-sign-in-alt mr-2"></i> {{ isLoading ? 'Logging in...' : 'Login' }}
          </button>
          <div class="register-link">
            <p>Don't have an account? <router-link to="/register" class="animated-link">Register</router-link></p>
          </div>
          <div class="admin-link">
            <a href="http://localhost:8000/admin" target="_blank" class="animated-link">
              <i class="fas fa-user-shield"></i> Admin Dashboard
            </a>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { djangoApi, setAuthToken } from '../utils/api';

export default {
  name: 'LoginComponent',
  data() {
    return {
      username: '',
      password: '',
      error: null,
      isLoading: false
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log('Attempting login to:', `${djangoApi.defaults.baseURL}/api/token/`);
        console.log('Login data:', { username: this.username, password: '***' });
        
        const response = await djangoApi.post('/api/token/', 
          {
            username: this.username,
            password: this.password
          },
          {
            headers: {
              'Content-Type': 'application/json'
            },
            withCredentials: false // Don't send credentials for this request
          }
        );
        
        console.log('Login success:', response.data);
        
        // Success - store token and redirect
        if (response.data.token) {
          setAuthToken(response.data.token);
          this.$router.push('/dashboard');
        } else {
          this.error = 'No token received from server';
        }
      } catch (error) {
        console.error('Login error details:', error);
        
        if (error.response) {
          console.error('Error response:', error.response.status, error.response.data);
          
          // Show the actual error message from the server
          if (error.response.data && error.response.data.error) {
            this.error = error.response.data.error;
          } else if (typeof error.response.data === 'object') {
            this.error = JSON.stringify(error.response.data);
          } else {
            this.error = error.response.data || 'Login failed. Please check your credentials.';
          }
        } else if (error.request) {
          // Request made but no response received
          this.error = 'Server not responding. Please try again later.';
        } else {
          this.error = 'Login failed: ' + error.message;
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
  background-image: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  overflow: hidden;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
}

.app-title {
  color: var(--dark-color);
  margin-bottom: 0.75rem;
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
}

.app-title i {
  margin-right: 8px;
  color: var(--primary-color);
}

h3 {
  color: var(--primary-color);
  margin-bottom: 1.8rem;
  text-align: center;
  font-size: 1.4rem;
  font-weight: 600;
}

.error-message {
  background-color: #fff3f3;
  color: var(--danger-color);
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  border-left: 4px solid var(--danger-color);
  display: flex;
  align-items: center;
}

.error-message i {
  margin-right: 10px;
  font-size: 1.1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.6rem;
  font-weight: 600;
  color: var(--dark-color);
  opacity: 0.8;
  font-size: 0.95rem;
}

label i {
  margin-right: 8px;
  color: var(--primary-color);
}

.form-control-modern {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: #f9fafc;
}

.form-control-modern:focus {
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
  border-color: var(--primary-color);
  background-color: #fff;
}

.login-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  padding: 0.9rem 1.2rem;
  font-size: 1rem;
  cursor: pointer;
  width: 100%;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.login-btn:hover {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  transform: translateY(-3px);
}

.login-btn:disabled {
  background: linear-gradient(135deg, #a0a0a0, #c0c0c0);
  cursor: not-allowed;
  transform: none;
}

.mr-2 {
  margin-right: 8px;
}

.form-actions {
  margin-top: 2rem;
}

.register-link, .admin-link {
  margin-top: 1.2rem;
  text-align: center;
}

.animated-link {
  color: var(--primary-color);
  text-decoration: none;
  position: relative;
  font-weight: 600;
  transition: all 0.2s ease;
}

.animated-link:after {
  content: '';
  position: absolute;
  width: 100%;
  height: 2px;
  bottom: -2px;
  left: 0;
  background-color: var(--accent-color);
  transform: scaleX(0);
  transform-origin: bottom right;
  transition: transform 0.3s;
}

.animated-link:hover {
  color: var(--accent-color);
}

.animated-link:hover:after {
  transform: scaleX(1);
  transform-origin: bottom left;
}

.admin-link {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.admin-link a {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Animation classes */
.animate__animated {
  animation-duration: 0.8s;
}

.animate__delay-1s {
  animation-delay: 0.3s;
}
</style>