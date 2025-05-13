import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Dashboard from '../components/Dashboard.vue'
import ClinicDashboard from '../components/ClinicDashboard.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/clinic-dashboard',
      name: 'ClinicDashboard',
      component: ClinicDashboard,
      meta: { requiresAuth: true, requiresStaff: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      // No token, redirect to login
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // For routes requiring staff access, additional check would be needed
      // In a real app, you'd check the user role from the backend
      if (to.matched.some(record => record.meta.requiresStaff)) {
        // For demo purposes, just let them through (in real app, check role)
        next()
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router 