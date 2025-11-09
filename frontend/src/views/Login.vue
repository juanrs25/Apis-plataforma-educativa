<template>
  <div class="login-page">
    <div class="login-container">
      <h2 class="welcome-text">Welcome Back</h2>
      <form @submit.prevent="loginUsuario">
        <label for="username">Username</label>
        <input
          id="username"
          v-model="form.Usuario"
          placeholder="Enter your username"
          required
        />

        <label for="password">Password</label>
        <input
          id="password"
          v-model="form.Clave"
          type="password"
          placeholder="Enter your password"
          required
        />

        <button type="submit" class="login-button">Login</button>
      </form>
      <!--<p class="forgot-password">Forgot Password?</p>-->
      <p class="message">{{ mensaje }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { useAuthStore } from "../store/auth";
import { useRouter } from "vue-router";

const form = ref({ Usuario: "", Clave: "" });
const mensaje = ref("");
const router = useRouter();
const auth = useAuthStore();

const loginUsuario = async () => {
  try {
    const res = await axios.post("http://localhost:5001/login", form.value);
    auth.login(res.data.token, res.data.rol, res.data.nombre);
    mensaje.value = res.data.message;
    if (res.data.rol?.toLowerCase() === "cliente") {
      router.push("/home");
  } else if (res.data.rol?.toLowerCase() === "docente") {
      router.push("/dashboard");
    }
  } catch (err) {
    mensaje.value =
      err.response?.data?.message || "Error en el inicio de sesión";
  }
};
</script>

<style scoped>
/* -------------------------------------- */
/* 2. Estilos del Contenedor del Formulario (AQUÍ ESTÁ EL CAMBIO) */
/* -------------------------------------- */
.login-container {
  width: 350px;
  padding: 40px;
  border-radius: 12px;
  background-color: #161b22;

  /* ¡AQUÍ ESTÁ EL EFECTO DE RESPLANDOR DEL BORDE! */
  /* Múltiples sombras: una para la profundidad y otra para el brillo */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5),
    /* Sombra de profundidad */ 0 0 20px rgba(4, 24, 248, 0.4); /* Resplandor verde tenue */

  /* El borde sólido se puede mantener o ajustar */
  border: 1px solid #30363d;
}

/* -------------------------------------- */
/* 3. Tipografía y Encabezado */
/* -------------------------------------- */
.welcome-text {
  font-size: 2.2em;
  font-weight: 700;
  color: white;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* -------------------------------------- */
/* 4. Labels y Campos de Entrada (Inputs) */
/* -------------------------------------- */
form {
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 15px;
  margin-bottom: 5px;
  font-size: 0.9em;
  color: #c9d1d9;
}

input {
  padding: 12px 15px;
  border: 1px solid #30363d;
  border-radius: 8px;
  background-color: #0d1117;
  color: white;
  font-size: 1em;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #38a169;
  outline: none;
}

input::placeholder {
  color: #586069;
}

/* -------------------------------------- */
/* 5. Botón de Login (Verde) */
/* -------------------------------------- */
.login-button {
  margin-top: 30px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background-color: #1203eb;
  color: white;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s;
}

.login-button:hover {
  background-color: #2f855a;
}

.login-button:active {
  transform: scale(0.99);
}

/* -------------------------------------- */
/* 6. Enlaces y Mensajes */
/* -------------------------------------- */
.forgot-password {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9em;
  color: #8b949e;
  cursor: pointer;
}

.forgot-password:hover {
  color: #58a6ff;
}

.message {
  text-align: center;
  margin-top: 15px;
  color: #e55353;
}
</style>
