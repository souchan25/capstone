<template>
  <div class="clinic-dashboard-container">
    <header class="app-header animate__animated animate__fadeIn">
      <div class="logo">
        <i class="fas fa-hospital pulse"></i>
        <h1>University Clinic Staff Dashboard</h1>
      </div>
      <div class="user-controls">
        <a href="/admin" target="_blank" class="admin-link-btn">
          <i class="fas fa-user-shield"></i> Admin Panel
        </a>
        <button @click="logout" class="logout-btn btn-modern">
          <i class="fas fa-sign-out-alt"></i> Logout
        </button>
      </div>
    </header>
    
    <div class="dashboard-content">
      <SystemStatus />
      
      <div class="dashboard-header" data-aos="fade-up">
        <h2><i class="fas fa-clipboard-list"></i> Student Health Reports</h2>
        <div class="dashboard-controls">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input 
              type="text" 
              v-model="searchTerm" 
              placeholder="Search by student name or symptoms" 
              @input="filterReports"
              class="form-control-modern"
            />
          </div>
          <div class="severity-filter">
            <select v-model="severityFilter" @change="filterReports" class="form-control-modern">
              <option value="ALL">All Severities</option>
              <option value="HIGH">High Severity</option>
              <option value="MEDIUM">Medium Severity</option>
              <option value="LOW">Low Severity</option>
            </select>
          </div>
        </div>
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="spinner-modern"></div>
        <p><i class="fas fa-spinner fa-spin"></i> Loading reports...</p>
      </div>
      
      <div v-else-if="filteredReports.length === 0" class="no-reports animate__animated animate__fadeIn">
        <i class="fas fa-search fa-2x"></i>
        <p>No reports found matching your criteria.</p>
      </div>
        <div v-else class="reports-table-container card-modern" data-aos="fade-up">
        <table class="reports-table">
          <thead>
            <tr>
              <th><i class="fas fa-calendar-alt"></i> Date</th>
              <th><i class="fas fa-user"></i> Student</th>
              <th><i class="fas fa-notes-medical"></i> Symptoms</th>
              <th><i class="fas fa-stethoscope"></i> Condition</th>
              <th><i class="fas fa-exclamation-triangle"></i> Severity</th>
              <th><i class="fas fa-cog"></i> Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="report in filteredReports" :key="report.id" 
                :class="[{ 'high-severity': report.prediction?.severity === 'HIGH',
                          'medium-severity': report.prediction?.severity === 'MEDIUM' }, 'animate__animated', 'animate__fadeIn']">
              <td><span class="date-field">{{ formatDate(report.created_at) }}</span></td>
              <td><span class="student-name">{{ report.student_name }}</span></td>
              <td><span class="symptoms-field">{{ formatSymptoms(report.symptoms) }}</span></td>
              <td><span class="condition-field">{{ report.prediction?.disease || 'N/A' }}</span></td>
              <td>
                <span :class="['severity-badge', report.prediction?.severity?.toLowerCase()]">
                  <i class="fas fa-circle status-dot"></i>
                  {{ report.prediction?.severity || 'N/A' }}
                </span>
              </td>
              <td>
                <button @click="viewReportDetails(report)" class="view-btn btn-modern">
                  <i class="fas fa-eye"></i> View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
      <!-- Report Details Modal -->
    <div v-if="selectedReport" class="modal" @click.self="closeModal">
      <div class="modal-content animate__animated animate__fadeInUp">
        <div class="modal-header">
          <h3><i class="fas fa-file-medical"></i> Report Details</h3>
          <button @click="closeModal" class="close-btn"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
          <div class="report-info card-modern">
            <h4><i class="fas fa-info-circle"></i> Basic Information</h4>
            <div class="info-group">
              <label><i class="fas fa-calendar-alt"></i> Date:</label>
              <span>{{ formatDate(selectedReport.created_at) }}</span>
            </div>
            <div class="info-group">
              <label><i class="fas fa-user-graduate"></i> Student:</label>
              <span class="highlight-text">{{ selectedReport.student_name }}</span>
            </div>
            <div class="info-group">
              <label><i class="fas fa-notes-medical"></i> Symptoms:</label>
              <span class="symptoms-list">{{ formatSymptoms(selectedReport.symptoms) }}</span>
            </div>
            <div class="info-group">
              <label><i class="fas fa-keyboard"></i> Input Method:</label>
              <span class="badge input-badge">
                <i :class="selectedReport.input_method === 'CHAT' ? 'fas fa-comment-dots' : 'fas fa-list-ul'"></i>
                {{ selectedReport.input_method === 'CHAT' ? 'Chat Interface' : 'Symptom Form' }}
              </span>
            </div>
          </div>
          
          <div v-if="selectedReport.prediction" class="prediction-info card-modern">
            <h4><i class="fas fa-stethoscope"></i> Prediction Results</h4>
            <div class="info-group">
              <label><i class="fas fa-heartbeat"></i> Condition:</label>
              <span class="condition-name">{{ selectedReport.prediction.disease }}</span>
            </div>            <div class="info-group">
              <label><i class="fas fa-percentage"></i> Confidence:</label>
              <span class="confidence-meter">
                <div class="progress-bar">
                  <div class="progress" :style="{width: Math.round(selectedReport.prediction.confidence_score * 100) + '%'}"></div>
                </div>
                <span class="confidence-text">{{ Math.round(selectedReport.prediction.confidence_score * 100) }}%</span>
              </span>
            </div>
            <div class="info-group">
              <label><i class="fas fa-exclamation-triangle"></i> Severity:</label>
              <span :class="['severity-indicator', selectedReport.prediction.severity?.toLowerCase()]">
                <i class="fas fa-circle status-dot"></i>
                {{ selectedReport.prediction.severity }}
              </span>
            </div>
            <div class="info-group advice">
              <label><i class="fas fa-comment-medical"></i> Advice Given:</label>
              <div class="advice-box">
                <p>{{ selectedReport.prediction.advice }}</p>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button @click="markReviewed(selectedReport)" class="action-btn reviewed-btn btn-modern">
              <i class="fas fa-check-circle"></i> Mark as Reviewed
            </button>
            <button class="action-btn contact-btn btn-modern">
              <i class="fas fa-envelope"></i> Contact Student
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { djangoApi, setAuthToken } from '../utils/api';
import SystemStatus from './SystemStatus.vue';
import './styles/clinic-dashboard.css';

export default {
  name: 'ClinicDashboardComponent',
  components: {
    SystemStatus
  },
  data() {
    return {
      reports: [],
      filteredReports: [],
      loading: true,
      searchTerm: '',
      severityFilter: 'ALL',
      selectedReport: null
    };
  },
  created() {
    // Check if token exists
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    
    // Load reports
    this.loadReports();
  },
  methods: {
    async loadReports() {
      this.loading = true;
      try {
        const response = await djangoApi.get('/api/clinic/dashboard/');
        
        // Process reports to include student name and prediction info
        this.reports = response.data.map(report => {
          // Get the prediction for the report if available
          const prediction = report.prediction_record || null;
          
          return {
            ...report,
            student_name: `${report.student.user.first_name} ${report.student.user.last_name}`,
            prediction: prediction
          };
        });
        
        // Initial filter
        this.filterReports();
      } catch (err) {
        console.error('Error loading reports:', err);
        if (err.response?.status === 401 || err.response?.status === 403) {
          // Unauthorized or Forbidden
          alert('You do not have permission to access this page.');
          this.logout();
        }
      } finally {
        this.loading = false;
      }
    },
    
    filterReports() {
      // Filter by search term (student name or symptoms)
      let filtered = this.reports;
      
      if (this.searchTerm.trim() !== '') {
        const term = this.searchTerm.toLowerCase().trim();
        filtered = filtered.filter(report => {
          return report.student_name.toLowerCase().includes(term) || 
                 this.formatSymptoms(report.symptoms).toLowerCase().includes(term) ||
                 report.prediction?.disease.toLowerCase().includes(term);
        });
      }
      
      // Filter by severity
      if (this.severityFilter !== 'ALL') {
        filtered = filtered.filter(report => {
          return report.prediction?.severity === this.severityFilter;
        });
      }
      
      this.filteredReports = filtered;
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    
    formatSymptoms(symptoms) {
      return symptoms.join(', ');
    },
    
    viewReportDetails(report) {
      this.selectedReport = report;
    },
    
    closeModal() {
      this.selectedReport = null;
    },
    
    markReviewed(report) {
      // This would normally call an API to mark the report as reviewed
      alert(`Report for ${report.student_name} marked as reviewed`);
      this.closeModal();
    },
    
    logout() {
      setAuthToken(null);
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.clinic-dashboard-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: white;
  padding: 1.2rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
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

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.admin-link-btn {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 30px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.admin-link-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
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
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.dashboard-content {
  padding: 2rem;
  flex: 1;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.dashboard-header h2 {
  margin: 0;
  color: var(--dark-color);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.dashboard-header h2 i {
  color: var(--primary-color);
}

.dashboard-controls {
  display: flex;
  gap: 1rem;
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}

.search-box input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  width: 280px;
  transition: all 0.3s ease;
}

.search-box input:focus {
  width: 320px;
}

.severity-filter select {
  padding: 0.75rem 1rem;
  min-width: 180px;
}

.reports-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: auto;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th {
  background-color: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
}

.reports-table td {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.reports-table tr:hover {
  background-color: #f8f9fa;
}

.reports-table tr.high-severity {
  background-color: #fff5f5;
}

.reports-table tr.medium-severity {
  background-color: #fffbeb;
}

.severity-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 16px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-block;
}

.severity-badge.high {
  background-color: #ffebee;
  color: #c62828;
}

.severity-badge.medium {
  background-color: #fff8e1;
  color: #ff8f00;
}

.severity-badge.low {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.view-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background-color: #2980b9;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-reports {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  background: white;
  border-radius: 8px;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 1.5rem;
}

.report-info, .prediction-info {
  margin-bottom: 1.5rem;
}

.prediction-info h4 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 0.5rem;
}

.info-group {
  margin-bottom: 0.8rem;
  display: flex;
}

.info-group label {
  font-weight: 600;
  width: 120px;
  color: #495057;
}

.info-group.advice {
  display: block;
}

.info-group.advice p {
  margin-top: 0.5rem;
  line-height: 1.5;
}

.severity-indicator {
  padding: 0.2rem 0.6rem;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 600;
}

.severity-indicator.high {
  background-color: #ffebee;
  color: #c62828;
}

.severity-indicator.medium {
  background-color: #fff8e1;
  color: #ff8f00;
}

.severity-indicator.low {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.action-btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.reviewed-btn {
  background-color: #4caf50;
  color: white;
}

.reviewed-btn:hover {
  background-color: #388e3c;
}

.contact-btn {
  background-color: #3498db;
  color: white;
}

.contact-btn:hover {
  background-color: #2980b9;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .dashboard-controls {
    width: 100%;
    flex-direction: column;
  }
  
  .info-group {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style> 