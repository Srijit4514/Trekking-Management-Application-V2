<template>
  <div class="row justify-content-center">
    <div class="col-md-5 col-lg-4">
      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-body p-4 p-sm-5">
          <h2 class="card-title text-center mb-4 fw-bold text-dark">Sign In</h2>
          
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="username" class="form-label fw-semibold">Username</label>
              <input 
                type="text" 
                class="form-control form-control-lg" 
                id="username" 
                v-model="form.username" 
                placeholder="Enter your username" 
                required
              >
            </div>

            <div class="mb-4">
              <label for="password" class="form-label fw-semibold">Password</label>
              <input 
                type="password" 
                class="form-control form-control-lg" 
                id="password" 
                v-model="form.password" 
                placeholder="Enter your password" 
                required
              >
            </div>

            <div v-if="errorMessage" class="alert alert-danger py-2 small" role="alert">
              {{ errorMessage }}
            </div>

            <div class="d-grid mb-3">
              <button type="submit" class="btn btn-primary btn-lg fw-bold" :disabled="isLoading">
                {{ isLoading ? 'Logging in...' : 'Log In' }}
              </button>
            </div>

            <div class="text-center">
              <span class="text-muted">New to the portal?</span> 
              <router-link to="/register" class="text-decoration-none fw-semibold ms-1">Create account</router-link>
            </div>
          </form>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api.js'  

const router = useRouter()

const form = reactive({
  username: '',
  password: ''
})

const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const data = await api.auth.login(form)
    
    localStorage.setItem('authToken', data.token)
    
    if (data.role === 'admin') {
      router.push('/admin_dashboard')
    } else if (data.role === 'staff') {
      router.push('/staff_dashboard')
    } else {
      router.push('/user_dashboard')
    }

  } catch (error) {
    errorMessage.value = error.message || 'An unexpected error occurred.'
  } finally {
    isLoading.value = false
  }
}
</script>