<template>
  <div class="register-container" data-aos="fade-in">
    <div class="register-card animate__animated animate__fadeIn">
      <h2 class="app-title"><i class="fas fa-heartbeat text-primary"></i> Student Health Assistant</h2>
      <h3 class="animate__animated animate__slideInDown">Register</h3>
      
      <div v-if="error" class="error-message animate__animated animate__shakeX">
        <i class="fas fa-exclamation-circle mr-2"></i> {{ error }}
      </div>
      
      <div v-if="success" class="success-message animate__animated animate__fadeIn">
        <i class="fas fa-check-circle mr-2"></i> {{ success }}
      </div>
      
      <form @submit.prevent="register" class="animate__animated animate__fadeIn animate__delay-1s">
        <div class="form-group">
          <label for="username"><i class="fas fa-user"></i> Username:</label>
          <input 
            type="text" 
            id="username" 
            class="form-control-modern" 
            v-model="formData.username" 
            required
            placeholder="Choose a username"
          >
        </div>
        <div class="form-group">
          <label for="school_id"><i class="fas fa-id-card"></i> School ID:</label>
          <input 
            type="text" 
            id="school_id" 
            class="form-control-modern" 
            v-model="formData.school_id" 
            required
            placeholder="Enter your school ID"
          >
        </div>
        <div class="form-row">
          <div class="form-group half">
            <label for="first_name"><i class="fas fa-user-edit"></i> First Name:</label>
            <input 
              type="text" 
              id="first_name" 
              class="form-control-modern" 
              v-model="formData.first_name" 
              required
              placeholder="Your first name"
            >
          </div>
          <div class="form-group half">
            <label for="last_name"><i class="fas fa-user-edit"></i> Last Name:</label>
            <input 
              type="text" 
              id="last_name" 
              class="form-control-modern" 
              v-model="formData.last_name" 
              required
              placeholder="Your last name"
            >
          </div>
        </div>
        <div class="form-group">
          <label for="email"><i class="fas fa-envelope"></i> Email:</label>
          <input 
            type="email" 
            id="email" 
            class="form-control-modern" 
            v-model="formData.email" 
            required
            placeholder="Your email address"
          >
        </div>
        <div class="form-group">
          <label for="dob"><i class="fas fa-calendar-alt"></i> Date of Birth:</label>
          <input 
            type="date" 
            id="dob" 
            class="form-control-modern" 
            v-model="formData.date_of_birth"
          >        </div>
        <div class="form-group">
          <label for="password"><i class="fas fa-lock"></i> Password:</label>
          <input 
            type="password" 
            id="password" 
            class="form-control-modern" 
            v-model="formData.password" 
            required
            placeholder="Create a secure password"
          >
        </div>
        <div class="form-group consent-checkbox">
          <div class="checkbox-wrapper">
            <input type="checkbox" id="consent" v-model="formData.share_data_consent">
            <span class="custom-checkbox">
              <i class="fas fa-check"></i>
            </span>
            <label for="consent">
              I consent to sharing my health data with university clinic staff for better care
            </label>
          </div>
          <p class="consent-info">
            <i class="fas fa-info-circle"></i> This helps us provide you with better healthcare services
          </p>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-modern register-btn" :disabled="isLoading">
            <i class="fas fa-user-plus mr-2"></i> {{ isLoading ? 'Registering...' : 'Register' }}
          </button>
          <div class="login-link">
            <p>Already have an account? <router-link to="/login" class="animated-link">Login</router-link></p>
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
  name: 'RegisterComponent',
  data() {
    return {
      formData: {
        username: '',
        school_id: '',
        first_name: '',
        last_name: '',
        email: '',
        date_of_birth: '',
        password: '',
        share_data_consent: false
      },
      error: null,
      success: null,
      isLoading: false
    };
  },
  methods: {
    async register() {
      this.isLoading = true;
      this.error = null;
      this.success = null;
      
      try {
        console.log('Sending registration data:', { 
          ...this.formData, 
          password: '***' // Mask password in logs
        });
        
        const response = await djangoApi.post('/api/register/', this.formData, {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: false // Don't send credentials for this request
        });
        
        console.log('Registration successful:', response.data);
        
        // Show success message
        this.success = 'Registration successful! You can now login.';
        
        // If a token is returned, we can auto-login the user
        if (response.data.token) {
          // Store the token
          localStorage.setItem('token', response.data.token);
          
          // Set auth header
          setAuthToken(response.data.token);
          
          // Redirect to dashboard after 1 second
          setTimeout(() => {
            this.$router.push('/dashboard');
          }, 1000);
        } else {
          // Otherwise redirect to login after 2 seconds
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000);
        }
        
        // Reset form
        this.formData = {
          username: '',
          school_id: '',
          first_name: '',
          last_name: '',
          email: '',
          date_of_birth: '',
          password: '',
          share_data_consent: false
        };
        
      } catch (err) {
        console.error('Registration error:', err);
        
        if (err.response) {
          console.error('Error response:', err.response.status, err.response.data);
          
          if (err.response.data.error) {
            this.error = err.response.data.error;
          } else if (err.response.data.detail && typeof err.response.data.detail === 'object') {
            // Format validation errors
            const errors = [];
            for (const field in err.response.data.detail) {
              errors.push(`${field}: ${err.response.data.detail[field]}`);
            }
            this.error = errors.join(', ');
          } else {
            this.error = err.response.data.detail || 'Registration failed. Please try again.';
          }
        } else if (err.request) {
          // Request made but no response received
          this.error = 'Server not responding. Please try again later.';
        } else {
          this.error = 'Registration failed: ' + err.message;
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  background-image: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  padding: 2rem 0;
  overflow: hidden;
}

.register-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 550px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.register-card::before {
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

.success-message {
  background-color: #e8f5e9;
  color: var(--success-color);
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  border-left: 4px solid var(--success-color);
  display: flex;
  align-items: center;
}

.success-message i {
  margin-right: 10px;
  font-size: 1.1rem;
}

.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 0;
}

.form-group.half {
  flex: 1;
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
  outline: none;
}

.consent-checkbox {
  margin-top: 1rem;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.checkbox-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  position: relative;
}

.checkbox-wrapper input {
  opacity: 0;
  position: absolute;
}

.custom-checkbox {
  width: 22px;
  height: 22px;
  border: 2px solid #ddd;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
  cursor: pointer;
}

.checkbox-wrapper input:checked ~ .custom-checkbox {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.custom-checkbox i {
  color: white;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.checkbox-wrapper input:checked ~ .custom-checkbox i {
  opacity: 1;
}

.consent-checkbox label {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  cursor: pointer;
}

.consent-info {
  margin-top: 0.7rem;
  margin-left: 32px;
  font-size: 0.8rem;
  color: #6c757d;
  display: flex;
  align-items: flex-start;
  gap: 5px;
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

.register-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  padding: 0.9rem 1.2rem;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
  width: 100%;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.register-btn:hover {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  transform: translateY(-3px);
  box-shadow: 0 7px 14px rgba(0, 0, 0, 0.1);
}

.register-btn:disabled {
  background: linear-gradient(135deg, #a0a0a0, #c0c0c0);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.form-actions {
  margin-top: 2rem;
}

.mr-2 {
  margin-right: 8px;
}

.login-link, .admin-link {
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