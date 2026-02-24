import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Signup from "../views/Signup.vue";
import AllEvents from "../views/AllEvents.vue";
import Dashboard from '../views/Dashboard.vue'; 
import CreateEvents from "../views/CreateEvents.vue";

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
    meta: { requiresAuth: true } //prevents access if not logged in
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true } //prevents access if not logged in
  },
  {
    path: '/create_events',
    name: 'CreateEvents',
    component: CreateEvents,
    meta: { requiresAuth: true },
    meta: { hideNavbar: true}
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;