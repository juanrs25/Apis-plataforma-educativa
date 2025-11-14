import { defineStore } from 'pinia'
import { jwtDecode } from "jwt-decode"


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    rol: localStorage.getItem('rol') || null,
    nombre: localStorage.getItem('nombre') || null  
  }),
  actions: {
    login(token, rol, nombre) {  
      this.token = token
      this.rol = rol
      this.nombre = nombre      
      localStorage.setItem('token', token)
      localStorage.setItem('rol', rol)
      localStorage.setItem('nombre', nombre)  
    },

    logout() {
      this.token = null
      this.rol = null
      this.nombre = null   
      localStorage.removeItem('token')
      localStorage.removeItem('rol')
      localStorage.removeItem('nombre')
    },

    checkToken() {
      if (!this.token) return

      try {
        const decoded = jwtDecode(this.token)

        const exp = decoded.exp * 1000
        const now = Date.now()

        if (now >= exp) {
          this.logout()
          alert("Tu sesión ha expirado. Por favor inicia sesión nuevamente.")
        }
      } catch (error) {
        this.logout()
      }
    }
  }
})
