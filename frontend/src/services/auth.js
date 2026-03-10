import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:56733";
let getCsrfTokenHandler = () => null;
let setCsrfTokenHandler = () => { };
let csrfRefreshPromise = null;

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
  async (config) => {
    const method = (config.method || "GET").toUpperCase();
    if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
      const requestUrl = String(config.url || "");
      const isCsrfEndpoint = requestUrl.includes("/auth/csrf");
      const isLoginTokenEndpoint = requestUrl.includes("/auth/token");

      if (!isCsrfEndpoint && !isLoginTokenEndpoint) {
        if (!getCsrfToken()) {
          await ensureCsrfToken();
        }
        const token = getCsrfToken();
        if (token) {
          config.headers = config.headers || {};
          config.headers["X-CSRF-Token"] = token;
        }
      }
    }
    // No Authorization header needed since JWT is in cookie
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error?.response?.status;
    const config = error?.config;
    const method = (config?.method || "GET").toUpperCase();
    const requestUrl = String(config?.url || "");

    const isMutating = ["POST", "PUT", "PATCH", "DELETE"].includes(method);
    const isCsrfEndpoint = requestUrl.includes("/auth/csrf");
    const isLoginTokenEndpoint = requestUrl.includes("/auth/token");

    if (
      config &&
      !config._csrfRetried &&
      isMutating &&
      !isCsrfEndpoint &&
      !isLoginTokenEndpoint &&
      (status === 401 || status === 403)
    ) {
      config._csrfRetried = true;
      await ensureCsrfToken(true);
      const token = getCsrfToken();
      if (token) {
        config.headers = config.headers || {};
        config.headers["X-CSRF-Token"] = token;
      }
      return axios(config);
    }

    return Promise.reject(error);
  }
);

export async function getUser() {
  const res = await axios.get(`${API_URL}/auth/me`);
  return res.data;
}

export async function requestSignUp(email) {
  await ensureCsrfToken();
  const res = await axios.post(`${API_URL}/auth/request/sign-up`, null, {
    params: { email },
  });
  return res.data;
}

export async function signup(payload) {
  await ensureCsrfToken();
  const res = await axios.post(`${API_URL}/auth/signup`, payload);
  return res.data;
}

export async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await axios.post(`${API_URL}/auth/token`, formData.toString(), {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  return res.data;
}

export function getCsrfToken() {
  return getCsrfTokenHandler() || null;
}

export function setCsrfToken(token) {
  setCsrfTokenHandler(token || null);
}

export function registerCsrfTokenHandlers({ getToken, setToken }) {
  if (typeof getToken === "function") {
    getCsrfTokenHandler = getToken;
  }
  if (typeof setToken === "function") {
    setCsrfTokenHandler = setToken;
  }
}

export async function refreshCsrfToken() {
  if (!csrfRefreshPromise) {
    csrfRefreshPromise = (async () => {
      const res = await axios.get(`${API_URL}/auth/csrf`);
      setCsrfToken(res.data?.csrf_token);
      return getCsrfToken();
    })();
  }

  try {
    return await csrfRefreshPromise;
  } finally {
    csrfRefreshPromise = null;
  }
}

export async function ensureCsrfToken(forceRefresh = false) {
  const token = getCsrfToken();
  if (token && !forceRefresh) {
    return token;
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

// Verify Email with Token
export async function verifyEmail(token) {
  await ensureCsrfToken();
  const res = await axios.post(`${API_URL}/auth/verify-email`, null, {
    params: { token },
  });
  return res.data;
}

export async function forgotPassword(email) {
  await ensureCsrfToken();
  const res = await axios.post(`${API_URL}/auth/request/password-reset`, null, {
    params: { email },
  });
  return res.data;
}

export async function createNewPassword(token) {
  await ensureCsrfToken();
  const res = await axios.post(`${API_URL}/auth/verify-password-reset-token`, null, {
    params: { token },
  });
  return res.data;
}

export async function resetPassword(new_password) {
  await ensureCsrfToken();
  const res = await axios.post(`${API_URL}/auth/reset-password`, null, {
    params: { new_password },
  });
  return res.data;
}
// Logout & Clear JWT
export async function logout() {
  await ensureCsrfToken();
  try {
    await axios.post(`${API_URL}/auth/logout`, null);
  } catch (error) {
    const status = error?.response?.status;
    if (status === 401 || status === 403) {
      await ensureCsrfToken(true);
      await axios.post(`${API_URL}/auth/logout`, null);
      return;
    }
    throw error;
  }
}
