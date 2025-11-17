import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Registro from '../views/Registro.vue'
import Dashboard from '../views/Dashboard.vue'
import AdminPanel from '../views/AdminPanel.vue'
import { useAuthStore } from "../store/auth";

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: Home },
  { path: '/login', component: Login },
  { path: '/registro', component: Registro },

  // Rutas protegidas
  { path: '/dashboard', component: Dashboard },
  { path: '/adminpanel', component: AdminPanel },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


//  PROTECCIÓN GLOBAL DE RUTAS Y TOKEN
router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  // Revisa si el token expiró en cada navegación
  auth.checkToken();

  // Si después de checkToken el usuario no tiene token, lo envia al login
  if (!auth.token && to.path !== "/login" && to.path !== "/registro") {
    return next("/login");
  }

  next();
});

export default router;
