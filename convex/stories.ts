import { v } from "convex/values";
import { action, mutation, query } from "./_generated/server";
import { api } from "./_generated/api";
import OpenAI from "openai";

// Add "use node" directive for OpenAI
"use node";

const openai = new OpenAI({
  baseURL: process.env.CONVEX_OPENAI_BASE_URL,
  apiKey: process.env.CONVEX_OPENAI_API_KEY,
});

// Story templates based on age groups
const storyTemplates = {
  "3-5": {
    complexity: "very simple",
    length: "2-3 minutes",
    focus: "basic emotions, colors, numbers, and simple actions",
    structure: "repetitive patterns and clear cause-effect relationships",
  },
  "5-8": {
    complexity: "simple to moderate",
    length: "5-7 minutes",
    focus: "friendship, sharing, problem-solving, and basic life lessons",
    structure: "clear beginning, middle, and end with a simple conflict and resolution",
  },
  "8-12": {
    complexity: "moderate",
    length: "8-10 minutes",
    focus: "teamwork, responsibility, courage, and complex emotions",
    structure: "more detailed plot with character development and multiple events",
  },
};

// Educational themes with learning objectives
const educationalThemes = {
  friendship: ["empathy", "sharing", "communication"],
  nature: ["environmental awareness", "animal habitats", "conservation"],
  adventure: ["problem-solving", "courage", "teamwork"],
  family: ["relationships", "responsibility", "care"],
  learning: ["curiosity", "persistence", "growth mindset"],
  diversity: ["acceptance", "cultural awareness", "inclusion"],
};

function getStoryPrompt(theme: string, characters: string[], ageGroup: string): string {
  const template = storyTemplates[ageGroup as keyof typeof storyTemplates];
  const learningGoals = educationalThemes[theme as keyof typeof educationalThemes] || 
    educationalThemes.friendship; // Default to friendship themes

  return `Create an engaging children's story with these specifications:

Age Group (${ageGroup} years):
- Complexity: ${template.complexity}
- Target Length: ${template.length}
- Focus Areas: ${template.focus}
- Story Structure: ${template.structure}

Characters: ${characters.join(", ")}
Theme: ${theme}
Learning Goals: ${learningGoals.join(", ")}

Story Requirements:
1. Include interactive elements (questions, simple puzzles, or counting opportunities)
2. Create clear character personalities and relationships
3. Include a moral lesson about ${theme}
4. Add age-appropriate humor and engaging dialogue
5. Include opportunities for learning ${learningGoals[0]} and ${learningGoals[1]}

Please write the story in a clear, engaging style with natural dialogue and descriptive language appropriate for ${ageGroup} year olds.`;
}

export const generateStory = action({
  args: {
    theme: v.string(),
    characters: v.array(v.string()),
    ageGroup: v.string(),
  },
  handler: async (ctx, args) => {
    try {
      console.log("Starting story generation with args:", args);
      
      const prompt = getStoryPrompt(args.theme, args.characters, args.ageGroup);
      console.log("Sending prompt to OpenAI:", prompt);
      
      const response = await openai.chat.completions.create({
        model: "gpt-4.1-nano",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.7
      });

      console.log("Received response from OpenAI");
      
      const story = response.choices[0].message.content;
      if (!story) {
        console.error("No story content in OpenAI response");
        throw new Error("No story generated");
      }

      console.log("Saving story to database");
      
      await ctx.runMutation(api.stories.saveStory, {
        title: `Story about ${args.theme}`,
        content: story,
        theme: args.theme,
        characters: args.characters,
        ageGroup: args.ageGroup,
      });

      return story;
    } catch (error) {
      console.error("Story generation error:", error);
      if (error instanceof Error) {
        throw new Error(`Story generation failed: ${error.message}`);
      }
      throw new Error("Failed to generate story. Please try again.");
    }
  },
});

export const saveStory = mutation({
  args: {
    title: v.string(),
    content: v.string(),
    theme: v.string(),
    characters: v.array(v.string()),
    ageGroup: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.auth.getUserIdentity();
    if (!user) throw new Error("Not authenticated");
    
    return await ctx.db.insert("stories", {
      ...args,
      authorId: user.subject,
      isFavorite: false,
    });
  },
});

export const listStories = query({
  handler: async (ctx) => {
    const user = await ctx.auth.getUserIdentity();
    if (!user) return [];

    return await ctx.db
      .query("stories")
      .withIndex("by_author", (q) => q.eq("authorId", user.subject))
      .order("desc")
      .collect();
  },
});

export const toggleFavorite = mutation({
  args: { storyId: v.id("stories") },
  handler: async (ctx, args) => {
    const story = await ctx.db.get(args.storyId);
    if (!story) throw new Error("Story not found");
    
    await ctx.db.patch(args.storyId, {
      isFavorite: !story.isFavorite,
    });
  },
});
