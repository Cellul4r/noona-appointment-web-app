<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-indigo-50 flex items-center justify-center p-4 relative">
        <!-- Decorative background elements -->
        <div class="absolute top-0 left-0 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div class="absolute top-0 right-0 w-72 h-72 bg-cyan-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div class="absolute bottom-0 left-1/2 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
        
        <div class="w-full max-w-md relative">

            <!-- Main Card -->
            <div class="bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 md:p-10 transform transition-all duration-500 hover:shadow-3xl">
                <!-- Header -->
                <div class="text-center mb-8">
                    <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent mb-3">
                        Create New Password
                    </h1>

                    <p class="text-gray-600 text-sm leading-relaxed">
                        Please choose a strong password that you haven't used before.
                    </p>
                </div>

                <!-- Form -->
                <form class="space-y-5" @submit.prevent="handleReset">

                    <!-- Email (readonly) -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            Email Address
                        </label>
                        <input v-model="email" type="email" readonly
                            class="w-full px-4 py-4 bg-gray-50 border-2 border-gray-200 rounded-xl outline-none text-gray-700 cursor-not-allowed"
                            placeholder="your@email.com" />
                    </div>

                    <!-- New password -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            New Password
                        </label>
                        <div class="relative">
                            <input v-model="password" :type="showPassword ? 'text' : 'password'"
                                class="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
                                placeholder="••••••••" />
                        </div>
                    </div>

                    <!-- Confirm password -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            Confirm New Password
                        </label>
                        <div class="relative">
                            <input v-model="confirmPassword" :type="showConfirm ? 'text' : 'password'"
                                class="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
                                placeholder="••••••••" />
                        </div>
                    </div>

                    <!-- Password rules -->
                    <div class="space-y-2">

                        <div class="flex items-center gap-2 text-sm">
                            <!-- Unchecked -->
                            <svg v-if="!validLength" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                class="size-5 text-gray-300">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <!-- Checked -->
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-5 text-green-500">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span class="text-gray-600">At least 8 characters</span>
                        </div>

                        <div class="flex items-center gap-2 text-sm">
                            <!-- Unchecked -->
                            <svg v-if="!hasNumber" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                class="size-5 text-gray-300">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <!-- Checked -->
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-5 text-green-500">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span class="text-gray-600">One number</span>
                        </div>

                        <div class="flex items-center gap-2 text-sm">
                            <!-- Unchecked -->
                            <svg v-if="!hasLowercase" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                class="size-5 text-gray-300">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <!-- Checked -->
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-5 text-green-500">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span class="text-gray-600">One lowercase letter</span>
                        </div>

                        <div class="flex items-center gap-2 text-sm">
                            <!-- Unchecked -->
                            <svg v-if="!hasUppercase" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                class="size-5 text-gray-300">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <!-- Checked -->
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-5 text-green-500">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span class="text-gray-600">One uppercase letter</span>
                        </div>

                    </div>

                    <!-- Reset button -->
                    <button type="submit" :disabled="!isValid || loading"
                        class="btn btn-active btn-primary w-full transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed">
                        {{ loading ? 'Resetting...' : 'Reset Password' }}
                    </button>

                </form>

                <!-- Back to Login -->
                <div class="mt-6 pt-6 border-t border-gray-200 text-center">
                    <RouterLink to="/login"
                        class="flex items-center justify-center gap-2 text-blue-600 font-semibold hover:text-blue-800 hover:underline transition">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
                        </svg>
                        Back to Sign In
                    </RouterLink>
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

const hasNumber = computed(() => /\d/.test(password.value))

const hasLowercase = computed(() => /[a-z]/.test(password.value))

const hasUppercase = computed(() => /[A-Z]/.test(password.value))

const isValid = computed(() =>
    validLength.value &&
    hasNumber.value &&
    hasLowercase.value &&
    hasUppercase.value &&
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

<style scoped>
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>