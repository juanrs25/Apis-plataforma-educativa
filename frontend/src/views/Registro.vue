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

          <select v-model.number="form.rol_id" required>
            <option disabled value="">Selecciona un rol</option>
            <option :value="2">Cliente</option>
            <option :value="3">Docente</option>
          </select>

          <!-- Campos adicionales SOLO para Docentes -->
          <template v-if="form.rol_id === 3">
            <input
              v-model="form.Experiencia"
              type="text"
              placeholder="Experiencia laboral"
              required
            />
            <input
              v-model="form.Titulo_Profesional"
              type="text"
              placeholder="Título profesional"
              required
            />
            <input
              type="file"
              @change="handleFileUpload"
              accept=".pdf,.doc,.docx"
              required
            />
          </template>

          <button type="submit" class="btn-registrar">Registrar</button>
        </form>

        <p class="mensaje">{{ mensaje }}</p>
      </div>

      <!-- Columna derecha: bienvenida -->
      <div class="welcome-section">
        <h2>¡Bienvenido!</h2>
        <p>
          Accede con tu cuenta para ingresar a nuestra plataforma educativa, donde encontrarás tus cursos, 
          materiales de estudio y recursos académicos disponibles.
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
  rol_id: '',
  Experiencia: '',
  Titulo_Profesional: ''
})

const archivo = ref(null)
const mensaje = ref('')

const handleFileUpload = (e) => {
  archivo.value = e.target.files[0]
}

const registrar = async () => {
  try {
    const formData = new FormData()
    Object.entries(form.value).forEach(([key, value]) => formData.append(key, value))
    if (archivo.value) formData.append('Hoja_de_Vida', archivo.value)

    const res = await axios.post('http://localhost:5001/registro', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    mensaje.value = res.data.message
  } catch (err) {
    mensaje.value = err.response?.data?.message || 'Error en el registro'
  }
}
</script>

<style scoped>
/* Contenedor principal centrado */
.registro-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 90vh;
  width: 100%;
  font-family: "Poppins", sans-serif;
}

/* Tarjeta general con dos secciones lado a lado */
.registro-card {
  display: flex;
  width: 900px;
  background: linear-gradient(170deg, #efefef, #07B3FA);
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
  justify-content: flex-start;
  background: rgba(255, 255, 255, 0.15);
}

/* Si el contenido crece, se activa el scroll interno */
.formulario {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 420px;
  overflow-y: auto;
  padding-right: 5px;
}

.formulario::-webkit-scrollbar {
  width: 6px;
}
.formulario::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.form-section h2 {
  margin-bottom: 15px;
  text-align: center;
  color: #000000;
}

.formulario input,
.formulario select {
  padding: 12px;
  border: 1px solid #fff;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s;
}

.formulario input:focus,
.formulario select:focus {
  border-color: #07B3FA;
}

.btn-registrar {
  margin-top: 10px;
  padding: 12px;
  background-color: #f9f9f9;
  color: #000;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-registrar:hover {
  background-color: #07B3FA;
}

.mensaje {
  margin-top: 10px;
  color: #000;
  text-align: center;
}

/* Sección derecha: bienvenida */
.welcome-section {
  flex: 1;
  background: linear-gradient(135deg, #07B3FA, #efefef);
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
  color: #000;
}

.welcome-section p {
  margin-bottom: 20px;
  font-size: 1rem;
  line-height: 1.5;
  color: #000;
}

.btn-login {
  background: white;
  color: #000;
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
