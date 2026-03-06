import axios from "axios";
import VueCookies from "vue-cookies";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:56733";
let csrfToken = null;

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
  (config) => {
    const method = (config.method || "GET").toUpperCase();
    if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
      config.headers["X-CSRF-Token"] = csrfToken;
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

export async function requestSignUp(email) {
  const res = await axios.post(`${API_URL}/auth/request/sign-up`, null, {
    params: { email },
  });
  return res.data;
}

export function getCsrfToken() {
  return csrfToken;
}

export function setCsrfToken(token) {
  csrfToken = token || null;
}

export async function refreshCsrfToken() {
  const res = await axios.get(`${API_URL}/auth/csrf`);
  setCsrfToken(res.data?.csrf_token);
  return csrfToken;
}

export async function ensureCsrfToken() {
  if (csrfToken) {
    return csrfToken;
  }
  return refreshCsrfToken();
}

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

// Verify Email with Token
export async function verifyEmail(token) {
  const res = await axios.post(`${API_URL}/auth/verify-email`, null, {
    params: { token },
  });
  return res.data;
}

// Logout & Clear JWT
export async function logout() {
  setCsrfToken(null);
  await axios.post(`${API_URL}/auth/logout`, null);
}
