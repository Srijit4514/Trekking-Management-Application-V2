<template>
  <div class="container my-4">
    <div class="border-bottom pb-3 mb-4 d-flex justify-content-between align-items-center">
      <div>
        <h2>Trekker Workspace Console</h2>
        <p class="text-muted mb-0">Welcome back, <strong>{{ username }}</strong>. Plan your next adventure below.</p>
      </div>
      <button class="btn btn-secondary btn-sm" @click="showProfileModal = true">
        Edit Profile
      </button>
    </div>

    <div class="mb-5">
      <h4 class="fw-bold mb-3 text-dark">Your Bookings & Expedition History</h4>
      <div v-if="bookings.length === 0" class="alert alert-light border text-center py-4">
        <p class="text-muted mb-0">You haven't booked any trekking expeditions yet.</p>
      </div>
      <div v-else class="row g-3">
        <div v-for="booking in bookings" :key="booking.id" class="col-md-4">
          <div class="card h-100 shadow-sm border border-light">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="fw-bold mb-0 text-primary">{{ booking.trek_name }}</h6>
                <span :class="getBadgeClass(booking.booking_status)">{{ booking.booking_status }}</span>
              </div>
              <p class="small text-muted mb-1"><strong>Location:</strong> {{ booking.location }}</p>
              <p class="small text-muted mb-1"><strong>Starts:</strong> {{ booking.start_date }}</p>
              <p class="small text-muted mb-1"><strong>Duration:</strong> {{ booking.duration }}</p>
              <p class="small text-muted mb-0"><strong>Payment:</strong> 
                <span class="badge bg-light text-dark ms-1">{{ booking.payment_status }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <h4 class="fw-bold mb-3 text-dark">Explore Available Expeditions</h4>
      
      <div class="row g-2 mb-4 p-3 bg-white border rounded shadow-sm">
        <div class="col-md-4">
          <label class="form-label small fw-bold">Search Location</label>
          <input type="text" v-model="filters.location" class="form-control form-control-sm" placeholder="e.g., Himalayas">
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold">Difficulty</label>
          <select v-model="filters.difficulty" class="form-select form-select-sm">
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-bold">Duration</label>
          <input type="text" v-model="filters.duration" class="form-control form-control-sm" placeholder="e.g., 7 Days">
        </div>
        <div class="col-md-2 d-flex align-items-end">
          <button class="btn btn-primary btn-sm w-100" @click="fetchDashboardData">Search</button>
        </div>
      </div>

      <div v-if="availableTreks.length === 0" class="alert alert-secondary text-center py-4">
        <p class="mb-0">No matching treks are currently open for registration.</p>
      </div>
      <div v-else class="row g-4">
        <div v-for="trek in availableTreks" :key="trek.id" class="col-md-6">
          <div class="card h-100 shadow-sm border">
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="fw-bold text-dark mb-0">{{ trek.name }}</h5>
                <span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">
                  ₹{{ trek.price }}
                </span>
              </div>
              <p class="card-text mb-1"><strong>Location:</strong> {{ trek.location }}</p>
              <p class="card-text mb-1"><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
              <p class="card-text mb-1"><strong>Duration:</strong> {{ trek.duration }}</p>
              <p class="card-text mb-1"><strong>Dates:</strong> {{ trek.start_date }} to {{ trek.end_date }}</p>
              <p class="card-text mb-3 text-secondary"><strong>Slots Left:</strong> {{ trek.slots }} remaining</p>
              
              <button 
                class="btn btn-dark btn-sm mt-auto w-100" 
                :disabled="trek.slots <= 0"
                @click="handleBookTrek(trek.id)"
              >
                {{ trek.slots > 0 ? 'Book Expedition' : 'Sold Out' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showProfileModal" class="modal-backdrop fade show"></div>
    <div v-if="showProfileModal" class="modal d-block tab-modal mt-5" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title fw-bold">Update Profile Settings</h5>
            <button type="button" class="btn-close" @click="showProfileModal = false"></button>
          </div>
          <form @submit.prevent="handleUpdateProfile">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label small fw-bold">Username</label>
                <input type="text" v-model="profileForm.username" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold">Email Address</label>
                <input type="email" v-model="profileForm.email" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold">New Password (Leave blank to keep current)</label>
                <input type="password" v-model="profileForm.password" class="form-control">
              </div>
            </div>
            <div class="modal-header border-top-0 d-flex gap-2">
              <button type="button" class="btn btn-secondary btn-sm" @click="showProfileModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary btn-sm">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { api } from '@/services/api.js'

const username = ref('user')
const availableTreks = ref([])
const bookings = ref([])
const showProfileModal = ref(false)

const filters = reactive({
  location: '',
  difficulty: '',
  duration: ''
})

const profileForm = reactive({
  username: '',
  email: '',
  password: ''
})

const fetchDashboardData = async () => {
  try {
    const data = await api.user.getDashboard(filters)
    username.value = data.user_profile.username
    availableTreks.value = data.available_treks
    bookings.value = data.bookings
    
    profileForm.username = data.user_profile.username
    profileForm.email = data.user_profile.email
  } catch (error) {
    alert(error.message || "Failed to load trekker dashboard elements.")
  }
}

onMounted(() => {
  fetchDashboardData()
})

const handleBookTrek = async (trekId) => {
  if (!confirm("Are you sure you want to book a reservation slot for this trek?")) return
  try {
    const response = await api.user.bookTrek(trekId)
    alert(response.message || "Trek successfully booked!")
    fetchDashboardData() 
  } catch (error) {
    alert(error.message || "Failed to finalize trek booking.")
  }
}

const handleUpdateProfile = async () => {
  try {
    const payload = { username: profileForm.username, email: profileForm.email }
    if (profileForm.password) payload.password = profileForm.password
    
    const response = await api.user.updateProfile(payload)
    alert(response.message || "Profile changes applied.")
    showProfileModal.value = false
    fetchDashboardData()
  } catch (error) {
    alert(error.message || "Profile synchronization failure.")
  }
}

const getBadgeClass = (status) => {
  const base = 'badge '
  if (status === 'Booked') return base + 'bg-primary-subtle text-primary'
  if (status === 'Completed') return base + 'bg-success-subtle text-success'
  if (status === 'Cancelled') return base + 'bg-danger-subtle text-danger'
  return base + 'bg-secondary-subtle text-secondary'
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}
.modal.tab-modal {
  z-index: 1050;
}
</style>