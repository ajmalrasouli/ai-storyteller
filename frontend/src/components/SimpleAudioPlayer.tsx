import React, { useState, useRef, useEffect } from 'react';

interface SimpleAudioPlayerProps {
    url: string;
}

/**
 * A very simple audio player component that works with external URLs
 */
export const SimpleAudioPlayer: React.FC<SimpleAudioPlayerProps> = ({ url }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    // Load the audio URL when it changes
    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.src = url;
            audioRef.current.load();
        }
    }, [url]);

    const togglePlayback = async () => {
        if (!audioRef.current) return;
        
        try {
            if (isPlaying) {
                audioRef.current.pause();
                setIsPlaying(false);
            } else {
                // Try to play and handle any errors
                await audioRef.current.play();
                setIsPlaying(true);
            }
        } catch (err) {
            console.error('Audio playback error:', err);
            setIsPlaying(false);
        }
    };

    return (
        <div className="my-2">
            <button 
                onClick={togglePlayback}
                className="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700 mr-2"
            >
                {isPlaying ? 'Pause' : 'Play'}
            </button>
            
            <audio 
                ref={audioRef}
                onEnded={() => setIsPlaying(false)}
                onError={(e) => {
                    console.error('Audio error:', e);
                    setIsPlaying(false);
                }}
                controls={isPlaying}
                className={isPlaying ? 'inline-block w-64 ml-2' : 'hidden'}
            />
        </div>
    );
};
