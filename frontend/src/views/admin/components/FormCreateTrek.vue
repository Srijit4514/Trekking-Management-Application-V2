<template>
  <div class="card p-3 shadow-sm">
    <h5>Create New Trek</h5>
    <form @submit.prevent="handleSubmit">
      <div class="mb-2"><input type="text" v-model="newTrek.name" class="form-control" placeholder="Trek Name" required></div>
      <div class="mb-2"><input type="text" v-model="newTrek.difficulty" class="form-control" placeholder="Difficulty (Easy / Moderate / Hard)" required></div>
      <div class="mb-2"><input type="number" v-model="newTrek.slots" class="form-control" placeholder="Slots Available" required></div>
      <div class="mb-2"><input type="text" v-model="newTrek.location" class="form-control" placeholder="Trek Location" required></div>
      <div class="mb-2"><input type="date" v-model="newTrek.start_date" class="form-control" required></div>
      <div class="mb-2"><input type="date" v-model="newTrek.end_date" class="form-control" required></div>
      <div class="mb-2"><input type="number" v-model="newTrek.price" class="form-control" placeholder="Trek Price" required></div>
      <button type="submit" class="btn btn-primary w-100 btn-sm">Save Route</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['create']);
const newTrek = ref({ name: '', difficulty: '', slots: null, location: '', start_date: '', end_date: '', price: null });

const handleSubmit = () => {
  emit('create', { ...newTrek.value });
  // Clear form
  newTrek.value = { name: '', difficulty: '', slots: null, location: '', start_date: '', end_date: '', price: null };
};
</script>