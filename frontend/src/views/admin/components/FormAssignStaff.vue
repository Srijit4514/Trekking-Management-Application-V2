<template>
  <div class="card p-3 shadow-sm">
    <h5>Assign Staff to Trail</h5>
    <form @submit.prevent="handleSubmit">
      <div class="mb-2">
        <select v-model="assignment.trek_id" class="form-select" required>
          <option value="">Select Target Trek Route...</option>
          <option v-for="t in treks" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
      </div>
      <div class="mb-2">
        <select v-model="assignment.staff_id" class="form-select">
          <option value="">-- No Staff Assigned / Clear Staff --</option>
          <option v-for="s in activeStaff" :key="s.id" :value="s.id">{{ s.username }}</option>
        </select>
      </div>
      <button type="submit" class="btn btn-dark w-100 btn-sm">Bind Assignment</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  treks: { type: Array, required: true },
  activeStaff: { type: Array, required: true }
});

const emit = defineEmits(['assign']);
const assignment = ref({ trek_id: '', staff_id: '' });

const handleSubmit = () => {
  emit('assign', { ...assignment.value });
  assignment.value = { trek_id: '', staff_id: '' };
};
</script>