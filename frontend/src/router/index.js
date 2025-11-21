import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Registro from "../views/Registro.vue";
import Dashboard from "../views/Dashboard.vue";
import AdminPanel from "../views/AdminPanel.vue";
import Profesores from "../views/Profesores.vue";
import { useAuthStore } from "../store/auth";
import Clases from "../views/Clases.vue";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: Home },
  { path: "/login", component: Login },
  { path: "/registro", component: Registro },
  { path: "/profesores", component: Profesores },
  {path:"/clases", component:Clases},

  // Rutas protegidas
  { path: "/dashboard", component: Dashboard },
  { path: "/adminpanel", component: AdminPanel },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

//  PROTECCIÓN GLOBAL DE RUTAS Y TOKEN
router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  // Rutas que NO requieren token
  const rutasPublicas = [
 
    "/home",
    "/we",
    "/login",
    "/registro",
    "/clases",
  ];
  // Ejecuta la verificación del token (mantiene tu lógica actual)
  auth.checkToken();

  // Si la ruta es pública → permitir el paso
  if (rutasPublicas.includes(to.path)) {
    return next();
  }

  // Si NO es pública y NO hay token → redirigir al login
  if (!auth.token) {
    return next("/login");
  }

  // Todo OK
  next();
});

export default router;
