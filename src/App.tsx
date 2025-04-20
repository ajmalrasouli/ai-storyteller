import React, { useEffect, useState } from 'react';
import { generateStory, listStories, Story, toggleFavorite } from './lib/api';
import { Toaster } from 'react-hot-toast';
import './App.css';

// Enhanced themes with emojis
const themes = ["🚀 Space Adventure", "🏰 Magic Kingdom", "🌊 Ocean Explorer", "🐯 Jungle Safari", "🦕 Dinosaur World"];

// Enhanced age groups with emojis
const ageGroups = [
  "🧒 Little Explorers (3-5 years)",
  "👦 Curious Minds (6-8 years)", 
  "👧 Young Adventurers (9-12 years)"
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
const StoryCard = ({ story, onView, onToggleFavorite }: { 
  story: Story, 
  onView: (story: Story) => void, 
  onToggleFavorite: (storyId: number) => void 
}) => {
  const themeIcon = getThemeIcon(story.theme);
  
  return (
    <div className="story-card" onClick={() => onView(story)}>
      <div className="story-card-header">
        <div className="theme-badge">{themeIcon} {story.theme.split(' ')[1]}</div>
        <button 
          className="favorite-btn"
          onClick={(e) => {
            e.stopPropagation();
            onToggleFavorite(story.id);
          }}
        >
          <span className="text-3xl">{story.isFavorite ? '❤️' : '🤍'}</span>
        </button>
      </div>
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
}

const StoryModal = ({ story, isOpen, onClose, onToggleFavorite }: StoryModalProps) => {
  if (!isOpen) return null;

  const handlePrint = () => {
    // Create a new window with just the story content for printing
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>${story.title}</title>
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
            </style>
          </head>
          <body>
            <h1>${story.title}</h1>
            <div class="story-meta">
              <div>Theme: ${story.theme}</div>
              <div>Age Group: ${story.ageGroup}</div>
              <div>Date: ${new Date(story.createdAt).toLocaleDateString()}</div>
            </div>
            ${story.content.split("\n\n").map((paragraph: string) => `<p>${paragraph}</p>`).join('')}
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
    }
  };

  const handleEmail = () => {
    const subject = encodeURIComponent(`Story: ${story.title}`);
    const body = encodeURIComponent(
      `${story.title}\n\n` +
      `Theme: ${story.theme}\n` +
      `Age Group: ${story.ageGroup}\n\n` +
      `${story.content}\n\n` +
      `Created with AI Storyteller`
    );
    window.location.href = `mailto:?subject=${subject}&body=${body}`;
  };

  return (
    <div style={styles.storyModalOverlay} onClick={onClose}>
      <div style={styles.storyModal} onClick={(e) => e.stopPropagation()}>
        <div style={styles.modalHeader}>
          <h2 style={styles.modalTitle}>{story.title}</h2>
          <button style={styles.closeModal} onClick={onClose}>×</button>
        </div>
        <div className="modal-content">
          <div className="modal-story-meta">
            <span className="modal-story-theme">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M2 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 6.586 1H2zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
              </svg>
              {story.theme}
            </span>
            <span className="modal-story-age">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
              </svg>
              {story.ageGroup}
            </span>
          </div>
          {story.content.split("\n\n").map((paragraph: string, index: number) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
        <div className="modal-footer" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #eee', padding: '15px 20px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              className={`favorite-button ${story.isFavorite ? 'active' : ''}`}
              onClick={() => onToggleFavorite(story.id)}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '6px',
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '4px',
                cursor: 'pointer',
                color: story.isFavorite ? '#ff6b6b' : '#666',
                fontWeight: 'bold'
              }}
            >
              {story.isFavorite ? '❤️' : '🤍'} {story.isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
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
          </div>
          
          <span className="story-date" style={{ color: '#888', fontSize: '0.9rem' }}>
            {new Date(story.createdAt).toLocaleDateString()}
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
    color: '#9333ea',
    border: 'none',
    borderRadius: '25px',
    padding: '10px 20px',
    fontSize: '1.1rem',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 0 rgba(0, 0, 0, 0.1)',
    display: 'flex',
    alignItems: 'center',
    gap: '6px'
  };

  const activeButtonStyle: React.CSSProperties = {
    ...navButtonStyle,
    backgroundColor: '#ff6b6b',
    color: 'white',
    transform: 'translateY(-3px)',
    boxShadow: '0 7px 0 rgba(0, 0, 0, 0.1)'
  };

  return (
    <header className="app-header">
      <img 
        src="/banner.svg" 
        alt="AI Storyteller Banner" 
        className="absolute top-0 left-0 w-full h-full object-cover"
      />
      <div className="relative z-10">
        <h1>✨ AI Storyteller ✨</h1>
        <div className="nav-tabs">
          <button 
            style={activeTab === 'create' ? activeButtonStyle : navButtonStyle}
            onClick={() => setActiveTab('create')}
          >
            ✏️ Create Story
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
      {themes.map((theme, index) => {
        const icon = getThemeIcon(theme);
        const name = theme.split(' ').slice(1).join(' ');
        
        return (
          <button
            key={index}
            style={selectedTheme === theme ? activeThemeStyle : themeButtonStyle}
            onClick={() => onSelectTheme(theme)}
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
      {ageGroups.map((ageGroup, index) => {
        const parts = ageGroup.split('(');
        const label = parts[0].trim();
        const range = parts[1] ? `(${parts[1]}` : '';
        const icon = getAgeGroupEmoji(ageGroup);
        
        return (
          <button
            key={index}
            style={selectedAgeGroup === ageGroup ? activeAgeStyle : ageButtonStyle}
            onClick={() => onSelectAgeGroup(ageGroup)}
          >
            <span style={iconStyle}>{icon}</span>
            <span style={labelStyle}>{label}</span>
            <span style={rangeStyle}>{range}</span>
          </button>
        );
      })}
    </div>
  );
};

// Footer component
const AppFooter = () => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-logo">✨ AI Storyteller ✨</div>
        <p>Create magical stories for children of all ages!</p>
        
        <div className="footer-links">
          <a href="#" className="footer-link">About</a>
          <a href="#" className="footer-link">Privacy Policy</a>
          <a href="#" className="footer-link">Contact Us</a>
          <a href="#" className="footer-link">Help</a>
        </div>
        
        <p className="text-sm">© 2025 AI Storyteller. All rights reserved.</p>
      </div>
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

export default function App() {
  const [stories, setStories] = useState<Story[]>([]);
  const [theme, setTheme] = useState("");
  const [characters, setCharacters] = useState("");
  const [ageGroup, setAgeGroup] = useState("");
  const [loading, setLoading] = useState(false);
  const [viewStory, setViewStory] = useState<Story | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [activeTab, setActiveTab] = useState("create");

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
      await toggleFavorite(storyId);
      await fetchStories();
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const handleCreateNew = () => {
    setActiveTab('create');
  };

  return (
    <div style={styles.appContainer}>
      <div style={styles.appBackground}>
        <div style={styles.backgroundWhite}></div>
      </div>
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
          <div className="create-story-container">
            <h2>Create Your Own Magical Story!</h2>
            
            <div className="form-group">
              <label>
                <span className="inline-block mr-2">🎭</span> Pick a Theme:
              </label>
              <ThemeSelector 
                selectedTheme={theme} 
                onSelectTheme={setTheme} 
              />
            </div>
            
            <div className="form-group">
              <label>
                <span className="inline-block mr-2">👨‍👩‍👧‍👦</span> Add Characters:
              </label>
              <div className="character-input-container">
                <textarea
                  className="form-control"
                  placeholder="Enter characters for your story (e.g., 'a brave knight named Max, a friendly dragon named Sparky')"
                  value={characters}
                  onChange={(e) => setCharacters(e.target.value)}
                  rows={3}
                />
                {characters.length === 0 && (
                  <div className="character-suggestions">
                    <div className="suggestion-title">Try these characters:</div>
                    <div className="suggestion-list">
                      <span className="suggestion-item" onClick={() => setCharacters("a brave princess, a talking cat, a wise wizard")}>Princess & Friends</span>
                      <span className="suggestion-item" onClick={() => setCharacters("a curious alien, a friendly robot, a space explorer")}>Space Crew</span>
                      <span className="suggestion-item" onClick={() => setCharacters("a playful puppy, a grumpy cat, a clever rabbit")}>Animal Adventures</span>
                      <span className="suggestion-item" onClick={() => setCharacters("a magical unicorn, a tiny fairy, a friendly dragon")}>Magical Creatures</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            <div className="form-group">
              <label>
                <span className="inline-block mr-2">📚</span> Choose Age Group:
              </label>
              <AgeGroupSelector 
                selectedAgeGroup={ageGroup} 
                onSelectAgeGroup={setAgeGroup} 
              />
            </div>
            
            <button
              className="btn btn-primary btn-full mt-6"
              onClick={handleGenerateStory}
              disabled={loading || !theme || !characters || !ageGroup}
              style={{ 
                backgroundColor: '#9333ea', 
                color: 'white', 
                fontWeight: 'bold',
                padding: '12px 24px',
                width: '100%',
                borderRadius: '8px',
                fontSize: '1.2rem',
                boxShadow: '0 4px 0 rgba(121, 45, 196, 0.5)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '10px'
              }}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Creating Your Story...
                </>
              ) : (
                <span>✨ Create Magical Story ✨</span>
              )}
            </button>
          </div>
        )}
        
        {(activeTab === 'stories' || activeTab === 'favorites') && (
          <>
            <h2 className="text-2xl font-bold mb-4 text-center">
              {activeTab === 'stories' ? 'All Your Magical Stories' : 'Your Favorite Stories'}
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
        />
      )}
    </div>
  );
}
