import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Registro from '../views/Registro.vue'
import Dashboard from '../views/Dashboard.vue'
import AdminPanel from '../views/AdminPanel.vue'

const routes = [
  { path: '/', redirect: '/home' },      // Redirige raíz a home
  { path: '/home', component: Home },    // Ahora sí existe /home
  { path: '/login', component: Login },
  { path: '/registro', component: Registro },
  { path: '/dashboard', component: Dashboard },
  { path: '/admin', component: AdminPanel },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
