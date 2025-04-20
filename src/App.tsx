import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Toaster, toast } from "sonner";
import { generateStory, listStories, toggleFavorite } from "./lib/api";

const themes = [
  "Adventure",
  "Friendship",
  "Animals",
  "Space",
  "Magic",
  "Sports",
  "Nature",
  "Music",
  "Art",
  "Science",
];

const ageGroups = [
  { label: "3-5 years", value: "3-5" },
  { label: "6-8 years", value: "6-8" },
  { label: "9-12 years", value: "9-12" },
];

function BackgroundPatterns() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-50 to-blue-50" />
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
    </div>
  );
}

function FloatingShapes() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <motion.div
        className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-purple-200/30"
        animate={{
          scale: [1, 1.2, 1],
          x: [0, 20, 0],
          y: [0, -20, 0],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
      <motion.div
        className="absolute bottom-1/4 right-1/4 w-64 h-64 rounded-full bg-blue-200/30"
        animate={{
          scale: [1, 1.2, 1],
          x: [0, -20, 0],
          y: [0, 20, 0],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    </div>
  );
}

// Modal component to display full story
function StoryModal({ story, isOpen, onClose }: { story: any; isOpen: boolean; onClose: () => void }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold text-gray-900">{story.title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="flex flex-wrap gap-2 mb-4">
          <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
            {story.theme}
          </span>
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
            {story.ageGroup} years
          </span>
          {story.characters.map((character: string, index: number) => (
            <span
              key={index}
              className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
            >
              {character}
            </span>
          ))}
        </div>
        
        <div className="prose prose-lg max-w-none">
          {story.content.split('\n').map((paragraph: string, index: number) => (
            paragraph.trim() ? <p key={index}>{paragraph}</p> : <br key={index} />
          ))}
        </div>
        
        <div className="mt-6 text-right">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function StoryCard({ story, onToggleFavorite }: { story: any; onToggleFavorite: (id: number) => void }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-lg p-6 space-y-4"
      >
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-bold text-gray-900">{story.title}</h3>
          <button
            onClick={() => onToggleFavorite(story.id)}
            className={`p-2 rounded-full ${
              story.isFavorite ? "text-yellow-500" : "text-gray-400"
            } hover:text-yellow-500 transition-colors`}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill={story.isFavorite ? "currentColor" : "none"}
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
              />
            </svg>
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
            {story.theme}
          </span>
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
            {story.ageGroup} years
          </span>
        </div>
        <div className="flex flex-wrap gap-2">
          {story.characters.map((character: string, index: number) => (
            <span
              key={index}
              className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
            >
              {character}
            </span>
          ))}
        </div>
        <div 
          className="text-gray-600 line-clamp-3 cursor-pointer hover:text-purple-600"
          onClick={() => setIsModalOpen(true)}
        >
          {story.content}
        </div>
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-500">
            {new Date(story.createdAt).toLocaleDateString()}
          </div>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="text-sm text-purple-600 hover:text-purple-800 font-medium"
          >
            Read Full Story
          </button>
        </div>
      </motion.div>
      
      <StoryModal 
        story={story} 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
      />
    </>
  );
}

export default function App() {
  const [stories, setStories] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState("");
  const [characters, setCharacters] = useState<string[]>([]);
  const [characterInput, setCharacterInput] = useState("");
  const [ageGroup, setAgeGroup] = useState("");

  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      const response = await listStories();
      setStories(response);
    } catch (error) {
      console.error("Error fetching stories:", error);
      toast.error("Failed to fetch stories");
    }
  };

  const handleGenerateStory = async () => {
    if (!theme || characters.length === 0 || !ageGroup) {
      toast.error("Please fill in all fields");
      return;
    }

    setIsLoading(true);
    try {
      const newStory = await generateStory(theme, characters, ageGroup);
      setStories([newStory, ...stories]);
      setTheme("");
      setCharacters([]);
      setCharacterInput("");
      setAgeGroup("");
      toast.success("Story generated successfully!");
    } catch (error) {
      console.error("Error generating story:", error);
      toast.error("Failed to generate story");
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleFavorite = async (storyId: number) => {
    try {
      const updatedStory = await toggleFavorite(storyId);
      setStories(
        stories.map((story) =>
          story.id === storyId ? updatedStory : story
        )
      );
    } catch (error) {
      console.error("Error toggling favorite:", error);
      toast.error("Failed to update favorite status");
    }
  };

  const addCharacter = () => {
    if (characterInput.trim() && !characters.includes(characterInput.trim())) {
      setCharacters([...characters, characterInput.trim()]);
      setCharacterInput("");
    }
  };

  const removeCharacter = (characterToRemove: string) => {
    setCharacters(characters.filter((char) => char !== characterToRemove));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <BackgroundPatterns />
      <FloatingShapes />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-bold text-gray-900 mb-4"
          >
            AI Storyteller
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-gray-600"
          >
            Create magical stories for children
          </motion.p>
        </header>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-lg shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Create a New Story
          </h2>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Theme
              </label>
              <select
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Select a theme</option>
                {themes.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Characters
              </label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={characterInput}
                  onChange={(e) => setCharacterInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && addCharacter()}
                  placeholder="Add a character"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <button
                  onClick={addCharacter}
                  className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {characters.map((character) => (
                  <span
                    key={character}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800"
                  >
                    {character}
                    <button
                      onClick={() => removeCharacter(character)}
                      className="ml-2 text-purple-600 hover:text-purple-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Age Group
              </label>
              <select
                value={ageGroup}
                onChange={(e) => setAgeGroup(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Select age group</option>
                {ageGroups.map((group) => (
                  <option key={group.value} value={group.value}>
                    {group.label}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={handleGenerateStory}
              disabled={isLoading}
              className="w-full px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Generating..." : "Generate Story"}
            </button>
          </div>
        </motion.div>

        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Stories</h2>
          {stories.length === 0 ? (
            <p className="text-center text-gray-500">No stories yet. Create one!</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {stories.map((story) => (
                <StoryCard
                  key={story.id}
                  story={story}
                  onToggleFavorite={handleToggleFavorite}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      <Toaster position="top-right" />
    </div>
  );
}
