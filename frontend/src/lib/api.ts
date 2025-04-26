const API_URL = "http://localhost:5000";

export interface User {
  id: number;
  email: string;
}

export interface Story {
  id: number;
  title: string;
  content: string;
  theme: string;
  characters: string[];
  ageGroup: string;
  isFavorite: boolean;
  imageUrl?: string;
  createdAt: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface ErrorResponse {
  message: string;
}

export interface ShareData {
  shareUrl: string;
  shareData: {
    title: string;
    theme: string;
    characters: string[];
    ageGroup: string;
    imageUrl?: string;
    preview: string;
  };
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  try {
    const response = await fetch(`${API_URL}${url}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "An error occurred");
    }

    return response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  return fetchWithAuth("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function register(email: string, password: string): Promise<void> {
  return fetchWithAuth("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getCurrentUser(token: string): Promise<User> {
  if (!token) {
    throw new Error("Authentication token is required");
  }
  return fetchWithAuth("/auth/me", { method: "GET" });
}

export async function generateStory(
  theme: string,
  characters: string[],
  ageGroup: string
): Promise<Story> {
  return fetchWithAuth("/stories", {
    method: "POST",
    body: JSON.stringify({ theme, characters, ageGroup }),
  });
}

export async function listStories(): Promise<Story[]> {
  return fetchWithAuth("/stories", { method: "GET" });
}

export async function toggleFavorite(storyId: number): Promise<Story> {
  return fetchWithAuth(`/stories/${storyId}/favorite`, { method: "POST" });
}

export async function regenerateIllustration(storyId: number): Promise<{ id: number, imageUrl: string }> {
  return fetchWithAuth(`/stories/${storyId}/regenerate-illustration`, { method: "POST" });
}

export async function deleteStory(storyId: number): Promise<void> {
  return fetchWithAuth(`/stories/${storyId}`, { method: "DELETE" });
}

export async function getShareLink(storyId: number): Promise<ShareData> {
  return fetchWithAuth(`/stories/${storyId}/share`, {
    method: "GET",
  });
} 