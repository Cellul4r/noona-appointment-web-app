import axios from "axios";
import VueCookies from "vue-cookies";

const API_URL =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:56733";

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
    (config) => {
        const method = (config.method || "GET").toUpperCase();
        if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
            const csrfToken = VueCookies.get("fastapi-csrf-token");
            config.headers["X-CSRF-Token"] = csrfToken; // Decode JWT for CSRF
        }
        // No Authorization header needed since JWT is in cookie
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Fetch User Settings
export async function fetchUserSettings() {
    const response = await axios.get(`${API_URL}/users/settings`, { withCredentials: true });
    return response.data;
}

export async function updateUserProfile(payload) {
    const response = await axios.patch(`${API_URL}/users/me`, payload, { withCredentials: true });
    return response.data;
}

export async function verifyUserPassword(password) {
    const response = await axios.post(
        `${API_URL}/users/verify-password`,
        { password },
        { withCredentials: true }
    );
    return response.data;
}

export async function unlinkOAuthAccount(provider) {
    const response = await axios.delete(`${API_URL}/users/unlink-accounts/${provider}`, {
        withCredentials: true,
    });
    return response.data;
}

export function getLinkAccountUrl(provider) {
    return `${API_URL}/users/link-accounts/${provider}`;
}
