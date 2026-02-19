import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/HelloWorld.vue'; // Replace with your desired home component
import Phonebook from '../components/Phonebook.vue';
import Contact from "../components/Contact.vue";
import Login from '../views/Login.vue';
import Signup from "../views/Signup.vue";
import AllEvents from "../views/AllEvents.vue";

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/phonebook', name: 'Phonebook', component: Phonebook },
  { path: "/contacts", name: "Contact", component: Contact },
  { path: '/login', component: Login },
  { path: "/login-success", component: Login }, // Handles token parsing
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: '/events',
    name: 'AllEvents',
    component: AllEvents,
    meta: { requiresAuth: true } //prevents access if not logged in
  }




];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;