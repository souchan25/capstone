<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  /* Color palette */
  --primary-color: #4361ee;
  --primary-light: #738eec;
  --primary-dark: #2541c9;
  --secondary-color: #3f37c9;
  --accent-color: #4cc9f0;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --info-color: #3b82f6;
  
  /* Neutrals */
  --light-color: #f8f9fa;
  --light-gray: #e5e7eb;
  --medium-gray: #94a3b8;
  --dark-gray: #64748b;
  --dark-color: #2c3e50;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-xxl: 3rem;
  
  /* Borders */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  --border-radius-xl: 16px;
  --border-radius-pill: 9999px;
  
  /* Animation */
  --transition-speed: 0.3s;
  --transition-function: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  
  /* Typography */
  --font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
  --line-height-sm: 1.25;
  --line-height-md: 1.5;
  --line-height-lg: 1.75;
}

/* Global Utility Classes */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.d-flex { display: flex; }
.flex-column { flex-direction: column; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.align-center { align-items: center; }
.flex-wrap { flex-wrap: wrap; }
.flex-grow { flex-grow: 1; }
.gap-sm { gap: var(--spacing-sm); }
.gap-md { gap: var(--spacing-md); }
.gap-lg { gap: var(--spacing-lg); }

.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
.mt-xl { margin-top: var(--spacing-xl); }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mb-xl { margin-bottom: var(--spacing-xl); }

.py-sm { padding-top: var(--spacing-sm); padding-bottom: var(--spacing-sm); }
.py-md { padding-top: var(--spacing-md); padding-bottom: var(--spacing-md); }
.py-lg { padding-top: var(--spacing-lg); padding-bottom: var(--spacing-lg); }
.px-sm { padding-left: var(--spacing-sm); padding-right: var(--spacing-sm); }
.px-md { padding-left: var(--spacing-md); padding-right: var(--spacing-md); }
.px-lg { padding-left: var(--spacing-lg); padding-right: var(--spacing-lg); }

.w-100 { width: 100%; }
.h-100 { height: 100%; }

.card {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
}

.text-primary { color: var(--primary-color); }
.text-secondary { color: var(--secondary-color); }
.text-accent { color: var(--accent-color); }
.text-success { color: var(--success-color); }
.text-warning { color: var(--warning-color); }
.text-danger { color: var(--danger-color); }
.text-dark { color: var(--dark-color); }
.text-light { color: var(--light-color); }

/* Animations */
.animate-fadeIn {
  animation: fadeIn 0.5s ease-in-out;
}

.animate-slideUp {
  animation: slideUp 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

body {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--dark-color);
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow-x: hidden;
}

/* Modern Button Styles */
.btn-modern {
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 7px 14px rgba(0, 0, 0, 0.2);
}

.btn-modern:active {
  transform: translateY(0);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Card Styles */
.card-modern {
  border-radius: 15px;
  border: none;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transition: all var(--transition-speed) ease;
}

.card-modern:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

/* Form Controls */
.form-control-modern {
  border-radius: 8px;
  border: 1px solid #e1e5eb;
  padding: 0.75rem 1.25rem;
  transition: all 0.2s ease;
}

.form-control-modern:focus {
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
  border-color: var(--primary-color);
}

/* Page Transitions */
.page-enter-active, .page-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.page-enter, .page-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Animation utilities */
.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.slide-up {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from { 
    transform: translateY(30px);
    opacity: 0;
  }
  to { 
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
