<template>
  <div class="flex flex-col md:flex-row min-h-screen">

    <div class="hidden md:flex flex-1 justify-center items-center relative h-screen overflow-hidden">
      <video autoplay loop muted playsinline class="w-full h-full object-cover">
        <source src="@/assets/boy_working.mp4" type="video/mp4" />
      </video>
      <!-- <script type="module" src="https://unpkg.com/@splinetool/viewer@1.12.61/build/spline-viewer.js"></script>-->
      <!-- <spline-viewer url="https://prod.spline.design/DnINat72jP3GNnBE/scene.splinecode"></spline-viewer> -->
    </div>

    <div class="flex-1 flex justify-center items-center p-6 md:p-14">
      <!-- ถ้ายังไม่ login -->
      <div>
        <form @submit.prevent="handleLogin" class="space-y-4 w-full max-w-md">
          <h2 class="flex text-3xl font-semibold tracking-tight">Welcome back!</h2>
          <p class="flex text-gray-600 leading-relaxed">Please enter your details to manage your sessions</p>
          
          <input
            type="email"
            v-model="email"
            placeholder="Email"
            class="w-full input validator"
            required 
          />
          <div class="validator-hint hidden">Enter valid email address</div>

          <input v-model="password" type="password" class="w-full input validator" required placeholder="Password" minlength="8" 
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
          <p class="validator-hint hidden">
            Must be more than 8 characters, including
            <br/>At least one number
            <br/>At least one lowercase letter
            <br/>At least one uppercase letter
          </p>

            <!-- <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" class="checkbox checkbox-success" v-model="remember" />
              Remember me
            </label> -->
          <div class="text-right">
            <a href="..." class="text-blue-600 hover:text-blue-800 hover:underline transition">Forgot password?</a>
          </div>

          <button
            class="btn btn-active btn-primary w-full transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95"
          >
            Log in
          </button>

          <div class="divider">OR</div>

          <!-- GitHub --> 
          <button type="button" @click="loginWithGithub" class="w-full px-5 py-4 shadow-lg btn bg-black text-white border-black transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95" > 
            <svg aria-label="GitHub logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="white" d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z"></path></svg>
             Login with GitHub 
          </button> 
          <!-- Google --> 
          <button type="button" @click="loginWithGoogle" class="w-full px-5 py-4 shadow-lg btn bg-white text-black border-[#e5e5e5] transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95" > 
            <svg aria-label="Google logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><g><path d="m0 0H512V512H0" fill="#fff"></path><path fill="#34a853" d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"></path><path fill="#4285f4" d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"></path><path fill="#fbbc02" d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"></path><path fill="#ea4335" d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"></path></g></svg> 
            Login with Google 
          </button>

        </form>

        <p class="w-full py-3 flex text-center justify-center">
          Don’t have an account?
          <a @click.prevent="goToSignup" href="..." class="px-2 text-blue-600 hover:text-blue-800 hover:underline transition">Sign up</a>
        </p>
      </div>

    </div>

  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle, loginWithGithub } from "@/services/auth";
import { useRouter } from 'vue-router'
export default {

  setup() {
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
        alert("Don'i have an account, login first.");
        router.push("/signup");
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
      loading,
      handleLogin,
      goToSignup,
      loginWithGoogle,
      loginWithGithub,
    };
  },
};
</script>


