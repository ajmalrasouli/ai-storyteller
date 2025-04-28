import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

export const SignOutButton: React.FC = () => {
    const { logout } = useAuth();

    return (
        <button
            onClick={logout}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
            Sign Out
        </button>
    );
}; 