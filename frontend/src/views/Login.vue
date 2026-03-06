<template>
  <div
    class="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-indigo-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Decorative background elements -->
    <div
      class="absolute top-0 left-0 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob">
    </div>
    <div
      class="absolute top-0 right-0 w-72 h-72 bg-cyan-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000">
    </div>
    <div
      class="absolute bottom-0 left-1/2 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000">
    </div>

    <div class="w-full max-w-md relative">
      <!-- Main Card -->
      <div
        class="bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 md:p-10 transform transition-all duration-500 hover:shadow-3xl">

        <!-- Header with icon -->
        <div class="flex justify-center mb-6">
          <div
            class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center shadow-lg">
            <svg id="Layer_1" class="w-6 h-6" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" data-name="Layer 1">
              <path fill="white"
                d="m15 6c0 3.309-2.691 6-6 6s-6-2.691-6-6 2.691-6 6-6 6 2.691 6 6zm2 16h-1c-.552 0-1-.449-1-1v-6c0-.551.448-1 1-1h1c.553 0 1-.448 1-1s-.447-1-1-1h-1c-1.654 0-3 1.346-3 3v6c0 1.654 1.346 3 3 3h1c.553 0 1-.448 1-1s-.447-1-1-1zm6.404-5.245-2.207-1.946c-.411-.363-1.046-.326-1.411.089-.365.414-.325 1.046.089 1.411l.783.691h-2.658c-.553 0-1 .448-1 1s.447 1 1 1h2.792l-.917.809c-.414.365-.454.997-.089 1.411.366.416.999.453 1.411.089l2.199-1.939c.384-.331.604-.809.604-1.311s-.22-.98-.596-1.304zm-12.404-1.755c0-.256.038-.503.076-.749-.668-.158-1.36-.251-2.076-.251-4.963 0-9 4.038-9 9 0 .552.447 1 1 1h11.026c-.635-.838-1.026-1.87-1.026-3z" />
            </svg>
          </div>
        </div>

        <h2
          class="text-center text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent mb-3">
          Welcome back!
        </h2>
        <p class="text-center text-gray-600 text-sm mb-8 leading-relaxed">
          Please enter your details to manage your sessions
        </p>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Email Input with Icon -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                </path>
              </svg>
            </div>
            <input type="email" v-model="email" placeholder="hello@example.com"
              class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-4 focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
              required />
          </div>

          <!-- Password Input with Icon -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
                </path>
              </svg>
            </div>
            <input v-model="password" type="password" placeholder="••••••••"
              class="w-full border-2 border-gray-200 rounded-xl pl-12 pr-4 py-4 focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300 text-gray-700 placeholder-gray-400"
              required minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
              title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
          </div>

          <p v-if="errorMessage" class="text-error text-sm">
            {{ errorMessage }}
          </p>

          <!-- <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" class="checkbox checkbox-success" v-model="remember" />
              Remember me
            </label> -->
          <div class="text-right">
            <router-link to="/forgot-password"
              class="text-blue-600 hover:text-blue-800 hover:underline transition">Forgot password?</router-link>
          </div>

          <button
            class="btn btn-active btn-primary w-full transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95">
            Log in
          </button>

          <div class="divider">OR</div>

          <!-- GitHub -->
          <button type="button" @click="loginWithGithub"
            class="w-full px-5 py-4 shadow-lg btn bg-black text-white border-black transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95">
            <svg aria-label="GitHub logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path fill="white"
                d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z">
              </path>
            </svg>
            Login with GitHub
          </button>
          <!-- Google -->
          <button type="button" @click="loginWithGoogle"
            class="w-full px-5 py-4 shadow-lg btn bg-white text-black border-[#e5e5e5] transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95">
            <svg aria-label="Google logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512">
              <g>
                <path d="m0 0H512V512H0" fill="#fff"></path>
                <path fill="#34a853" d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"></path>
                <path fill="#4285f4" d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"></path>
                <path fill="#fbbc02" d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"></path>
                <path fill="#ea4335" d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"></path>
              </g>
            </svg>
            Login with Google
          </button>

        </form>

        <p class="w-full py-3 flex text-center justify-center">
          Don’t have an account?
          <router-link to="/signup" class="px-2 text-blue-600 hover:text-blue-800 hover:underline transition">Sign
            up</router-link>
        </p>
      </div>

    </div>

  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle, loginWithGithub, setCsrfToken } from "@/services/auth";
import { useRouter } from 'vue-router'
export default {

  setup() {
    const auth = useAuthStore();
    const email = ref("");
    const password = ref("");
    const router = useRouter();
    const loading = ref(false);
    const errorMessage = ref("");

    function saveTokenFromUrl() {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get("token");

      if (token) {
        auth.login(token);
        window.history.replaceState({}, document.title, "/events");
      }
    }

    async function handleLogin() {
      try {
        loading.value = true;
        errorMessage.value = "";

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
          const payload = await response.json().catch(() => null);
          const detail = typeof payload?.detail === "string"
            ? payload.detail
            : Array.isArray(payload?.detail)
              ? payload.detail.map((item) => item?.msg).filter(Boolean).join(", ")
              : "";

          if (response.status === 401) {
            throw new Error(detail || "Invalid email or password.");
          }
          if (response.status === 422) {
            throw new Error(detail || "Please check your email and password format.");
          }

          throw new Error(detail || "Unable to log in right now. Please try again.");
        }

        const loginPayload = await response.json().catch(() => null);
        setCsrfToken(loginPayload?.csrf_token);

        // หลัง login สำเร็จ → ดึง user
        const me = await fetch("http://localhost:56733/auth/me", {
          credentials: "include"
        });

        const userData = await me.json();
        auth.user = userData;

        router.replace("/dashboard");

      } catch (error) {
        errorMessage.value = error?.message || "Unable to log in right now. Please try again.";
      } finally {
        loading.value = false;
      }
    }



    onMounted(() => {
      saveTokenFromUrl();
    });

    return {
      auth,
      email,
      password,
      errorMessage,
      loading,
      handleLogin,
      loginWithGoogle,
      loginWithGithub,
    };
  },
};
</script>
