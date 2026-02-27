import axios from "axios";
import VueCookies from "vue-cookies";
import { jwtDecode } from "jwt-decode";

const API_URL =
  import.meta.env.VITE_API_BASE_URL;

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && ["POST", "PUT", "DELETE"].includes(config.method.toUpperCase())) {
      const decoded = jwtDecode(token);
      config.headers["X-CSRF-Token"] = decoded.csrf_token; // Decode JWT for CSRF
    }
    // No Authorization header needed since JWT is in cookie
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export async function getUser() {
  const res = await axios.get(`${API_URL}/auth/me`);
  return res.data;
}
const api = axios.create({
  baseURL: "http://localhost:56733",
  withCredentials: true, // สำคัญมาก (cookie / session)
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  }
});

// login
export const login = (email, password) => {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  return api.post("/auth/token", formData);
};

// get current user
export const getMe = () => {
  return api.get("/auth/me");
};
// Login with Google OAuth
export async function loginWithGoogle() {
  window.location.href = `${API_URL}/auth/google/login`;
}
// Login with Github OAuth
export function loginWithGithub() {
  window.location.href = `${API_URL}/auth/github/login`;
}

// JWT Handling - Store & Retrieve Token in Cookies
export function getToken() {
  return VueCookies.get("jwt");
}

export function saveToken(token) {
  VueCookies.set("jwt", token, "1d", "/", "", false, "Lax"); // Non-HttpOnly cookie
}

export function removeToken() {
  VueCookies.remove("jwt");
}

// Logout & Clear JWT
export function logout() {
  window.location.reload(); // Optional
}
