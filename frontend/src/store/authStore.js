import { defineStore } from "pinia";
import { getUser, saveToken, logout } from "@/services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: getUser(),
  }),
  actions: {
    updateUser() {
      this.user = getUser();
    },
    setUser(userData) {
      this.user = userData;
    },
    login(token) {
      saveToken(token); // Saves to cookie
      this.updateUser();
    },
    logout() {
      logout();
      this.user = null;
    },
  },
});