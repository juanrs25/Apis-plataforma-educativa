import { createApp } from 'vue'
import { createPinia } from 'pinia' //cc
import './style.css'
import App from './App.vue'
import router from './router'   //this

// createApp(App).mount('#app')
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
