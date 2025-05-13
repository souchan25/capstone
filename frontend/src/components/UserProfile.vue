<template>
  <div class="user-profile card-modern">
    <h3><i class="fas fa-id-card"></i> Profile</h3>
    
    <div v-if="loading" class="loading-profile">
      <i class="fas fa-spinner fa-spin"></i> Loading profile...
    </div>    <div v-else class="profile-content">
      <div v-if="updateStatus.message" :class="['status-message', `status-${updateStatus.type}`]" class="animate__animated animate__fadeIn">
        <i :class="updateStatus.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
        {{ updateStatus.message }}
      </div>
      
      <div class="profile-avatar">
        <div class="avatar-circle" @click="editProfile" title="Click to edit profile">
          <span class="initials">{{ userInitials }}</span>
          <span class="edit-overlay"><i class="fas fa-pencil-alt"></i></span>
        </div>
      </div>
      
      <div class="profile-info">
        <h4>{{ userName }} {{ userLastName }}</h4>
        <p class="user-email"><i class="fas fa-envelope"></i> {{ email || 'No email provided' }}</p>
        <p class="student-id"><i class="fas fa-id-badge"></i> ID: {{ studentId || 'Not available' }}</p>
      </div>
      
      <div class="profile-actions">
        <button @click="editProfile" class="btn-profile btn-modern">
          <i class="fas fa-user-edit"></i> Edit Profile
        </button>
      </div>
      
      <div v-if="showEditForm" class="edit-form animate__animated animate__fadeIn">
        <h4>Edit Profile</h4>
        <form @submit.prevent="saveProfile">
          <div class="form-group">
            <label for="firstName"><i class="fas fa-user"></i> First Name:</label>
            <input 
              type="text" 
              id="firstName" 
              class="form-control-modern" 
              v-model="editedProfile.firstName" 
              required
            >
          </div>
          
          <div class="form-group">
            <label for="lastName"><i class="fas fa-user"></i> Last Name:</label>
            <input 
              type="text" 
              id="lastName" 
              class="form-control-modern" 
              v-model="editedProfile.lastName" 
              required
            >
          </div>
          
          <div class="form-group">
            <label for="email"><i class="fas fa-envelope"></i> Email:</label>
            <input 
              type="email" 
              id="email" 
              class="form-control-modern" 
              v-model="editedProfile.email"
            >
          </div>
            <div class="form-actions">
            <button type="button" class="btn-cancel" @click="cancelEdit" :disabled="loading">
              <i class="fas fa-times"></i> Cancel
            </button>
            <button type="submit" class="btn-save btn-modern" :disabled="loading">
              <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-save'"></i> {{ loading ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserProfile, updateUserProfile } from '../utils/api';

export default {
  name: 'UserProfile',  data() {
    return {
      loading: true,
      showEditForm: false,
      firstName: '',
      lastName: '',
      email: '',
      studentId: '',
      editedProfile: {
        firstName: '',
        lastName: '',
        email: ''
      },
      updateStatus: {
        message: '',
        type: ''
      }
    };
  },
  computed: {
    userName() {
      return this.firstName || 'User';
    },
    userLastName() {
      return this.lastName || '';
    },
    userInitials() {
      const first = this.firstName ? this.firstName.charAt(0).toUpperCase() : '?';
      const last = this.lastName ? this.lastName.charAt(0).toUpperCase() : '';
      return `${first}${last}`;
    }
  },
  created() {
    this.loadUserData();
  },
  methods: {    async loadUserData() {
      this.loading = true;
      try {
        console.log('Loading user profile data...');
        const userData = await getUserProfile();
        console.log('User profile data received:', userData);
        
        // Handle different formats of API response
        if (userData.user) {
          // Format: {user: {...}, ...}
          this.firstName = userData.user.first_name || '';
          this.lastName = userData.user.last_name || '';
          this.email = userData.user.email || '';
          this.studentId = userData.school_id || '';
        } else {
          // Direct user data format
          this.firstName = userData.first_name || '';
          this.lastName = userData.last_name || '';
          this.email = userData.email || '';
          this.studentId = userData.school_id || '';
        }
        
        // Initialize edited profile with current data
        this.editedProfile = {
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email
        };
        
        // Emit event for parent components to update
        this.$emit('profile-updated', {
          firstName: this.firstName,
          lastName: this.lastName
        });
      } catch (error) {
        console.error('Error loading user profile:', error);
      } finally {
        this.loading = false;
      }
    },
    
    editProfile() {
      this.showEditForm = true;
    },
    
    cancelEdit() {
      this.showEditForm = false;
      // Reset edited profile to current values
      this.editedProfile = {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email
      };
    },      async saveProfile() {
      this.loading = true;
      this.updateStatus = { message: '', type: '' };
      
      try {
        await updateUserProfile({
          first_name: this.editedProfile.firstName,
          last_name: this.editedProfile.lastName,
          email: this.editedProfile.email
        });
        
        // Update local data
        this.firstName = this.editedProfile.firstName;
        this.lastName = this.editedProfile.lastName;
        this.email = this.editedProfile.email;
        
        this.showEditForm = false;
        
        // Show success message
        this.updateStatus = {
          message: 'Profile updated successfully!',
          type: 'success'
        };
        
        // Clear message after 3 seconds
        setTimeout(() => {
          this.updateStatus = { message: '', type: '' };
        }, 3000);
        
        // Emit event for parent components to update
        this.$emit('profile-updated', {
          firstName: this.firstName,
          lastName: this.lastName
        });
      } catch (error) {
        console.error('Error updating profile:', error);
        this.updateStatus = {
          message: 'Failed to update profile. Please try again.',
          type: 'error'
        };
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.user-profile {
  padding: 1.5rem;
  margin-bottom: var(--spacing-lg);
}

.user-profile h3 {
  margin-top: 0;
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--dark-color);
  font-size: 1.1rem;
}

.user-profile h3 i {
  color: var(--primary-color);
}

.loading-profile {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: var(--dark-gray);
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 100%;
}

.status-message {
  width: 100%;
  text-align: center;
}

.profile-avatar {
  margin-bottom: var(--spacing-md);
}

.avatar-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  position: relative;
}

.avatar-circle:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.avatar-circle .edit-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.avatar-circle:hover .edit-overlay {
  opacity: 1;
}

.edit-overlay i {
  font-size: 1.2rem;
}

.profile-info {
  text-align: center;
  margin-bottom: var(--spacing-md);
  width: 100%;
}

.profile-info h4 {
  margin-top: 0;
  margin-bottom: var(--spacing-sm);
  color: var(--dark-color);
  font-weight: 600;
}

.user-email, .student-id {
  margin: 0.25rem 0;
  color: var(--dark-gray);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.profile-actions {
  width: 100%;
  margin-top: var(--spacing-sm);
}

.btn-profile {
  width: 100%;
}

.edit-form {
  margin-top: var(--spacing-lg);
  border-top: 1px solid var(--light-gray);
  padding-top: var(--spacing-md);
  width: 100%;
  transition: all 0.3s ease;
}

.edit-form h4 {
  text-align: center;
  margin-bottom: var(--spacing-md);
  color: var(--dark-color);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.edit-form h4:before {
  content: '\f4ff';
  font-family: 'Font Awesome 5 Free';
  font-weight: 900;
  color: var(--primary-color);
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 500;
  color: var(--dark-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group label i {
  color: var(--primary-color);
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
  flex-wrap: wrap;
}

@media (max-width: 480px) {
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .form-actions button {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  
  .profile-avatar {
    margin-bottom: 1rem;
  }
  
  .avatar-circle {
    margin: 0 auto;
  }
  
  .profile-info {
    text-align: center;
  }
  
  .status-message {
    font-size: 0.9rem;
    padding: 0.5rem;
  }
}

.btn-cancel {
  background-color: var(--light-gray);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}

.btn-save {
  flex-grow: 1;
}

.status-message {
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.status-success {
  background-color: rgba(75, 181, 67, 0.15);
  color: #2e7d32;
  border: 1px solid rgba(75, 181, 67, 0.3);
}

.status-error {
  background-color: rgba(211, 47, 47, 0.15);
  color: #c62828;
  border: 1px solid rgba(211, 47, 47, 0.3);
}

.btn-cancel {
  flex: 1;
  padding: 0.6rem 1rem;
  background-color: var(--light-gray);
  color: var(--dark-color);
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-cancel:hover {
  background-color: #d1d5db;
}

.btn-save {
  flex: 1;
}
</style>
