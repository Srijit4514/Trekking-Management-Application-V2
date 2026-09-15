<template>
  <table class="table table-striped">
    <thead>
      <tr><th>User ID</th><th>Username</th><th>Email Address</th><th>Status</th><th>Restriction Matrix</th></tr>
    </thead>
    <tbody>
      <tr v-for="u in users" :key="u.id">
        <td>#{{ u.id }}</td>
        <td>{{ u.username }}</td>
        <td>{{ u.email }}</td>
        <td>
          <span v-if="u.is_active" class="badge bg-success">Active</span>
          <span v-else class="badge bg-danger">Blacklisted</span>
        </td>
        <td>
          <button 
            class="btn btn-sm" 
            :class="u.is_active ? 'btn-danger' : 'btn-success'" 
            @click="$emit('toggle-status', u.id)"
          >
            {{ u.is_active ? 'Blacklist User' : 'Approve/Unban' }}
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({
  users: { type: Array, required: true }
});
defineEmits(['toggle-status']);
</script>