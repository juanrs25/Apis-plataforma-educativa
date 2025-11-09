import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    rol: localStorage.getItem('rol') || null,
  }),
  actions: {
    login(token, rol) {
      this.token = token
      this.rol = rol
      localStorage.setItem('token', token)
      localStorage.setItem('rol', rol)
    },
    logout() {
      this.token = null
      this.rol = null
      localStorage.removeItem('token')
      localStorage.removeItem('rol')
    }
  }
})
