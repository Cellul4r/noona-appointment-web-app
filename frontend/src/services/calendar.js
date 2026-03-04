import axios from "axios";
import VueCookies from "vue-cookies";

const API_URL = import.meta.env.VITE_API_BASE_URL;

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

export async function getCalendar(start_datetime, end_datetime, scope = "all") {
    const params = { start_datetime, end_datetime, scope }
    const res = await axios.get(`${API_URL}/calendar`, { params });
    return res.data;
}