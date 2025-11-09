<template>
  <div>
    <Navbar />
    <div class="contenido-principal">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style>

body{
  background-color: #E0E0E0;
}
/* 🔹 Agrega un margen superior para que el contenido no quede debajo del navbar */
.contenido-principal {
  margin-top: 70px; /* Altura un poco mayor que la del navbar */
  padding: 20px;
  min-height: 100vh;
}
</style>
