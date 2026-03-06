<template>
  <div
    class="min-h-screen bg-gradient-to-br from-[#f8f6f6] via-slate-50 to-indigo-50/30 dark:from-[#221610] dark:via-slate-950 dark:to-indigo-950/20 text-slate-900 dark:text-slate-100 flex flex-col relative overflow-hidden">

    <!-- Animated background elements -->
    <div
      class="absolute top-0 left-0 w-96 h-96 bg-indigo-200/20 dark:bg-indigo-900/20 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 animate-pulse">
    </div>
    <div
      class="absolute bottom-0 right-0 w-96 h-96 bg-[#ec5b13]/10 dark:bg-[#ec5b13]/5 rounded-full blur-3xl translate-x-1/2 translate-y-1/2 animate-pulse"
      style="animation-delay: 1s"></div>

    <!-- Main -->
    <main class="flex flex-1 items-center justify-center p-4 md:p-6 relative z-10">

      <div class="max-w-[500px] w-full">

        <!-- Card Container -->
        <div
          class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md rounded-2xl md:rounded-3xl shadow-2xl border border-white/50 dark:border-slate-700/50 overflow-hidden transition-all duration-500"
          :class="isVerified ? 'ring-2 ring-emerald-400/50' : ''">

          <!-- Header Gradient -->
          <div class="h-2 bg-gradient-to-r from-indigo-400 via-[#ec5b13] to-indigo-400"></div>

          <div class="p-8 md:p-12 text-center flex flex-col">

            <!-- Illustration -->
            <div class="mb-8 md:mb-10 flex justify-center">
              <div class="relative">
                <!-- Outer circle -->
                <div :class="[
                  'relative w-56 h-56 md:w-64 md:h-64 rounded-full flex items-center justify-center border-4 border-white dark:border-slate-800 shadow-2xl overflow-hidden transition-all duration-500',
                  isVerified
                    ? 'bg-gradient-to-tr from-emerald-400/20 via-emerald-300/20 to-transparent'
                    : 'bg-gradient-to-tr from-indigo-400/20 via-[#ec5b13]/20 to-transparent'
                ]">

                  <!-- gradient background -->
                  <div :class="[
                    'absolute inset-0 transition-all duration-500',
                    isVerified
                      ? 'bg-gradient-to-tr from-emerald-400/30 via-emerald-300/20 to-transparent'
                      : 'bg-gradient-to-tr from-[#ec5b13]/20 via-indigo-400/20 to-transparent'
                  ]"></div>

                  <!-- center icon -->
                  <div :class="[
                    'z-10 bg-white dark:bg-slate-700 p-8 rounded-full shadow-2xl border transition-all duration-500 transform',
                    isVerified
                      ? 'border-emerald-400/30 scale-110'
                      : 'border-[#ec5b13]/10'
                  ]">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-20">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
                    </svg>

                  </div>

                  <!-- decorative dots -->
                  <div class="absolute top-4 right-8 w-4 h-4 rounded-full bg-indigo-400/40 animate-pulse"></div>
                  <div class="absolute bottom-10 left-6 w-6 h-6 rounded-full bg-[#ec5b13]/30 animate-bounce"
                    style="animation-delay: 0.2s"></div>
                  <div class="absolute top-1/2 left-4 w-3 h-3 rounded-full bg-[#ec5b13]/20 animate-pulse"
                    style="animation-delay: 0.4s"></div>

                </div>
              </div>
            </div>

            <!-- Title -->
            <h1 class="text-xl md:text-4xl font-bold mb-3 transition-all duration-300"
              :class="isVerified ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-900 dark:text-white'">
              {{ isVerified ? '✓ Email Verified!' : 'Verify Your Email' }}
            </h1>

            <!-- Subtitle -->
            <p class="text-slate-600 dark:text-slate-400 text-base md:text-lg leading-relaxed mb-8 px-2">
              {{ isVerified
                ? 'Your account is now fully active. Welcome to the family! 🎉'
                : 'We sent a verification link to your email. Click the button below to activate your account.' }}
            </p>

            <!-- Error Message -->
            <transition name="slide-fade">
              <div v-if="errorMsg && !isVerified"
                class="mb-6 p-4 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/50 rounded-lg">
                <p class="text-red-700 dark:text-red-400 text-sm font-medium flex items-start gap-2">
                  <span class="material-symbols-outlined text-base flex-shrink-0 mt-0.5">error</span>
                  <span>{{ errorMsg }}</span>
                </p>
              </div>
            </transition>

            <!-- Success Message -->
            <transition name="slide-fade">
              <div v-if="isVerified"
                class="mb-6 p-4 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/50 rounded-lg">
                <p class="text-emerald-700 dark:text-emerald-400 text-sm font-medium flex items-start gap-2">
                  <span class="material-symbols-outlined text-base flex-shrink-0 mt-0.5">task_alt</span>
                  <span>Your email has been successfully verified. You're all set!</span>
                </p>
              </div>
            </transition>

            <!-- Verify Button (if not verified) -->
            <template v-if="!isVerified">
              <button @click="handleVerify" :disabled="loading || !token"
                class="w-full h-14 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 text-white text-lg font-bold shadow-lg shadow-indigo-400/40 hover:shadow-xl hover:shadow-indigo-400/50 hover:from-indigo-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 mb-4 group">
                <span class="transition-transform group-hover:scale-110">
                  <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <svg v-else class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>
                </span>
                <span>{{ loading ? 'Verifying...' : 'Verify Email' }}</span>
              </button>
            </template>

            <!-- Continue Button (if verified) -->
            <template v-else>
              <button @click="goCreateAccount"
                class="w-full h-14 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-lg font-bold shadow-lg shadow-emerald-400/40 hover:shadow-xl hover:shadow-emerald-400/50 hover:from-emerald-600 hover:to-teal-700 transition-all duration-200 flex items-center justify-center gap-2 group">
                <span class="transition-transform group-hover:translate-x-1">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6">
                    </path>
                  </svg>
                </span>
                Continue to Create Account
              </button>
            </template>

          </div>

        </div>

        <!-- Help Text -->
        <!-- <div class="mt-8 text-center">
          <p class="text-slate-600 dark:text-slate-400 text-sm">
            Didn't receive the email?
            <button
              @click="resendEmail"
              :disabled="resendLoading"
              class="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-semibold transition-colors disabled:opacity-50">
              {{ resendLoading ? 'Sending...' : 'Resend verification' }}
            </button>
          </p>
        </div> -->

      </div>

    </main>

    <!-- Footer dots -->
    <footer class="py-6 md:py-8 flex justify-center relative z-10">
      <div class="flex gap-3">
        <div class="w-2 h-2 rounded-full bg-indigo-400/40 animate-pulse"></div>
        <div class="w-2 h-2 rounded-full bg-[#ec5b13]/40 animate-bounce"></div>
        <div class="w-2 h-2 rounded-full bg-indigo-400/40 animate-pulse" style="animation-delay: 0.2s"></div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { verifyEmail, saveToken } from "@/services/auth"
import { useAuthStore } from "@/store/authStore"

const router = useRouter()
const auth = useAuthStore()
const token = ref("")
const loading = ref(false)
const resendLoading = ref(false)
const isVerified = ref(false)
const errorMsg = ref("")

const goCreateAccount = () => {
  router.push("/create-account")
}

async function handleVerify() {
  if (!token.value) {
    errorMsg.value = "Please provide a verification token"
    return
  }

  try {
    loading.value = true
    errorMsg.value = ""
    const response = await verifyEmail(token.value)

    if (response && response.access_token) {
      saveToken(response.access_token)
      await auth.login()
      isVerified.value = true
      // Auto-redirect to create account page after 2 seconds
      setTimeout(() => {
        goCreateAccount()
      }, 2000)
    }
  } catch (error) {
    errorMsg.value =
      error?.response?.data?.detail ||
      "Verification failed. Invalid or expired token."
    token.value = ""
  } finally {
    loading.value = false
  }
}

async function resendEmail() {
  try {
    resendLoading.value = true
    // Call your resend email endpoint here
    // await resendVerificationEmail()
    errorMsg.value = ""
    // Show success message
    alert("Verification email has been resent! Check your inbox.")
  } catch (error) {
    errorMsg.value = "Failed to resend email. Please try again later."
  } finally {
    resendLoading.value = false
  }
}

// Check if token is in URL and auto-fill it
onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const urlToken = urlParams.get("token")

  if (urlToken) {
    token.value = urlToken
  }
})
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateX(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}
</style>