<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Decorative background elements -->
    <div class="absolute top-0 left-0 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
    <div class="absolute top-0 right-0 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
    <div class="absolute bottom-0 left-1/2 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
    
    <div class="w-full max-w-md relative">
      <!-- Main Card -->
      <div class="bg-white/90 backdrop-blur-lg rounded-3xl shadow-2xl p-4 md:p-5 transform transition-all duration-500 hover:shadow-3xl max-h-[95vh] overflow-y-auto">
        
        <!-- Header -->
        <div class="flex justify-center mb-2">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
            </svg>
          </div>
        </div>

        <h2 class="text-center text-2xl font-bold text-gray-800 mb-1">Create Account. It's free!!</h2>
        <p class="text-center text-gray-600 text-sm mb-2 leading-relaxed">Let's join our Noona. Get set up in under a minute.</p>

        <form class="space-y-2 w-full">
          <!-- Full Name -->
          <div>
            <label class="block text-left font-semibold text-gray-700 mb-1 text-base">Full Name</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <input
                type="text"
                v-model="fullname"
                placeholder="Janny Games"
                class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-2 text-base focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-left font-semibold text-gray-700 mb-1 text-base">Email address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <input
                type="email"
                v-model="email"
                placeholder="Janny_games@example.com"
                :readonly="isEmailLocked"
                :class="isEmailLocked ? 'bg-gray-50 cursor-not-allowed' : ''"
                class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-2 text-base focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
                required 
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-left font-semibold text-gray-700 mb-1 text-base">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <input 
                v-model="password" 
                type="password" 
                class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-2 text-base focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400" 
                placeholder="Enter password"
                required 
                minlength="8" 
                pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
                title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" 
              />
            </div>
            <!-- Password Requirements -->
            <div v-if="password" class="mt-0.5 space-y-0.5">
              <div class="flex items-center gap-1.5 text-sm">
                <svg v-if="passwordValidation.minLength" class="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <svg v-else class="w-3 h-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                <span :class="passwordValidation.minLength ? 'text-green-600' : 'text-red-600'">At least 8 characters</span>
              </div>
              <div class="flex items-center gap-1.5 text-sm">
                <svg v-if="passwordValidation.hasNumber" class="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <svg v-else class="w-3 h-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                <span :class="passwordValidation.hasNumber ? 'text-green-600' : 'text-red-600'">At least one number</span>
              </div>
              <div class="flex items-center gap-1.5 text-sm">
                <svg v-if="passwordValidation.hasLowercase" class="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <svg v-else class="w-3 h-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                <span :class="passwordValidation.hasLowercase ? 'text-green-600' : 'text-red-600'">At least one lowercase letter</span>
              </div>
              <div class="flex items-center gap-1.5 text-sm">
                <svg v-if="passwordValidation.hasUppercase" class="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <svg v-else class="w-3 h-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                <span :class="passwordValidation.hasUppercase ? 'text-green-600' : 'text-red-600'">At least one uppercase letter</span>
              </div>
            </div>
          </div>

          <!-- Confirmed Password -->
          <div>
            <label class="block text-left font-semibold text-gray-700 mb-1 text-base">Confirmed Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
              <input 
                v-model="confirmPassword" 
                type="password" 
                class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-2 text-base focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400" 
                placeholder="Confirm password"
                required 
                minlength="8" 
                pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
                title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" 
              />
            </div>
          </div>

          <!-- Create Account Button -->
          <button
            @click.prevent="handleSignup"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-2 text-base rounded-xl font-semibold shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>{{ loading ? 'Creating Account...' : 'Create Account' }}</span>
            <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
            </svg>
            <svg v-else class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </button>

          <!-- Divider -->
          <div class="relative flex py-1.5 items-center">
            <div class="flex-grow border-t border-gray-300"></div>
            <span class="flex-shrink mx-3 text-gray-500 text-xs">OR</span>
            <div class="flex-grow border-t border-gray-300"></div>
          </div>

         <!-- GitHub --> 
          <button 
            type="button" 
            @click="loginWithGithub" 
            class="w-full px-4 py-2 text-base shadow-lg rounded-xl bg-black text-white border-black transition-all duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2"
          > 
            <svg aria-label="GitHub logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="white" d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z"></path></svg>
            <span>Login with GitHub</span>
          </button> 

          <!-- Google --> 
          <button 
            type="button" 
            @click="loginWithGoogle" 
            class="w-full px-4 py-2 text-base shadow-lg rounded-xl bg-white text-gray-700 border-2 border-gray-200 transition-all duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2" 
          > 
            <svg aria-label="Google logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><g><path d="m0 0H512V512H0" fill="#fff"></path><path fill="#34a853" d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"></path><path fill="#4285f4" d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"></path><path fill="#fbbc02" d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"></path><path fill="#ea4335" d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"></path></g></svg> 
            <span>Login with Google</span>
          </button>

          <!-- Sign In Link -->
          <p class="text-center text-gray-600 mt-2 text-base">
            Already have an account?
            <a @click.prevent="goToLogin" href="#" class="text-blue-600 hover:text-blue-800 hover:underline transition font-semibold">Sign In</a>
          </p>

        </form>

      </div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted, computed } from "vue";
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle, loginWithGithub, signup } from "@/services/auth";
import { useRouter, useRoute } from "vue-router";

export default {
  setup() {
    const auth = useAuthStore();
    const router = useRouter();
    const route = useRoute();
    
    const fullname = ref("");
    const email = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const loading = ref(false);
    const isEmailLocked = ref(false);

    // Real-time password validation
    const passwordValidation = computed(() => {
      const pwd = password.value;
      return {
        minLength: pwd.length >= 8,
        hasNumber: /\d/.test(pwd),
        hasLowercase: /[a-z]/.test(pwd),
        hasUppercase: /[A-Z]/.test(pwd),
        isValid: pwd.length >= 8 && /\d/.test(pwd) && /[a-z]/.test(pwd) && /[A-Z]/.test(pwd)
      };
    });

    onMounted(() => {
      const queryEmail = route.query.email;
      if (typeof queryEmail === "string" && queryEmail.trim()) {
        email.value = queryEmail;
        isEmailLocked.value = true;
      }
    });

    async function goToLogin() {
      router.push("/login");
    }
    
    async function handleSignup() {
      // Use the computed passwordValidation
      if (!passwordValidation.value.isValid) {
        const missingReqs = [];
        if (!passwordValidation.value.minLength) missingReqs.push("at least 8 characters");
        if (!passwordValidation.value.hasNumber) missingReqs.push("at least one number");
        if (!passwordValidation.value.hasLowercase) missingReqs.push("at least one lowercase letter");
        if (!passwordValidation.value.hasUppercase) missingReqs.push("at least one uppercase letter");
        
        alert(`Password must contain:\n- ${missingReqs.join("\n- ")}`);
        return;
      }

      if (password.value !== confirmPassword.value) {
        alert("Passwords do not match");
        return;
      }

      try {
        loading.value = true;

        await signup({
          full_name: fullname.value,
          email: email.value,
          password: password.value,
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        });

        alert("Account created successfully!");
        router.push("/login");

      } catch (error) {
        console.error("Signup error:", error);
        const detail =
          typeof error?.response?.data?.detail === "string"
            ? error.response.data.detail
            : error?.message || "Signup failed";
        alert(detail);
      } finally {
        loading.value = false;
      }
    }




    return {
      auth,
      fullname,
      email,
      isEmailLocked,
      password,
      confirmPassword,
      loading,
      passwordValidation,
      goToLogin,
      handleSignup,
      loginWithGoogle,
      loginWithGithub,
    };
  },
};
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