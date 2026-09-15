<template>
  <div class="row g-3 mb-4">
    <div class="col-6 col-lg-3">
      <div class="p-3 bg-white border rounded shadow-sm text-center">
        <h6>Total Treks</h6>
        <h3>{{ metrics.totalTreks }}</h3>
      </div>
    </div>
    <div class="col-6 col-lg-3">
      <div class="p-3 bg-white border rounded shadow-sm text-center">
        <h6>Registered Users</h6>
        <h3>{{ metrics.totalUsers }}</h3>
      </div>
    </div>
    <div class="col-6 col-lg-3">
      <div class="p-3 bg-white border rounded shadow-sm text-center">
        <h6>Trek Staff</h6>
        <h3>{{ metrics.totalStaff }}</h3>
      </div>
    </div>
    <div class="col-6 col-lg-3">
      <div class="p-3 bg-white border rounded shadow-sm text-center">
        <h6>Bookings History</h6>
        <h3>{{ metrics.totalBookings }}</h3>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  metrics: {
    type: Object,
    required: true
  }
});
</script>