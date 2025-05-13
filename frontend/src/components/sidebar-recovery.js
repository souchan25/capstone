/**
 * Sidebar Recovery Script
 * This script provides fallback recovery mechanisms to ensure the sidebar is always available
 */

// This function will be automatically called when imported
(function initializeSidebarRecovery() {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupSidebarRecovery);
  } else {
    setupSidebarRecovery();
  }
})();

function setupSidebarRecovery() {
  // Add global event listener to detect when Vue app is mounted
  window.addEventListener('load', checkSidebarVisibility);
  
  // Check periodically to ensure sidebar remains visible
  setInterval(checkSidebarVisibility, 2000);
}

function checkSidebarVisibility() {
  // Target sidebar and toggle elements
  const sidebarWrapper = document.querySelector('.sidebar-wrapper');
  // No need to select sidebar element if we're not using it
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  
  // If sidebar wrapper exists but is not visible, force display it
  if (sidebarWrapper) {
    const computedStyle = window.getComputedStyle(sidebarWrapper);
    if (computedStyle.display === 'none' || computedStyle.visibility === 'hidden') {
      console.log('Sidebar recovery: Restoring hidden sidebar wrapper');
      sidebarWrapper.style.display = 'block';
      sidebarWrapper.style.visibility = 'visible';
    }
  }
  
  // If toggle button exists but is not visible, force display it
  if (sidebarToggle) {
    const computedStyle = window.getComputedStyle(sidebarToggle);
    if (computedStyle.display === 'none' || computedStyle.visibility === 'hidden') {
      console.log('Sidebar recovery: Restoring hidden sidebar toggle button');
      sidebarToggle.style.display = 'flex';
      sidebarToggle.style.visibility = 'visible';
      sidebarToggle.style.zIndex = '100';
    }
  }
  
  // Check localStorage for sidebar state
  const sidebarState = localStorage.getItem('sidebarCollapsed');
  if (sidebarState === null || sidebarState === undefined) {
    // If state is missing, reset it to default (sidebar visible)
    localStorage.setItem('sidebarCollapsed', 'false');
  }
}

// Export a function that can be called manually if needed
export function recoverSidebar() {
  checkSidebarVisibility();
}
