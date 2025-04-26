import React, { useState, useEffect } from 'react';
import { Story } from '../../types';
import { speechApi } from '../../services/api';

interface StoryCardProps {
    story: Story;
    onDelete: (id: number) => void;
    onToggleFavorite: (id: number) => void;
    onRegenerateIllustration: (id: number) => void;
}

export const StoryCard: React.FC<StoryCardProps> = ({
    story,
    onDelete,
    onToggleFavorite,
    onRegenerateIllustration,
}) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);

    const handlePlayAudio = async () => {
        if (isPlaying) {
            setIsPlaying(false);
            return;
        }

        try {
            const audioBlob = await speechApi.textToSpeech(story.content);
            const url = URL.createObjectURL(audioBlob);
            setAudioUrl(url);
            setIsPlaying(true);
        } catch (err) {
            console.error('Failed to play audio:', err);
        }
    };

    useEffect(() => {
        return () => {
            if (audioUrl) {
                URL.revokeObjectURL(audioUrl);
            }
        };
    }, [audioUrl]);

    return (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
            {story.image_url && (
                <img
                    src={story.image_url}
                    alt={story.title}
                    className="w-full h-48 object-cover"
                />
            )}
            <div className="p-4">
                <div className="flex justify-between items-start">
                    <h3 className="text-lg font-semibold">{story.title}</h3>
                    <button
                        onClick={() => onToggleFavorite(story.id)}
                        className={`text-2xl ${story.is_favorite ? 'text-yellow-500' : 'text-gray-300'}`}
                    >
                        ★
                    </button>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                    Theme: {story.theme} | Age: {story.age_group}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                    Characters: {story.characters.join(', ')}
                </p>
                <div className="mt-4">
                    <p className="text-gray-700 line-clamp-3">{story.content}</p>
                </div>
                <div className="mt-4 flex justify-between">
                    <button
                        onClick={handlePlayAudio}
                        className="text-indigo-600 hover:text-indigo-800"
                    >
                        {isPlaying ? 'Stop' : 'Play'} Audio
                    </button>
                    <div className="space-x-2">
                        <button
                            onClick={() => onRegenerateIllustration(story.id)}
                            className="text-indigo-600 hover:text-indigo-800"
                        >
                            Regenerate Image
                        </button>
                        <button
                            onClick={() => onDelete(story.id)}
                            className="text-red-600 hover:text-red-800"
                        >
                            Delete
                        </button>
                    </div>
                </div>
            </div>
            {isPlaying && audioUrl && (
                <audio
                    src={audioUrl}
                    autoPlay
                    onEnded={() => setIsPlaying(false)}
                />
            )}
        </div>
    );
}; 