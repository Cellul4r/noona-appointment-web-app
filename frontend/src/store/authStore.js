import { defineStore } from "pinia";
import { ensureCsrfToken, logout, setCsrfToken } from "@/services/auth";
import { getUser } from "../services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
  },
  actions: {
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
      setCsrfToken(null);
      await logout();
      this.user = null;
    },
  },
});