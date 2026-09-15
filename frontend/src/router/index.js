import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import StaffDashboard from '@/views/staff/StaffDashboard.vue'
import UserDashboard from '@/views/user/UserDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
    path: '/admin_dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/staff_dashboard',
    name: 'StaffDashboard',
    component: StaffDashboard
  },
  {
    path: '/user_dashboard',
    name: 'UserDashboard',
    component: UserDashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router