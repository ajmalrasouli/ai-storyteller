export interface Story {
    id: number;
    title: string;
    content: string;
    theme: string;
    characters: string[];
    age_group: string;
    is_favorite: boolean;
    image_url: string | null;
    created_at: string;
    user_id: number;
}

export interface User {
    id: number;
    email: string;
}

export interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
}

export interface StoryFormData {
    title: string;
    theme: string;
    characters: string[];
    age_group: string;
}

export interface AuthFormData {
    email: string;
    password: string;
} 