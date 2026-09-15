<template>
  <div>
    <h5 class="fw-bold text-dark mb-3">Pending Verification Requests</h5>
    <table class="table table-bordered bg-light mb-4">
      <thead class="table-warning">
        <tr><th>Staff ID</th><th>Name</th><th>Email Address</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="s in pendingStaff" :key="s.id">
          <td>#{{ s.id }}</td>
          <td><strong>{{ s.username }}</strong></td>
          <td>{{ s.email }}</td>
          <td>
            <button class="btn btn-sm btn-success fw-bold" @click="$emit('toggle-status', s.id)">Activate</button>
          </td>
        </tr>
        <tr v-if="pendingStaff.length === 0">
          <td colspan="4" class="text-center text-muted py-2 small">No new pending staff approval requests found.</td>
        </tr>
      </tbody>
    </table>

    <h5 class="fw-bold text-dark mb-3">Active & Verified Staff</h5>
    <table class="table table-striped">
      <thead class="table-striped">
        <tr><th>Staff ID</th><th>Name</th><th>Email Address</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="s in activeStaff" :key="s.id">
          <td>#{{ s.id }}</td>
          <td>{{ s.username }}</td>
          <td>{{ s.email }}</td>
          <td>
            <button class="btn btn-sm btn-danger" @click="$emit('toggle-status', s.id)">Blacklist Staff</button>
          </td>
        </tr>
        <tr v-if="activeStaff.length === 0">
          <td colspan="3" class="text-center text-muted py-2 small">No active staff found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  pendingStaff: { type: Array, required: true },
  activeStaff: { type: Array, required: true }
});
defineEmits(['toggle-status']);
</script>