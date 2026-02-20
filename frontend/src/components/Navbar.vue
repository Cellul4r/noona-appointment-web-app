<script setup>
import { ref } from "vue"
const isOpen = ref(false)
</script>

<template>
  <nav class="sticky top-0 z-50 bg-white shadow px-6">
    
    <!-- Top Bar -->
    <div class="flex justify-between items-center h-16">
      
      <!-- Left: Logo -->
        <div class="hidden md:flex items-center space-x-4 text-xl font-bold"> 
            <router-link 
            to="/dashboard" 
            class="text-xl font-bold hover:opacity-80"
            >
            MyApp
            </router-link>
            <router-link to="/events" v-slot="{ isActive }"> 
                <span :class="[ 'btn btn-ghost', isActive ? 'text-base-content font-bold' : 'text-base-content/60' ]" > Events </span> 
            </router-link> 
            <router-link to="/login" v-slot="{ isActive }"> 
                <span :class="[ 'btn btn-ghost', isActive ? 'text-base-content font-bold' : 'text-base-content/60' ]" > Dashboard </span> 
            </router-link> 
            <router-link to="/signup" v-slot="{ isActive }"> 
                <span :class="[ 'btn btn-ghost', isActive ? 'text-base-content font-bold' : 'text-base-content/60' ]" > Calendar </span>
            </router-link>
        </div>

        <!-- Mobile Button -->
        <button
            class="md:hidden text-2xl"
            @click="isOpen = !isOpen"
        >
            ☰
        </button>

        <div class="dropdown dropdown-end">
  
            <!-- Avatar (ปุ่มกด) -->
            <div tabindex="0" role="button" class="avatar avatar-online cursor-pointer">
                <div class="bg-neutral text-neutral-content w-10 rounded-full">
                <span class="text-xl">AI</span>
                </div>
            </div>

            <!-- Dropdown menu -->
            <ul
            tabindex="0"
            class="dropdown-content menu bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
            <li>
                <router-link to="/settings" @click="$event.currentTarget.blur()">
                Settings
                </router-link>
            </li>
            <li>
                <router-link to="/login" class="text-error" @click="$event.currentTarget.blur()">
                Logout
                </router-link>
            </li>
            </ul>

        </div>
      
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="isOpen"
      class="md:hidden pb-4 space-y-2"
    >
        <router-link to="/events" class="block btn btn-ghost">
            Events
        </router-link>
        <router-link to="/dashboard" class="block btn btn-ghost">
            Dashboard
        </router-link>
        <router-link to="/calendar" class="block btn btn-ghost">
            Calendar
        </router-link>
    </div>


  </nav>
</template>