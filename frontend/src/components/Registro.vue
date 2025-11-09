<template>
  <div class="registro-container">
    <div class="registro-card">
      <!-- Columna izquierda: formulario -->
      <div class="form-section">
        <h2>Registro de Usuario</h2>
        <form @submit.prevent="registrar" class="formulario">
          <input v-model="form.Usuario" placeholder="Usuario" required />
          <input v-model="form.Clave" type="password" placeholder="Contraseña" required />
          <input v-model="form.Nombre_Completo" placeholder="Nombre completo" required />
          <input v-model="form.Telefono" placeholder="Teléfono" />
          <input v-model="form.Direccion" type="text" placeholder="Dirección" required />
          <input v-model="form.Email" type="email" placeholder="Correo electrónico" required />

          <select v-model="form.rol_id" required>
            <option disabled value="">Selecciona un rol</option>
            <option value="2">Cliente</option>
            <option value="3">Docente</option>
          </select>

          <button type="submit" class="btn-registrar">Registrar</button>
        </form>
        <p class="mensaje">{{ mensaje }}</p>
      </div>

      <!-- Columna derecha: bienvenida -->
      <div class="welcome-section">
        <h2>¡Bienvenido!</h2>
        <p>
          Crea tu cuenta para acceder a nuestra plataforma educativa y disfrutar
          de herramientas interactivas, recursos exclusivos y más.
        </p>
        <router-link to="/login">
          <button class="btn-login">Iniciar sesión</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const form = ref({
  Usuario: '',
  Clave: '',
  Nombre_Completo: '',
  Telefono: '',
  Direccion: '',
  Email: '',
  rol_id: ''
})

const mensaje = ref('')

const registrar = async () => {
  try {
    const res = await axios.post('http://localhost:5001/registro', form.value)
    mensaje.value = res.data.message
  } catch (err) {
    mensaje.value = err.response?.data?.message || 'Error en el registro'
  }
}
</script>

<style scoped>
/* Centrado del contenedor general */
.registro-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 75vh;
  width: 840px;
  background: linear-gradient(135deg, #7db2ff, #0b08d3);
  font-family: "Poppins", sans-serif;
}

/* Tarjeta con dos secciones */
.registro-card {
  display: flex;
  width: 800px;
  height: 500px;

  background: #fbfbfb;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

/* Sección izquierda: formulario */
.form-section {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-section h2 {
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.formulario {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.formulario input,
.formulario select {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s;
}

.formulario input:focus,
.formulario select:focus {
  border-color: #340bfe;
}

.btn-registrar {
  margin-top: 10px;
  padding: 12px;
  background-color: #2d08e6;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-registrar:hover {
  background-color: #3620a5;
}

.mensaje {
  margin-top: 10px;
  color: #333;
  text-align: center;
}

/* Sección derecha: bienvenida */
.welcome-section {
  flex: 1;
  background: linear-gradient(135deg, #2201c8, #3a03de);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px;
}

.welcome-section h2 {
  margin-bottom: 10px;
}

.welcome-section p {
  margin-bottom: 20px;
  font-size: 1rem;
  line-height: 1.5;
}

.btn-login {
  background: white;
  color: #7b61ff;
  font-weight: bold;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-login:hover {
  background: #f2f2f2;
}
</style>
