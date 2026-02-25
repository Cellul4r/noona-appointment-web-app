import { defineStore } from "pinia";
import { getUser, saveToken, logout } from "@/services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: getUser(),
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
  },
  actions: {
    updateUser() {
      this.user = getUser();
    },
    setUser(userData) {
      this.user = userData;
    },
    login() {
      this.updateUser();
    },
    logout() {
      logout();
      this.user = null;
    },
  },
});