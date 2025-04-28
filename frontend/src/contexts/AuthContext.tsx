import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthState, User } from '../types';
import { authApi } from '../services/api';

interface AuthContextType extends AuthState {
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [state, setState] = useState<AuthState>({
        user: null,
        token: localStorage.getItem('token'),
        isAuthenticated: false,
    });

    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const data = await authApi.verifyToken(token);
                    setState({
                        user: data.user,
                        token,
                        isAuthenticated: true,
                    });
                } catch (error) {
                    localStorage.removeItem('token');
                    setState({
                        user: null,
                        token: null,
                        isAuthenticated: false,
                    });
                }
            }
        };

        verifyToken();
    }, []);

    const login = async (email: string, password: string) => {
        const data = await authApi.login(email, password);
        localStorage.setItem('token', data.token);
        setState({
            user: data.user,
            token: data.token,
            isAuthenticated: true,
        });
    };

    const register = async (email: string, password: string) => {
        await authApi.register(email, password);
        await login(email, password);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setState({
            user: null,
            token: null,
            isAuthenticated: false,
        });
    };

    return (
        <AuthContext.Provider value={{ ...state, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}; 