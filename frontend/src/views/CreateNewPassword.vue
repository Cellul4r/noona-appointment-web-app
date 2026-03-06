<template>
    <div class="min-h-screen flex flex-col bg-[#fffefa] text-slate-900">
        <!-- font-[Inter] -->
        <!-- Center container -->
        <div class="flex-grow flex items-center justify-center px-6 py-12">
            <div class="w-full max-w-[440px] flex flex-col items-center">

                <!-- Logo -->
                <div class="mb-10 flex flex-col items-center gap-2">
                    <img src="/src/assets/boy.png" class="h-13" />
                    <img src="/src/assets/noona_pink.png" class="h-13" />
                </div>

                <!-- Card -->
                <div class="w-full bg-white p-8 md:p-10 rounded-xl border border-slate-100 shadow-sm">

                    <!-- Header -->
                    <div class="text-center mb-8">
                        <h1 class="text-3xl font-bold mb-3">
                            Create New Password
                        </h1>

                        <p class="text-slate-500 text-base">
                            Please choose a strong password that you haven't used before.
                        </p>
                    </div>

                    <!-- Form -->
                    <form class="space-y-6" @submit.prevent="handleReset">

                        <!-- Email (readonly) -->
                        <div class="space-y-2">

                            <label class="text-sm font-semibold ml-1">
                                Email Address
                            </label>

                            <input v-model="email" type="email" readonly
                                class="w-full px-5 py-4 bg-slate-100 border-none rounded-2xl outline-none text-slate-600 cursor-not-allowed"
                                placeholder="your@email.com" />

                        </div>

                        <!-- New password -->
                        <div class="space-y-2">

                            <label class="text-sm font-semibold ml-1">
                                New Password
                            </label>

                            <div class="relative">
                                <input v-model="password" :type="showPassword ? 'text' : 'password'"
                                    class="w-full px-5 py-4 pr-12 bg-slate-50 border-none rounded-2xl focus:ring-2 focus:ring-zinc-700/20 outline-none"
                                    placeholder="••••••••" />
                            </div>

                        </div>

                        <!-- Confirm password -->
                        <div class="space-y-2">

                            <label class="text-sm font-semibold ml-1">
                                Confirm New Password
                            </label>

                            <div class="relative">
                                <input v-model="confirmPassword" :type="showConfirm ? 'text' : 'password'"
                                    class="w-full px-5 py-4 pr-12 bg-slate-50 border-none rounded-2xl focus:ring-2 focus:ring-zinc-700/20 outline-none"
                                    placeholder="••••••••" />
                            </div>

                        </div>

                        <!-- Password rules -->
                        <div class="space-y-2 py-2">

                            <div class="flex items-center gap-2 text-sm">
                                <!-- Unchecked -->
                                <svg v-if="!validLength" xmlns="http://www.w3.org/2000/svg" fill="none"
                                    viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                    class="size-5 text-slate-300">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                                <!-- Checked -->
                                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-5 text-green-500">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>

                                At least 8 characters
                            </div>

                            <div class="flex items-center gap-2 text-sm">
                                <!-- Unchecked -->
                                <svg v-if="!hasSpecial" xmlns="http://www.w3.org/2000/svg" fill="none"
                                    viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                    class="size-5 text-slate-300">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                                <!-- Checked -->
                                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-5 text-green-500">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>

                                One special character
                            </div>

                        </div>

                        <!-- Reset button -->
                        <button type="submit" :disabled="!isValid || loading"
                            class="w-full bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-4 rounded-full shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ loading ? 'Resetting...' : 'Reset Password' }}
                        </button>

                    </form>

                    <!-- Back -->
                    <div class="mt-8 pt-6 border-t flex justify-center">

                        <RouterLink to="/login"
                            class="flex items-center gap-2 text-zinc-800 font-semibold hover:underline">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
                            </svg>

                            Back to Sign In
                        </RouterLink>

                    </div>

                </div>

                <!-- Footer -->
                <div class="mt-10 text-center">
                    <p class="text-slate-400 text-sm">
                        © 2024 Noona Inc. All rights reserved.
                    </p>
                </div>

            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { createNewPassword, resetPassword } from "@/services/auth"

const router = useRouter()
const route = useRoute()

const email = ref("")
const token = ref("")
const password = ref("")
const confirmPassword = ref("")
const loading = ref(false)
const tokenVerified = ref(false)

const showPassword = ref(false)
const showConfirm = ref(false)

// Extract email and token from URL on mount
onMounted(async () => {
    email.value = route.query.email || ""
    token.value = route.query.token || ""

    if (!token.value) {
        alert("Invalid reset link. Please request a new password reset.")
        router.push("/forget-password")
        return
    }

    // If email is in URL, we can skip verification for now
    if (email.value) {
        return
    }

    // If email not in URL, get it from backend by verifying token
    try {
        loading.value = true
        const response = await createNewPassword(token.value)
        email.value = response.email || ""
        tokenVerified.value = true

        if (!email.value) {
            alert("Unable to retrieve email. Please request a new password reset.")
            router.push("/forget-password")
        }
    } catch (error) {
        alert("Invalid or expired reset link. Please request a new password reset.")
        router.push("/forget-password")
    } finally {
        loading.value = false
    }
})

const validLength = computed(() => password.value.length >= 8)

const hasSpecial = computed(() =>
    /[!@#$%^&*(),.?":{}|<>]/.test(password.value)
)

const isValid = computed(() =>
    validLength.value &&
    hasSpecial.value &&
    password.value === confirmPassword.value &&
    password.value.length > 0
)

async function handleReset() {
    if (!isValid.value) return

    try {
        loading.value = true

        // Verify token if not already verified (e.g., email was in URL)
        if (!tokenVerified.value) {
            await createNewPassword(token.value)
        }

        // Then reset the password
        await resetPassword(password.value)

        alert("Password reset successfully! Please login with your new password.")
        router.push("/login")

    } catch (error) {
        const detail =
            typeof error?.response?.data?.detail === "string"
                ? error.response.data.detail
                : "Unable to reset password. Please try again or request a new reset link."
        alert(detail)
    } finally {
        loading.value = false
    }
}
</script>