export interface Story {
    id: number;
    title: string;
    content: string;
    theme: string;
    characters: string[];
    ageGroup: string;
    isFavorite: boolean;
    imageUrl: string | null;
    createdAt: string;
    userId: number;
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