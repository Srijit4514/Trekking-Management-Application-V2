<template>
  <div class="table-responsive">
    <table class="table table-striped align-middle">
      <thead>
        <tr><th>ID</th><th>Trek Name</th><th>Difficulty</th><th>Duration</th><th>Remaining Slots</th><th>Location</th><th>Starting Date</th><th>Ending Date</th><th>Trek Price</th><th>Assigned Guide</th><th>Operations</th></tr>
      </thead>
      <tbody>
        <tr v-for="t in treks" :key="t.id">
          <td>{{ t.id }}</td>
          <td><strong>{{ t.name }}</strong></td>
          <td>{{ t.difficulty }}</td>
          <td>{{ t.duration }}</td>
          <td>{{ t.slots }} Slots</td>
          <td>{{ t.location }}</td>
          <td>{{ t.start_date }}</td>
          <td>{{ t.end_date }}</td>
          <td>{{ t.price }}₹</td>
          <td>
            <span v-if="t.assigned_staff" class="badge bg-dark">{{ t.assigned_staff.username }}</span>
            <span v-else class="text-muted small">None Assigned</span>
          </td>
          <td>
            <div class="d-flex gap-2">
              <button class="btn btn-sm btn-success" @click="$emit('edit', t)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="$emit('remove', t.id)">Remove</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  treks: { type: Array, required: true }
});
defineEmits(['edit', 'remove']);
</script>