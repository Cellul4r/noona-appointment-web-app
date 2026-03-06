import axios from 'axios';
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

export async function getUserSessions(params = {}) {
  const res = await axios.get(`${API_URL}/sessions/`, {
    params,
    timeout: 7000,
    // Add this custom serializer to strip out the [] from arrays
    paramsSerializer: (paramsObj) => {
      const searchParams = new URLSearchParams();

      Object.keys(paramsObj).forEach(key => {
        const value = paramsObj[key];
        if (Array.isArray(value)) {
          // Append the key multiple times for arrays (e.g., key=val1&key=val2)
          value.forEach(val => searchParams.append(key, val));
        } else if (value !== undefined && value !== null) {
          // Append standard key-value pairs
          searchParams.append(key, value);
        }
      });

      return searchParams.toString();
    }
  });

  return res.data;
}

export async function registerForSession(sessionUuid, reminder = []) {
  const res = await axios.post(`${API_URL}/sessions/${sessionUuid}/registration`, reminder);
  return res.data;
}

export async function confirmSession(sessionUuid, reminder = []) {
  const res = await axios.post(`${API_URL}/sessions/${sessionUuid}/confirm`, reminder);
  return res.data;
}

export async function unregisterUserByHost(sessionUuid, userId) {
  const res = await axios.delete(`${API_URL}/sessions/${sessionUuid}/registrations/${userId}`);
  return res;
}

export async function getRegisteredUsers(sessionUuid, status = "confirmed", cursor = null, size = 10) {
  const params = { status, size }
  if (cursor) params.cursor = cursor

  const res = await axios.get(`${API_URL}/sessions/${sessionUuid}/users`, { params });
  return res.data;
}

export async function getSessionByUuid(sessionUuid) {
  const res = await axios.get(`${API_URL}/sessions/${sessionUuid}`);
  return res.data;
}

export async function cancelSession(sessionUuid) {
  const res = await axios.delete(
    `${API_URL}/sessions/${sessionUuid}/registration`
  );
  return res.data;
}


