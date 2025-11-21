<template>
  <div class="dashboard">
    <!-- MODAL DE CONFIRMACIÓN -->
    <transition name="fade">
      <div v-if="showConfirm" class="modal-overlay">
        <div class="modal">
          <h3>¿Eliminar clase?</h3>
          <p>
            ¿Estás seguro de que deseas eliminar la clase "<strong>{{
              claseSeleccionada?.titulo
            }}</strong
            >"? Esta acción no se puede deshacer.
          </p>

          <div class="modal-buttons">
            <button class="btn-cancel" @click="closeConfirm">Cancelar</button>
            <button class="btn-accept" @click="confirmarEliminacion">
              Sí, eliminar
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL DE EDITAR CLASE -->
    <transition name="fade">
      <div v-if="showEdit" class="modal-overlay">
        <div class="modal">
          <h3>Editar clase</h3>

          <div class="form-group">
            <label>Título</label>
            <input v-model="editForm.titulo" />
          </div>

          <div class="form-group">
            <label>Descripción</label>
            <input v-model="editForm.descripcion" />
          </div>

          <div class="form-group">
            <label>Precio</label>
            <input type="number" v-model.number="editForm.precio" />
          </div>

          <div class="form-group">
            <label>Estado</label>
            <select v-model="editForm.estado">
              <option value="Activa">Activa</option>
              <option value="Inactiva">Inactiva</option>
              <option value="Finalizada">Finalizada</option>
            </select>
          </div>

          <div class="modal-buttons">
            <button class="btn-cancel" @click="closeEdit">Cancelar</button>
            <button class="btn-editar" @click="actualizarClase">
              Actualizar
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL CREAR CLASE -->
    <transition name="fade">
      <div v-if="showCreate" class="modal-overlay">
        <div class="modal">
          <h3>Crear nueva clase</h3>

          <div class="form-group">
            <label>Título</label>
            <input v-model="createForm.titulo" />
          </div>

          <div class="form-group">
            <label>Descripción</label>
            <input v-model="createForm.descripcion" />
          </div>

          <div class="form-group">
            <label>Precio</label>
            <input type="number" v-model.number="createForm.precio" />
          </div>

          <div class="form-group">
            <label>Día</label>
            <select v-model="createForm.dia">
              <option value="Lunes">Lunes</option>
              <option value="Martes">Martes</option>
              <option value="Miércoles">Miércoles</option>
              <option value="Jueves">Jueves</option>
              <option value="Viernes">Viernes</option>
              <option value="Sábado">Sábado</option>
              <option value="Domingo">Domingo</option>
            </select>
          </div>

          <div class="modal-buttons">
            <button class="btn-cancel" @click="closeCreate">Cancelar</button>
            <button class="btn-accept" :disabled="creating" @click="crearClase">
              {{ creating ? "Creando..." : "Crear" }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL DE ÉXITO -->
    <transition name="fade">
      <div v-if="showSuccess" class="modal-overlay">
        <div class="modal success">
          <h3>Clase eliminada</h3>
          <p>La clase fue eliminada exitosamente.</p>
          <button class="btn-success" @click="closeSuccess">Cerrar</button>
        </div>
      </div>
    </transition>

    <!-- HEADER -->
    <div class="header">
      <div class="title">
        <i class="fas fa-book"></i>
        <h2>Tus Clases</h2>
      </div>

      <button class="btn-crear" @click="abrirCrear">
        <i class="fas fa-plus-circle"></i>
        Crear nueva clase
      </button>
    </div>

    <!-- TABLA -->
    <table class="tabla">
      <thead>
        <tr>
          <th>Clase</th>
          <th>Descripción</th>
          <th>Fecha Creación</th>
          <th>Día</th>
          <th>Precio</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(item, index) in clases" :key="index">
          <td>{{ item.clase.titulo }}</td>
          <td>{{ item.clase.descripcion }}</td>
          <td>{{ item.clase.fecha_creacion }}</td>

          <td>
            <span v-if="item.horarios?.length">
              {{ item.horarios[0].dia }}
            </span>
            <span v-else>—</span>
          </td>

          <td>{{ formatCOP(item.clase.precio) }}</td>

          <td>
            <span class="estado-activo">{{ item.clase.estado }}</span>
          </td>

          <td class="acciones">
            <button class="btn-eliminar" @click="openConfirm(item.clase)">
              <i class="fas fa-trash"></i>
            </button>
            <button class="btn-editar" @click="abrirEditar(item.clase)">
              <i class="fas fa-pen"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- SECCIÓN SOLICITUDES -->
    <div class="solicitudes">
      <div class="solicitudes-header">
        <i class="fas fa-users"></i>
        <h2>Nuevas Solicitudes</h2>
      </div>

      <div class="solicitudes-content">
        <p>No hay solicitudes pendientes.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "../store/auth";

const auth = useAuthStore();
const clases = ref([]);

const BACKEND_BASE = "http://127.0.0.1:5002";

/* ------------------ MODALES ------------------ */
const showConfirm = ref(false);
const showSuccess = ref(false);
const showEdit = ref(false);
const showCreate = ref(false);
const creating = ref(false);


const claseSeleccionada = ref(null);

const editForm = ref({
  titulo: "",
  descripcion: "",
  precio: 0,
  estado: "Activa",
});

const createForm = ref({
  titulo: "",
  descripcion: "",
  precio: 0,
  dia: "Lunes",
});

/* ------------------ ELIMINAR ------------------ */
function openConfirm(clase) {
  claseSeleccionada.value = clase;
  showConfirm.value = true;
}

function closeConfirm() {
  showConfirm.value = false;
  claseSeleccionada.value = null;
}

async function confirmarEliminacion() {
  if (!claseSeleccionada.value) return;

  try {
    const id = claseSeleccionada.value.id_clase;

    await axios.delete(`${BACKEND_BASE}/clases/${id}`);

    clases.value = clases.value.filter((c) => c.clase.id_clase !== id);

    showConfirm.value = false;
    showSuccess.value = true;
  } catch (err) {
    console.error("ERROR:", err);
    alert("No se pudo eliminar la clase.");
  }
}

function closeSuccess() {
  showSuccess.value = false;
}

/* ------------------ EDITAR ------------------ */
function abrirEditar(clase) {
  claseSeleccionada.value = clase;
  editForm.value = { ...clase };
  showEdit.value = true;
}

function closeEdit() {
  showEdit.value = false;
  claseSeleccionada.value = null;
}

async function actualizarClase() {
  try {
    const id = claseSeleccionada.value.id_clase;

    const res = await axios.put(`${BACKEND_BASE}/clases/${id}`, {
      titulo: editForm.value.titulo,
      descripcion: editForm.value.descripcion,
      precio: editForm.value.precio,
      estado: editForm.value.estado,
    });

    const index = clases.value.findIndex((c) => c.clase.id_clase === id);

    if (index !== -1) {
      clases.value[index].clase = res.data.clase;
    }

    showEdit.value = false;
    alert("Clase actualizada correctamente.");
  } catch (err) {
    console.error("Error actualizando:", err);
    alert("Error al actualizar la clase.");
  }
}

/* ------------------ CREAR ------------------ */
function abrirCrear() {
  createForm.value = {
    titulo: "",
    descripcion: "",
    precio: 0,
    dia: "Lunes",
  };
  showCreate.value = true;
}

function closeCreate() {
  showCreate.value = false;
}

async function crearClase() {
  if (creating.value) return; 

  creating.value = true; 

  try {
    const body = {
      titulo: createForm.value.titulo,
      descripcion: createForm.value.descripcion,
      precio: createForm.value.precio,
      dia: createForm.value.dia,
      profesor_id: auth.id,
      estado: "Activa",
    };

    const res = await axios.post(`${BACKEND_BASE}/clases`, body);

    clases.value.push({
      clase: res.data.clase,
      horarios: [res.data.horario],
    });

    showCreate.value = false;
    alert("Clase creada exitosamente.");
  } catch (err) {
    console.error("Error creando clase:", err);
    alert("No se pudo crear la clase.");
  } finally {
    creating.value = false; 
  }
}

/* ------------------ CARGAR CLASES ------------------ */
onMounted(async () => {
  auth.token = localStorage.getItem("token");
  auth.id = Number(localStorage.getItem("id"));

  if (!auth.id) return;

  try {
    const res = await axios.get(`${BACKEND_BASE}/clases/profesor/${auth.id}`);
    clases.value = res.data;
  } catch (err) {
    console.error("Error cargando clases:", err);
  }
});

/* ------------------ FORMATOS ------------------ */
function formatCOP(value) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
  }).format(value);
}
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css");

.dashboard {
  background-color: #f9fafb;
  padding: 40px;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
  color: #000;
}

/* MODALES */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal {
  background: #fff;
  padding: 26px;
  border-radius: 12px;
  width: 420px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(2, 6, 23, 0.2);
}

.modal.success {
  background: #ecfdf5;
  border-left: 6px solid #10b981;
}

.modal h3 {
  font-size: 20px;
  margin-bottom: 8px;
  color: #0f172a;
}

.modal p {
  color: #475569;
  margin-bottom: 16px;
}

/* Botones del modal */
.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 8px;
}

.btn-cancel {
  background: #6b7280;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.btn-accept {
  background: #dc2626;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.btn-success {
  background: #10b981;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

/* FORMULARIO DENTRO DEL MODAL */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 10px;
}
.form-group input,
.form-group select {
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid #e6e7eb;
}

/* HEADER */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title h2 {
  font-size: 28px;
  font-weight: bold;
  color: #2563eb;
}

.title i {
  color: #2563eb;
  font-size: 26px;
}

.btn-crear {
  background-color: #16a34a;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
}
.btn-crear:hover {
  background-color: #15803d;
}

/* Tabla */
.tabla {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tabla thead {
  background-color: #bfdbfe;
  color: #000;
}
.tabla th,
.tabla td {
  padding: 14px 16px;
  text-align: left;
}

/* Estado */
.estado-activo {
  background-color: #16a34a;
  color: white;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
}

/* Botones acciones */
.acciones {
  display: flex;
  gap: 8px;
}
.btn-editar {
  background-color: #facc15;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
}
.btn-editar:hover {
  background-color: #eab308;
}
.btn-eliminar {
  background-color: #dc2626;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
}

/* Sección de Nuevas Solicitudes */
.solicitudes {
  margin-top: 50px;
}
.solicitudes-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}
.solicitudes-header h2 {
  font-size: 26px;
  font-weight: bold;
  color: #2563eb;
}
.solicitudes-header i {
  color: #2563eb;
  font-size: 24px;
}
.solicitudes-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  font-size: 16px;
  text-align: center;
  color: #374151;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
