<template>
    <div
        class="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-indigo-50 flex flex-col relative overflow-hidden">

        <!-- Animated glow background -->
        <div class="absolute inset-0 bg-glow pointer-events-none animate-pulse"></div>
        <div
            class="absolute top-10 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob">
        </div>
        <div
            class="absolute top-40 right-10 w-72 h-72 bg-cyan-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000">
        </div>

        <!-- Content -->
        <main class="flex-1 flex items-center justify-center px-4 sm:px-6 z-10 py-12 sm:py-0">
            <div class="max-w-md w-full text-center space-y-8 sm:space-y-10 animate-fade-in">

                <!-- Icon -->
                <div class="flex justify-center animate-bounce" style="animation-delay: 0.1s;">
                    <div
                        class="w-24 h-24 sm:w-32 sm:h-32 rounded-[24px] sm:rounded-[32px] glass-icon flex items-center justify-center text-blue-500 shadow-2xl">
                        <svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24"
                            class="w-12 h-12 sm:w-16 sm:h-16 fill-current">
                            <path fill="darkblue"
                                d="M24,10v9c0,2.76-2.24,5-5,5H5c-2.76,0-5-2.24-5-5V8C0,5.24,2.24,3,5,3H13c.55,0,1,.45,1,1s-.45,1-1,1H5c-1.15,0-2.14,.65-2.65,1.59l7.53,7.53c1.17,1.17,3.07,1.17,4.24,0l3.82-3.82c.39-.39,1.02-.39,1.41,0s.39,1.02,0,1.41l-3.82,3.82c-.97,.97-2.26,1.46-3.54,1.46s-2.56-.49-3.54-1.46L2,9.07v9.93c0,1.65,1.35,3,3,3h14c1.65,0,3-1.35,3-3V10c0-.55,.45-1,1-1s1,.45,1,1Zm-8-6c0-2.21,1.79-4,4-4s4,1.79,4,4-1.79,4-4,4-4-1.79-4-4Zm2,0c0,1.1,.9,2,2,2s2-.9,2-2-.9-2-2-2-2,.9-2,2Z" />
                        </svg>
                    </div>
                </div>

                <!-- Title -->
                <div>
                    <h1
                        class="text-3xl sm:text-4xl font-bold font-rounded text-blue-800 tracking-tight">
                        Check Your Email
                    </h1>
                </div>

                <!-- Description -->
                <p class="text-gray-600 text-base sm:text-lg leading-relaxed px-2 sm:px-4 font-medium">
                    We've sent a password reset link to your email.
                    <br class="hidden sm:block" />
                    Please click the link to create a new password.
                </p>

                <!-- Button -->
                <div class="pt-4">
                    <button @click="goBack"
                        class="group relative inline-flex items-center justify-center gap-2 px-6 sm:px-8 py-3 sm:py-3 font-semibold text-sm sm:text-base text-white bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95 transition-all duration-300 overflow-hidden">
                        <span
                            class="absolute inset-0 bg-gradient-to-r from-blue-700 to-cyan-700 rounded-full blur opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></span>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-4 inline group-hover:-translate-x-1 transition-transform">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
                        </svg>
                        Back to Forget Password Page
                    </button>
                </div>
                <p class="text-gray-400 text-sm">
                    Didn't receive it? Check your junk mail or return to the previous page to request a new reset link.
                </p>

            </div>
        </main>

    </div>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const goBack = () => {
    router.push("/forgot-password")
}

</script>

<style scoped>
.glass-icon {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(59, 130, 246, 0.3);
    box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.bg-glow {
    background: radial-gradient(circle at center, rgba(59, 130, 246, 0.25), transparent 70%);
}

.font-rounded {
    font-family: 'Quicksand', 'Segoe UI', sans-serif;
}

@keyframes blob {

    0%,
    100% {
        transform: translate(0px, 0px) scale(1);
    }

    33% {
        transform: translate(30px, -50px) scale(1.1);
    }

    66% {
        transform: translate(-20px, 20px) scale(0.9);
    }
}

@keyframes fade-in {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-blob {
    animation: blob 7s infinite;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animate-fade-in {
    animation: fade-in 0.6s ease-out;
}
</style>