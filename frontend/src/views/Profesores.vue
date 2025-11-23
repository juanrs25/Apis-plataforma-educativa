<template>
  <section class="tabla-profesores-section">
    <h2>Profesores</h2>

    <div class="tabla-container">
      <table class="tabla-profesores">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Título</th>
            <th>Experiencia</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(doc, i) in profesores" :key="i">
            <td>{{ doc.nombre }}</td>
            <td>{{ doc.correo }}</td>
            <td>{{ doc.titulo || "No registrado" }}</td>
            <td>{{ doc.experiencia || "No registrada" }}</td>
            <td>
              <button class="btn-contacto" @click="contactar(doc)">
                Contactar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const profesores = ref([]);
const BACKEND_BASE = "http://127.0.0.1:5001";



async function cargarProfesores() {
  try {
    const res = await axios.get(`${BACKEND_BASE}/docentes`);
    profesores.value = res.data.usuarios;
  } catch (err) {
    console.error("Error cargando profesores", err);
  }
}

function contactar(doc) {
  alert(`Puedes contactar a ${doc.nombre} al correo: ${doc.correo}`);
}

onMounted(() => {
  cargarProfesores();
});
</script>

<style scoped>
.tabla-profesores-section {
  padding: 50px 0;
  background-color: #f5f5f5;
  width: 100%;
  text-align: center;
}

.tabla-profesores-section h2 {
  margin-bottom: 30px;
  font-size: 2rem;
  color: #0c0c0c;
}

.tabla-container {
  padding: 0 40px;
  overflow-x: auto;
}

.tabla-profesores {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.tabla-profesores th {
  background: #2700ea;
  color: white;
  padding: 15px;
  font-size: 1rem;
  text-align: left;
}

.tabla-profesores td {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  font-size: 0.95rem;
  color: #333;
}



.btn-contacto {
  background-color: #2700ea;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  font-size: 0.85rem;
  cursor: pointer;
}

.btn-contacto:hover {
  background-color: #455dc9;
}

@media (max-width: 768px) {
  .tabla-profesores th,
  .tabla-profesores td {
    font-size: 0.85rem;
    padding: 10px;
  }
}




</style>
