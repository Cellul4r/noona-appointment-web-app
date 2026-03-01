<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/authStore'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
    try {
        await authStore.updateUser()
        router.replace({ name: 'Dashboard' })
    } catch (error) {
        router.replace({ name: 'Login' })
    }
})
</script>

<template>
    <div class="flex justify-center items-center h-screen">
        Logging you in...
    </div>
</template>