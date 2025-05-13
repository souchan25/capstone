// Version check utility
import { version } from 'vue';

console.log('Vue version:', version);

// Check if we're using Vue 2 or Vue 3
const isVue3 = version.startsWith('3');
console.log('Is Vue 3:', isVue3);

// Export this to use in main.js
export const vueInfo = {
  version,
  isVue3
}; 