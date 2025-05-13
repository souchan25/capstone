/**
 * Custom filter dropdown functionality for CPSU Health Assistant
 */
document.addEventListener('DOMContentLoaded', function() {
  // Initialize custom dropdowns
  initDropdowns();
  
  // Initialize filter dropdowns
  initFilterDropdowns();
});

/**
 * Initialize custom dropdowns
 */
function initDropdowns() {
  const dropdowns = document.querySelectorAll('.custom-dropdown');
  
  dropdowns.forEach(dropdown => {
    const selected = dropdown.querySelector('.dropdown-selected');
    const options = dropdown.querySelector('.dropdown-options');
    
    // Toggle dropdown
    selected.addEventListener('click', function() {
      dropdown.classList.toggle('dropdown-open');
      
      // Close other dropdowns
      dropdowns.forEach(otherDropdown => {
        if (otherDropdown !== dropdown) {
          otherDropdown.classList.remove('dropdown-open');
        }
      });
    });
    
    // Select option
    const optionsList = dropdown.querySelectorAll('.dropdown-option');
    optionsList.forEach(option => {
      option.addEventListener('click', function() {
        // Update selected value
        const value = this.getAttribute('data-value');
        const text = this.textContent.trim();
        selected.querySelector('span').textContent = text;
        
        // Update hidden input
        const hiddenInput = dropdown.querySelector('input[type="hidden"]');
        if (hiddenInput) {
          hiddenInput.value = value;
        }
        
        // Update selected state
        optionsList.forEach(opt => opt.classList.remove('selected'));
        this.classList.add('selected');
        
        // Close dropdown
        dropdown.classList.remove('dropdown-open');
      });
    });
  });
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.custom-dropdown')) {
      dropdowns.forEach(dropdown => {
        dropdown.classList.remove('dropdown-open');
      });
    }
  });
}

/**
 * Initialize filter dropdowns
 */
function initFilterDropdowns() {
  const filterDropdowns = document.querySelectorAll('.filter-dropdown');
  
  filterDropdowns.forEach(dropdown => {
    const header = dropdown.querySelector('.filter-dropdown-header');
    
    // Toggle dropdown menu
    header.addEventListener('click', function() {
      dropdown.classList.toggle('open');
      
      // Close other dropdowns
      filterDropdowns.forEach(otherDropdown => {
        if (otherDropdown !== dropdown) {
          otherDropdown.classList.remove('open');
        }
      });
    });
    
    // Select filter option
    const items = dropdown.querySelectorAll('.filter-dropdown-item');
    items.forEach(item => {
      item.addEventListener('click', function() {
        // Toggle selection
        items.forEach(i => i.classList.remove('selected'));
        this.classList.add('selected');
        
        // Update header text
        const value = this.getAttribute('data-value');
        const text = this.textContent.trim();
        header.querySelector('span').textContent = text;
        
        // Update hidden input if exists
        const hiddenInput = dropdown.querySelector('input[type="hidden"]');
        if (hiddenInput) {
          hiddenInput.value = value;
        }
        
        // Close dropdown
        dropdown.classList.remove('open');
      });
    });
  });
  
  // Close filter dropdowns when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.filter-dropdown')) {
      filterDropdowns.forEach(dropdown => {
        dropdown.classList.remove('open');
      });
    }
  });
}
