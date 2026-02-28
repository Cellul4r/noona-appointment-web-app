import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Signup from "../views/Signup.vue";
import AllEvents from "../views/AllEvents.vue";
import Dashboard from '../views/Dashboard.vue';
import CreateEvents from "../views/CreateEvents.vue";
import EventOverview from '../views/EventOverview.vue';
import Setting from "../views/Setting.vue";
import EditEvent from '../views/EditEvent.vue';
import Calendar from '../views/Calendar.vue';

const routes = [
  { path: '/login', component: Login, meta: { hideNavbar: true } },
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
    path: '/event/create',
    name: 'CreateEvents',
    component: CreateEvents,
    meta: { requiresAuth: true },
    meta: { hideNavbar: true }
  },
  {
    path: '/event/overview/:event_uuid',
    name: 'EventOverview',
    component: EventOverview,
  },
  {
    path: '/setting',
    name: 'setting',
    component: Setting,
    meta: { requiresAuth: true } //prevents access if not logged in
  },
  {
    path: '/events/edit/:event_uuid',
    name: 'EditEvent',
    component: EditEvent,
    meta: { requiresAuth: true },
    meta: { hideNavbar: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
  }


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;