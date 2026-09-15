<template>
  <div class="container my-4">
    <div class="border-bottom pb-3 mb-4">
      <h2>Staff Operations Console</h2>
      <p class="text-muted">
        Welcome back, <strong>{{ username }}</strong>. Manage your assigned treks and view registered travelers below.
      </p>
    </div>

    <h4 class="fw-bold mb-3">Your Assigned Trekking Expeditions</h4>
    
    <div class="row g-4">
      <div v-for="trek in treks" :key="trek.id" class="col-md-6">
        <div class="card shadow-sm border h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title fw-bold text-primary mb-0">{{ trek.name }}</h5>
              <span :class="getStatusBadgeClass(trek.status)">
                {{ trek.status }}
              </span>
            </div>
            
            <p class="card-text mb-1"><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
            <p class="card-text mb-1"><strong>Duration:</strong> {{ trek.duration }}</p>
            <p class="card-text mb-1"><strong>Starting-date:</strong> {{ trek.start_date }}</p>
            <p class="card-text mb-1"><strong>Ending-date:</strong> {{ trek.end_date }}</p>
            <p class="card-text mb-1"><strong>Remaining Slots:</strong> {{ trek.slots }} left</p>
            <p class="card-text mb-3"><strong>Trek Price:</strong> {{ trek.price }}</p>
            
            <hr>

            <form @submit.prevent="updateTrekParameters(trek)" class="row g-2 align-items-end mb-4">
              <div class="col-6">
                <label class="form-label small fw-bold mb-1">Update Slots</label>
                <input 
                  type="number" 
                  v-model.number="trek.slots" 
                  class="form-control form-control-sm" 
                  required
                >
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold mb-1">Trek Status</label>
                <select v-model="trek.status" class="form-select form-select-sm" required>
                  <option value="Pending">Pending</option>
                  <option value="Approved">Approved</option>
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
              <div class="col-12 mt-2">
                <button type="submit" class="btn btn-dark btn-sm w-100">Save</button>
              </div>
              <div v-if="trek.isSaved" class="col-12 mt-2">
                <div class="alert alert-success py-1 text-center mb-0 small">
                  Trek data updated successfully!
                </div>
              </div>
            </form>

            <h6 class="fw-bold text-secondary mb-2">
              Registered Trekkers ({{ trek.bookings ? trek.bookings.length : 0 }})
            </h6>
            <div class="border rounded bg-light p-2" style="max-height: 150px; overflow-y: auto;">
              <ul v-if="trek.bookings && trek.bookings.length > 0" class="list-group list-group-flush small">
                <li 
                  v-for="booking in trek.bookings" 
                  :key="booking.id" 
                  class="list-group-item d-flex justify-content-between align-items-center bg-transparent py-1 px-1"
                >
                  <span>{{ booking.user?.username }}</span>
                  <span>
                    <span :class="getBookingBadgeClass(booking.booking_status)">
                      {{ booking.booking_status }}
                    </span>
                  </span>
                </li>
              </ul>
              <p v-else class="text-muted small text-center mb-0 py-2">
                No trekkers registered for this expedition yet.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="treks.length === 0" class="col-12">
        <div class="alert alert-secondary text-center py-4" role="alert">
          <h5 class="alert-heading fw-bold mb-1">No Assignments Yet</h5>
          <p class="mb-0 text-muted">You are not currently assigned to any active trekking routes. Please contact the administrator.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/services/api.js'

const username = ref('Staff Member')
const treks = ref([])

onMounted(async () => {
    try {
        const data = await api.staff.getDashboard()
        username.value = data.username
        treks.value = data.treks
    } catch (error) {
        console.error("Dashboard fetch error:", error)
        alert(error.message || "Failed to load dashboard data.")
    }
})

const updateTrekParameters = async (trek) => {
    try {
        const payload = {
            slots: parseInt(trek.slots, 10),
            status: trek.status 
        }

        const response = await api.staff.updateTrek(trek.id, payload)
        alert(response.message)

        trek.isSaved = true

        if (trek.status === "Completed") {
            trek.bookings.forEach(b => {
                if (b.booking_status === "Booked") b.booking_status = "Completed"
            })
        }

        setTimeout(() => {
            trek.isSaved = false
        }, 3000)  // 3 seconds feedback display

    } catch (error) {
        console.error("Error updating trek parameters:", error)
        alert(error.message || "Failed to update trek parameters.")
    }

}

const getStatusBadgeClass = (status) => {
  const baseClasses = 'badge border px-2 py-1 '
  switch (status) {
    case 'Open': return baseClasses + 'bg-success-subtle text-success border-success-subtle'
    case 'Completed': return baseClasses + 'bg-info-subtle text-info border-info-subtle'
    case 'Pending': return baseClasses + 'bg-warning-subtle text-warning border-warning-subtle'
    case 'Approved': return baseClasses + 'bg-primary-subtle text-primary border-primary-subtle'
    default: return baseClasses + 'bg-danger-subtle text-danger border-danger-subtle'
  }
}

const getBookingBadgeClass = (status) => {
  const baseClasses = 'badge small '
  switch (status) {
    case 'Booked': return baseClasses + 'bg-primary-subtle text-primary'
    case 'Cancelled': return baseClasses + 'bg-danger-subtle text-danger'
    case 'Completed': return baseClasses + 'bg-success-subtle text-success'
    default: return baseClasses + 'bg-secondary-subtle text-secondary'
  }
}
</script>