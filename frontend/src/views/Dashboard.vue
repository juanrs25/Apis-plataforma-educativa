<template>
  <div class="dashboard-container">
    <h2>Bienvenido al Dashboard</h2>
    <p>Bienvenido a tu panel de profesor  {{ auth.nombre }}</p>
    
  </div>
</template>

<script setup>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const cerrarSesion = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
</style>