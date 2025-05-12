import React, { useState } from 'react';
import { Story } from '../../types';
import { speechApi } from '../../services/api';
import { SimpleAudioPlayer } from '../../components/SimpleAudioPlayer';

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
    // State to track if we're generating audio
    const [isGenerating, setIsGenerating] = useState(false);
    // State to store dynamically generated audio URL
    const [generatedAudioUrl, setGeneratedAudioUrl] = useState<string | null>(null);
    
    // Function to handle audio generation if needed
    const handleAudioGeneration = async () => {
        // If we already have a story audio URL or already generated one, don't do it again
        if (story.audioUrl || generatedAudioUrl) {
            return;
        }
        
        try {
            setIsGenerating(true);
            console.log('Generating audio for story');
            // Get audio URL from API
            const audioUrl = await speechApi.textToSpeech(story.content);
            console.log('Received audio URL from API:', audioUrl);
            
            if (typeof audioUrl === 'string') {
                setGeneratedAudioUrl(audioUrl);
            } else {
                console.error('Expected string URL but got:', typeof audioUrl);
            }
        } catch (err) {
            console.error('Error generating audio:', err);
        } finally {
            setIsGenerating(false);
        }
    };

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
                <div className="mt-4">
                    <div className="flex justify-between mb-2">
                        {/* Audio button - either plays existing audio or generates new audio */}
                        <button
                            onClick={handleAudioGeneration}
                            className="text-indigo-600 hover:text-indigo-800 flex items-center"
                            disabled={isGenerating}
                        >
                            {isGenerating ? 'Generating Audio...' : 'Listen to Story'}
                            {isGenerating && (
                                <span className="ml-2 animate-spin">⟳</span>
                            )}
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
                    
                    {/* Use our SimpleAudioPlayer if we have an audio URL */}
                    {(story.audioUrl || generatedAudioUrl) && (
                        <SimpleAudioPlayer url={story.audioUrl || generatedAudioUrl!} />
                    )}
                </div>
            </div>
        </div>
    );
}; 