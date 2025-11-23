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
            <th>E-mail</th>
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
            <td>{{ c.profesor.email }}</td>


            <td>
              <span v-for="h in c.horarios" :key="h.id_horario">
                {{ h.dia }}&nbsp;
              </span>
            </td>
            <td>{{ c.clase.precio || "No definido" }}</td>

            <td>
              <button
                class="btn-inscribirse"
                @click="registrarse(c.clase.id_clase)"
              >
                Registrarse
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL DE REGISTRO -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>Confirmar inscripción</h3>

        <div class="modal-info">
          <p><strong>Clase:</strong> {{ claseSeleccionadaObj.clase.titulo }}</p>
          <p>
            <strong>Profesor:</strong>
            {{ claseSeleccionadaObj.profesor.nombre }}
          </p>
          <p>
            <strong>Días:</strong>
            <span
              v-for="h in claseSeleccionadaObj.horarios"
              :key="h.id_horario"
            >
              {{ h.dia }}&nbsp;
            </span>
          </p>
          <p>
            <strong>Precio:</strong>
            {{ claseSeleccionadaObj.clase.precio || "No definido" }}
          </p>
        </div>

        <p class="modal-pregunta">¿Deseas inscribirte en esta clase?</p>

        <div class="modal-buttons">
          <button class="btn-cancel" @click="showModal = false">
            Cancelar
          </button>
          <button
            class="btn-accept"
            @click="enviarInscripcion"
            :disabled="cargando"
          >
            {{ cargando ? "Procesando solicitud..." : "Enviar inscripción" }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const BACKEND = "http://127.0.0.1:5002";
const SOLICITUDES_BACKEND = "http://127.0.0.1:5004";

const clases = ref([]);
const showModal = ref(false);
const claseSeleccionada = ref(null);
const claseSeleccionadaObj = ref(null);
const cargando = ref(false);

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
  claseSeleccionada.value = idClase;
  claseSeleccionadaObj.value = clases.value.find(
    (c) => c.clase.id_clase === idClase
  );
  showModal.value = true;
}

async function enviarInscripcion() {
  try {
    cargando.value = true;

    const body = {
      id_usuario: Number(localStorage.getItem("id")),
      id_clase: claseSeleccionada.value,
    };

    await axios.post(`${SOLICITUDES_BACKEND}/inscripciones`, body);

    showModal.value = false;
    alert("Inscripción enviada. El profesor debe aprobarla.");
  } catch (error) {
    console.error(error);

    // Verificar si el backend devolvió información útil
    if (error.response && error.response.data) {
      const data = error.response.data;
      const estado = data.estado_actual;

      // Cuando existe inscripción previa
      if (estado === "Pendiente") {
        alert("Ya enviaste esta solicitud y está pendiente de aprobación.");
      }
      else if (estado === "Aprobada") {
        alert("Ya estás inscrito en esta clase.");
      }
      else if (estado === "Rechazada") {
        alert("Tu solicitud fue rechazada. Consulta al profesor.");
      }
      else if (data.error) {
        alert(data.error);
      }
      else {
        alert("No se pudo enviar la inscripción. Intenta más tarde.");
      }

      showModal.value = false;
    } else {
      alert("No se pudo enviar la inscripción por un error inesperado.");
    }
  } finally {
    cargando.value = false;
  }
}

onMounted(async () => {
  cargando.value = true;   
  await cargarClases();
  cargando.value = false;  
});

</script>

<style scoped>
/* Fondo oscuro */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* Ventana modal */
.modal {
  background: white;
  width: 450px;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  animation: fadeIn 0.25s ease-out;
}

/* Animación */
@keyframes fadeIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-info p {
  text-align: left;
  margin: 8px 0;
  font-size: 0.95rem;
}

.modal-pregunta {
  margin-top: 15px;
  font-size: 1rem;
  font-weight: bold;
}

/* Botones */
.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
}

.btn-cancel {
  background: #ccc;
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #b3b3b3;
}

.btn-accept {
  background: #2700ea;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-accept:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


.btn-accept:hover {
  background: #4f46e5;
}

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
