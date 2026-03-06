<template>
    <div class="min-h-screen flex flex-col bg-white text-slate-900">

        <!-- Center -->
        <div class="flex-grow flex items-center justify-center px-6 py-12">
            <div class="w-full max-w-[440px] flex flex-col items-center">

                <!-- Logo -->
                <div class="mb-10 flex flex-col items-center gap-2">
                    <img src="/src/assets/boy.png" class="h-13" />
                    <img src="/src/assets/noona_black.png" class="h-13" />
                </div>

                <!-- Card -->
                <div class="w-full bg-white p-8 md:p-10 rounded-2xl border border-slate-100 shadow-sm">

                    <!-- Title -->
                    <div class="text-center mb-8">
                        <h1 class="text-3xl font-bold tracking-tight mb-3">
                            Forgot Password?
                        </h1>

                        <p class="text-slate-500 text-base leading-relaxed">
                            No worries! Enter the email address associated with your account,
                            and we'll send you a link to reset your password.
                        </p>
                    </div>

                    <!-- Form -->
                    <form class="space-y-6" @submit.prevent="handlePasswordResetToken">

                        <div class="space-y-2">
                            <label class="text-sm font-semibold ml-1">
                                Email address
                            </label>

                            <input v-model="email" type="email" placeholder="e.g. hello@noona.app"
                                class="w-full px-5 py-4 bg-slate-50 border-none rounded-2xl placeholder:text-slate-400 focus:ring-2 focus:ring-primary/20 outline-none"
                                required />
                        </div>

                        <!-- Button -->
                        <button
                            type="submit"
                            :disabled="loading"
                            class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-4 rounded-full shadow-lg shadow-primary/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                            <span>{{ loading ? 'Sending...' : 'Send Reset Link' }}</span>

                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
                            </svg>

                        </button>

                    </form>

                    <!-- Back -->
                    <div class="mt-8 pt-6 border-t border-slate-100 flex justify-center">

                        <button @click="goBack"
                            class="flex items-center gap-2 text-primary font-semibold hover:underline underline-offset-4">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
                            </svg>


                            Back to Sign In
                        </button>

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

        <!-- Background Blur -->
        <div class="fixed inset-0 -z-10 pointer-events-none overflow-hidden">
            <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-primary/5 blur-[120px] rounded-full"></div>
            <div class="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-primary/5 blur-[120px] rounded-full">
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref } from "vue"
import { forgotPassword } from "@/services/auth";
import { useRouter } from 'vue-router'

const router = useRouter();
const email = ref("")
const loading = ref(false)
const goBack = () => {
    router.push("/login")
}
async function handlePasswordResetToken() {
  if (!email.value) return;

  try {
    loading.value = true;
    await forgotPassword(email.value);
    router.push("/email-sent-reset-password");
  } catch (error) {
    const detail =
      typeof error?.response?.data?.detail === "string"
        ? error.response.data.detail
        : "Unable to send password reset email. Please try again.";
    alert(detail);
  } finally {
    loading.value = false;
  }
}
</script>

<style>
:root {
    --primary: #136dec;
}

.bg-primary {
    background-color: var(--primary);
}

.text-primary {
    color: var(--primary);
}
</style>