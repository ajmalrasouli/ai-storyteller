import axios from 'axios';
import { Story, StoryFormData } from '../types';

const API_URL = 'https://storyteller-backend.proudhill-96526a5c.westeurope.azurecontainerapps.io/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const storyApi = {
    getAll: async (userId?: number) => {
        const url = userId ? `/stories?user_id=${userId}` : '/stories';
        const response = await api.get(url);
        return response.data;
    },

    create: async (data: StoryFormData) => {
        const response = await api.post('/stories', data);
        return response.data;
    },

    delete: async (id: number): Promise<void> => {
        const response = await api.delete(`/stories/${id}`);
        if (response.status !== 204) {
            throw new Error('Error deleting story');
        }
    },

    toggleFavorite: async (id: number): Promise<{ isFavorite: boolean }> => {
        const response = await api.post(`/stories/${id}/favorite`);
        return { isFavorite: response.data.isFavorite };
    },

    regenerateIllustration: async (id: number) => {
        const response = await api.post(`/stories/${id}/regenerate-illustration`);
        return response.data;
    },
};

export const authApi = {
    login: async (email: string, password: string) => {
        const response = await api.post('/login', { email, password });
        return response.data;
    },

    register: async (email: string, password: string) => {
        const response = await api.post('/register', { email, password });
        return response.data;
    },

    verifyToken: async (token: string) => {
        const response = await api.post('/verify-token', { token });
        return response.data;
    },
};

export const speechApi = {
    textToSpeech: async (text: string) => {
        const response = await api.post('/speech', { text }, {
            responseType: 'blob',
        });
        return response.data;
    },
}; 