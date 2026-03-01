import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL;

// Fetch Event Details
export async function getEvent(uuid) {
    const res = await axios.get(`${API_URL}/events/${uuid}`);
    return res.data;
}

export async function getSessions(eventUuid, cursor = null, size = 6, upcoming_only = false) {
    const params = { size, upcoming_only }
    if (cursor) params.cursor = cursor

    const res = await axios.get(`${API_URL}/events/${eventUuid}/sessions`, { params });
    return res.data;
}

export async function getAllEvents({ scope = 'all', size = 12, cursor = null, title = null } = {}) {
    // params object mirrors what the front-end used previously in AllEvents.vue
    const params = { scope, size };
    if (title) params.title = title;
    if (cursor) params.cursor = cursor;

    const res = await axios.get(`${API_URL}/events/`, {
        params,
        timeout: 5000
    });
    return res.data;
}

export async function getEventOverview(uuid) {
    const res = await axios.get(`${API_URL}/events/overview/${uuid}`);
    return res.data;
}

export async function createEvent(payload) {
    const res = await axios.post(`${API_URL}/events`, payload);
    return res.data;
}

export async function deleteEvent(uuid) {
    await axios.delete(`${API_URL}/events/${uuid}`);
}