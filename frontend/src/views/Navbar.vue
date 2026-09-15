<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/">TrekkingPortal</router-link>
      
      <div class="ms-auto">
        <template v-if="isAdminRoute">
          <button @click="handleAdminLogout" class="btn btn-danger btn-sm">
            Admin Logout
          </button>
        </template>

        <template v-if="isStaffRoute">
          <button @click="handleStaffLogout" class="btn btn-danger btn-sm">
            Staff Logout
          </button>
        </template>

        <template v-if="isUserRoute">
          <button @click="handleUserLogout" class="btn btn-danger btn-sm">
            User Logout
          </button>
        </template>

        <template v-if="!isAdminRoute && !isStaffRoute && !isUserRoute">
          <router-link to="/login" class="btn btn-light btn-sm me-2">Login</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm me-2">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const isAdminRoute = computed(() => {
  return route.path.startsWith('/admin');
});

const handleAdminLogout = () => {
  console.log("Admin logging out... clearing session parameters.");
  router.push('/login');
};

const isStaffRoute = computed(() => {
  return route.path.startsWith('/staff');
});

const handleStaffLogout = () => {
  console.log("Staff logging out... clearing session parameters.");
  router.push('/login');
};

const isUserRoute = computed(() => {
  return route.path.startsWith('/user');
});

const handleUserLogout = () => {
  console.log("User logging out... clearing session parameters.");
  router.push('/login');
};
</script>