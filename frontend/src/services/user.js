import axios from "axios";
import VueCookies from "vue-cookies";

const API_URL =
    import.meta.env.VITE_API_BASE_URL;

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
    (config) => {
        if (["POST", "PUT", "DELETE"].includes(config.method.toUpperCase())) {
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
    try {
        const response = await axios.get(`${API_URL}/users/settings`, { withCredentials: true });
        return response.data; // email, full_name, profile_image, timezone, email_notifications
    } catch (err) {
        console.error("Error fetching user settings:", err);
        return null;
    }
}