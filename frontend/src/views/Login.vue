<template>
  <div class="container animate-fade-in">
    <div class="card">

      <!-- ถ้ายังไม่ login -->
      <div v-if="!auth.user" class="right">
        <h2>Welcome back!</h2>
        <p class="subtitle">Please enter your details to manage your sessions</p>

        <form @submit.prevent="handleLogin">
          <input
            type="email"
            placeholder="Email"
            class="w-full rounded-full border border-gray-300 px-5 py-3 
            focus:outline-none focus:ring-2 focus:ring-emerald-500 
            focus:border-emerald-500 transition duration-300"
          />

          <input
            type="password"
            placeholder="Password"
            class="w-full rounded-full border border-gray-300 px-5 py-3 
            focus:outline-none focus:ring-2 focus:ring-emerald-500 
            focus:border-emerald-500 transition duration-300"
            v-model="password"
            required
          />

          <div class="options">
            <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" class="checkbox checkbox-success" v-model="remember" />
              Remember me
            </label>
            <a href="#">Forgot password?</a>
          </div>

          <button
            class="login-btn w-full py-3 rounded-full bg-gradient-to-r 
            from-emerald-600 to-teal-600 text-white font-semibold 
            shadow-lg hover:shadow-xl hover:scale-[1.02] 
            active:scale-95 transition duration-300"
          >
            Log in
          </button>

          <div class="divider">OR</div>

         <!-- GitHub --> 
          <button type="button" @click="githubLogin" class="googlegithub-btn btn bg-black text-white border-black" > 
            <svg aria-label="GitHub logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="black" d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z"></path></svg>
             Login with GitHub 
          </button> 
          <!-- Google --> 
          <button type="button" @click="googleLogin" class="googlegithub-btn btn bg-white text-black border-[#e5e5e5]" > 
            <svg aria-label="Google logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><g><path d="m0 0H512V512H0" fill="#fff"></path><path fill="#34a853" d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"></path><path fill="#4285f4" d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"></path><path fill="#fbbc02" d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"></path><path fill="#ea4335" d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"></path></g></svg> 
            Login with Google 
          </button>

        </form>

        <p class="signup">
          Don’t have an account?
          <a href="#">Sign up</a>
        </p>
      </div>

      <!-- ถ้า login แล้ว -->
      <div v-else class="right">
        <h3>Welcome, {{ auth.user.name }}</h3>
        <p>Email: {{ auth.user.email }}</p>
        <button class="login-btn" @click="auth.logout">
          Logout
        </button>
      </div>

    </div>
  </div>
</template>


<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffffff;
}


/* Card อยู่ด้านหน้า */
.card {
  width: 600px;
  padding: 40px;
  border-radius: 20px;
  background: #ffffff;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.08),
    0 2px 6px rgba(0,0,0,0.04);
  backdrop-filter: blur(10px);
}



.left {
  flex: 1;
  background: #fafafa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.shapes {
  position: relative;
  width: 200px;
  height: 200px;
}

.shape {
  position: absolute;
  border-radius: 20px;
}

.orange {
  width: 140px;
  height: 100px;
  background: orange;
  bottom: 0;
  left: 0;
  border-radius: 100px 100px 0 0;
}

.purple {
  width: 100px;
  height: 160px;
  background: purple;
  top: 0;
  left: 60px;
}

.black {
  width: 80px;
  height: 140px;
  background: #222;
  bottom: 0;
  left: 120px;
}

.yellow {
  width: 60px;
  height: 120px;
  background: gold;
  bottom: 0;
  left: 170px;
  border-radius: 50px;
}

.right {
  flex: 1;
  padding: 50px;
}

h2 {
  margin-bottom: 5px;
}

.subtitle {
  color: #777;
  margin-bottom: 30px;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border-radius: 20px;
  border: 1px solid #ddd;
}


.options {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #2C8160;
  color: white;
  border: none;
  border-radius: 6px;
  margin-bottom: 10px;
  border-radius: 20px;
  cursor: pointer;
}

.googlegithub-btn {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
}

.signup {
  margin-top: 20px;
  font-size: 14px;
  text-align: center;
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}

</style>


<script>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle, loginWithGithub } from "@/services/auth";

import AuthLayout from "@/components/AuthLayout.vue";
import Logo from "@/components/Logo.vue";

export default {
  components: { AuthLayout, Logo },

  setup() {
    const auth = useAuthStore();

    const email = ref("");
    const password = ref("");
    const remember = ref(false);

    function saveTokenFromUrl() {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get("token");

      if (token) {
        auth.login(token);
        window.history.replaceState({}, document.title, "/");
      }
    }

    function handleLogin() {
      // ตัวอย่าง login ปกติ
      auth.loginWithEmail(email.value, password.value);
    }

    onMounted(() => {
      saveTokenFromUrl();
    });

    return {
      auth,
      email,
      password,
      remember,
      handleLogin,
      googleLogin: loginWithGoogle,
      githubLogin: loginWithGithub,
    };
  },
};
</script>
