<template>
  <div class="admin-panel">
    <!-- Encabezado -->
    <div class="header">
      <div class="title">
        <i class="fas fa-user-shield"></i>
        <h2>Panel de Administración</h2>
      </div>
    </div>

    <!-- Tabla de Docentes Pendientes -->
    <div class="tabla-container">
      <h3>
        <i class="fas fa-chalkboard-teacher"></i> Docentes Pendientes por
        Aprobar
      </h3>

      <table class="tabla">
        <thead>
          <tr>
            <th>Nombre Completo</th>
            <th>Email</th>
            <th>Estado</th>
            <th>Hoja de Vida</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(docente, index) in docentesPendientes" :key="index">
            <td>{{ docente.nombre }}</td>
            <td>{{ docente.email }}</td>

            <td>
              <span class="estado-pendiente">{{ docente.estado }}</span>
            </td>
            <td>
             <a :href="`http://localhost:5001/uploads/${docente.hoja_vida_path}`" target="_blank">
             Ver Hoja de Vida
            </a>
            </td>
            <td class="acciones">
              <button class="btn-aprobar" @click="aprobarDocente(docente)">
                <i class="fas fa-check"></i> Aprobar
              </button>
              <button class="btn-rechazar" @click="rechazarDocente(docente)">
                <i class="fas fa-times"></i> Rechazar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Sección informativa -->
    <div class="info">
      <i class="fas fa-info-circle"></i>
      <p>
        Los docentes aprobados podrán ofrecer sus servicios en la plataforma.
        Revisa cuidadosamente la información antes de aprobar.
      </p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useAuthStore } from "../store/auth";

const auth = useAuthStore();
const docentesPendientes = ref([]);

const cargarDocentes = async () => {
  try {
    const res = await axios.get("http://localhost:5001/usuarios/pendientes", {
      headers: {
        Authorization: `Bearer ${auth.token}`
      }
    });
    docentesPendientes.value = res.data;
  } catch (err) {
    console.error("Error al cargar docentes:", err);
  }
};

onMounted(() => {
  cargarDocentes();
});

const aprobarDocente = async (docente) => {
  try {
    const res = await axios.put(
      `http://localhost:5001/usuarios/aprobar/${docente.id}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${auth.token}`
        }
      }
    );

    alert(res.data.message);

    // Recargar tabla
    cargarDocentes();

  } catch (err) {
    alert(err.response?.data?.message || "Error al aprobar");
  }
};

const rechazarDocente = async (docente) => {
  try {
    const res = await axios.put(
      `http://localhost:5001/usuarios/rechazar/${docente.id}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${auth.token}`
        }
      }
    );

    alert(res.data.message);
    cargarDocentes();
  } catch (err) {
    alert(err.response?.data?.message || "Error al rechazar");
  }
};
</script>


<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css");

.admin-panel {
  background-color: #f9fafb;
  padding: 40px;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
  color: #000;
}

/* Encabezado */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title h2 {
  font-size: 28px;
  font-weight: bold;
  color: #1d4ed8;
}

.title i {
  color: #1d4ed8;
  font-size: 26px;
}

/* Tabla */
.tabla-container h3 {
  font-size: 22px;
  color: #2563eb;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tabla {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tabla thead {
  background-color: #dbeafe;
  color: #000;
}

.tabla th,
.tabla td {
  padding: 14px 16px;
  text-align: left;
}

.tabla tbody tr:hover {
  background-color: #f3f4f6;
}

.estado-pendiente {
  background-color: #facc15;
  color: #000;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
}

/* Botones */
.acciones {
  display: flex;
  gap: 8px;
  align-items: center;
  height: 100%;
}

.btn-aprobar {
  background-color: #16a34a;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-aprobar:hover {
  background-color: #15803d;
}

.btn-rechazar {
  background-color: #dc2626;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px; 
  cursor: pointer;
  font-weight: 600;
}

.btn-rechazar:hover {
  background-color: #b91c1c;
}
/* Info final */
.info {
  margin-top: 40px;
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: #e0f2fe;
  padding: 15px 20px;
  border-radius: 8px;
  color: #0c4a6e;
  font-size: 15px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}
</style>
