# AI Storyteller

An interactive AI-powered storytelling application that generates personalized children's stories based on themes, characters, and age groups.

## Features

- 🤖 AI-powered story generation using OpenAI's GPT-4
- 👥 User authentication
- 📚 Multiple age group support (3-5, 5-8, 8-12 years)
- 🎨 Various story themes (Friendship, Adventure, Nature, etc.)
- ⭐ Story favoriting system
- 🎯 Educational focus with learning objectives
- ✨ Modern, animated UI with Framer Motion

## Tech Stack

- Frontend: React + Vite + TypeScript
- Backend: Convex
- AI: OpenAI GPT-4
- Styling: TailwindCSS
- Animations: Framer Motion

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd ai-storyteller
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the root directory with your Convex and OpenAI credentials:
   ```
   CONVEX_DEPLOY_KEY=your_convex_deploy_key
   CONVEX_DEPLOYMENT=your_convex_deployment
   VITE_CONVEX_URL=your_convex_url
   CONVEX_OPENAI_API_KEY=your_openai_api_key
   CONVEX_OPENAI_BASE_URL=https://api.openai.com/v1
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

- `CONVEX_DEPLOY_KEY`: Your Convex deployment key
- `CONVEX_DEPLOYMENT`: Your Convex deployment name
- `VITE_CONVEX_URL`: Your Convex deployment URL
- `CONVEX_OPENAI_API_KEY`: Your OpenAI API key
- `CONVEX_OPENAI_BASE_URL`: OpenAI API base URL

## Development

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run lint`: Run TypeScript type checking

## License

MIT
