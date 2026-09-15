<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Navbar />
    <main class="container my-auto py-4">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './views/Navbar.vue'
import Footer from './views/Footer.vue';
</script>

<style>
[v-cloak] {
  display: none;
}
</style>