import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL;

// Fetch Event Details
export async function getEvent(uuid) {
    const res = await axios.get(`${API_URL}/events/${uuid}`);
    return res.data;
}

export async function getSessions(eventUuid, cursor = null, size = 6) {
    const params = { size }
    if (cursor) params.cursor = cursor

    const res = await axios.get(`${API_URL}/events/${eventUuid}/sessions`, { params });
    return res.data;
}