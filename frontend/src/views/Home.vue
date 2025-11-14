<template>
  <div class="home">
    <!--  CARRUSEL -->
    <section class="carousel-section">
      <swiper
        loop
        :autoplay="{ delay: 4000, disableOnInteraction: false }"
        :pagination="{ clickable: true }"
        navigation
        class="mySwiper"
      >
        <swiper-slide v-for="(item, index) in slides" :key="index" class="slide">
          <img :src="item.image" class="carousel-image" />
          <div class="carousel-text">
            <h2>{{ item.title }}</h2>
            <p>{{ item.description }}</p>
            <!-- <a href="" class="btn">Comenzar</a> -->
          </div>
        </swiper-slide>
      </swiper>
    </section>

    <!--  SECCIÓN DE CURSOS -->
    <section class="cursos-section">
      <h2>Cursos Destacados</h2>
      <div class="cursos-grid">
        <div class="curso-card" v-for="(curso, i) in cursos" :key="i">
          <img :src="curso.image" alt="curso" />
          <h3>{{ curso.nombre }}</h3>
          <p>{{ curso.descripcion }}</p>
          <a href="" class="btn-small">Inscribirse</a>
        </div>
      </div>
    </section>

    <!--  INFORMACIÓN DE LA PLATAFORMA -->
    <section class="info-section">
      <div class="info-card">
        <h3>Misión</h3>
        <p>Brindar educación inclusiva y accesible mediante tecnología, fomentando el aprendizaje colaborativo y personalizado.</p>
      </div>
      <div class="info-card">
        <h3>Visión</h3>
        <p>Ser una plataforma educativa líder en innovación y accesibilidad, reconocida por su impacto en la formación integral de los estudiantes.</p>
      </div>
      <div class="info-card">
        <h3>Acerca de Nosotros</h3>
        <p>Somos un equipo comprometido con el desarrollo de herramientas educativas digitales que promueven la inclusión y la calidad en la enseñanza.</p>
      </div>
    </section>

    <!--  FOOTER -->
    <footer class="footer">
      <p>© 2025 Plataforma Educativa Inclusiva - Todos los derechos reservados</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Swiper Vue 3
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

// Datos del carrusel
const slides = ref([
  {
    image: 'https://i.pinimg.com/1200x/81/92/63/81926307369646a043bc8f71ef7f47ac.jpg',
    title: 'Aprende a tu ritmo',
    description: 'Nuestra plataforma se adapta a tu estilo de aprendizaje y horario.'
  },
  {
    image: 'https://img.freepik.com/foto-gratis/profesor-explicando-estudiantes-clase_23-2148852731.jpg',
    title: 'Educación inclusiva',
    description: 'Creamos espacios accesibles y participativos para todos los estudiantes.'
  },
  {
    image: 'https://img.freepik.com/foto-gratis/personas-estudiando-juntas-biblioteca_23-2148863450.jpg',
    title: 'Comunidades de aprendizaje',
    description: 'Conéctate con docentes y compañeros para potenciar tus conocimientos.'
  }
])

// Cursos
const cursos = ref([
  {
    nombre: 'Matemáticas',
    descripcion: 'Refuerza tus habilidades en álgebra, geometría y cálculo con clases interactivas.',
    image: 'https://i.pinimg.com/736x/17/c4/2f/17c42f496478fa4413a9bf0c0cbdb142.jpg'
  },
  {
    nombre: 'Ciencias Naturales',
    descripcion: 'Explora el fascinante mundo de la biología, física y química.',
    image: 'https://i.pinimg.com/736x/34/f4/ca/34f4ca1cab7f7af2465ac1ec51d01cb8.jpg'
  },
  {
    nombre: 'Lenguaje y Comunicación',
    descripcion: 'Mejora tu comprensión lectora y habilidades de escritura.',
    image: 'https://i.pinimg.com/736x/5d/e7/b0/5de7b0e7d713b877ae74977589964608.jpg'
  },
  {
    nombre: 'Historia y Cultura',
    descripcion: 'Aprende sobre civilizaciones, eventos históricos y patrimonio cultural.',
    image: 'https://i.pinimg.com/736x/a6/1c/4e/a61c4ea4d03afa8ae430d4dadd3bd501.jpg'
  }
])
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* 🎠 CARRUSEL */
.carousel-section {
  width: 100%;
  position: relative;
  margin-top: 2px;
}
.slide {
  position: relative;
}
.carousel-image {
  width: 100%;
  height: 450px;
  object-fit: cover;
  filter: brightness(70%);
}
.carousel-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 25px 50px;
  border-radius: 12px;
}
.carousel-text h2 {
  font-size: 2rem;
  margin-bottom: 10px;
}
.carousel-text p {
  font-size: 1.2rem;
  margin-bottom: 15px;
}
.btn {
  display: inline-block;
  background-color: #2700ea;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.3s;
}
.btn:hover {
  background-color: #2700ea;
}

/* 📚 CURSOS */
.cursos-section {
  padding: 50px 0;
  background-color: #f5f5f5;
  width: 100%;
}
.cursos-section h2 {
  margin-bottom: 40px;
  font-size: 2rem;
  color: #0c0c0c;
}
.cursos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  padding: 0 50px;
  color: black;
}
.curso-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  padding: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.curso-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}
.curso-card img {
  width: 100%;
  height: 180px;
  border-radius: 10px;
  object-fit: cover;
}
.curso-card h3 {
  margin-top: 15px;
  color: #302c2c;
}
.btn-small {
  margin-top: 10px;
  display: inline-block;
  background-color: #2700ea;
  color: white;
  padding: 7px 15px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
}
.btn-small:hover {
  background-color: #455dc9;
}

/* 🏛️ INFORMACIÓN */
.info-section {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
  padding: 60px 50px;
  background-color: #ffffff;
}
.info-card {
  flex: 1;
  min-width: 280px;
  max-width: 320px;
  background-color: #f3f3f3;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}
.info-card h3 {
  color: #121212;
  margin-bottom: 15px;
}
.info-card p {
  font-size: 1rem;
  line-height: 1.5;
  color: black;
}

/* ⚓ FOOTER */
.footer {
  background-color: #302c2c;
  color: white;
  width: 100%;
  padding: 25px 0;
  text-align: center;
  margin-top: 40px;
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .cursos-grid {
    padding: 0 30px;
  }
  .info-section {
    padding: 50px 30px;
  }
}

@media (max-width: 768px) {
  .carousel-text h2 {
    font-size: 1.6rem;
  }
  .carousel-text p {
    font-size: 1rem;
  }
  .cursos-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
  }
}
</style>
