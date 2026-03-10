<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'

const route = useRoute()

onMounted(() => {
  const savedTheme = localStorage.getItem('app-theme')
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme)
  }
})
</script>
<template>
  <div>
    <!-- <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a> -->
    <!-- Render the appropriate component for the current route -->
    <Navbar v-if="!route.meta.hideNavbar" />
    <router-view />
    <!-- <router-view /> -->
  </div>
</template>