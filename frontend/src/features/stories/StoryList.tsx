import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { storyApi } from '../../services/api';
import { Story } from '../../types';
import { StoryCard } from './StoryCard';

export const StoryList: React.FC = () => {
    const { user } = useAuth();
    const [stories, setStories] = useState<Story[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchStories = async () => {
            if (!user) return;
            
            try {
                const data = await storyApi.getAll(user.id);
                setStories(data);
            } catch (err) {
                setError('Failed to load stories');
            } finally {
                setLoading(false);
            }
        };

        fetchStories();
    }, [user]);

    const handleDelete = async (id: number) => {
        try {
            await storyApi.delete(id);
            setStories(stories.filter(story => story.id !== id));
        } catch (err) {
            setError('Failed to delete story');
        }
    };

    const handleToggleFavorite = async (id: number) => {
        try {
            const updatedStory = await storyApi.toggleFavorite(id);
            setStories(stories.map(story => 
                story.id === id ? updatedStory : story
            ));
        } catch (err) {
            setError('Failed to update story');
        }
    };

    const handleRegenerateIllustration = async (id: number) => {
        try {
            const updatedStory = await storyApi.regenerateIllustration(id);
            setStories(stories.map(story => 
                story.id === id ? updatedStory : story
            ));
        } catch (err) {
            setError('Failed to regenerate illustration');
        }
    };

    if (loading) {
        return <div className="text-center">Loading stories...</div>;
    }

    if (error) {
        return <div className="text-red-500 text-center">{error}</div>;
    }

    if (stories.length === 0) {
        return <div className="text-center">No stories yet. Create your first story!</div>;
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stories.map(story => (
                <StoryCard
                    key={story.id}
                    story={story}
                    onDelete={handleDelete}
                    onToggleFavorite={handleToggleFavorite}
                    onRegenerateIllustration={handleRegenerateIllustration}
                />
            ))}
        </div>
    );
}; 