<template>
  <div class="dashboard">
    <!-- Sección de clases -->
    <div class="header">
      <div class="title">
        <i class="fas fa-book"></i>
        <h2>Tus Clases</h2>
      </div>

      <button class="btn-crear">
        <i class="fas fa-plus-circle"></i>
        Crear nueva clase
      </button>
    </div>

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
            <span v-if="item.horarios && item.horarios.length > 0">
              {{ item.horarios[0].dia }}
            </span>
            <span v-else>—</span>
          </td>

          <td>{{ formatCOP(item.clase.precio) }}</td>


          <td>
            <span class="estado-activo">
              {{ item.clase.estado }}
            </span>
          </td>

          <td class="acciones">
            <button class="btn-editar"><i class="fas fa-pen"></i></button>
            <button class="btn-eliminar"><i class="fas fa-trash"></i></button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Sección de nuevas solicitudes -->
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

onMounted(async () => {
  // Sincroniza store con localStorage
  auth.token = localStorage.getItem("token");
  auth.id = Number(localStorage.getItem("id"));
  auth.rol = localStorage.getItem("rol");
  auth.nombre = localStorage.getItem("nombre");

  console.log("ID después de sincronizar:", auth.id);

  if (!auth.id) {
    console.warn("El ID sigue siendo null — No puedo cargar clases.");
    return;
  }

  try {
    const response = await axios.get(
      `http://127.0.0.1:5002/clases/profesor/${auth.id}`
    );

  
    clases.value = response.data;

  } catch (error) {
    console.error("Error cargando clases:", error);
  }
});

const formatCOP = (value) => {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0
  }).format(value);
};


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

/* Encabezado de Clases */
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

.tabla tbody tr:hover {
  background-color: #f1f5f9;
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

.btn-eliminar:hover {
  background-color: #b91c1c;
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
</style>
