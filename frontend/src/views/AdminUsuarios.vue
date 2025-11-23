<template>
  <div class="admin-panel">
    <h2>Gestión de Usuarios</h2>

    <table class="tabla">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Estado</th>
          <th>Activo</th>
          <th>Hoja de Vida</th>
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="u in usuarios" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.nombre }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.rol }}</td>

          <td>
            <span :class="u.estado">{{ u.estado }}</span>
          </td>

          <td>
            <span :class="u.activo ? 'activo' : 'inactivo'">
              {{ u.activo ? 'Sí' : 'No' }}
            </span>
          </td>

          <td>
            <a
              v-if="u.hoja_vida"
              :href="`http://localhost:5001/uploads/${u.hoja_vida}`"
              target="_blank"
              style="text-decoration: underline; color: blue"
            >
              Ver PDF
            </a>

            <span v-else>—</span>
          </td>

          <td class="acciones">
            <button @click="activar(u.id)" class="btn-aprobar">Activar</button>
            <button @click="desactivar(u.id)" class="btn-rechazar">Desactivar</button>
            <button @click="eliminar(u.id)" class="btn-eliminar">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const usuarios = ref([]);

const cargarUsuarios = async () => {
  try {
    const token = localStorage.getItem("token");
    const resp = await axios.get("http://localhost:5001/usuarios/todos", {
      headers: { Authorization: `Bearer ${token}` },
    });

    usuarios.value = resp.data;
  } catch (error) {
    console.error("Error cargando usuarios:", error);
  }
};

// Activar
const activar = async (id) => {
  await axios.put(`http://localhost:5001/usuarios/activar/${id}`, {}, {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
  });
  cargarUsuarios();
};

// Desactivar
const desactivar = async (id) => {
  await axios.put(`http://localhost:5001/usuarios/desactivar/${id}`, {}, {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
  });
  cargarUsuarios();
};

// Eliminar
const eliminar = async (id) => {
  await axios.delete(`http://localhost:5001/usuarios/eliminar/${id}`, {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
  });
  cargarUsuarios();
};

onMounted(cargarUsuarios);
</script>

<style scoped>
.admin-panel {
  max-width: 1200px;
  margin: 30px auto;
  background: #ffffff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #000000;
  font-size: 26px;
  font-weight: bold;
}

/* TABLA */
.tabla {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.tabla th, .tabla td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #000000;
}

.tabla th {
  background-color: #fffcfc;
  font-weight: bold;
  color: #000000;
}

/* Hover en filas */
.tabla tbody tr:hover {
  background-color: #07b3fa;
  transition: background 0.3s;
}
.tabla td {
  color: #000 !important;
  font-weight: 500;
}
.tabla td:nth-child(5) {
  color: #000 !important;
  font-weight: 500;
}


/* ESTADOS */
.activo {
  padding: 6px 10px;
  background-color: #ffffff;
  color: rgb(0, 0, 0);
  border-radius: 8px;
  font-size: 14px;
}

.inactivo {
  padding: 6px 10px;
  background-color: #c0392b;
  color: white;
  border-radius: 8px;
  font-size: 14px;
}

.Pendiente {
  padding: 6px 10px;
  background-color: #f1c40f;
  color: black;
  border-radius: 8px;
  font-size: 14px;
}

.Aprobado {
  padding: 6px 10px;
  background-color: #07b3fa;
  color: rgb(0, 0, 0);
  border-radius: 8px;
  font-size: 14px;
}

/* BOTONES */
.acciones button {
  margin: 3px;
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  transition: 0.3s;
}

.btn-aprobar {
  background-color: #07b3fa;
  color: white;
}

.btn-aprobar:hover {
  background-color: #07b3fa;
}

.btn-rechazar {
  background-color: #f1c40f;
  color: black;
}

.btn-rechazar:hover {
  background-color: #d4ac0d;
}

.btn-eliminar {
  background-color: #e74c3c;
  color: white;
}

.btn-eliminar:hover {
  background-color: #c0392b;
}

a {
  color: #07b3fa;
  font-weight: bold;
}
</style>
