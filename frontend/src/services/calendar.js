import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL;

export async function getCalendar(start_datetime, end_datetime, scope = "all") {
    const params = { start_datetime, end_datetime, scope }
    const res = await axios.get(`${API_URL}/calendar`, { params });
    return res.data;
}