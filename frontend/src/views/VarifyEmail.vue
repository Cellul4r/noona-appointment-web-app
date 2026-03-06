<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Decorative background elements -->
    <div class="absolute top-0 left-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
    <div class="absolute top-0 right-0 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
    <div class="absolute bottom-0 left-1/2 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
    
    <div class="w-full max-w-md relative">
      <!-- Main Card -->
      <div class="bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 md:p-10 transform transition-all duration-500 hover:shadow-3xl">
        
        <!-- Header with icon -->
        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
        </div>

        <h2 class="text-center text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
          Verify your email
        </h2>
        <p class="text-center text-gray-500 text-sm mb-8 leading-relaxed">
          Enter your email address to get started with your account verification
        </p>

        <!-- Email Input with Icon -->
        <div class="relative mb-6">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
            </svg>
          </div>
          <input 
            v-model="email" 
            type="email" 
            placeholder="hello@example.com"
            class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-4 focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
          />
        </div>

        <!-- Continue Button -->
        <button 
          @click="handleContinue"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>{{ loading ? 'Processing...' : 'Continue' }}</span>
          <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
          </svg>
          <svg v-else class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </button>

        <!-- Divider -->
        <div class="relative my-8">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-white text-gray-500 font-medium">Or continue with</span>
          </div>
        </div>

        <!-- Social Login Buttons -->
        <div class="grid grid-cols-2 gap-4 mb-8">
          <!-- GitHub Button -->
          <button 
            type="button" 
            @click="loginWithGithub"
            class="flex items-center justify-center gap-3 px-4 py-3 bg-gray-900 text-white rounded-xl shadow-md hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 group"
          >
            <svg class="w-5 h-5 group-hover:rotate-12 transition-transform" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z"></path>
            </svg>
            <span class="font-medium text-sm hidden sm:inline">GitHub</span>
          </button>

          <!-- Google Button -->
          <button 
            type="button" 
            @click="loginWithGoogle"
            class="flex items-center justify-center gap-3 px-4 py-3 bg-white border-2 border-gray-200 text-gray-700 rounded-xl shadow-md hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 group hover:border-gray-300"
          >
            <svg class="w-5 h-5 group-hover:rotate-12 transition-transform" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span class="font-medium text-sm hidden sm:inline">Google</span>
          </button>
        </div>

        <!-- Footer -->
        <p class="text-center text-sm text-gray-500">
          Already have an account? 
          <a href="/login" class="text-purple-600 hover:text-purple-700 font-semibold hover:underline transition-colors">
            Log in
          </a>
        </p>

      </div>
      
      <!-- Bottom decoration -->
      <div class="text-center mt-6 text-xs text-gray-400">
        <p>Secure and encrypted email verification</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle, loginWithGithub } from "@/services/auth";
import { useRouter } from 'vue-router'

const auth = useAuthStore();
const email = ref("");
const password = ref("");
const router = useRouter();
const loading = ref(false);

function saveTokenFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");

  if (token) {
    auth.login(token);
    window.history.replaceState({}, document.title, "/events");
  }
}

async function goToSignup() {
  router.push("/signup");
}

async function handleContinue() {
  if (!email.value) return;
  // Handle email verification logic here
  console.log('Email:', email.value);
}

async function handleLogin() {
  try {
    loading.value = true;

    const formData = new URLSearchParams();
    formData.append("username", email.value);
    formData.append("password", password.value);

    const response = await fetch("http://localhost:56733/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: formData.toString(),
      credentials: "include"
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    // หลัง login สำเร็จ → ดึง user
    const me = await fetch("http://localhost:56733/auth/me", {
      credentials: "include"
    });

    const userData = await me.json();
    auth.user = userData;

    router.replace("/events");

  } catch (error) {
    alert("Don't have an account, login first.");
    router.push("/signup");
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  saveTokenFromUrl();
});
</script>

<style scoped>
body {
  font-family: Inter, sans-serif;
}

@keyframes blob {
  0%, 100% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
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

/* Custom shadow for enhanced depth */
.shadow-3xl {
  box-shadow: 0 35px 60px -15px rgba(0, 0, 0, 0.3);
}

/* Smooth input transition */
input:focus {
  transform: translateY(-2px);
}

/* Custom scrollbar if needed */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #9333ea, #ec4899);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #7e22ce, #db2777);
}
</style>
