/**
 * Sidebar Debug Tool
 * This script provides helper functions to troubleshoot sidebar visibility issues
 */

// Debug information
console.log('Sidebar Debug Tool loaded');

// Print sidebar state on page load
window.addEventListener('load', () => {
  printSidebarState();
});

// Helper function to print sidebar state
function printSidebarState() {
  const sidebarWrapper = document.querySelector('.sidebar-wrapper');
  const sidebar = document.querySelector('.sidebar');
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const storedState = localStorage.getItem('sidebarCollapsed');
  
  console.log('--------- Sidebar Debug Info ---------');
  console.log('Sidebar localStorage state:', storedState);
  
  if (sidebarWrapper) {
    const style = window.getComputedStyle(sidebarWrapper);
    console.log('Sidebar Wrapper:', {
      display: style.display,
      visibility: style.visibility,
      width: style.width,
      opacity: style.opacity,
      position: style.position,
      zIndex: style.zIndex
    });
  } else {
    console.log('Sidebar Wrapper: Not found in DOM!');
  }
  
  if (sidebar) {
    const style = window.getComputedStyle(sidebar);
    console.log('Sidebar Element:', {
      display: style.display,
      visibility: style.visibility,
      width: style.width,
      transform: style.transform,
      opacity: style.opacity,
      position: style.position,
      zIndex: style.zIndex
    });
  } else {
    console.log('Sidebar Element: Not found in DOM!');
  }
  
  if (sidebarToggle) {
    const style = window.getComputedStyle(sidebarToggle);
    console.log('Sidebar Toggle Button:', {
      display: style.display,
      visibility: style.visibility,
      position: style.position,
      zIndex: style.zIndex
    });
  } else {
    console.log('Sidebar Toggle Button: Not found in DOM!');
  }
  
  console.log('-------------------------------------');
}

// Add a helper function to force sidebar visibility
window.forceSidebarVisibility = function() {
  const sidebarWrapper = document.querySelector('.sidebar-wrapper');
  const sidebar = document.querySelector('.sidebar');
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  
  if (sidebarWrapper) {
    sidebarWrapper.style.display = 'block';
    sidebarWrapper.style.visibility = 'visible';
    sidebarWrapper.style.width = '300px';
    sidebarWrapper.classList.remove('hidden');
  }
  
  if (sidebar) {
    sidebar.style.display = 'block';
    sidebar.style.visibility = 'visible';
    sidebar.style.width = '300px';
    sidebar.style.transform = 'none';
    sidebar.classList.remove('collapsed');
  }
  
  if (sidebarToggle) {
    sidebarToggle.style.display = 'flex';
    sidebarToggle.style.visibility = 'visible';
    sidebarToggle.style.zIndex = '100';
  }
  
  // Reset localStorage
  localStorage.setItem('sidebarCollapsed', 'false');
  
  // Print updated state
  console.log('Force sidebar visibility applied!');
  printSidebarState();
  
  return 'Sidebar visibility forced. Check console for details.';
};

// Export functions for use in Vue components
export { printSidebarState };
