import axios from "axios";
import { getCsrfToken } from "./auth";

const API_URL =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:56733";

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
    (config) => {
        const method = (config.method || "GET").toUpperCase();
        if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
            config.headers["X-CSRF-Token"] = getCsrfToken();
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