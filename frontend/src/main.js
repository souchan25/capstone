import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './utils/api' // Import API setup to ensure auth token is initialized
import 'bootstrap/dist/css/bootstrap.min.css'
import 'animate.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import AOS from 'vue-aos'

// Configure AOS (Animate On Scroll)
Vue.use(AOS, {
  duration: 800,
  easing: 'ease-out-quad',
  once: true
})

Vue.config.productionTip = false

// Create the Vue instance
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

// Add a global function to ensure sidebar visibility after app is mounted
window.addEventListener('load', () => {
  // Wait for app to be fully loaded and rendered
  setTimeout(() => {
    const sidebarWrapper = document.querySelector('.sidebar-wrapper');
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    if (sidebarWrapper) {
      sidebarWrapper.style.display = 'block';
      sidebarWrapper.style.visibility = 'visible';
    }
    
    if (sidebar) {
      sidebar.style.display = 'block';
      sidebar.style.visibility = 'visible';
    }
    
    if (sidebarToggle) {
      sidebarToggle.style.display = 'flex';
      sidebarToggle.style.visibility = 'visible';
    }
    
    // Add this to global window for debugging
    window.fixSidebar = function() {
      if (sidebarWrapper) {
        sidebarWrapper.style.display = 'block';
        sidebarWrapper.style.visibility = 'visible';
      }
      
      if (sidebar) {
        sidebar.style.display = 'block';
        sidebar.style.visibility = 'visible';
      }
      
      if (sidebarToggle) {
        sidebarToggle.style.display = 'flex';
        sidebarToggle.style.visibility = 'visible';
      }
      
      return 'Sidebar visibility forced';
    };
  }, 1000);
});

// Add a global function to force sidebar visibility globally
window.forceSidebarVisible = function() {
  const sidebarWrapper = document.querySelector('.sidebar-wrapper');
  const sidebar = document.querySelector('.sidebar');
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  
  if (sidebarWrapper) {
    sidebarWrapper.style.display = 'block';
    sidebarWrapper.style.visibility = 'visible';
    sidebarWrapper.style.width = '300px';
    sidebarWrapper.style.opacity = '1';
    sidebarWrapper.style.flex = '0 0 300px';
    sidebarWrapper.style.zIndex = '100';
    sidebarWrapper.classList.remove('hidden');
  }
  
  if (sidebar) {
    sidebar.style.display = 'block';
    sidebar.style.visibility = 'visible';
    sidebar.style.width = '300px';
    sidebar.style.height = '100%';
    sidebar.style.opacity = '1';
    sidebar.style.zIndex = '100';
    sidebar.style.transform = 'none';
    sidebar.classList.remove('collapsed');
  }
  
  if (sidebarToggle) {
    sidebarToggle.style.display = 'flex';
    sidebarToggle.style.visibility = 'visible';
    sidebarToggle.style.zIndex = '1000';
  }

  // Also update localStorage
  localStorage.setItem('sidebarCollapsed', 'false');
  
  // Force layout recalculation
  window.dispatchEvent(new Event('resize'));
  
  return 'Sidebar visibility forced';
};
