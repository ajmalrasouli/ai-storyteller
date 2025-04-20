# AI Storyteller

An interactive AI-powered storytelling application that generates personalized children's stories based on themes, characters, and age groups.

## Features

- 🤖 AI-powered story generation using Azure OpenAI
- 📚 Multiple age group support (3-5, 5-8, 8-12 years)
- 🎨 Various story themes (Friendship, Adventure, Nature, etc.)
- ⭐ Story favoriting system
- 🎯 Educational focus with learning objectives
- ✨ Modern, animated UI with Framer Motion

## Tech Stack

- Frontend: React + Vite + TypeScript
- Backend: Flask + SQLAlchemy
- AI: Azure OpenAI
- Styling: TailwindCSS
- Animations: Framer Motion

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ajmalrasouli/ai-storyteller.git
   cd ai-storyteller
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory with your Azure OpenAI credentials:
   ```
   DATABASE_URL=sqlite:///stories.db
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

4. Start the development servers:
   ```bash
   # Start the Flask backend
   python app.py
   
   # In a separate terminal, start the frontend
   npm run dev:frontend
   ```

## Environment Variables

- `DATABASE_URL`: SQLite database URL
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `FLASK_APP`: Flask application entry point
- `FLASK_ENV`: Flask environment (development/production)

## Development

- `npm run dev:frontend`: Start frontend development server
- `python app.py`: Start backend server
- `npm run build`: Build frontend for production

## License

MIT
