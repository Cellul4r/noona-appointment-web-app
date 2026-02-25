import { defineStore } from "pinia";
import { logout } from "@/services/auth";
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
    },
    setUser(userData) {
      this.user = userData;
    },
    async login() {
      await this.updateUser();
    },
    logout() {
      logout();
      this.user = null;
    },
  },
});