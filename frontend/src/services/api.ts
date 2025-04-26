import axios from 'axios';
import { Story, StoryFormData } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

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
    getAll: async () => {
        const response = await api.get('/stories');
        return response.data;
    },

    create: async (data: StoryFormData) => {
        const response = await api.post('/stories', data);
        return response.data;
    },

    delete: async (id: number) => {
        await api.delete(`/stories/${id}`);
    },

    toggleFavorite: async (id: number) => {
        const response = await api.post(`/stories/${id}/favorite`);
        return response.data;
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