import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import VueCookies from "vue-cookies";


const app = createApp(App);
app.use(createPinia()); // Add Pinia
app.use(router);
app.use(VueCookies);
app.mount("#app");
