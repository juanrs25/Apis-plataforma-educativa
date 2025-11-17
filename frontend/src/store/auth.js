import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    rol: localStorage.getItem("rol") || null,
    nombre: localStorage.getItem("nombre") || null,
    id: Number(localStorage.getItem("id")) || null,
  }),

  actions: {
    login(token, rol, nombre) {
      const decoded = jwtDecode(token);

      this.token = token;
      this.rol = rol;
      this.nombre = nombre;

      this.id = decoded.id; 

      localStorage.setItem("token", token);
      localStorage.setItem("rol", rol);
      localStorage.setItem("nombre", nombre);
      localStorage.setItem("id", decoded.id);

    },


    logout() {
      this.token = null;
      this.rol = null;
      this.nombre = null;
      this.id = null;

      localStorage.removeItem("token");
      localStorage.removeItem("rol");
      localStorage.removeItem("nombre");
      localStorage.removeItem("id");
    },

    checkToken() {
      if (!this.token) return;

      try {
        const decoded = jwtDecode(this.token);
        const exp = decoded.exp * 1000;
        const now = Date.now();

        if (now >= exp) {
          this.logout();
          alert("Tu sesión ha expirado. Por favor inicia sesión nuevamente.");
        }
      } catch (error) {
        this.logout();
      }
    },
  },
});
