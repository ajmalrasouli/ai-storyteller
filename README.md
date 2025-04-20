# AI Storyteller

An interactive AI-powered storytelling application that generates personalized children's stories based on themes, characters, and age groups.

## Features

- 🤖 AI-powered story generation using Azure OpenAI
- 📚 Multiple age group support (3-5, 6-8, 9-12 years)
- 🎨 Various story themes (Space Adventure, Magic Kingdom, Ocean Explorer, etc.)
- ⭐ Story favoriting system
- 📧 Email stories directly from the application
- 🖨️ Print-friendly story formatting
- 🎯 Educational focus with learning objectives
- ✨ Modern, animated UI with visual feedback

## Tech Stack

- Frontend: React + TypeScript
- Backend: Flask + SQLAlchemy
- AI: Azure OpenAI (GPT-4 Mini)
- Database: SQLite
- Styling: CSS with inline styles for consistent rendering

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ajmalrasouli/ai-storyteller.git
   cd ai-storyteller
   ```

2. Install dependencies:
   ```bash
   npm install
   pip install -r requirements.txt
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

## Using the Application

1. **Create a Story**:
   - Select a theme (Space Adventure, Magic Kingdom, etc.)
   - Add characters (comma-separated)
   - Choose an age group
   - Click "Create Magical Story" to generate

2. **View Stories**:
   - Browse all stories in the "My Stories" tab
   - View favorite stories in the "Favorites" tab
   - Click on a story card to view the full content

3. **Story Actions**:
   - Add/remove stories from favorites
   - Email stories to share them with others
   - Print stories in a nicely formatted layout

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
