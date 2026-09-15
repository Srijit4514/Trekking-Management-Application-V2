<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-body p-4 p-sm-5">
          <h2 class="card-title text-center mb-4 fw-bold text-dark">Create an Account</h2>
          
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label for="username" class="form-label fw-semibold">Username</label>
              <input 
                type="text" 
                class="form-control form-control-lg" 
                id="username" 
                v-model="form.username" 
                placeholder="johndoe" 
                required
              >
            </div>

            <div class="mb-3">
              <label for="email" class="form-label fw-semibold">Email address</label>
              <input 
                type="email" 
                class="form-control form-control-lg" 
                id="email" 
                v-model="form.email" 
                placeholder="name@example.com" 
                required
              >
            </div>

            <div class="mb-3">
              <label for="password" class="form-label fw-semibold">Password</label>
              <input 
                type="password" 
                class="form-control form-control-lg" 
                id="password" 
                v-model="form.password" 
                placeholder="••••••••" 
                required
              >
            </div>
            <div v-if="errorMessage" class="alert alert-danger py-2 small" role="alert">
              {{ errorMessage }}
            </div>
            <div class="d-grid mb-3">
              <button type="submit" class="btn btn-primary btn-lg fw-bold" :disabled="isLoading">
                {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
              </button>
            </div>

            <div class="text-center">
              <span class="text-muted">Already have an account?</span> 
              <router-link to="/login" class="text-decoration-none fw-semibold ms-1">Log In</router-link>
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

const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: ''
})

const isLoading = ref(false) 
const errorMessage = ref('')

async function handleRegister() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('http://127.0.0.1:5001/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form)
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Registration failed. Please try again.')
    }

    alert('Account created successfully! Please log in.')
    router.push('/login')

  } catch (error) {
    errorMessage.value = error.message || 'An unexpected backend error occurred.'
  } finally {
    isLoading.value = false
  }
}
</script>