<template>
  <nav class="navbar">
    <a href="/" class="nav-link main-link">Educando</a>

    <div class="nav-links-group">
      <a href="/registro" class="nav-link">Registro</a>
      <a href="/login" class="nav-link">Login</a>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;              /* 🔹 Ocupa todo el ancho */
  height: 60px;
  background-color: #22577A;
  color: white;
  display: flex;
  justify-content: space-between; /* 🔹 Logo a la izquierda, links a la derecha */
  align-items: center;
  padding: 0 40px;          /* 🔹 Espacio interno */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 1000;            /* 🔹 Siempre visible arriba */
}

/* Enlaces generales */
.nav-link {
  color: white;
  text-decoration: none;
  margin-left: 20px;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #9a79ff;
}

/* Nombre principal o logo */
.main-link {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
}

/* Contenedor de enlaces de la derecha */
.nav-links-group {
  display: flex;
  align-items: center;
}
</style>
