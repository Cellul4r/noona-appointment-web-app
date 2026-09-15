import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import ConfirmEmail from "../views/ConfirmEmail.vue";
import AllEvents from "../views/AllEvents.vue";
import Dashboard from '../views/Dashboard.vue';
import CreateEvents from "../views/CreateEvents.vue";
import EventOverview from '../views/EventOverview.vue';
import Setting from "../views/Setting.vue";
import EditEvent from '../views/EditEvent.vue';
import Calendar from '../views/Calendar.vue';
import NotFound from '../views/NotFound.vue';
import { useAuthStore } from '../store/authStore';
import LoginSuccess from '../views/LoginSuccess.vue';
import EventRegistration from '../views/EventRegistration.vue';
import CreateAccount from '../views/CreateAccount.vue';
import VerifyEmail from '../views/VerifyEmail.vue';
import EmailSent from '../views/EmailSent.vue';
import ForgetPassword from '../views/ForgetPassword.vue';
import EmailSentResetPassword from '../views/EmailSentResetPassword.vue';
import CreateNewPassword from '../views/CreateNewPassword.vue';
const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { hideNavbar: true } },
  { path: "/login-success", name: 'LoginSuccess', component: LoginSuccess, meta: { hideNavbar: true } }, // Handles token parsing
  {
    path: "/confirm-email",
    name: "ConfirmEmail",
    component: ConfirmEmail,
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
    meta: { requiresAuth: true, hideNavbar: true },
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
    meta: { requiresAuth: true, hideNavbar: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
    meta: { requiresAuth: true }
  },
  {
    path: '/about-us',
    name: 'AboutUs',
    component: () => import('../views/AboutUs.vue'),
    alias: '',
  },
  {
    path: `/event/register/:event_uuid`,
    name: "EventRegistration",
    component: EventRegistration,
    meta: { requiresAuth: true }
  },
  {
    path: '/create-account',
    name: 'CreateAccount',
    component: CreateAccount,
    meta: { hideNavbar: true }
  },
  {
    path: '/verify-email',
    name: 'VerifyEmail',
    component: VerifyEmail,
    meta: { hideNavbar: true }
  },
  {
    path: '/email-sent',
    name: 'EmailSent',
    component: EmailSent,
    meta: { hideNavbar: true }
  },
  {
    path: '/forgot-password',
    name: 'ForgetPassword',
    component: ForgetPassword,
    meta: { hideNavbar: true }
  },
  {
    path: '/email-sent-reset-password',
    name: 'EmailSentResetPassword',
    component: EmailSentResetPassword,
    meta: { hideNavbar: true }
  },
  {
    path: '/reset-password',
    name: 'CreateNewPassword',
    component: CreateNewPassword,
    meta: { hideNavbar: true }
  },
  {
    path: '/:patchMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { hideNavbar: true }
    // catch-all route, should be last in the list
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth) {
    if (!authStore.user) {
      try {
        await authStore.updateUser();
      } catch (err) {
        authStore.user = null;
      }
    }
    if (!authStore.isAuthenticated) {
      return next({ name: 'Login' });
    }

  }
  if ((to.name === 'Login' || to.name === 'Signup') && authStore.isAuthenticated) {
    return next({ name: 'Dashboard' });
  }
  return next();
})


export default router;