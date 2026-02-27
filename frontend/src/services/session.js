import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL;

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

export async function registerForSession(sessionUuid) {
  const res = await axios.post(`${API_URL}/sessions/${sessionUuid}/registration`, {});
  return res.data;
}

export async function confirmSession(sessionUuid) {
  const res = await axios.post(`${API_URL}/sessions/${sessionUuid}/confirm`, {});
  return res.data;
}
