<template>
  <div class="flex flex-col md:flex-row min-h-screen">

    <div class="hidden md:flex flex-1 justify-center items-center relative h-screen overflow-hidden">
      <video autoplay loop muted playsinline class="w-full h-full object-cover">
        <source src="@/assets/boy_working.mp4" type="video/mp4" />
      </video>
    </div>

    <div class="flex-1 flex justify-center items-center p-6 md:p-14">

        <form class="space-y-4 w-full max-w-md">
          <h2 class="flex text-3xl font-semibold tracking-tight">Create Account. It's free!!</h2>
          <p class="flex text-gray-600 leading-relaxed">Let's join our Noona. Get set up in under a minute.</p>
          <div class="px-1 py-2">
            <p class="block text-left font-semibold py-2">
              Full Name
            </p>
            <input
              type = "text"
              v-model="fullname"
              placeholder="Janny Games"
              class="w-full input"
            />
          </div>

          <div>
            <p class="block text-left font-semibold py-2">
              Email address
            </p>
            <input
              type="email"
              v-model="email"
              placeholder="Janny_games@example.com"
              class="w-full input validator"
              required 
            />
            </div>
          <div class="validator-hint hidden">Enter valid email address</div>

          <div>
            <p class="block text-left font-semibold py-2">
              Password
            </p>
            <input v-model="password" type="password" class="w-full input validator" required minlength="8" 
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
            <p class="validator-hint hidden">
              Must be more than 8 characters, including
              <br/>At least one number
              <br/>At least one lowercase letter
              <br/>At least one uppercase letter
            </p>
          </div>

          <div>
            <p class="block text-left font-semibold py-2">
              Confirmed Password
            </p>
            <input v-model = "confirmPassword" type="password" class="w-full input validator" required minlength="8" 
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
            <p class="validator-hint hidden">
              Must be more than 8 characters, including
              <br/>At least one number
              <br/>At least one lowercase letter
              <br/>At least one uppercase letter
            </p>
          </div>

          <button
            @click.prevent="handleSignup"
            class="btn btn-active btn-primary w-full transition duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95"
          >
            Create Account
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

          <p class="w-full py-3 flex text-center justify-center">
            Already have an account?
            <a @click.prevent="goToLogin" href="..." class="flex text-center justify-center px-2 text-blue-600 hover:text-blue-800 hover:underline transition">Sign In</a>
          </p>

        </form>

      </div>

    </div>
</template>


<script>
import { ref } from "vue";
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle, loginWithGithub } from "@/services/auth";
import { useRouter } from "vue-router";

export default {
  setup() {
    const auth = useAuthStore();
    const router = useRouter();
    
    const fullname = ref("");
    const email = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const loading = ref(false);

    async function goToLogin() {
      router.push("/login");
    }
    async function loginWithGithub() {
      window.location.href = "http://localhost:56733/auth/github/login";
    }
    async function loginWithGoogle() {
      window.location.href = "http://localhost:56733/auth/google/login";
    }
    async function handleSignup() {
      if (password.value !== confirmPassword.value) {
        alert("Passwords do not match");
        return;
      }

      try {
        loading.value = true;

        const signupRes = await fetch("http://localhost:56733/auth/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            full_name: fullname.value,
            email: email.value,
            password: password.value,

          })
        });

        const signupData = await signupRes.json();
      
        if (!signupRes.ok) {
          throw new Error(signupData.detail || "Signup failed");
        }
        alert("Account created successfully!");
        router.push("/login");

      } catch (error) {
        console.error("Signup error:", error);
        alert(error.message);
      } finally {
        loading.value = false;
      }
    }




    return {
      auth,
      fullname,
      email,
      password,
      confirmPassword,
      loading,
      goToLogin,
      handleSignup,
      loginWithGoogle,
      loginWithGithub,
    };
  },
};
</script>