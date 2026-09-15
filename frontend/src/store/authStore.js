import { defineStore } from "pinia";
import { ensureCsrfToken, logout, registerCsrfTokenHandlers } from "@/services/auth";
import { getUser } from "../services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    csrfToken: null,
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
  },
  actions: {
    initializeCsrfTokenBinding() {
      registerCsrfTokenHandlers({
        getToken: () => this.csrfToken,
        setToken: (token) => {
          this.csrfToken = token || null;
        },
      });
    },
    setCsrfToken(token) {
      this.csrfToken = token || null;
    },
    async updateUser() {
      this.user = await getUser();
      await ensureCsrfToken();
    },
    setUser(userData) {
      this.user = userData;
    },
    async login() {
      await this.updateUser();
    },
    async logout() {
      await logout();
      this.user = null;
      this.csrfToken = null;
    },
  },
});