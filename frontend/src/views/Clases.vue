<template>
  <section class="tabla-clases-section">

    <!-- LOADING -->
    <div v-if="cargando" class="loading">Cargando clases...</div>

    <!-- TABLA -->
    <div v-else class="tabla-container">
      <h2>Clases Disponibles</h2>

      <table class="tabla-clases">
        <thead>
          <tr>
            <th>Título</th>
            <th>Descripción</th>
            <th>Profesor</th>
            <th>Días</th>
            <th>Precio</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(c, i) in clases" :key="i">
            <td>{{ c.clase.titulo }}</td>
            <td>{{ c.clase.descripcion }}</td>
            <td>{{ c.profesor.nombre }}</td>

            <td>
              <span v-for="h in c.horarios" :key="h.id_horario">
                {{ h.dia }}&nbsp;
              </span>
            </td>
            <td>{{ c.clase.precio || "No definido" }}</td>

            <td>
              <button class="btn-inscribirse" @click="registrarse(c.clase.id_clase)">
                Registrarse
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const BACKEND = "http://127.0.0.1:5002";


const clases = ref([]);
const cargando = ref(true);

async function cargarClases() {
  try {
    console.time("cargar_clases");
    const resp = await axios.get(`${BACKEND}/clases`);
    console.timeEnd("cargar_clases");

    // Ya no hacemos llamadas adicionales
    clases.value = resp.data;

    

  } catch (err) {
    console.error("Error cargando clases:", err);
  }
}


function registrarse(idClase) {
  alert(`Registro pendiente para la clase ID ${idClase}`);
}

onMounted(async () => {
  await cargarClases();
  cargando.value = false;
});
</script>

<style scoped>
.tabla-clases-section {
  padding: 40px 0;
  background: #f5f5f5;
  width: 100%;
  text-align: center;
}

.loading {
  font-size: 1.6rem;
  font-weight: bold;
  color: #2700ea;
  margin-top: 50px;
}

.tabla-container {
  padding: 0 40px;
  overflow-x: auto;
}

h2 {
  margin-bottom: 25px;
  font-size: 2rem;
  color: #111;
}

.tabla-clases {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.tabla-clases th {
  background: #2700ea;
  color: white;
  padding: 15px;
  font-size: 1rem;
  text-align: left;
}

.tabla-clases td {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  color: #333;
}

.btn-inscribirse {
  background: #2700ea;
  color: white;
  padding: 7px 15px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-inscribirse:hover {
  background: #455dc9;
}

@media (max-width: 768px) {
  .tabla-clases th,
  .tabla-clases td {
    padding: 10px;
    font-size: 0.85rem;
  }
}
</style>
