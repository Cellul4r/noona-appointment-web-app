import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL;

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