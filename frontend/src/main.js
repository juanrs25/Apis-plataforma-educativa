import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'   // <-- importa tu store

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)

// Aquí ya puedes usar el store
const auth = useAuthStore()
auth.checkToken() // <-- verifica si el token expiró

app.mount('#app')
