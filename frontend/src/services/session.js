import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL;

/**
 * params: { scope, start_datetime, end_datetime, cursor, size, registration_status_list }
 * registration_status_list should be an array of strings matching backend enum values:
 * e.g. ['waitlist','available'] or ['confirmed']
 */
export async function getUserSessions(params = {}, token = '') {
  const res = await axios.get(`${API_URL}/sessions/`, {
    params,
    headers: { Authorization: `Bearer ${token}` },
    timeout: 7000,
  });
  return res.data;
}
