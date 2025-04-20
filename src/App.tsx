import { Authenticated, Unauthenticated, useQuery, useMutation, useAction } from "convex/react";
import { api } from "../convex/_generated/api";
import { SignInForm } from "./SignInForm";
import { SignOutButton } from "./SignOutButton";
import { useState, useEffect } from "react";
import { Toaster, toast } from "sonner";
import { motion, AnimatePresence, useAnimation } from "framer-motion";

// Theme definitions
const themes = [
  {
    value: "friendship",
    label: "Friendship",
    icon: "🤝",
    description: "Stories about making friends and being kind"
  },
  {
    value: "adventure",
    label: "Adventure",
    icon: "🗺️",
    description: "Epic quests and exciting journeys"
  },
  {
    value: "nature",
    label: "Nature",
    icon: "🌳",
    description: "Tales about animals and the environment"
  },
  {
    value: "magic",
    label: "Magic",
    icon: "✨",
    description: "Magical stories with wonder and fantasy"
  },
  {
    value: "learning",
    label: "Learning",
    icon: "📚",
    description: "Educational stories that teach new things"
  },
  {
    value: "family",
    label: "Family",
    icon: "👨‍👩‍👧‍👦",
    description: "Stories about family love and togetherness"
  }
];

// Age group definitions
const ageGroups = [
  {
    value: "3-5",
    label: "Preschool",
    icon: "🎨",
    description: "Simple, colorful stories"
  },
  {
    value: "5-8",
    label: "Early readers",
    icon: "📖",
    description: "Engaging tales with morals"
  },
  {
    value: "8-12",
    label: "Confident readers",
    icon: "🚀",
    description: "More complex adventures"
  }
];

// Interactive background patterns
function BackgroundPatterns() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* Floating shapes */}
      <FloatingShapes />
      {/* Animated patterns */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-0 w-full h-full pattern-dots" />
        <div className="absolute top-0 left-0 w-full h-full pattern-crosses rotate-45 scale-150" />
      </div>
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/80 via-purple-50/80 to-pink-50/80" />
    </div>
  );
}

// Enhanced floating shapes with more variety
function FloatingShapes() {
  return (
    <>
      {[...Array(25)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute"
          initial={{
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            scale: Math.random() * 0.5 + 0.5,
            rotate: Math.random() * 360,
          }}
          animate={{
            x: [
              Math.random() * window.innerWidth,
              Math.random() * window.innerWidth,
              Math.random() * window.innerWidth,
            ],
            y: [
              Math.random() * window.innerHeight,
              Math.random() * window.innerHeight,
              Math.random() * window.innerHeight,
            ],
            rotate: [0, 180, 360],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: Math.random() * 20 + 20,
            repeat: Infinity,
            ease: "linear",
            times: [0, 0.5, 1],
          }}
        >
          <div 
            className={`opacity-10 ${
              i % 4 === 0 
                ? "w-12 h-12 bg-indigo-400 rounded-full" 
                : i % 4 === 1 
                ? "w-10 h-10 bg-pink-400 rounded" 
                : i % 4 === 2
                ? "w-8 h-8 bg-yellow-400 triangle"
                : "w-16 h-16 bg-purple-400 star"
            }`}
          />
        </motion.div>
      ))}
    </>
  );
}

// Interactive card component with hover effects
function StoryCard({ story, onToggleFavorite }: { 
  story: any; 
  onToggleFavorite: (id: string) => void;
}) {
  const controls = useAnimation();
  
  useEffect(() => {
    controls.start({ scale: 1, opacity: 1 });
  }, []);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.8 }}
      animate={controls}
      whileHover={{ 
        scale: 1.02,
        boxShadow: "0 25px 30px -5px rgba(0, 0, 0, 0.1), 0 15px 15px -5px rgba(0, 0, 0, 0.04)",
      }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="p-8 bg-white/80 backdrop-blur-sm rounded-xl shadow-xl transform-gpu max-w-4xl mx-auto"
    >
      <motion.div 
        className="flex justify-between items-start mb-6"
        whileHover={{ y: -2 }}
      >
        <h3 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
          {story.title}
        </h3>
        <motion.button
          onClick={() => onToggleFavorite(story._id)}
          className={`text-4xl ${story.isFavorite ? 'text-yellow-500' : 'text-gray-300'}`}
          whileHover={{ scale: 1.2, rotate: [0, -10, 10, 0] }}
          whileTap={{ scale: 0.8 }}
          transition={{ type: "spring", stiffness: 400, damping: 10 }}
        >
          {story.isFavorite ? "★" : "☆"}
        </motion.button>
      </motion.div>
      <motion.p 
        className="text-xl leading-relaxed text-gray-700 whitespace-pre-wrap mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        {story.content}
      </motion.p>
      <motion.div 
        className="mt-6 flex flex-wrap gap-3"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        {story.characters.map((char: string, i: number) => (
          <motion.span
            key={i}
            className="px-5 py-2 bg-indigo-100 rounded-full text-lg font-medium"
            whileHover={{ scale: 1.1, backgroundColor: "#e0e7ff" }}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            {char}
          </motion.span>
        ))}
      </motion.div>
      <motion.div 
        className="mt-4 text-lg text-gray-600 font-medium"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        Age group: {story.ageGroup}
      </motion.div>
    </motion.div>
  );
}

// Theme selector with visual feedback
function ThemeSelector({ value, onChange, themes }: {
  value: string;
  onChange: (value: string) => void;
  themes: Array<{
    value: string;
    label: string;
    icon: string;
    description: string;
  }>;
}) {
  return (
    <div className="space-y-4">
      <label className="block text-xl font-bold mb-4">Story Theme</label>
      <div className="grid grid-cols-2 gap-6 sm:grid-cols-3">
        {themes.map((t) => (
          <motion.button
            key={t.value}
            onClick={() => onChange(t.value)}
            className={`p-6 rounded-xl text-left transition-colors ${
              value === t.value 
                ? 'bg-indigo-100 border-3 border-indigo-500' 
                : 'bg-white/80 border-3 border-transparent hover:border-indigo-200'
            }`}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="text-4xl mb-3 block">{t.icon}</span>
            <span className="text-xl font-bold block mb-2">{t.label}</span>
            <span className="text-lg text-gray-600">{t.description}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [currentTheme, setCurrentTheme] = useState("default");
  
  const themeStyles = {
    default: "from-indigo-50 via-purple-50 to-pink-50",
    fantasy: "from-blue-50 via-purple-50 to-pink-50",
    nature: "from-green-50 via-emerald-50 to-teal-50",
    space: "from-slate-800 via-purple-900 to-slate-900 text-white",
  };

  return (
    <div className={`min-h-screen flex flex-col bg-gradient-to-br ${themeStyles[currentTheme as keyof typeof themeStyles]} transition-colors duration-1000`}>
      <BackgroundPatterns />
      <header className="sticky top-0 z-10 bg-white/80 backdrop-blur-sm p-4 flex justify-between items-center border-b">
        <div className="flex items-center gap-4">
          <motion.h2 
            className="text-xl font-semibold text-indigo-600"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            AI Storyteller
          </motion.h2>
          <div className="flex gap-2">
            {Object.keys(themeStyles).map((theme) => (
              <motion.button
                key={theme}
                onClick={() => setCurrentTheme(theme)}
                className={`w-6 h-6 rounded-full ${
                  theme === currentTheme ? 'ring-2 ring-offset-2 ring-indigo-500' : ''
                }`}
                whileHover={{ scale: 1.2 }}
                whileTap={{ scale: 0.9 }}
                style={{
                  background: theme === 'default' ? 'linear-gradient(135deg, #818cf8, #c084fc, #f472b6)' :
                           theme === 'fantasy' ? 'linear-gradient(135deg, #60a5fa, #c084fc, #f472b6)' :
                           theme === 'nature' ? 'linear-gradient(135deg, #34d399, #10b981, #14b8a6)' :
                           'linear-gradient(135deg, #1e293b, #6b21a8, #1e293b)'
                }}
              />
            ))}
          </div>
        </div>
        <SignOutButton />
      </header>
      <main className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-4xl mx-auto">
          <Content />
        </div>
      </main>
      <Toaster />
    </div>
  );
}

function Content() {
  const [theme, setTheme] = useState("");
  const [characters, setCharacters] = useState<string[]>([]);
  const [ageGroup, setAgeGroup] = useState("5-8");
  const [newCharacter, setNewCharacter] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  
  const stories = useQuery(api.stories.listStories);
  const generateStory = useAction(api.stories.generateStory);
  const toggleFavorite = useMutation(api.stories.toggleFavorite);

  const handleAddCharacter = () => {
    if (newCharacter && !characters.includes(newCharacter)) {
      setCharacters([...characters, newCharacter]);
      setNewCharacter("");
    }
  };

  const handleGenerateStory = async () => {
    if (!theme || characters.length === 0) {
      toast.error("Please enter a theme and at least one character");
      return;
    }

    setIsGenerating(true);
    try {
      await generateStory({ theme, characters, ageGroup });
      toast.success("Story created successfully!");
      setTheme("");
      setCharacters([]);
    } catch (error) {
      toast.error("Failed to create story. Please try again.");
      console.error("Story generation error:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <div className="text-center">
        <motion.h1 
          className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-4 animate-gradient"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          AI Storyteller
        </motion.h1>
        <Authenticated>
          <motion.div 
            className="max-w-xl mx-auto space-y-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <ThemeSelector value={theme} onChange={setTheme} themes={themes} />

            <div className="space-y-2">
              <label className="block text-sm font-medium">Characters</label>
              <div className="flex gap-2">
                <motion.input
                  type="text"
                  value={newCharacter}
                  onChange={(e) => setNewCharacter(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAddCharacter()}
                  placeholder="Add a character"
                  className="flex-1 p-2 border rounded bg-white/80 backdrop-blur-sm"
                  whileFocus={{ scale: 1.02 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                />
                <motion.button
                  onClick={handleAddCharacter}
                  className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Add
                </motion.button>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                <AnimatePresence>
                  {characters.map((char, i) => (
                    <motion.span 
                      key={char}
                      initial={{ opacity: 0, scale: 0, rotate: -180 }}
                      animate={{ opacity: 1, scale: 1, rotate: 0 }}
                      exit={{ opacity: 0, scale: 0, rotate: 180 }}
                      className="px-3 py-1 bg-white/80 backdrop-blur-sm rounded-full flex items-center gap-2 shadow-sm"
                    >
                      {char}
                      <button
                        onClick={() => setCharacters(characters.filter((_, idx) => idx !== i))}
                        className="text-indigo-600 hover:text-indigo-800"
                      >
                        ×
                      </button>
                    </motion.span>
                  ))}
                </AnimatePresence>
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium">Age Group</label>
              <select
                value={ageGroup}
                onChange={(e) => setAgeGroup(e.target.value)}
                className="w-full p-2 border rounded bg-white/80 backdrop-blur-sm"
              >
                {ageGroups.map((ag) => (
                  <option key={ag.value} value={ag.value}>
                    {ag.icon} {ag.label} - {ag.description}
                  </option>
                ))}
              </select>
            </div>

            <motion.button
              onClick={handleGenerateStory}
              disabled={isGenerating || !theme || characters.length === 0}
              className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              whileHover={{ scale: 1.02, boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}
              whileTap={{ scale: 0.98 }}
            >
              {isGenerating ? (
                <div className="flex items-center justify-center gap-2">
                  <motion.div
                    className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  />
                  Creating Story...
                </div>
              ) : (
                "Generate Story"
              )}
            </motion.button>
          </motion.div>

          <motion.div 
            className="mt-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <h2 className="text-2xl font-bold mb-6">Your Stories</h2>
            <div className="grid gap-6 md:grid-cols-2">
              <AnimatePresence>
                {stories?.map((story) => (
                  <StoryCard 
                    key={story._id} 
                    story={story} 
                    onToggleFavorite={toggleFavorite}
                  />
                ))}
              </AnimatePresence>
            </div>
          </motion.div>
        </Authenticated>
        
        <Unauthenticated>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-xl text-slate-600 mb-4">Sign in to create magical stories!</p>
            <SignInForm />
          </motion.div>
        </Unauthenticated>
      </div>
    </div>
  );
}
