import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Signup from "../views/Signup.vue";
import AllEvents from "../views/AllEvents.vue";

const routes = [
  { path: '/login', component: Login, meta: { hideNavbar: true}},
  { path: "/login-success", component: Login }, // Handles token parsing
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
    meta: { hideNavbar: true }
  },
  {
    path: '/events',
    name: 'AllEvents',
    component: AllEvents,
    //meta: { requiresAuth: true } // Optional: prevents access if not logged in
  },



];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;