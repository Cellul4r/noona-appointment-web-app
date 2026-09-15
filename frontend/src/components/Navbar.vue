<script setup>
import { ref, computed, onMounted } from "vue"
import { useAuthStore } from "../store/authStore"
import { useRouter } from "vue-router"

const isLoggedIn = computed(() => !!authStore.user)
const isOpen = ref(false)
const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
    if (!authStore.user) {
        authStore.updateUser()
    }
})

const getAvatar = () => {
    return authStore.user?.profile_image
}

const handleLogout = async () => {
    await authStore.logout()
    router.push("/login")
}
</script>

<template>
    <nav class="sticky top-0 z-50 bg-base-200 shadow px-6">

        <!-- Top Bar -->
        <div class="flex justify-between items-center h-20">

            <template v-if="isLoggedIn">
                <!-- Hamburger Button (left on mobile) -->
                <button class="md:hidden text-2xl" @click="isOpen = !isOpen">
                    ☰
                </button>
            </template>

            <!-- Left: Logo + Desktop Nav -->
            <div class="flex items-center space-x-4 text-xl font-bold">
                <router-link to="/about-us" class="flex items-center gap-2 text-2xl font-bold hover:opacity-80 mr-9">
                    <img src="/src/assets/boy.png" class="h-13" />
                    <img src="/src/assets/noona_black.png" class="h-13" />
                    <!-- <span class="font-extrabold text-xl">Noona</span> -->
                </router-link>

                <div class="hidden md:flex items-center space-x-4">
                    <template v-if="isLoggedIn">
                        <router-link to="/dashboard" v-slot="{ isActive }">
                            <span
                                :class="['btn p-0 btn-ghost', isActive ? 'text-base-content font-bold' : 'text-base-content/60']">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 0 1-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0 1 12 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 1.5v-1.5m0 0c0-.621.504-1.125 1.125-1.125m0 0h7.5" />
                                </svg>

                                Dashboard </span>
                        </router-link>
                        <router-link to="/events" v-slot="{ isActive }">
                            <span
                                :class="['btn p-0 btn-ghost', isActive ? 'text-base-content font-bold' : 'text-base-content/60']">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
                                </svg>

                                Events </span>
                        </router-link>

                        <router-link to="/calendar" v-slot="{ isActive }">
                            <span
                                :class="['btn p-0 btn-ghost', isActive ? 'text-base-content font-bold' : 'text-base-content/60']">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M6.75 2.994v2.25m10.5-2.25v2.25m-14.252 13.5V7.491a2.25 2.25 0 0 1 2.25-2.25h13.5a2.25 2.25 0 0 1 2.25 2.25v11.251m-18 0a2.25 2.25 0 0 0 2.25 2.25h13.5a2.25 2.25 0 0 0 2.25-2.25m-18 0v-7.5a2.25 2.25 0 0 1 2.25-2.25h13.5a2.25 2.25 0 0 1 2.25 2.25v7.5m-6.75-6h2.25m-9 2.25h4.5m.002-2.25h.005v.006H12v-.006Zm-.001 4.5h.006v.006h-.006v-.005Zm-2.25.001h.005v.006H9.75v-.006Zm-2.25 0h.005v.005h-.006v-.005Zm6.75-2.247h.005v.005h-.005v-.005Zm0 2.247h.006v.006h-.006v-.006Zm2.25-2.248h.006V15H16.5v-.005Z" />
                                </svg>
                                Calendar </span>
                        </router-link>
                    </template>
                </div>
            </div>

            <div class="flex items-center gap-4">
                <div class="dropdown dropdown-end">
                    <template v-if="isLoggedIn">

                        <!-- Avatar (ปุ่มกด) -->
                        <div tabindex="0" role="button" class="avatar cursor-pointer">
                            <div class="bg-neutral text-neutral-content w-10 rounded-full">
                                <img :src="getAvatar()" alt="Profile Image">
                            </div>
                        </div>

                        <!-- Dropdown menu -->
                        <ul tabindex="0"
                            class="dropdown-content menu bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
                            <li>
                                <router-link to="/setting" @click="$event.currentTarget.blur()">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                    </svg>
                                    Settings
                                </router-link>
                            </li>
                            <li>
                                <router-link to="/login" class="text-error" @click.prevent="handleLogout()">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                                    </svg>

                                    Logout
                                </router-link>
                            </li>
                        </ul>
                    </template>

                    <template v-else>
                        <router-link to="/login" class="text-blue-500 underline hover:text-blue-700 text-sm">
                            Sign In
                        </router-link>
                        <span class="mx-2 text-gray-400">|</span>
                        <router-link to="/verify-email" class="text-blue-500 underline hover:text-blue-700 text-sm">
                            Sign Up
                        </router-link>
                    </template>
                </div>
            </div>

        </div>


        <!-- Mobile Menu -->
        <div v-if="isOpen" class="md:hidden pb-4 space-y-2">
            <template v-if="isLoggedIn">
                <router-link to="/dashboard" class="block btn btn-ghost">
                    Dashboard
                </router-link>
                <router-link to="/events" class="block btn btn-ghost">
                    Events
                </router-link>
                <router-link to="/calendar" class="block btn btn-ghost">
                    Calendar
                </router-link>
            </template>
            <template v-else>
                <router-link to="/login" class="text-blue-500 underline hover:text-blue-700 text-sm">
                    Sign In
                </router-link>
                <span class="mx-2 text-gray-400">|</span>
                <router-link to="/register" class="text-blue-500 underline hover:text-blue-700 text-sm">
                    Sign Up
                </router-link>
            </template>

        </div>
    </nav>
</template>