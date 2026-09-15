<template>
  <div class="card p-3 shadow-sm">
    <h5>Add New Trek Staff</h5>
    <form @submit.prevent="handleSubmit">
      <div class="mb-2"><input type="text" v-model="newStaff.username" class="form-control" placeholder="Username" required></div>
      <div class="mb-2"><input type="email" v-model="newStaff.email" class="form-control" placeholder="Staff Email Address" required></div>
      <div class="mb-2"><input type="password" v-model="newStaff.password" class="form-control" placeholder="Password" required></div>
      <button type="submit" class="btn btn-success w-100 btn-sm">Register Staff Account</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['add']);
const newStaff = ref({ username: '', email: '', password: '' });

const handleSubmit = () => {
  emit('add', { ...newStaff.value });
  newStaff.value = { username: '', email: '', password: '' };
};
</script>