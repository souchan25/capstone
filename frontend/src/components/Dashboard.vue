<template>
  <div class="dashboard-container">
    <!-- Fixed toggle button that will always stay visible -->
    <button class="fixed-sidebar-toggle" @click="toggleSidebar">
      <i :class="sidebarCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
    </button>
    
    <header class="app-header animate__animated animate__fadeIn">
      <div class="logo">
        <i class="fas fa-heartbeat pulse"></i>
        <h1>Student Health Assistant</h1>
      </div>
      <div class="user-controls">
        <span class="welcome-text"><i class="fas fa-user-circle"></i> Hello, {{ userName }}</span>
        <button @click="logout" class="logout-btn btn-modern">
          <i class="fas fa-sign-out-alt"></i> Logout
        </button>
      </div>
    </header>    <div class="main-content main-layout">
      <div class="sidebar-wrapper" :class="{ 'hidden': sidebarCollapsed }">
        <div class="sidebar card-modern" :class="{ collapsed: sidebarCollapsed }" data-aos="fade-right">
          <UserProfile @profile-updated="updateUserName" />
          
          <div class="sidebar-section">
            <SystemStatus />
          </div>
          
          <div class="sidebar-section consent-toggle">
            <h3><i class="fas fa-shield-alt"></i> Data Sharing</h3>
            <div class="toggle-container">
              <label class="switch">
                <input type="checkbox" v-model="shareDataConsent" @change="updateConsent">
                <span class="slider round"></span>
              </label>
              <span :class="shareDataConsent ? 'text-success' : 'text-muted'">
                {{ shareDataConsent ? 'Enabled' : 'Disabled' }}
              </span>
            </div>
            <p class="consent-info">
              <i class="fas fa-info-circle"></i> When enabled, your health data will be shared with university clinic staff to help provide better care.
            </p>          </div>
          <div class="sidebar-section history-section">
            <h3><i class="fas fa-history"></i> Recent Reports</h3>
            <div v-if="loading" class="loading">
              <i class="fas fa-spinner fa-spin"></i> Loading history...
            </div>
            <div v-else-if="reports.length === 0" class="no-reports">
              <i class="fas fa-inbox"></i> You haven't submitted any reports yet.
            </div>
            <ul v-else class="history-list">
              <li v-for="report in reports" :key="report.id" class="history-item animate__animated animate__fadeIn" data-aos="fade-up">
                <div class="report-date"><i class="fas fa-calendar-alt"></i> {{ formatDate(report.created_at) }}</div>
                <div class="report-symptoms">
                  <strong><i class="fas fa-notes-medical"></i> Symptoms:</strong> {{ formatSymptoms(report.symptoms) }}
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="content-area" :class="{ expanded: sidebarCollapsed }" data-aos="fade-up">
        <div class="tabs">
          <button 
            :class="['tab-btn', { active: activeTab === 'form' }]" 
            @click="activeTab = 'form'">
            <i class="fas fa-clipboard-list"></i> Symptom Form          </button>
          <button 
            :class="['tab-btn', { active: activeTab === 'chat' }]" 
            @click="activeTab = 'chat'">
            <i class="fas fa-comments"></i> Chatbot
          </button>
        </div>
        
        <div v-if="activeTab === 'form'" class="symptom-form-container card-modern">
          <h2 class="animate__animated animate__slideInDown"><i class="fas fa-stethoscope"></i> Report Your Symptoms</h2>
          <div class="form-intro">
            <i class="fas fa-info-circle text-primary"></i> Please select the symptoms you are experiencing for an initial assessment.
          </div>
          
          <div class="form-content">
            <div class="symptom-selection animate__animated animate__fadeIn">
              <div class="input-with-button">
                <input 
                  type="text" 
                  v-model="newSymptom" 
                  @keyup.enter="addSymptom"
                  placeholder="Enter a symptom (e.g., headache, cough)"
                  class="form-control-modern"
                />
                <button @click="addSymptom" class="add-btn btn-modern">
                  <i class="fas fa-plus"></i> Add
                </button>
              </div>
              
              <div v-if="symptoms.length > 0" class="selected-symptoms animate__animated animate__fadeIn">
                <h4><i class="fas fa-list-check"></i> Selected Symptoms:</h4>
                <ul class="symptom-list">
                  <li v-for="(symptom, index) in symptoms" :key="index" class="symptom-tag animate__animated animate__bounceIn">
                    {{ symptom }}
                    <span @click="removeSymptom(index)" class="remove-symptom"><i class="fas fa-times"></i></span>
                  </li>
                </ul>
                <button 
                  @click="submitSymptoms" 
                  :disabled="symptoms.length === 0 || submitting"
                  class="submit-btn btn-modern">
                  <i class="fas fa-paper-plane"></i> {{ submitting ? 'Processing...' : 'Get Assessment' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else-if="activeTab === 'chat'" class="chat-container" :class="{ 'full-width': sidebarCollapsed }">
          <h2>Chat with Health Assistant</h2>
          <div class="chat-intro">
            Describe your symptoms in your own words and our chatbot will help you.
          </div>
          
          <div class="chat-messages">
            <div v-for="(message, index) in chatMessages" :key="index" 
              :class="['chat-message', message.sender]">
              <div class="message-content">{{ message.text }}</div>
            </div>
          </div>
          
          <div class="chat-input">
            <input 
              type="text" 
              v-model="chatInput" 
              @keyup.enter="sendChatMessage"
              placeholder="Type your message here..." 
            />
            <button @click="sendChatMessage" :disabled="!chatInput.trim()" class="send-btn">Send</button>
          </div>
        </div>
        
        <div v-if="prediction" class="prediction-results">
          <h3>Assessment Results</h3>
          <div class="result-card">
            <div class="result-header">
              <div :class="['severity-badge', prediction.severity.toLowerCase()]">
                {{ prediction.severity }} Severity
              </div>
            </div>
            <div class="disease-prediction">
              <h4>Possible Condition:</h4>
              <div class="disease-name">{{ prediction.disease }}</div>
              <div class="confidence">
                Confidence: {{ Math.round(prediction.confidence * 100) }}%
              </div>
            </div>
            <div class="advice-section">
              <h4>Advice:</h4>
              <p>{{ prediction.advice }}</p>
            </div>
            <div class="disclaimer">
              <strong>Note:</strong> This is not a medical diagnosis. 
              If symptoms are severe or persistent, please seek professional medical help.
            </div>          </div>
        </div>
      </div> <!-- Closing content-area div -->
    </div> <!-- Closing main-content main-layout div -->
  </div> <!-- Closing dashboard-container div -->
</template>

<script>
import { djangoApi, setAuthToken, predictDisease, sendChatMessage } from '../utils/api';
import SystemStatus from './SystemStatus.vue';
import UserProfile from './UserProfile.vue';
import axios from 'axios';
import './styles/sidebar.css';
import './fix-sidebar.css';
import './fix-sidebar-update.css';
import './sidebar-force-visible.css';
import './fullscreen-fix.css';
import './fix-sidebar-extreme.css';
import { recoverSidebar } from './sidebar-recovery.js';
import { printSidebarState } from './debug-sidebar.js';

export default {
  name: 'DashboardComponent',  components: {
    SystemStatus,
    UserProfile
  },data() {
    return {
      userName: '',
      shareDataConsent: false,
      activeTab: 'form',
      newSymptom: '',
      symptoms: [],
      prediction: null,
      submitting: false,
      chatInput: '',
      chatMessages: [
        { sender: 'bot', text: 'Hello! I\'m your health assistant. How can I help you today?' }
      ],
      reports: [],
      loading: true,
      sidebarCollapsed: false
    };
  },  created() {
    // Check if token exists
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    
    // Set default axios header
    axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    
    // Load sidebar state from localStorage - with fallback to ensure sidebar is visible by default
    try {
      const savedSidebarState = localStorage.getItem('sidebarCollapsed');
      // Only use the saved state if it's a valid value
      if (savedSidebarState === 'true' || savedSidebarState === 'false') {
        this.sidebarCollapsed = savedSidebarState === 'true';
      } else {
        // If the value is invalid or not present, default to false (sidebar visible)
        this.sidebarCollapsed = false;
        localStorage.setItem('sidebarCollapsed', 'false');
      }
    } catch (error) {
      console.error('Error loading sidebar state:', error);
      // Default to visible sidebar on error
      this.sidebarCollapsed = false;
      localStorage.setItem('sidebarCollapsed', 'false');
    }
    
    // Load user profile and history
    this.loadProfile();
    this.loadHistory();
  },
  mounted() {
    // Initialize sidebar state from localStorage - always visible
    localStorage.setItem('sidebarCollapsed', 'false');
    this.sidebarCollapsed = false;
    
    // Log sidebar state for debugging
    printSidebarState();
    
    // Ensure sidebar visibility after component is fully mounted
    this.$nextTick(() => {
      recoverSidebar();
      
      // Force sidebar to be visible on initial load
      setTimeout(() => {
        const sidebarWrapper = document.querySelector('.sidebar-wrapper');
        const sidebar = document.querySelector('.sidebar');
        const sidebarToggle = document.querySelector('.sidebar-toggle');
        
        if (sidebarWrapper) {
          sidebarWrapper.style.display = 'block';
          sidebarWrapper.style.visibility = 'visible';
          sidebarWrapper.style.width = '300px';
          sidebarWrapper.style.opacity = '1';
          sidebarWrapper.style.zIndex = '100';
        }
        
        if (sidebar) {
          sidebar.style.display = 'block';
          sidebar.style.visibility = 'visible';
          sidebar.style.width = '300px';
          sidebar.style.opacity = '1';
          sidebar.style.transform = 'none';
          sidebar.style.zIndex = '100';
        }
        
        if (sidebarToggle) {
          sidebarToggle.style.display = 'flex';
          sidebarToggle.style.visibility = 'visible';
          sidebarToggle.style.zIndex = '1000';
          sidebarToggle.style.opacity = '1';
        }
        
        // Force recalculation of layout
        this.$forceUpdate();
        window.dispatchEvent(new Event('resize'));
      }, 500);
    });
    
    // Set up a MutationObserver to ensure sidebar stays visible
    this.setupSidebarVisibilityMonitor();
    
    // Add explicit visibility monitoring for the toggle button
    this.monitorToggleButtonVisibility();
  },
  methods: {
    async loadProfile() {
      try {
        console.log('Loading profile in Dashboard component...');
        const response = await djangoApi.get('/api/profile/');
        console.log('Profile data in Dashboard:', response.data);
        
        // Handle different response formats
        if (response.data.user) {
          // Format: {user: {...}, ...}
          this.userName = `${response.data.user.first_name || ''} ${response.data.user.last_name || ''}`.trim() || 'User';
          this.shareDataConsent = response.data.share_data_consent || false;
        } else {
          // Direct user data format
          this.userName = `${response.data.first_name || ''} ${response.data.last_name || ''}`.trim() || 'User';
          this.shareDataConsent = response.data.share_data_consent || false;
        }
      } catch (err) {
        console.error('Error loading profile:', err);
        this.userName = 'User'; // Default fallback
        
        if (err.response?.status === 401) {
          // Unauthorized, token expired
          this.logout();
        }
      }
    },
      async loadHistory() {
      this.loading = true;
      try {
        const response = await djangoApi.get('/api/history/');
        this.reports = response.data;
      } catch (err) {
        console.error('Error loading history:', err);
      } finally {
        this.loading = false;
      }
    },
  toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
      localStorage.setItem('sidebarCollapsed', this.sidebarCollapsed);
      
      // Force update after toggle
      this.$nextTick(() => {
        const sidebarWrapper = document.querySelector('.sidebar-wrapper');
        const sidebar = document.querySelector('.sidebar');
        const contentArea = document.querySelector('.content-area');
        const sidebarToggle = document.querySelector('.sidebar-toggle');
        
        if (this.sidebarCollapsed) {
          // Sidebar is being collapsed
          if (sidebar) {
            sidebar.classList.add('collapsed');
            sidebar.style.width = '0';
            sidebar.style.visibility = 'hidden';
            sidebar.style.opacity = '0';
          }
          if (sidebarWrapper) {
            sidebarWrapper.classList.add('hidden');
            sidebarWrapper.style.width = '0';
            sidebarWrapper.style.flex = '0 0 0';
          }
          if (contentArea) {
            contentArea.classList.add('expanded');
            contentArea.style.marginLeft = '0';
            contentArea.style.width = '100%';
          }
          if (sidebarToggle) {
            sidebarToggle.innerHTML = '<i class="fas fa-chevron-right"></i>';
          }
        } else {
          // Sidebar is being expanded
          if (sidebar) {
            sidebar.classList.remove('collapsed');
            sidebar.style.width = '300px';
            sidebar.style.visibility = 'visible';
            sidebar.style.opacity = '1';
            sidebar.style.transform = 'none';
          }
          if (sidebarWrapper) {
            sidebarWrapper.classList.remove('hidden');
            sidebarWrapper.style.width = '300px';
            sidebarWrapper.style.flex = '0 0 300px';
          }
          if (contentArea) {
            contentArea.classList.remove('expanded');
            contentArea.style.width = 'calc(100% - 300px)';
          }
          if (sidebarToggle) {
            sidebarToggle.innerHTML = '<i class="fas fa-chevron-left"></i>';
          }
        }
        
        // Trigger a window resize event to force layout recalculation
        window.dispatchEvent(new Event('resize'));
        
        // Log sidebar state for debugging
        printSidebarState();
      });
    },
    
    updateUserName(profile) {
      if (profile && profile.firstName) {
        this.userName = `${profile.firstName} ${profile.lastName || ''}`;
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    
    formatSymptoms(symptoms) {
      return symptoms.join(', ');
    },
    
    addSymptom() {
      if (this.newSymptom.trim() && !this.symptoms.includes(this.newSymptom.trim())) {
        this.symptoms.push(this.newSymptom.trim());
        this.newSymptom = '';
      }
    },
    
    removeSymptom(index) {
      this.symptoms.splice(index, 1);
    },
    
    async submitSymptoms() {
      if (this.symptoms.length === 0) return;
      
      this.submitting = true;
      
      try {
        const response = await djangoApi.post('/api/submit-symptoms/', {
          symptoms: this.symptoms,
          input_method: 'FORM'
        });
        
        // Set prediction
        this.prediction = {
          disease: response.data.disease,
          confidence: response.data.confidence,
          advice: response.data.advice,
          severity: response.data.severity || 'MODERATE'
        };
        
        // Reload history
        this.loadHistory();
      } catch (err) {
        console.error('Error submitting symptoms:', err);
        alert('Failed to get prediction. Please try again.');
      } finally {
        this.submitting = false;
      }
    },
    
    async sendChatMessage() {
      if (!this.chatInput.trim()) return;
      
      // Add user message to chat
      this.chatMessages.push({ sender: 'user', text: this.chatInput });
      
      // Store message and clear input
      const message = this.chatInput;
      this.chatInput = '';
      
      // Add typing indicator
      this.chatMessages.push({ sender: 'bot', text: 'Typing...' });
      
      try {
        // Send message to Rasa
        const responses = await sendChatMessage(message);
        
        // Remove typing indicator
        this.chatMessages.pop();
        
        if (responses && responses.length > 0) {
          // Add all bot responses
          responses.forEach(response => {
            this.chatMessages.push({ 
              sender: 'bot', 
              text: response.text
            });
          });
          
          // Check if this might be a symptom report - extract symptoms
          const symptoms = this.extractSymptoms(message);
          
          if (symptoms.length > 0) {
            // Get prediction directly without creating a user report
            try {
              const predictionData = await predictDisease(symptoms);
              
              // Set prediction
              this.prediction = {
                disease: predictionData.disease,
                confidence: predictionData.confidence,
                advice: predictionData.advice,
                severity: predictionData.severity || 'MODERATE' // Default severity if not provided
              };
              
              // Record the prediction in the user's history
              await djangoApi.post('/api/submit-symptoms/', {
                symptoms: symptoms,
                input_method: 'CHAT'
              });
              
              // Reload history
              this.loadHistory();
            } catch (predictionErr) {
              console.error('Error getting prediction:', predictionErr);
            }
          }
        } else {
          // No response from Rasa
          this.chatMessages.push({ 
            sender: 'bot', 
            text: "I'm sorry, I couldn't process your message. Could you try again or use the Symptom Form?" 
          });
        }
      } catch (err) {
        console.error('Error in chat processing:', err);
        // Remove typing indicator
        this.chatMessages.pop();
        this.chatMessages.push({ 
          sender: 'bot', 
          text: "I'm sorry, I'm having trouble connecting to the chat service. Please check your connection or try the Symptom Form instead." 
        });
      }
    },
    
    extractSymptoms(message) {
      // This is a very simplified approach for the demo
      // In production, this would be replaced by Rasa NLU
      const commonSymptoms = [
        'headache', 'fever', 'cough', 'sore throat', 'runny nose', 'fatigue',
        'pain', 'nausea', 'vomiting', 'diarrhea', 'rash', 'dizziness'
      ];
      
      const found = [];
      const lowerMessage = message.toLowerCase();
      
      commonSymptoms.forEach(symptom => {
        if (lowerMessage.includes(symptom)) {
          found.push(symptom);
        }
      });
      
      return found;
    },
    
    async updateConsent() {
      try {
        await djangoApi.post('/api/update-consent/', {
          share_data_consent: this.shareDataConsent
        });
      } catch (err) {
        console.error('Error updating consent:', err);
        this.shareDataConsent = !this.shareDataConsent; // Revert on error
        alert('Failed to update consent. Please try again.');
      }
    },
      logout() {
      setAuthToken(null);
      this.$router.push('/login');
    },
      // Handle window resize for proper layout
    handleResize() {
      // Ensure chat container is properly sized
      this.$forceUpdate();
      
      // Ensure sidebar visibility
      const sidebarWrapper = document.querySelector('.sidebar-wrapper');
      if (sidebarWrapper) {
        sidebarWrapper.style.display = 'block';
      }
    },
    
    // Handle visibility change (e.g., when switching tabs or returning to the app)
    handleVisibilityChange() {
      if (!document.hidden) {
        // When page becomes visible again, ensure sidebar state is correct
        setTimeout(() => {
          const currentState = localStorage.getItem('sidebarCollapsed');
          if (currentState === 'true' || currentState === 'false') {
            this.sidebarCollapsed = currentState === 'true';
          }
          this.$forceUpdate();
        }, 100);
      }
    },
      // Setup mutation observer to detect DOM changes that might affect the sidebar
    setupSidebarVisibilityMonitor() {
      // Use MutationObserver to monitor any changes to the sidebar
      if (window.MutationObserver) {
        const observer = new MutationObserver(() => {
          const sidebarWrapper = document.querySelector('.sidebar-wrapper');
          const sidebar = document.querySelector('.sidebar');
          
          if (sidebarWrapper && getComputedStyle(sidebarWrapper).display === 'none') {
            sidebarWrapper.style.display = 'block';
            sidebarWrapper.style.visibility = 'visible';
          }
          
          if (sidebar && getComputedStyle(sidebar).display === 'none') {
            sidebar.style.display = 'block';
            sidebar.style.visibility = 'visible';
          }
        });
        
        // Start observing the document with the configured parameters
        observer.observe(document.body, { attributes: true, childList: true, subtree: true });
      }
    },
    monitorToggleButtonVisibility() {
      // Set an interval to check toggle button visibility periodically
      setInterval(() => {
        const toggleButton = document.querySelector('.fixed-sidebar-toggle');
        if (toggleButton) {
          // Always ensure toggle button is visible
          toggleButton.style.display = 'flex';
          toggleButton.style.visibility = 'visible';
          toggleButton.style.opacity = '1';
          toggleButton.style.zIndex = '2000';
          
          // Update the button icon based on sidebar state
          const icon = toggleButton.querySelector('i');
          if (icon) {
            if (this.sidebarCollapsed) {
              icon.className = 'fas fa-chevron-right';
            } else {
              icon.className = 'fas fa-chevron-left';
            }
          }
        }
      }, 1000);
    }
  }
};
</script>

<style scoped>
/* Component-specific override styles for dashboard */
.dashboard-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.main-layout {
  display: flex !important;
  flex: 1;
  height: calc(100vh - 70px) !important; /* Adjust for header height */
  overflow: hidden;
}

.sidebar-wrapper {
  display: block !important;
  visibility: visible !important;
  width: 300px !important;
  flex: 0 0 300px !important;
  position: relative !important;
  height: 100% !important;
  overflow-y: auto;
  transition: width 0.3s ease, opacity 0.3s ease;
}

.sidebar-wrapper.hidden {
  width: 0 !important;
  flex: 0 0 0 !important;
  opacity: 0;
  overflow: hidden;
}

.sidebar {
  display: block !important;
  visibility: visible !important;
  width: 300px !important;
  height: 100% !important;
  overflow-y: auto;
}

.sidebar-toggle {
  position: absolute;
  right: -15px;
  top: 20px;
  z-index: 1000 !important;
  width: 36px;
  height: 36px;
  background-color: #4361ee;
  color: white;
  border: 2px solid white;
  border-radius: 50%;
  cursor: pointer;
  display: flex !important;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  visibility: visible !important;
  opacity: 1 !important;
  font-size: 16px;
}

.sidebar-wrapper.hidden .sidebar-toggle {
  right: auto;
  left: 15px;
  position: fixed;
  top: 90px;
  background-color: #5e72e4;
  transform: rotate(180deg);
}

.content-area {
  flex: 1 !important;
  overflow-y: auto;
  height: 100%;
  padding: 20px;
  transition: margin-left 0.3s ease, width 0.3s ease;
  position: relative;
  width: calc(100% - 300px);
}

.content-area.expanded {
  margin-left: 0 !important;
  width: 100% !important;
  padding-left: 50px;
}

.app-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 1.2rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo i {
  font-size: 1.8rem;
  color: var(--accent-color);
}

.pulse {
  animation: pulse 2s infinite ease-in-out;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.welcome-text {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  backdrop-filter: blur(5px);
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.consent-toggle h3, .history-section h3 {
  margin-top: 0;
  color: var(--dark-color);
  font-size: 1.15rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
}

.consent-toggle h3 i, .history-section h3 i {
  color: var(--primary-color);
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
  background: #f8fafc;
  padding: 0.8rem;
  border-radius: 10px;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.02);
}

.text-success {
  color: var(--success-color);
  font-weight: 600;
}

.text-muted {
  color: #6c757d;
  font-weight: 500;
}

.consent-info {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 1.8rem;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 0.5rem 0;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}

.history-section {
  margin-top: 1.5rem;
  padding-top: 1.8rem;
  position: relative;
  border-top: 1px solid rgba(225, 228, 232, 0.6);
}

.history-section::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 2px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  color: #6c757d;
  gap: 10px;
}

.loading i {
  color: var(--primary-color);
}

.no-reports {
  text-align: center;
  padding: 2rem 0;
  background-color: #f8fafc;
  border-radius: 10px;
  color: #6c757d;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.no-reports i {
  font-size: 2rem;
  color: #ced4da;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 300px;
  overflow-y: auto;
}

.history-list::-webkit-scrollbar {
  width: 5px;
}

.history-list::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.history-list::-webkit-scrollbar-thumb {
  background: #cdcdcd;
  border-radius: 5px;
}

.history-item {
  border-bottom: 1px dashed rgba(225, 228, 232, 0.7);
  padding: 1rem 0;
  transition: all 0.2s ease;
  cursor: pointer;
}

.history-item:hover {
  background-color: #f8fafc;
  padding: 1rem 0.8rem;
  margin: 0 -0.8rem;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
}

.report-date {
  font-size: 0.85rem;
  color: #6c757d;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 0.4rem;
}

.report-date i {
  color: var(--accent-color);
}

.report-symptoms {
  font-size: 0.95rem;
  margin-top: 0.4rem;
  line-height: 1.5;
}

.report-symptoms strong {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 0.3rem;
}

.report-symptoms strong i {
  color: var(--primary-color);
}

.tabs {
  display: flex;
  padding: 0.5rem;
  border-bottom: 1px solid #e1e4e8;
  background: #f8fafc;
  border-radius: 15px 15px 0 0;
}

.tab-btn {
  padding: 0.85rem 1.5rem;
  background: none;
  border: none;
  border-radius: 8px;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 0.3rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn i {
  font-size: 1.1rem;
}

.tab-btn.active {
  color: var(--primary-color);
  background-color: white;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  font-weight: 600;
}

.tab-btn:hover:not(.active) {
  color: var(--secondary-color);
  background-color: rgba(67, 97, 238, 0.05);
  transform: translateY(-2px);
}

.symptom-form-container, .chat-container {
  padding: 2rem;
  flex: 1;
  width: 100%; /* Ensure it takes full width */
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: all 0.3s ease-in-out;
  max-width: 100%;
}

.chat-container.full-width {
  width: 100%;
  max-width: 100%;
  transition: all 0.3s ease-in-out;
}

h2 {
  margin-top: 0;
  color: var(--dark-color);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
}

h2 i {
  color: var(--primary-color);
}

.form-intro, .chat-intro {
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.6;
  padding-left: 10px;
  border-left: 3px solid var(--accent-color);
  font-size: 0.95rem;
}

.text-primary {
  color: var(--primary-color);
}

.form-content {
  margin-bottom: 2rem;
  border-radius: 12px;
  padding: 1.5rem;
  background: #f8fafc;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.03);
}

.input-with-button {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
}

.input-with-button input {
  flex: 1;
  padding: 0.9rem 1.2rem;
  border: 1px solid #e1e5eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02);
}

.input-with-button input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
  outline: none;
}

.add-btn, .send-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  padding: 0 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-btn:hover, .send-btn:hover {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.2);
}

.selected-symptoms {
  margin-top: 2rem;
  background: white;
  padding: 1.2rem;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
}

.selected-symptoms h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--dark-color);
  display: flex;
  align-items: center;
  gap: 8px;
}

.selected-symptoms h4 i {
  color: var(--primary-color);
}

.symptom-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}

.symptom-tag {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #0d47a1;
  padding: 0.5rem 1rem;
  border-radius: 30px;
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.symptom-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
}

.remove-symptom {
  margin-left: 8px;
  cursor: pointer;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}

.remove-symptom:hover {
  background-color: #ff5252;
  color: white;
}

.submit-btn {
  background: linear-gradient(135deg, var(--success-color), #2e7d32);
  color: white;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #43a047, #2e7d32);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
  transform: translateY(-2px);
}

.submit-btn:disabled {
  background: linear-gradient(135deg, #a5d6a7, #81c784);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.chat-messages {
  height: 350px;
  overflow-y: auto;
  padding: 1.5rem;
  background-color: #f8fafc;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.03);
  position: relative;
  width: 100%; /* Ensure it takes full width */
  flex: 1;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #cdcdcd;
  border-radius: 10px;
}

.chat-message {
  margin-bottom: 1.2rem;
  max-width: 80%;
  animation: fadeIn 0.5s ease;
}

.chat-message.user {
  margin-left: auto;
  text-align: right;
}

.chat-message.bot {
  margin-right: auto;
}

.message-content {
  padding: 1rem 1.3rem;
  border-radius: 18px;
  display: inline-block;
  max-width: 100%;
  word-wrap: break-word;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  position: relative;
  transition: transform 0.2s ease;
}

.message-content:hover {
  transform: translateY(-2px);
}

.chat-message.user .message-content {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-message.bot .message-content {
  background-color: white;
  color: var(--dark-color);
  border-bottom-left-radius: 4px;
  border-left: 3px solid var(--accent-color);
}

.chat-input {
  display: flex;
  gap: 0.8rem;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  width: 100%; /* Ensure it takes full width */
}

.chat-input input {
  flex: 1;
  padding: 0.9rem 1.2rem;
  border: 1px solid #e1e5eb;
  border-radius: 30px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.chat-input input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
}

.send-btn {
  border-radius: 30px;
  min-width: 100px;
  justify-content: center;
}

.prediction-results {
  margin-top: 2.5rem;
  animation: fadeIn 0.6s ease;
}

.prediction-results h3 {
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
  position: relative;
  display: inline-block;
  color: var(--dark-color);
}

.prediction-results h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
  border-radius: 2px;
}

.result-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  animation: slideUp 0.7s ease;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.result-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(76, 201, 240, 0.1), transparent);
  z-index: 0;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  position: relative;
}

.severity-badge {
  padding: 0.5rem 1rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.9rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.07);
  display: flex;
  align-items: center;
  gap: 8px;
}

.severity-badge.low {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  color: #2e7d32;
}

.severity-badge.low::before {
  content: '•';
  font-size: 1.5rem;
  color: #4caf50;
}

.severity-badge.medium {
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  color: #ff8f00;
}

.severity-badge.medium::before {
  content: '•';
  font-size: 1.5rem;
  color: #ffc107;
}

.severity-badge.high {
  background: linear-gradient(135deg, #ffebee, #ffcdd2);
  color: #c62828;
}

.severity-badge.high::before {
  content: '•';
  font-size: 1.5rem;
  color: #f44336;
}

.disease-prediction {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  position: relative;
}

.disease-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--dark-color);
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.confidence {
  font-size: 1rem;
  color: #6c757d;
  display: flex;
  align-items: center;
  gap: 8px;
}

.confidence::before {
  content: '✓';
  color: var(--success-color);
}

.advice-section {
  margin-bottom: 1.8rem;
}

.advice-section h4, .disease-prediction h4 {
  margin-top: 0;
  margin-bottom: 0.8rem;
  color: var(--dark-color);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.advice-section h4::before, .disease-prediction h4::before {
  content: '';
  width: 12px;
  height: 12px;
  background-color: var(--primary-color);
  border-radius: 50%;
}

.advice-section p {
  line-height: 1.7;
  color: #444;
  padding: 0.5rem 0 0.5rem 20px;
  position: relative;
  border-left: 2px solid var(--primary-color);
}

.disclaimer {
  font-size: 0.9rem;
  padding: 1.2rem;
  background-color: #fff3cd;
  border-radius: 8px;
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.disclaimer::before {
  content: '⚠️';
  font-size: 1.2rem;
}

.loading, .no-reports {
  color: #6c757d;
  text-align: center;
  padding: 1rem;
}

/* Sidebar component styles */
.sidebar-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
}

.sidebar-section:not(:last-child) {
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

/* Improving sidebar transition */
.sidebar {
  transition: transform 0.3s ease, width 0.3s ease;
}

.sidebar.collapsed {
  transform: translateX(-100%);
  width: 0;
  padding: 0;
  overflow: hidden;
}

/* Animation for sidebar toggle */
@keyframes pulse-icon {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.sidebar-toggle:hover {
  transform: scale(1.1);
  background-color: #5e72e4;
}

.sidebar-toggle i {
  animation: pulse-icon 2s infinite ease-in-out;
}

/* Fixed sidebar toggle that stays visible regardless of sidebar state */
.fixed-sidebar-toggle {
  position: fixed;
  left: 10px;
  top: 90px;
  z-index: 2000;
  width: 40px;
  height: 40px;
  background-color: #4361ee;
  color: white;
  border: 2px solid white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  font-size: 18px;
}

.fixed-sidebar-toggle:hover {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .sidebar-wrapper {
    width: 100%;
  }
  
  .sidebar {
    width: 100%;
    max-width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--light-gray);
  }
  
  .sidebar.collapsed {
    transform: translateY(-100%);
    height: 0;
    overflow: hidden;
  }
  
  .sidebar-toggle {
    top: auto;
    bottom: -15px;
    right: 20px;
    transform: rotate(90deg);
  }
  
  .sidebar.collapsed + .sidebar-toggle {
    transform: rotate(-90deg);
  }
  
  .content-area {
    flex-direction: column;
    width: 100% !important;
    margin-left: 0 !important;
  }
  
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e1e4e8;
  }
  
  .chat-messages {
    height: 300px;
  }
  
  .chat-input {
    flex-wrap: wrap;
  }
  
  .chat-input input {
    width: 100%;
  }
}
</style>