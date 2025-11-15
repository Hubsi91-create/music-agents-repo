import axios from 'axios';

const apiClient = axios.create({
    // Liest die URL dynamisch aus den Umgebungsvariablen
    // VITE_API_BASE_URL ist in .env.development auf http://localhost:5000/api/storyboard gesetzt
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Globales Error Handling (Interceptor)
apiClient.interceptors.response.use(
    response => response,
    error => {
        console.error('API Error:', error.response || error.message);
        // Hier könnte man auch eine UI-Benachrichtigung (Toast) auslösen
        return Promise.reject(error);
    }
);

export default apiClient;
