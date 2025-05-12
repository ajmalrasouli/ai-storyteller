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
            console.log('Attempting to play audio for story:', story.id);
            
            if (story.audioUrl) {
                console.log('Using story.audioUrl:', story.audioUrl);
                // Add cache buster to avoid caching issues
                const audioUrlWithCacheBuster = `${story.audioUrl}${story.audioUrl.includes('?') ? '&' : '?'}cacheBuster=${Date.now()}`;
                setAudioUrl(audioUrlWithCacheBuster);
                setIsPlaying(true);
            } else {
                console.log('No audioUrl found, generating speech...');
                try {
                    // API now returns the URL string directly
                    const audioUrlFromApi = await speechApi.textToSpeech(story.content);
                    console.log('Received audio URL from API:', audioUrlFromApi);
                    
                    // The API now directly returns the URL string
                    if (typeof audioUrlFromApi === 'string') {
                        setAudioUrl(audioUrlFromApi);
                    } else {
                        console.error('Expected string URL but got:', typeof audioUrlFromApi);
                        throw new Error('Unexpected response format');
                    }
                } catch (err) {
                    console.error('Error generating speech:', err);
                    throw err;
                }
                setIsPlaying(true);
            }
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
            {story.imageUrl && (
                <img
                    src={story.imageUrl}
                    alt={story.title}
                    className="w-full h-48 object-cover"
                />
            )}
            <div className="p-4">
                <div className="flex justify-between items-start">
                    <h3 className="text-lg font-semibold">{story.title}</h3>
                    <button
                        onClick={() => onToggleFavorite(story.id)}
                        className={`text-2xl ${story.isFavorite ? 'text-yellow-500' : 'text-gray-300'}`}
                    >
                        ★
                    </button>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                    Theme: {story.theme} | Age: {story.ageGroup}
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
                    controls
                    onPlay={() => console.log('Audio started playing')}
                    onError={(e) => console.error('Audio error:', e)}
                    onEnded={() => {
                        console.log('Audio playback ended');
                        setIsPlaying(false);
                    }}
                />
            )}
        </div>
    );
}; 