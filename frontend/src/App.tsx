import React, { useEffect, useState, useRef } from 'react';
import { generateStory, listStories, Story, toggleFavorite, regenerateIllustration, deleteStory } from './lib/api';
import { Toaster, toast } from 'react-hot-toast';
import confetti from 'canvas-confetti';
import './App.css';

// Background patterns component
const BackgroundPatterns: React.FC = () => {
  return (
    <>
      <div className="improved-background" />
      <div 
        className="static-circle" 
        style={{ 
          width: '400px', 
          height: '400px', 
          backgroundColor: 'rgba(255, 182, 193, 0.4)', // Light pink
          top: '10%', 
          left: '15%'
        }} 
      />
      <div 
        className="static-circle" 
        style={{ 
          width: '300px', 
          height: '300px', 
          backgroundColor: 'rgba(135, 206, 250, 0.4)', // Light sky blue
          bottom: '15%', 
          right: '10%'
        }} 
      />
      <div 
        className="static-circle" 
        style={{ 
          width: '250px', 
          height: '250px', 
          backgroundColor: 'rgba(152, 251, 152, 0.3)', // Light green
          top: '60%', 
          left: '25%'
        }} 
      />
    </>
  );
};

// Floating shapes component
const FloatingShapes: React.FC = () => {
  return (
    <>
      <div 
        style={{
          position: 'fixed',
          width: '120px',
          height: '120px',
          borderRadius: '24px',
          backgroundColor: 'rgba(255, 255, 255, 0.4)',
          boxShadow: '0 8px 32px rgba(31, 38, 135, 0.2)',
          backdropFilter: 'blur(4px)',
          transform: 'rotate(15deg)',
          top: '20%',
          right: '15%',
          zIndex: -2,
          animation: 'float1 25s ease-in-out infinite'
        }}
      />
      <div 
        style={{
          position: 'fixed',
          width: '80px',
          height: '80px',
          backgroundColor: 'rgba(255, 255, 255, 0.25)',
          borderRadius: '50%',
          boxShadow: '0 8px 32px rgba(31, 38, 135, 0.15)',
          backdropFilter: 'blur(4px)',
          bottom: '15%',
          left: '10%',
          zIndex: -2,
          animation: 'float2 20s ease-in-out infinite'
        }}
      />
      <div 
        style={{
          position: 'fixed',
          width: '150px',
          height: '150px',
          backgroundColor: 'rgba(255, 255, 255, 0.2)',
          borderRadius: '30%',
          boxShadow: '0 8px 32px rgba(31, 38, 135, 0.1)',
          backdropFilter: 'blur(4px)',
          transform: 'rotate(-10deg)',
          top: '70%',
          right: '30%',
          zIndex: -2,
          animation: 'float1 30s ease-in-out infinite'
        }}
      />
    </>
  );
};

// --- NEW: Playful Decorations Component ---
const PlayfulDecorations = () => {
  // Define decorations: position, type, color, animation style
  const decorations = [
    // Left Side Decorations
    { id: 'deco-1', type: 'squiggle', color: '#FF914D', top: '20%', left: '5%', animation: 'drift-slow 18s' },
    { id: 'deco-2', type: 'dots', color: '#5CE1E6', top: '40%', left: '8%', animation: 'drift 15s' },
    { id: 'deco-3', type: 'plus', color: '#A8E05F', top: '65%', left: '6%', animation: 'spin-subtle 25s', interactive: true },
    { id: 'deco-4', type: 'circle-outline', color: '#7371FC', bottom: '10%', left: '10%', animation: 'drift-alt 20s' },

    // Right Side Decorations
    { id: 'deco-5', type: 'star', color: '#FFDE59', top: '25%', right: '6%', animation: 'spin-bounce 12s', interactive: true },
    { id: 'deco-6', type: 'scribble', color: '#FF5757', top: '50%', right: '8%', animation: 'drift 16s' },
    { id: 'deco-7', type: 'triangle-outline', color: '#CB6CE6', top: '70%', right: '5%', animation: 'drift-slow 22s', interactive: true },
    { id: 'deco-8', type: 'dots', color: '#A8E05F', bottom: '15%', right: '10%', animation: 'drift-alt 19s' },
  ];

  return (
    <div className="playful-decorations-container">
      {decorations.map(deco => {
        const [animName, animDuration] = deco.animation.split(' ');
        return (
          <div
            key={deco.id}
            // Remove Tailwind animation class
            className={`playful-deco ${deco.type} ${deco.interactive ? 'interactive' : ''}`}
            style={{
              top: deco.top,
              left: deco.left,
              right: deco.right,
              bottom: deco.bottom,
              color: deco.color, 
              // --- Re-apply full longhand properties inline --- 
              animationName: animName,
              animationDuration: animDuration,
              animationTimingFunction: 'ease-in-out',
              animationIterationCount: 'infinite',
              animationDirection: 'alternate', // Note: spin-bounce might not want alternate?
              animationDelay: `${Math.random() * 5}s`, 
            }}
          />
        );
      })}
    </div>
  );
};

// Add this new component after PlayfulDecorations
const MovingBubbles = () => {
  const bubbles = [
    { size: 120, left: '10%', top: '15%', delay: 0, duration: 25 },
    { size: 80, left: '75%', top: '20%', delay: 2, duration: 18 },
    { size: 150, left: '50%', top: '60%', delay: 5, duration: 22 },
    { size: 60, left: '20%', top: '70%', delay: 7, duration: 15 },
    { size: 100, left: '85%', top: '75%', delay: 10, duration: 20 },
    { size: 70, left: '35%', top: '40%', delay: 3, duration: 17 },
    { size: 90, left: '60%', top: '85%', delay: 8, duration: 23 },
  ];

  return (
    <div className="moving-bubbles-container">
      {bubbles.map((bubble, index) => (
        <div 
          key={index}
          className="moving-bubble"
          style={{
            width: `${bubble.size}px`,
            height: `${bubble.size}px`,
            left: bubble.left,
            top: bubble.top,
            animationDelay: `${bubble.delay}s`,
            animationDuration: `${bubble.duration}s`
          }}
        />
      ))}
    </div>
  );
};

// Add this new component after MovingBubbles
const FloatingItems = () => {
  const items = [
    // Corner icons (will remain visible on all screen sizes)
    { icon: "📚", size: 40, left: '5%', top: '20%', delay: 1, duration: 20, className: 'floating-item-corners' },
    { icon: "🐉", size: 45, left: '15%', top: '90%', delay: 0, duration: 17, className: 'floating-item-corners' },
    { icon: "🌟", size: 35, left: '85%', top: '18%', delay: 5, duration: 18, className: 'floating-item-corners' },
    { icon: "🏰", size: 45, left: '80%', top: '92%', delay: 8, duration: 23, className: 'floating-item-corners' },
    
    // Secondary icons (visible on medium and large screens)
    { icon: "🧙‍♂️", size: 40, left: '3%', top: '40%', delay: 2, duration: 22, className: 'floating-item-secondary' },
    { icon: "🧚", size: 35, left: '92%', top: '65%', delay: 6, duration: 21, className: 'floating-item-secondary' },
    
    // Middle-positioned icons (only visible on large screens)
    { icon: "✨", size: 30, left: '25%', top: '22%', delay: 3, duration: 15, className: 'floating-item-middle' },
    { icon: "🦄", size: 40, left: '12%', top: '60%', delay: 7, duration: 16, className: 'floating-item-middle' },
    { icon: "🔮", size: 35, left: '75%', top: '35%', delay: 4, duration: 19, className: 'floating-item-middle' }
  ];

  return (
    <>
      <div className="floating-items-container">
        {items.map((item, index) => (
          <div 
            key={index}
            className={`floating-item ${item.className}`}
            style={{
              fontSize: `${item.size}px`,
              left: item.left,
              top: item.top,
              animationDelay: `${item.delay}s`,
              animationDuration: `${item.duration}s`,
              textShadow: '0 0 10px rgba(0,0,0,0.3)'
            }}
          >
            {item.icon}
          </div>
        ))}
      </div>
      <div className="content-safe-area"></div>
    </>
  );
};

// Story loading animation component
const StoryLoadingAnimation = () => {
  const [loadingMessage, setLoadingMessage] = useState("Creating your magical story...");
  
  const loadingMessages = [
    "Creating your magical story...",
    "Weaving characters into adventures...",
    "Painting worlds with words...",
    "Sprinkling in some fairy dust...",
    "Whispering to the muses...",
    "Gathering inspiration from the stars...",
    "Crafting memorable moments...",
    "Mixing imagination and magic..."
  ];
  
  useEffect(() => {
    let messageIndex = 0;
    const messageInterval = setInterval(() => {
      messageIndex = (messageIndex + 1) % loadingMessages.length;
      setLoadingMessage(loadingMessages[messageIndex]);
    }, 3000);
    
    return () => clearInterval(messageInterval);
  }, []);
  
  return (
    <div className="story-loading-container">
      <div className="story-loading-text">{loadingMessage}</div>
      <div className="story-loading-animation">
        <div className="book"></div>
        <div className="book-page page-1"></div>
        <div className="book-page page-2"></div>
        <div className="book-page page-3"></div>
        <div className="writing-line line-1"></div>
        <div className="writing-line line-2"></div>
        <div className="writing-line line-3"></div>
        <div className="writing-line line-4"></div>
        <div className="story-loading-sparkles">
          <div className="sparkle sparkle-1"></div>
          <div className="sparkle sparkle-2"></div>
          <div className="sparkle sparkle-3"></div>
          <div className="sparkle sparkle-4"></div>
          <div className="sparkle sparkle-5"></div>
        </div>
      </div>
      <div className="loading-text">
        <span className="typing-effect">Imagining wonderful adventures...</span>
      </div>
    </div>
  );
};

// Enhanced themes with emojis and descriptions
const themeIslands = [
  {
    id: "space",
    name: "🚀 Space Adventure",
    description: "Journey through the stars and discover new planets with brave astronauts and friendly aliens.",
    color: "#4c1d95",
    backgroundColor: "#c4b5fd",
    icon: "🚀"
  },
  {
    id: "magic",
    name: "🏰 Magic Kingdom",
    description: "Explore enchanted castles, meet wizards, and discover magical creatures in a world of wonder.",
    color: "#5b21b6",
    backgroundColor: "#ddd6fe",
    icon: "🏰"
  },
  {
    id: "ocean",
    name: "🌊 Ocean Explorer",
    description: "Dive deep into underwater adventures with mermaids, friendly sea creatures, and hidden treasures.",
    color: "#1e40af",
    backgroundColor: "#bfdbfe",
    icon: "🌊"
  },
  {
    id: "jungle",
    name: "🐯 Jungle Safari",
    description: "Trek through lush jungles filled with exotic animals, ancient ruins, and exciting discoveries.",
    color: "#166534",
    backgroundColor: "#bbf7d0",
    icon: "🐯"
  },
  {
    id: "dinosaur",
    name: "🦕 Dinosaur World",
    description: "Travel back in time to when dinosaurs ruled the Earth. Meet friendly dinos and discover their world.",
    color: "#92400e",
    backgroundColor: "#fed7aa",
    icon: "🦕"
  }
];

// Enhanced age groups with progression levels
const ageGroupLevels = [
  {
    id: "beginner",
    name: "🧒 Little Explorers",
    range: "(3-5 years)",
    description: "Simple stories with basic words and concepts, perfect for the youngest adventurers.",
    color: "#0891b2",
    backgroundColor: "#a5f3fc",
    icon: "🧒"
  },
  {
    id: "intermediate",
    name: "👦 Curious Minds", 
    range: "(6-8 years)",
    description: "More detailed adventures with expanded vocabulary and engaging plots.",
    color: "#0e7490",
    backgroundColor: "#67e8f9",
    icon: "👦"
  },
  {
    id: "advanced",
    name: "👧 Young Adventurers",
    range: "(9-12 years)",
    description: "Complex stories with rich language, deeper themes, and exciting challenges.",
    color: "#0369a1",
    backgroundColor: "#bae6fd",
    icon: "👧"
  }
];

// Decorative bubbles for the header
const HeaderBubbles = () => {
  const bubbles = Array.from({ length: 15 }, (_, i) => ({
    size: Math.random() * 40 + 10,
    left: Math.random() * 100,
    animationDelay: Math.random() * 5,
    opacity: Math.random() * 0.5 + 0.1
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {bubbles.map((bubble, i) => (
        <div 
          key={i}
          className="decorative-shape"
          style={{
            width: `${bubble.size}px`,
            height: `${bubble.size}px`,
            left: `${bubble.left}%`,
            top: Math.random() * 100,
            animationDelay: `${bubble.animationDelay}s`,
            opacity: bubble.opacity
          }}
        />
      ))}
    </div>
  );
};

// Story card component
const StoryCard = ({ story, onView, onToggleFavorite, onDelete }: { 
  story: Story, 
  onView: (story: Story) => void, 
  onToggleFavorite: (storyId: number) => void,
  onDelete?: (storyId: number) => void
}) => {
  const themeIcon = getThemeIcon(story.theme);
  
  return (
    <div className="story-card" onClick={() => onView(story)}>
      <div className="story-card-header">
        <div className="theme-badge">{themeIcon} {story.theme.split(' ')[1]}</div>
        <div className="story-actions">
          <button 
            className="favorite-btn"
            onClick={(e) => {
              e.stopPropagation();
              onToggleFavorite(story.id);
            }}
          >
            <span className="text-3xl">{story.isFavorite ? '❤️' : '🤍'}</span>
          </button>
          
          {onDelete && (
            <button 
              className="delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                if (window.confirm("Are you sure you want to delete this story?")) {
                  onDelete(story.id);
                }
              }}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                fontSize: '1.2rem',
                padding: '5px',
                marginLeft: '5px',
                opacity: 0.7
              }}
            >
              🗑️
            </button>
          )}
        </div>
      </div>
      
      {/* Display AI-generated illustration if available */}
      {story.imageUrl && (
        <div className="story-illustration">
          <img 
            src={story.imageUrl} 
            alt={`Illustration for "${story.title}"`} 
            className="w-full h-48 object-cover rounded-lg mb-3"
            loading="lazy"
          />
        </div>
      )}
      
      <div className="story-card-content">
        <h3>{story.title}</h3>
        <div className="story-preview">
          <p className="text-gray-600">
            {story.content.substring(0, 300)}...
          </p>
        </div>
        <div className="character-list">
          {story.characters.slice(0, 3).map((character, index) => (
            <span key={index} className="character-tag">
              <span className="character-emoji">👤</span> {character}
            </span>
          ))}
          {story.characters.length > 3 && (
            <span className="character-tag">+{story.characters.length - 3} more</span>
          )}
        </div>
        <div className="story-card-footer">
          <span className="age-badge">{story.ageGroup}</span>
          <span className="story-date">{new Date(story.createdAt).toLocaleDateString()}</span>
        </div>
      </div>
    </div>
  );
};

interface StoryModalProps {
  story: Story;
  isOpen: boolean;
  onClose: () => void;
  onToggleFavorite: (storyId: number) => void;
  onDelete: (storyId: number) => void;
}

const StoryModal = ({ story, isOpen, onClose, onToggleFavorite, onDelete }: StoryModalProps) => {
  const [showContent, setShowContent] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isRegeneratingImage, setIsRegeneratingImage] = useState(false);
  const [storyData, setStoryData] = useState(story);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    // Update storyData when the story prop changes
    setStoryData(story);
  }, [story]);

  useEffect(() => {
    if (isOpen) {
      // Add a slight delay before showing content to allow for animation preparation
      const timer = setTimeout(() => {
        setShowContent(true);
      }, 300);
      return () => clearTimeout(timer);
    } else {
      setShowContent(false);
      // Stop speaking if modal is closed
      if (isSpeaking) {
        stopSpeaking();
      }
    }
  }, [isOpen, isSpeaking]);

  // Clean up speech synthesis when component unmounts
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
    };
  }, []);

  if (!isOpen) return null;

  const handlePrint = () => {
    // Create a new window with just the story content for printing
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>${storyData.title}</title>
            <style>
              body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
              }
              h1 {
                font-size: 24px;
                margin-bottom: 20px;
              }
              p {
                margin-bottom: 15px;
              }
              .story-meta {
                color: #666;
                font-size: 14px;
                margin-bottom: 20px;
              }
              .story-illustration {
                max-width: 100%;
                margin-bottom: 20px;
              }
            </style>
          </head>
          <body>
            <h1>${storyData.title}</h1>
            <div class="story-meta">
              <div>Theme: ${storyData.theme}</div>
              <div>Age Group: ${storyData.ageGroup}</div>
              <div>Date: ${new Date(storyData.createdAt).toLocaleDateString()}</div>
            </div>
            ${storyData.imageUrl ? `<img src="${storyData.imageUrl}" alt="Story Illustration" class="story-illustration"/>` : ''}
            ${storyData.content.split("\n\n").map((paragraph: string) => `<p>${paragraph}</p>`).join('')}
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
    }
  };

  const handleEmail = () => {
    try {
        const subject = encodeURIComponent(`Story: ${storyData.title}`);
        
        // Create a more concise version of the story for email
        const maxEmailLength = 1500;
        const contentPreview = storyData.content.length > maxEmailLength 
            ? storyData.content.substring(0, maxEmailLength) + "...\n\n(Story continues in the app)"
            : storyData.content;
        
        // Include the illustration URL if available
        const illustrationText = storyData.imageUrl 
            ? `\n\nView the story illustration here: ${storyData.imageUrl}\n\n` 
            : '\n\n';
        
        const body = encodeURIComponent(
            `${storyData.title}\n\n` +
            `Theme: ${storyData.theme}\n` +
            `Age Group: ${storyData.ageGroup}\n` +
            illustrationText +
            `${contentPreview}\n\n` +
            `Created with AI Storyteller\n` +
            `View the full story at: ${window.location.origin}/stories/${storyData.id}`
        );
        
        // Create a temporary link element and trigger it
        const mailtoLink = document.createElement('a');
        mailtoLink.href = `mailto:?subject=${subject}&body=${body}`;
        mailtoLink.target = '_blank';
        document.body.appendChild(mailtoLink);
        mailtoLink.click();
        document.body.removeChild(mailtoLink);
        
        toast.success("Email client opened!");
    } catch (error) {
        toast.error("Could not open email client. Please try again or use another method to share.");
        console.error("Email error:", error);
    }
  };

  // Add new social sharing functions
  const handleShare = async () => {
    try {
        if (navigator.share) {
            const shareData = {
                title: storyData.title,
                text: `Check out this story: ${storyData.title}\nTheme: ${storyData.theme}\nAge Group: ${storyData.ageGroup}`,
                url: `${window.location.origin}/stories/${storyData.id}`
            };
            
            await navigator.share(shareData);
            toast.success("Story shared successfully!");
        } else {
            // Fallback for browsers that don't support Web Share API
            const shareUrl = `${window.location.origin}/stories/${storyData.id}`;
            const shareText = `Check out this story: ${storyData.title}\nTheme: ${storyData.theme}\nAge Group: ${storyData.ageGroup}\n${shareUrl}`;
            
            // Copy to clipboard
            await navigator.clipboard.writeText(shareText);
            toast.success("Story link copied to clipboard!");
        }
    } catch (error) {
        console.error("Error sharing:", error);
        toast.error("Could not share the story. Please try again.");
    }
  };

  // Add social media sharing buttons
  const SocialShareButtons = () => {
    const shareUrl = encodeURIComponent(`${window.location.origin}/stories/${storyData.id}`);
    const shareTitle = encodeURIComponent(storyData.title);
    const shareText = encodeURIComponent(`Check out this story: ${storyData.title}\nTheme: ${storyData.theme}\nAge Group: ${storyData.ageGroup}`);

    return (
        <div className="social-share-buttons">
            <button 
                onClick={() => window.open(`https://twitter.com/intent/tweet?url=${shareUrl}&text=${shareText}`, '_blank')}
                className="social-share-button twitter"
            >
                <span className="social-icon">🐦</span> Twitter
            </button>
            <button 
                onClick={() => window.open(`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`, '_blank')}
                className="social-share-button facebook"
            >
                <span className="social-icon">📘</span> Facebook
            </button>
            <button 
                onClick={() => window.open(`https://api.whatsapp.com/send?text=${shareText}%20${shareUrl}`, '_blank')}
                className="social-share-button whatsapp"
            >
                <span className="social-icon">💬</span> WhatsApp
            </button>
        </div>
    );
  };

  const startSpeaking = async (text: string) => {
    try {
      // Cancel any existing request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      
      // Stop any existing playback
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
        audioRef.current = null;
      }
      
      setIsSpeaking(true);
      
      // Create new abort controller
      abortControllerRef.current = new AbortController();
      
      const response = await fetch('http://localhost:5000/api/speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
        signal: abortControllerRef.current.signal
      });
      
      if (!response.ok) {
        throw new Error('Speech synthesis failed');
      }
      
      const data = await response.json();
      
      // Create new audio element
      const audio = new Audio();
      audio.onended = () => {
        setIsSpeaking(false);
        audioRef.current = null;
      };
      audio.onerror = () => {
        setIsSpeaking(false);
        audioRef.current = null;
      };
      audio.onpause = () => {
        setIsSpeaking(false);
        audioRef.current = null;
      };
      
      // Set the audio source
      audio.src = `data:audio/wav;base64,${data.audio}`;
      
      // Store the audio reference
      audioRef.current = audio;
      
      // Play the audio
      await audio.play();
      
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        console.log('Speech synthesis aborted');
      } else {
        console.error('Error:', error);
      }
      setIsSpeaking(false);
      audioRef.current = null;
    }
  };

  const stopSpeaking = () => {
    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    
    // Stop any existing playback
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
    }
    
    setIsSpeaking(false);
  };

  // Cleanup on component unmount
  useEffect(() => {
    return () => {
      stopSpeaking();
    };
  }, []);

  const handleListen = () => {
    if (isSpeaking) {
      stopSpeaking();
    } else {
      startSpeaking(storyData.content);
    }
  };

  // Function to regenerate the illustration
  const handleRegenerateIllustration = async () => {
    try {
      setIsRegeneratingImage(true);
      const response = await regenerateIllustration(storyData.id);
      
      // Update the local story data with the new image URL
      setStoryData({
        ...storyData,
        imageUrl: response.imageUrl
      });
      
      toast.success("Illustration regenerated successfully!");
      // Trigger a confetti celebration
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (error) {
      toast.error("Failed to regenerate illustration. Please try again.");
      console.error("Error regenerating illustration:", error);
    } finally {
      setIsRegeneratingImage(false);
    }
  };

  const handleDelete = () => {
    onDelete(storyData.id);
  };

  // Split the content into paragraphs
  const paragraphs = storyData.content.split("\n\n");
  const title = storyData.title;

  return (
    <div style={styles.storyModalOverlay} onClick={onClose}>
      <div style={styles.storyModal} onClick={(e) => e.stopPropagation()}>
        <div style={styles.modalHeader}>
          <h2 style={styles.modalTitle} className="typing-effect">{title}</h2>
          <button style={styles.closeModal} onClick={onClose}>×</button>
        </div>
        <div className="modal-content">
          <div className="modal-story-meta">
            <span className="modal-story-theme">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M2 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 6.586 1H2zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
              </svg>
              {storyData.theme}
            </span>
            <span className="modal-story-age">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
              </svg>
              {storyData.ageGroup}
            </span>
          </div>

          {/* Display AI-generated illustration if available */}
          {storyData.imageUrl && (
            <div className="modal-story-illustration" style={{ marginBottom: '20px', textAlign: 'center', position: 'relative' }}>
              <img 
                src={storyData.imageUrl} 
                alt={`Illustration for "${storyData.title}"`} 
                style={{ 
                  maxWidth: '100%', 
                  maxHeight: '400px', 
                  borderRadius: '8px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                  opacity: isRegeneratingImage ? 0.6 : 1,
                  transition: 'opacity 0.3s ease'
                }}
              />
              {isRegeneratingImage && (
                <div style={{ 
                  position: 'absolute', 
                  top: '50%', 
                  left: '50%', 
                  transform: 'translate(-50%, -50%)',
                  backgroundColor: 'rgba(255, 255, 255, 0.8)',
                  padding: '10px 20px',
                  borderRadius: '20px',
                  boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                }}>
                  <div className="loading-dots">Regenerating illustration</div>
                </div>
              )}
              <button 
                onClick={handleRegenerateIllustration}
                disabled={isRegeneratingImage}
                style={{ 
                  position: 'absolute', 
                  bottom: '10px', 
                  right: '10px',
                  backgroundColor: isRegeneratingImage ? '#ccc' : '#6366f1',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '5px 10px',
                  cursor: isRegeneratingImage ? 'not-allowed' : 'pointer',
                  fontSize: '0.8rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  opacity: isRegeneratingImage ? 0.7 : 1
                }}
              >
                {isRegeneratingImage ? 'Working...' : '🔄 Regenerate Illustration'}
              </button>
            </div>
          )}

          <div className="typing-container">
            {showContent && paragraphs.map((paragraph: string, index: number) => (
              <p 
                key={index} 
                className={`fade-in typewriter-delay-${Math.min(index + 1, 4)}`}
              >
                {paragraph}
              </p>
            ))}
          </div>
        </div>
        <div className="modal-footer" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #eee', padding: '15px 20px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              className={`favorite-button ${storyData.isFavorite ? 'active' : ''}`}
              onClick={() => onToggleFavorite(storyData.id)}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: storyData.isFavorite ? '#ff6b6b' : '#666',
                fontWeight: 'bold'
              }}
            >
              {storyData.isFavorite ? '❤️' : '🤍'} {storyData.isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
            </button>
            
            <button 
              onClick={handleEmail}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: '#0077cc',
                fontWeight: 'bold'
              }}
            >
              ✉️ Email Story
            </button>
            
            <button 
              onClick={handlePrint}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: '#333',
                fontWeight: 'bold'
              }}
            >
              🖨️ Print Story
            </button>
            
            <button 
              onClick={handleListen}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: '#009688',
                fontWeight: 'bold'
              }}
            >
              {isSpeaking ? '🔇 Stop' : '🔊 Listen'}
            </button>
            
            <button 
              onClick={handleShare}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: '#4CAF50',
                fontWeight: 'bold'
              }}
            >
              📤 Share Story
            </button>
            
            <button 
              onClick={handleDelete}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: '#ff5252',
                fontWeight: 'bold'
              }}
            >
              🗑️ Delete Story
            </button>
          </div>
          
          <span className="story-date" style={{ color: '#888', fontSize: '0.9rem' }}>
            {new Date(storyData.createdAt).toLocaleDateString()}
          </span>
        </div>
      </div>
    </div>
  );
};

// Confetti component for celebrations
const Confetti = ({ active = false }) => {
  if (!active) return null;
  
  const confettiPieces = Array.from({ length: 50 }, (_, i) => {
    const colors = ['bg-red-500', 'bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-pink-500', 'bg-purple-500'];
    const size = Math.random() * 10 + 5;
    const left = Math.random() * 100;
    const delay = Math.random() * 3;
    const duration = Math.random() * 3 + 2;
    
    return (
      <div 
            key={i}
        className={`confetti-piece ${colors[Math.floor(Math.random() * colors.length)]}`}
        style={{
          left: `${left}%`,
          width: `${size}px`,
          height: `${size}px`,
          animation: `fall ${duration}s linear forwards`,
          animationDelay: `${delay}s`
        }}
      />
    );
  });
  
  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {confettiPieces}
    </div>
  );
};

// Helper function to get theme emoji
const getThemeIcon = (theme: string) => {
  if (theme.includes("Space")) return "🚀";
  if (theme.includes("Magic")) return "🏰";
  if (theme.includes("Ocean")) return "🌊";
  if (theme.includes("Jungle")) return "🐯";
  if (theme.includes("Dinosaur")) return "🦕";
  return "📚";
};

// Helper function to get age group emoji
const getAgeGroupEmoji = (ageGroup: string) => {
  if (ageGroup.includes("3-5")) return "🧒";
  if (ageGroup.includes("6-8")) return "👦";
  if (ageGroup.includes("9-12")) return "👧";
  return "👪";
};

// Header with banner
interface AppHeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  storiesCount: number;
}

const AppHeader = ({ activeTab, setActiveTab, storiesCount }: AppHeaderProps) => {
  const navButtonStyle: React.CSSProperties = {
    backgroundColor: 'white',
    color: '#1A67A3',
    border: 'none',
    borderRadius: '25px',
    padding: '12px 24px',
    fontSize: '1.1rem',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 0 rgba(0, 0, 0, 0.1), 0 0 10px rgba(255, 255, 255, 0.5)',
    display: 'flex',
    alignItems: 'center',
    gap: '6px'
  };

  const activeButtonStyle: React.CSSProperties = {
    ...navButtonStyle,
    backgroundColor: '#FFC857',
    color: '#1A67A3',
    transform: 'translateY(-3px)',
    boxShadow: '0 7px 0 rgba(0, 0, 0, 0.1), 0 0 15px rgba(255, 220, 89, 0.7)'
  };

  return (
    <header className="app-header">
      <div className="sun"></div>
      <div className="relative z-10">
        <h1 className="site-title">✨ AI Storyteller ✨</h1>
        <p className="site-subtitle">Embark on a journey through magical worlds of storytelling</p>
        <div className="nav-tabs">
          <button 
            style={activeTab === 'create' ? activeButtonStyle : navButtonStyle}
            onClick={() => setActiveTab('create')}
          >
            🗺️ Story Adventure
          </button>
          <button 
            style={activeTab === 'stories' ? activeButtonStyle : navButtonStyle}
            onClick={() => setActiveTab('stories')}
          >
            📚 My Stories ({storiesCount})
          </button>
          <button 
            style={activeTab === 'favorites' ? activeButtonStyle : navButtonStyle}
            onClick={() => setActiveTab('favorites')}
          >
            ❤️ Favorites
          </button>
        </div>
      </div>
    </header>
  );
};

const ThemeSelector = ({ selectedTheme, onSelectTheme }: { selectedTheme: string, onSelectTheme: (theme: string) => void }) => {
  const themeButtonStyle: React.CSSProperties = {
    padding: '20px 15px',
    backgroundColor: 'white',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  };

  const activeThemeStyle: React.CSSProperties = {
    ...themeButtonStyle,
    backgroundColor: 'rgba(147, 51, 234, 0.1)',
    borderColor: '#9333ea',
    transform: 'translateY(-2px)'
  };

  const iconStyle: React.CSSProperties = {
    fontSize: '3rem',
    marginBottom: '10px'
  };

  const nameStyle: React.CSSProperties = {
    fontSize: '1.1rem',
    fontWeight: 'bold',
    color: '#333'
  };

  return (
    <div className="theme-selector">
      {themeIslands.map((theme, index) => {
        const icon = getThemeIcon(theme.name);
        const name = theme.name.split(' ').slice(1).join(' ');
        
        return (
          <button
            key={index}
            style={selectedTheme === theme.name ? activeThemeStyle : themeButtonStyle}
            onClick={() => onSelectTheme(theme.name)}
          >
            <span style={iconStyle}>{icon}</span>
            <span style={nameStyle}>{name}</span>
          </button>
        );
      })}
    </div>
  );
};

const AgeGroupSelector = ({ selectedAgeGroup, onSelectAgeGroup }: { selectedAgeGroup: string, onSelectAgeGroup: (age: string) => void }) => {
  const ageButtonStyle: React.CSSProperties = {
    flex: 1,
    minWidth: '120px',
    backgroundColor: 'white',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    padding: '15px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  };

  const activeAgeStyle: React.CSSProperties = {
    ...ageButtonStyle,
    backgroundColor: 'rgba(147, 51, 234, 0.1)',
    borderColor: '#9333ea'
  };

  const iconStyle: React.CSSProperties = {
    fontSize: '2.5rem',
    marginBottom: '8px'
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '1.1rem',
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center'
  };

  const rangeStyle: React.CSSProperties = {
    fontSize: '0.8rem',
    color: '#6b7280'
  };

  return (
    <div className="age-selector">
      {ageGroupLevels.map((level, index) => {
        const isSelected = selectedAgeGroup === `${level.name} ${level.range}`;
        
        return (
          <button
            key={index}
            style={isSelected ? activeAgeStyle : ageButtonStyle}
            onClick={() => onSelectAgeGroup(`${level.name} ${level.range}`)}
          >
            <span style={iconStyle}>{level.icon}</span>
            <span style={labelStyle}>{level.name}</span>
            <span style={rangeStyle}>{level.range}</span>
          </button>
        );
      })}
    </div>
  );
};

// Add a popup component to display footer information
const FooterPopup = ({ 
  title, 
  content, 
  isOpen, 
  onClose,
  popupType
}: { 
  title: string, 
  content: React.ReactNode, 
  isOpen: boolean, 
  onClose: () => void,
  popupType: 'about' | 'privacy' | 'contact' | 'help'
}) => {
  // Use a ref for the popup content
  const popupRef = useRef<HTMLDivElement>(null);
  
  // Handle clicks outside the popup
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
        onClose();
      }
    };
    
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);
  
  if (!isOpen) return null;
  
  return (
    <div 
      className="footer-popup"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 999,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0, 0, 0, 0.2)',
      }}
    >
      <div 
        ref={popupRef}
        className={`footer-popup-content popup-${popupType}`}
        style={{
          position: 'relative',
          maxWidth: '90%',
          animation: 'popup-appear 0.3s forwards'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <h3>{title}</h3>
          <button className="footer-popup-close" onClick={onClose}>
            ×
          </button>
        </div>
        <div>
          {content}
        </div>
      </div>
    </div>
  );
};

// Footer component with popups
const AppFooter = () => {
  const [activePopup, setActivePopup] = useState<string | null>(null);
  
  // Content for each popup
  const aboutContent = (
    <>
      <p>AI Storyteller is an interactive storytelling app designed for children of all ages.</p>
      <p>Our mission is to spark creativity and imagination through personalized stories tailored to each child's interests.</p>
      <p>Created with ❤️ by Ajmal Rasouli, a passionate educator and developer.</p>
      <p>AI Agents Hackathon 2025. https://microsoft.github.io/AI_Agents_Hackathon/</p>
      <p>Version 1.0.0</p>
    </>
  );
  
  const privacyContent = (
    <>
      <p><strong>Data Collection:</strong> We only collect information necessary to provide our services.</p>
      <p><strong>Story Data:</strong> Stories generated are stored securely and only accessible to your account.</p>
      <p><strong>Children's Privacy:</strong> We're committed to protecting children's privacy and complying with all applicable laws.</p>
      <p><strong>Third Parties:</strong> We don't sell your data to third parties.</p>
      <p>For the complete policy, please contact us.</p>
    </>
  );
  
  const contactContent = (
    <>
      <p><strong>Email:</strong> ajrasouli@hotmail.com</p>
      <p><strong>Hours:</strong> Monday-Friday, 9am-5pm EST</p>
      <p><strong>Response Time: GMT</strong> We aim to respond to all inquiries within 24 hours.</p>
      <p>For urgent matters, please include "URGENT" in your email subject.</p>
    </>
  );
  
  const helpContent = (
    <>
      <p><strong>Creating Stories:</strong> Select a theme, add characters, choose an age group, and click "Generate".</p>
      <p><strong>Reading Stories:</strong> Use the Listen button to hear your story read aloud.</p>
      <p><strong>Sharing:</strong> Click Email Story to share via email, or Print Story for a paper copy.</p>
      <p><strong>Favorites:</strong> Click the heart icon to add stories to your favorites collection.</p>
    </>
  );
  
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-logo">✨ AI Storyteller ✨</div>
        <p>Create magical stories for children of all ages!</p>
        
        <div className="footer-links">
          <button 
            className="footer-link" 
            onClick={() => setActivePopup('about')}
          >
            About
          </button>
          <button
            className="footer-link" 
            onClick={() => setActivePopup('privacy')}
          >
            Privacy Policy
          </button>
          <button 
            className="footer-link" 
            onClick={() => setActivePopup('contact')}
          >
            Contact Us
          </button>
          <button 
            className="footer-link" 
            onClick={() => setActivePopup('help')}
          >
            Help
          </button>
        </div>
        
        <p className="text-sm">© 2025 AI Storyteller. All rights reserved.</p>
      </div>
      
      {/* Render the active popup */}
      {activePopup === 'about' && (
        <FooterPopup
          title="About AI Storyteller"
          content={aboutContent}
          isOpen={true}
          onClose={() => setActivePopup(null)}
          popupType="about"
        />
      )}
      
      {activePopup === 'privacy' && (
        <FooterPopup
          title="Privacy Policy"
          content={privacyContent}
          isOpen={true}
          onClose={() => setActivePopup(null)}
          popupType="privacy"
        />
      )}
      
      {activePopup === 'contact' && (
        <FooterPopup
          title="Contact Us"
          content={contactContent}
          isOpen={true}
          onClose={() => setActivePopup(null)}
          popupType="contact"
        />
      )}
      
      {activePopup === 'help' && (
        <FooterPopup
          title="Help & Instructions"
          content={helpContent}
          isOpen={true}
          onClose={() => setActivePopup(null)}
          popupType="help"
        />
      )}
    </footer>
  );
};

// Empty State component
const EmptyState = ({ onCreateNew }: { onCreateNew: () => void }) => {
  return (
    <div className="empty-state">
      <div className="empty-illustration">
        <img src="/grid.svg" alt="No stories yet" />
        </div>
      <h3 className="empty-title">No Stories Yet!</h3>
      <p className="empty-message">Create your first magical story adventure!</p>
      <button className="action-button" onClick={onCreateNew}>
        <span>✏️</span> Create My First Story
      </button>
    </div>
  );
};

// Define CSS styles as a regular CSS string
const styles = {
  appContainer: {
    position: 'relative',
    minHeight: '100vh',
    overflowX: 'hidden',
  } as React.CSSProperties,
  
  appBackground: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    zIndex: -1,
  } as React.CSSProperties,
  
  backgroundWhite: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: '#ffffff',
  } as React.CSSProperties,
  
  storyModalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  } as React.CSSProperties,
  
  storyModal: {
    backgroundColor: 'white',
    borderRadius: '8px',
    width: '90%',
    maxWidth: '700px',
    maxHeight: '90vh',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
  } as React.CSSProperties,
  
  modalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px 20px',
    borderBottom: '1px solid #eee',
  } as React.CSSProperties,
  
  modalTitle: {
    margin: 0,
    fontSize: '1.5rem',
    color: '#333',
  } as React.CSSProperties,
  
  closeModal: {
    background: 'none',
    border: 'none',
    fontSize: '1.5rem',
    cursor: 'pointer',
    color: '#666',
  } as React.CSSProperties,
};

// New component: Adventure Map
const AdventureMap = ({ 
  selectedTheme, 
  onSelectTheme, 
  selectedAgeGroup, 
  onSelectAgeGroup,
  storyCount
}: { 
  selectedTheme: string, 
  onSelectTheme: (theme: string) => void,
  selectedAgeGroup: string,
  onSelectAgeGroup: (age: string) => void,
  storyCount: number
}) => {
  return (
    <div className="adventure-map">
      <h2 className="adventure-title">Your Story Adventure Map</h2>
      <p className="adventure-subtitle">Choose an island theme and skill level to begin your storytelling journey!</p>
      
      <div className="island-selection">
        <h3 className="section-heading">Choose Your Story Island</h3>
        <div className="islands-grid">
          {themeIslands.map((island) => {
            const isSelected = selectedTheme === island.name;
            
            return (
              <div 
                key={island.id}
                className={`island-card ${isSelected ? 'selected' : ''}`}
                onClick={() => onSelectTheme(island.name)}
                style={{
                  backgroundColor: isSelected ? island.backgroundColor : '#ffffff',
                  borderColor: isSelected ? island.color : '#e5e7eb',
                  boxShadow: isSelected ? `0 10px 15px -3px ${island.backgroundColor}` : '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              >
                <div className="island-icon" style={{ backgroundColor: island.color }}>
                  <span>{island.icon}</span>
                </div>
                <div className="island-content">
                  <h4 className="island-name">{island.name.split(' ').slice(1).join(' ')}</h4>
                  <p className="island-description">{island.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      <div className="skill-selection">
        <h3 className="section-heading">Choose Your Skill Level</h3>
        <div className="skills-grid">
          {ageGroupLevels.map((level) => {
            const isSelected = selectedAgeGroup === `${level.name} ${level.range}`;
            
            return (
              <div 
                key={level.id}
                className={`skill-card ${isSelected ? 'selected' : ''}`}
                onClick={() => onSelectAgeGroup(`${level.name} ${level.range}`)}
                style={{
                  backgroundColor: isSelected ? level.backgroundColor : '#ffffff',
                  borderColor: isSelected ? level.color : '#e5e7eb',
                  boxShadow: isSelected ? `0 10px 15px -3px ${level.backgroundColor}` : '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              >
                <div className="skill-icon" style={{ backgroundColor: level.color }}>
                  <span>{level.icon}</span>
                </div>
                <div className="skill-content">
                  <h4 className="skill-name">{level.name}</h4>
                  <p className="skill-range">{level.range}</p>
                  <p className="skill-description">{level.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      <div className="progress-tracker">
        <div className="progress-stats">
          <div className="stat-box">
            <span className="stat-value">{storyCount}</span>
            <span className="stat-label">Stories Created</span>
          </div>
          <div className="stat-box">
            <span className="stat-value">{selectedTheme ? 1 : 0}/5</span>
            <span className="stat-label">Islands Explored</span>
          </div>
          <div className="stat-box">
            <span className="stat-value">{selectedAgeGroup ? 1 : 0}/3</span>
            <span className="stat-label">Skill Levels</span>
          </div>
        </div>
        </div>
    </div>
  );
};

// Create Story Section
const CreateStorySection = ({
  theme,
  characters,
  ageGroup,
  loading,
  setCharacters,
  handleGenerateStory
}: {
  theme: string,
  characters: string,
  ageGroup: string,
  loading: boolean,
  setCharacters: (characters: string) => void,
  handleGenerateStory: () => void
}) => {
  const selectedTheme = themeIslands.find(i => i.name === theme);
  const selectedLevel = ageGroupLevels.find(l => `${l.name} ${l.range}` === ageGroup);
  
  if (!selectedTheme || !selectedLevel) {
    return (
      <div className="character-section">
        <h3 className="section-heading">Complete Your Selection</h3>
        <p className="section-description">
          Please select a story theme and skill level to continue your adventure!
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="character-section">
        <StoryLoadingAnimation />
      </div>
    );
  }

  return (
    <div className="character-section">
      <div className="adventure-header">
        <div className="adventure-badge" style={{ backgroundColor: selectedTheme.backgroundColor, color: selectedTheme.color }}>
          {selectedTheme.icon} {selectedTheme.name.split(' ').slice(1).join(' ')}
        </div>
        <div className="adventure-badge" style={{ backgroundColor: selectedLevel.backgroundColor, color: selectedLevel.color }}>
          {selectedLevel.icon} {selectedLevel.name}
        </div>
      </div>
      
      <h3 className="section-heading">Create Your Adventure Characters</h3>
      <p className="section-description">
        Who will join you on this adventure to {selectedTheme.name.split(' ').slice(1).join(' ')}? 
        Add your main characters below, separated by commas.
      </p>
      
      <div className="character-input-container">
        <textarea
          className="form-control"
          placeholder="Enter characters for your story (e.g., 'a brave knight named Max, a friendly dragon named Sparky')"
          value={characters}
          onChange={(e) => setCharacters(e.target.value)}
          rows={3}
          style={{
            borderColor: selectedTheme.color,
            boxShadow: `0 0 0 2px ${selectedTheme.backgroundColor}`
          }}
        />
        {characters.length === 0 && (
          <div className="character-suggestions">
            <div className="suggestion-title">Try these characters:</div>
            <div className="suggestion-list">
              {selectedTheme.id === "space" && (
                <>
                  <span className="suggestion-item" onClick={() => setCharacters("Captain Stella, a friendly alien named Zorp, a robot dog called Byte")}>Space Crew</span>
                  <span className="suggestion-item" onClick={() => setCharacters("Dr. Nova, twin astronauts Tim and Tom, a mysterious space creature")}>Galaxy Explorers</span>
                </>
              )}
              {selectedTheme.id === "magic" && (
                <>
                  <span className="suggestion-item" onClick={() => setCharacters("a brave princess, a talking cat, a wise wizard")}>Royal Magic</span>
                  <span className="suggestion-item" onClick={() => setCharacters("Merlin the young wizard, a magical dragon egg, a forest fairy")}>Enchanted Friends</span>
                </>
              )}
              {selectedTheme.id === "ocean" && (
                <>
                  <span className="suggestion-item" onClick={() => setCharacters("Marina the mermaid, Bubbles the dolphin, Captain Coral")}>Ocean Friends</span>
                  <span className="suggestion-item" onClick={() => setCharacters("a curious submarine pilot, a giant friendly octopus, a lost whale")}>Deep Sea Explorers</span>
                </>
              )}
              {selectedTheme.id === "jungle" && (
                <>
                  <span className="suggestion-item" onClick={() => setCharacters("Zara the explorer, Stripes the tiger cub, a wise old elephant")}>Jungle Team</span>
                  <span className="suggestion-item" onClick={() => setCharacters("Dr. Leaf the botanist, a playful monkey, a colorful parrot guide")}>Rainforest Adventurers</span>
                </>
              )}
              {selectedTheme.id === "dinosaur" && (
                <>
                  <span className="suggestion-item" onClick={() => setCharacters("a time-traveling scientist, Rex the friendly T-Rex, Pterry the pterodactyl")}>Dino Buddies</span>
                  <span className="suggestion-item" onClick={() => setCharacters("twins Tara and Tim, a baby triceratops, Dr. Fossil")}>Prehistoric Gang</span>
                </>
              )}
            </div>
          </div>
        )}
      </div>
      
      <button
        className="adventure-button"
        onClick={handleGenerateStory}
        disabled={!characters}
        style={{
          backgroundColor: selectedTheme.color,
          color: 'white',
          fontWeight: 'bold',
          padding: '16px 24px',
          width: '100%',
          borderRadius: '8px',
          fontSize: '1.2rem',
          boxShadow: `0 4px 0 rgba(0, 0, 0, 0.2)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '10px'
        }}
      >
        <span>✨ Begin Your Magical Adventure ✨</span>
      </button>
    </div>
  );
};

// Add this new component for moving clouds
const MovingClouds = () => {
  const clouds = [
    { width: 120, top: '10%', left: '-10%', delay: 0, duration: 100 },
    { width: 180, top: '15%', left: '-15%', delay: 20, duration: 120 },
    { width: 150, top: '5%', left: '-5%', delay: 10, duration: 90 },
    { width: 200, top: '20%', left: '-20%', delay: 5, duration: 110 },
    { width: 100, top: '25%', left: '-8%', delay: 15, duration: 95 },
    { width: 160, top: '8%', left: '-12%', delay: 25, duration: 105 },
  ];

  return (
    <div className="moving-clouds-container">
      {clouds.map((cloud, index) => (
        <div 
          key={index}
          className="moving-cloud"
          style={{
            width: `${cloud.width}px`,
            top: cloud.top,
            left: cloud.left,
            animationDelay: `${cloud.delay}s`,
            animationDuration: `${cloud.duration}s`
          }}
        />
      ))}
    </div>
  );
};

// Main App component
export default function App() {
  const [stories, setStories] = useState<Story[]>([]);
  const [theme, setTheme] = useState("");
  const [characters, setCharacters] = useState("");
  const [ageGroup, setAgeGroup] = useState("");
  const [loading, setLoading] = useState(false);
  const [viewStory, setViewStory] = useState<Story | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [activeTab, setActiveTab] = useState("create");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      const fetchedStories = await listStories();
      setStories(fetchedStories);
    } catch (error) {
      console.error('Error fetching stories:', error);
    }
  };

  const handleGenerateStory = async () => {
    if (!theme || !characters || !ageGroup) {
      alert("Please fill in all fields to create your magical story!");
      return;
    }

    setLoading(true);
    
    try {
      // Split characters by commas and trim whitespace
      const charactersArray = characters.split(',')
        .map(char => char.trim())
        .filter(char => char.length > 0); // Filter out empty strings
      
      if (charactersArray.length === 0) {
        alert("Please add at least one character to your story!");
        setLoading(false);
        return;
      }
      
      await generateStory(theme, charactersArray, ageGroup);
      await fetchStories();
      // Show confetti when a story is successfully created
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 5000);
      
      // Clear form
      setTheme("");
      setCharacters("");
      setAgeGroup("");
      
      // Switch to the stories tab
      setActiveTab("stories");
    } catch (error) {
      console.error('Error generating story:', error);
      alert("Sorry, there was an error creating your story. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFavorite = async (storyId: number) => {
    try {
      const response = await toggleFavorite(storyId);
      await fetchStories();
      
      // Show appropriate toast based on favorite status
      if (response.isFavorite) {
        toast.success("Added to favorites!");
      } else {
        toast.success("Removed from favorites");
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      toast.error("Could not update favorite status. Please try again.");
    }
  };

  const handleCreateNew = () => {
    setActiveTab('create');
  };

  const handleDeleteStory = async (storyId: number) => {
    if (window.confirm("Are you sure you want to delete this story? This action cannot be undone.")) {
      try {
        await deleteStory(storyId);
        toast.success("Story deleted successfully!");
        
        // Close the modal if open
        if (viewStory && viewStory.id === storyId) {
          setViewStory(null);
        }
        
        // Refresh the stories list
        await fetchStories();
      } catch (error) {
        console.error('Error deleting story:', error);
        toast.error("Could not delete the story. Please try again.");
      }
    }
  };

  return (
    <div style={{
      position: 'relative',
      minHeight: '100vh',
      background: 'linear-gradient(to bottom, #70D6FF, #C0EAFF)',
      overflow: 'hidden', // Prevent shapes from overflowing
      fontFamily: 'Nunito, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
    }}>
      {/* --- Background Components --- */}
      <MovingClouds />
      <MovingBubbles />
      <FloatingItems />
      <div className="ground"></div>
      <BackgroundPatterns />
      <FloatingShapes />
      <PlayfulDecorations />

      <Toaster position="top-center" />
      <Confetti active={showConfetti} />
      
      {/* Header */}
      <AppHeader 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        storiesCount={stories.length}
      />
      
      {/* Main content */}
      <main className="content-area">
        {activeTab === 'create' && (
          <div className="adventure-layout">
            <AdventureMap 
              selectedTheme={theme} 
              onSelectTheme={setTheme}
              selectedAgeGroup={ageGroup}
              onSelectAgeGroup={setAgeGroup}
              storyCount={stories.length}
            />
            
            <CreateStorySection
              theme={theme}
              characters={characters}
              ageGroup={ageGroup}
              loading={loading}
              setCharacters={setCharacters}
              handleGenerateStory={handleGenerateStory}
            />
              </div>
        )}
        
        {(activeTab === 'stories' || activeTab === 'favorites') && (
          <>
            <h2 className="adventure-collection-title">
              {activeTab === 'stories' ? 'Your Story Collection' : 'Your Favorite Adventures'}
            </h2>
            
            <div className="stories-grid">
              {stories.length === 0 || (activeTab === 'favorites' && !stories.some(s => s.isFavorite)) ? (
                <div className="col-span-full">
                  <EmptyState onCreateNew={handleCreateNew} />
                </div>
              ) : (
                (activeTab === 'stories' ? stories : stories.filter(s => s.isFavorite)).map(story => (
                  <StoryCard 
                    key={story.id}
                    story={story} 
                    onView={setViewStory}
                    onToggleFavorite={handleToggleFavorite}
                    onDelete={handleDeleteStory}
                  />
                ))
              )}
            </div>
          </>
        )}
      </main>
      
      {/* Footer */}
      <AppFooter />
      
      {viewStory && (
        <StoryModal
          story={viewStory}
          isOpen={viewStory !== null}
          onClose={() => setViewStory(null)}
          onToggleFavorite={handleToggleFavorite}
          onDelete={handleDeleteStory}
        />
      )}
    </div>
  );
}
