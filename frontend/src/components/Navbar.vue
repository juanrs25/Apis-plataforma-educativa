<template>
  <nav class="navbar">
    <a href="/" class="nav-link main-link">Educando</a>

    <div class="nav-links-group">
      <template v-if="!auth.token">
        <div class="guest-links">
          <a href="/registro" class="nav-link">Registro</a>
          <a href="/login" class="nav-link">Login</a>
        </div>
      </template>

      <template v-else>
        <!-- CLIENTE -->
        <template v-if="auth.rol.toLowerCase() === 'cliente'">
          <a href="/clases" class="nav-link">Clases Solicitadas</a>
          <a href="/pqrs" class="nav-link">PQRS</a>
          <a href="/acerca" class="nav-link">Acerca de Nosotros</a>
        </template>

        <!-- DOCENTE -->
        <template v-else-if="auth.rol && auth.rol.toLowerCase() === 'docente'">
          <a href="/pqrs" class="nav-link">PQRS</a>
          <a href="/mis-pqrs" class="nav-link">Mis PQR</a>
        </template>

        <div class="user-menu">
          <div class="user-trigger" @click="toggleMenu">
            Hola, {{ auth.nombre }} ▼
          </div>

          <div class="dropdown" v-if="mostrarMenu">
            <p class="dropdown-name">{{ auth.nombre }}</p>
            <p class="dropdown-rol">{{ auth.rol }}</p>
            <button @click="cerrarSesion" class="dropdown-logout">
              Cerrar&nbsp;Sesión
            </button>
          </div>
        </div>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "../store/auth";
import { useRouter } from "vue-router";
import { ref } from "vue";
const mostrarMenu = ref(false);

const auth = useAuthStore();
const router = useRouter();
const toggleMenu = () => {
  mostrarMenu.value = !mostrarMenu.value;
};
const cerrarSesion = () => {
  auth.logout();
  router.push("/"); // vuelve al home tras cerrar sesión
};
</script>

<style scoped>
.guest-links {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1; /* Esto permite que tome todo el espacio disponible */
}

.user-menu {
  position: relative;
  margin-left: 20px;
  cursor: pointer;
  color: white;
  font-weight: 500;
}

/* Contenedor del dropdown */
.dropdown {
  position: absolute;
  top: 48px;
  right: 0;
  background: white;
  color: black;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  min-width: 160px;
  text-align: left;
  z-index: 2000;

}



/* Nombre y rol */
.dropdown-name {
  font-weight: bold;
  margin: 0;
}

.dropdown-rol {
  font-size: 0.85rem;
  color: #555;
  margin: 4px 0 12px 0;
}

/* Botón de cerrar sesión dentro del dropdown */
.dropdown-logout {
  width: 100%;
  background: #ff5555;
  border: none;
  padding: 8px 10px;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}

.dropdown-logout:hover {
  background: #ff2f2f;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #22577a;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin-left: 20px;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #9a79ff;
}

.main-link {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
}

.nav-links-group {
  display: flex;
  align-items: center;
  flex: 0.6; /* Añadir esta línea si no está */
}

.logout-btn {
  margin-left: 20px;
  background-color: #ff5555;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.logout-btn:hover {
  background-color: #ff2f2f;
}
</style>
