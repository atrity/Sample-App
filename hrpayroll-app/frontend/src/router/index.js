import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Route Components
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import Employees from '@/views/Employees.vue'
import Departments from '@/views/Departments.vue'
import Payroll from '@/views/Payroll.vue'
import Attendance from '@/views/Attendance.vue'
import NotFound from '@/views/NotFound.vue'

// Route Configuration
const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      layout: 'auth',
      title: 'Login',
      requiresAuth: false
    }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: {
      title: 'Dashboard',
      requiresAuth: true
    }
  },
  {
    path: '/employees',
    name: 'employees',
    component: Employees,
    meta: {
      title: 'Employees',
      requiresAuth: true
    }
  },
  {
    path: '/departments',
    name: 'departments',
    component: Departments,
    meta: {
      title: 'Departments',
      requiresAuth: true
    }
  },
  {
    path: '/payroll',
    name: 'payroll',
    component: Payroll,
    meta: {
      title: 'Payroll',
      requiresAuth: true
    }
  },
  {
    path: '/attendance',
    name: 'attendance',
    component: Attendance,
    meta: {
      title: 'Attendance',
      requiresAuth: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: {
      title: 'Page Not Found',
      requiresAuth: false
    }
  }
]

// Router Instance
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation Guards
router.beforeEach(async (to, from, next) => {
  // Update page title
  document.title = `${to.meta.title} - HR Payroll`

  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = authStore.isAuthenticated

  // Handle authentication
  if (requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

// Error Handling
router.onError((error) => {
  console.error('Router error:', error)
  router.push({ name: 'not-found' })
})

export default router
