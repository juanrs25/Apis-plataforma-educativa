<template>
  <div class="dashboard-container">
    <h2>Bienvenido al Dashboard</h2>
    <p>Tu rol: {{ auth.rol }}</p>
    <button @click="cerrarSesion">Cerrar sesión</button>
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