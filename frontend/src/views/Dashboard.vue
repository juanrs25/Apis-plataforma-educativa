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
        <tr v-for="(clase, index) in clases" :key="index">
          <td>{{ clase.nombre }}</td>
          <td>{{ clase.descripcion }}</td>
          <td>{{ clase.fecha }}</td>
          <td>{{ clase.dia }}</td>
          <td>{{ clase.precio }}</td>
          <td>
            <span class="estado-activo">{{ clase.estado }}</span>
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
import { ref } from 'vue'

const clases = ref([
  {
    nombre: 'Ingles',
    descripcion: 'todo dobre ingles',
    fecha: '2025-05-22',
    dia: 'Martes',
    precio: '$14,000 COP',
    estado: 'Activa',
  },
  {
    nombre: 'Limites hacia el infinito',
    descripcion: 'Aprenderas todo acerca factorizacion',
    fecha: '2025-05-18',
    dia: 'Sábado',
    precio: '$12,000 COP',
    estado: 'Activa',
  },
])
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

.dashboard {
  background-color: #f9fafb;
  padding: 40px;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
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
