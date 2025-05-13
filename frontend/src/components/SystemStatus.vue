<template>
  <div class="system-status card-modern" data-aos="fade-up">
    <div class="status-header">
      <h3><i class="fas fa-server"></i> System Status</h3>
      <button class="refresh-btn" @click="checkStatus" :disabled="checking">
        <i :class="checking ? 'fas fa-spinner fa-spin' : 'fas fa-sync-alt'"></i>
        {{ checking ? 'Checking...' : 'Refresh' }}
      </button>
    </div>
    
    <div class="status-container">
      <div class="status-card">
        <div class="status-icon">
          <i class="fas fa-database" :class="djangoStatus.status"></i>
        </div>
        <div class="status-info">
          <h4>Django API</h4>
          <span :class="['status-indicator', djangoStatus.status]">
            <i class="fas fa-circle status-dot"></i>
            {{ djangoStatus.status === 'online' ? 'Online' : 'Offline' }}
          </span>
        </div>
      </div>
      
      <div class="status-card">
        <div class="status-icon">
          <i class="fas fa-comments" :class="rasaStatus.status"></i>
        </div>
        <div class="status-info">
          <h4>Rasa API</h4>
          <span :class="['status-indicator', rasaStatus.status]">
            <i class="fas fa-circle status-dot"></i>
            {{ rasaStatus.status === 'online' ? 'Online' : 'Offline' }}
          </span>
        </div>
      </div>
    </div>
    
    <div v-if="showDetails" class="status-details animate__animated animate__fadeIn">
      <div v-if="djangoStatus.status === 'offline'" class="error-message">
        <i class="fas fa-exclamation-triangle"></i>
        Django API Error: {{ djangoStatus.error }}
      </div>
      <div v-if="rasaStatus.status === 'offline'" class="error-message">
        <i class="fas fa-exclamation-triangle"></i>
        Rasa API Error: {{ rasaStatus.error }}
      </div>
    </div>
  </div>
</template>

<script>
import { checkDjangoHealth, checkRasaHealth } from '../utils/api';
import './styles/system-status.css';

export default {
  name: 'SystemStatus',
  data() {
    return {
      djangoStatus: { status: 'unknown' },
      rasaStatus: { status: 'unknown' },
      checking: false,
      showDetails: false
    };
  },
  created() {
    this.checkStatus();
  },
  methods: {
    async checkStatus() {
      this.checking = true;
      
      try {
        // Check both APIs in parallel
        const [djangoResult, rasaResult] = await Promise.all([
          checkDjangoHealth(),
          checkRasaHealth()
        ]);
        
        this.djangoStatus = djangoResult;
        this.rasaStatus = rasaResult;
        
        // Show details if either service is offline
        this.showDetails = djangoResult.status === 'offline' || rasaResult.status === 'offline';
      } catch (error) {
        console.error('Error checking system status:', error);
      } finally {
        this.checking = false;
      }
    }
  }
};
</script>

<style scoped>
.system-status {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.system-status h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  color: #343a40;
}

.status-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-label {
  font-weight: 500;
  color: #495057;
}

.status-indicator {
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-indicator.online {
  background-color: #28a745;
  color: white;
}

.status-indicator.offline {
  background-color: #dc3545;
  color: white;
}

.status-indicator.unknown {
  background-color: #6c757d;
  color: white;
}

.status-details {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  padding: 0.3rem 0.5rem;
  border-radius: 3px;
  margin-bottom: 0.3rem;
}

.refresh-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  margin-top: 0.5rem;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #5a6268;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style> 