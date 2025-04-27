# AI Storyteller

An interactive AI-powered storytelling application that generates personalized children's stories based on themes, characters, and age groups.

## Video Demo

[![AI Storyteller Demo](https://img.youtube.com/vi/6-H0OcEAI7s/0.jpg)](https://youtu.be/M3X0Q5n2AjA)

*Click the image above to watch the demo video*

## Screenshots

| ![Adventure](frontend/public/images/adventure.png) | ![Story Creation](frontend/public/images/story.png) |
|:---:|:---:|
| *Adventure Map* | *Story Creation* |

| ![My Stories](frontend/public/images/mystories.png) | ![Favorites](frontend/public/images/favorites.png) |
|:---:|:---:|
| *My Stories* | *Favorites* |

| ![Story Page View](frontend/public/images/storypage.png) | ![About](frontend/public/images/about.png) |
|:---:|:---:|
| *Story Page with Read Aloud* | *About* |

## Features

- 🤖 AI-powered story generation using Azure OpenAI (GPT-4)
- 🎨 AI-generated illustrations using Azure DALL-E 3
  - Child-friendly, whimsical digital art style
  - Theme and character-specific illustrations
  - Age-appropriate visual content
  - Automatic regeneration option
  - Fallback to curated theme-based images
- 🗣️ High-quality text-to-speech using Azure Speech Service
  - Natural-sounding voices with multiple language support
  - Custom voice styles for different story characters
  - Dynamic speech rate adjustment based on age group
  - Background music integration for immersive storytelling
  - Voice selection for different story themes
- 📚 Multiple age group support (3-5, 6-8, 9-12 years)
- 🎨 Various story themes (Space Adventure, Magic Kingdom, Ocean Explorer, etc.)
- ⭐ Story favoriting system
- 🔊 Text-to-speech narration with natural-sounding voices
- 📧 Email stories with smart content truncation
  - Automatic length management for email clients
  - Includes story metadata and illustration links
  - Fallback to print option for long stories
- 📱 Social sharing integration
  - Direct sharing to Twitter, Facebook, and WhatsApp
  - Native Web Share API support
  - Clipboard fallback for unsupported browsers
  - Custom sharing messages with story metadata
- 🖨️ Print-friendly story formatting
- 🎯 Educational focus with learning objectives
- ✨ Enhanced animated UI with visual feedback:
  - 📝 Typewriter effect for story reveal
  - 📖 Book flipping animation during story generation
  - 💫 Magical sparkle effects and dynamic elements
  - 🔄 Rotating loading messages during story creation
  - ✨ Confetti celebration when stories are generated
  - 📱 Responsive design with smooth transitions

## Tech Stack

- Frontend: React + TypeScript
- Backend: Flask + SQLAlchemy
- AI: Azure OpenAI (GPT-4)
- Image Generation: Azure DALL-E 3
- Text-to-Speech: Azure Speech Service with premium voice selection
- Database: SQLite
- Styling: CSS with inline styles for consistent rendering
- Containerization: Docker

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ajmalrasouli/ai-storyteller.git
   cd ai-storyteller
   ```

2. Install backend Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend` directory with your Azure credentials and database URL:
   ```bash
   DATABASE_URL=sqlite:///stories.db
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_azure_openai_deployment_name
   AZURE_OPENAI_API_VERSION=2024-02-01
   AZURE_DALLE_API_KEY=your_azure_dalle_api_key
   AZURE_DALLE_ENDPOINT=your_azure_dalle_endpoint
   AZURE_DALLE_DEPLOYMENT_NAME=your_azure_dalle_deployment_name
   AZURE_DALLE_API_VERSION=2024-02-01
   AZURE_SPEECH_KEY=your_azure_speech_key
   AZURE_SPEECH_REGION=your_azure_speech_region
   ```

4. Start the Flask backend:
   ```bash
   # Option 1: Run directly
   python -m backend.app

   # Option 2: Run with Docker
   docker build -t storyteller-backend -f Dockerfile .
   docker run -p 5000:5000 storyteller-backend
   ```

5. Open a new terminal, install frontend dependencies and start the React app:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. Open your browser at http://localhost:5173 to use the app.

## Project Structure

```
ai-storyteller/
├── frontend/              # React/TypeScript frontend
│   ├── src/              # Source code
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
├── backend/              # Flask backend
│   ├── app.py           # Main application
│   ├── services/        # Azure service integrations
│   ├── routes/          # API routes
│   ├── models/          # Database models
│   ├── config/          # Configuration
│   ├── Dockerfile       # Docker configuration
│   └── requirements.txt # Backend dependencies
└── README.md            # Project documentation
```

## System Architecture

```mermaid
graph TD
    A[Frontend React/TypeScript] --> B[Flask Backend]
    B --> C[SQLite Database]
    B --> D[Azure OpenAI]
    B --> E[Azure DALL-E 3]
    B --> F[Azure Speech Service]
    
    subgraph Frontend
        A --> G[Story Creation UI]
        A --> H[Story Viewing UI]
        A --> I[User Authentication]
    end
    
    subgraph Backend Services
        D --> J[Story Generation]
        E --> K[Image Generation]
        F --> L[Text-to-Speech]
    end
    
    subgraph Data Storage
        C --> M[Stories]
        C --> N[User Data]
        C --> O[Favorites]
    end
```

## Component Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AzureServices
    participant Database

    User->>Frontend: Select Story Parameters
    Frontend->>Backend: Send Story Request
    Backend->>AzureServices: Generate Story (OpenAI)
    AzureServices-->>Backend: Story Content
    Backend->>AzureServices: Generate Image (DALL-E)
    AzureServices-->>Backend: Story Image
    Backend->>Database: Store Story
    Backend-->>Frontend: Story Data
    Frontend->>User: Display Story
    
    User->>Frontend: Request Narration
    Frontend->>Backend: Text-to-Speech Request
    Backend->>AzureServices: Convert to Speech
    AzureServices-->>Backend: Audio Stream
    Backend-->>Frontend: Audio Data
    Frontend->>User: Play Narration
```

## Development

- `npm run dev`: Start frontend development server
- `python -m backend.app`: Start backend server
- `docker build -t storyteller-backend -f Dockerfile .`: Build Docker image
- `docker run -p 5000:5000 storyteller-backend`: Run Docker container
- `npm run build`: Build frontend for production
- `python migrate_db.py`: Initialize or update database schema

## Testing

The project includes several test scripts:
- `test_azure_apis.py`: Tests Azure API integrations
- `validate_azure_services.py`: Validates Azure service configurations
- `check_openai_key.py`: Verifies OpenAI API key
- `Azurekeycheck.py`: Validates Azure service keys

## Using the Application

1. **Create a Story**:
   - Select a theme (Space Adventure, Magic Kingdom, etc.)
   - Add characters (comma-separated)
   - Choose an age group
   - Click "Begin Your Magical Adventure" to generate
   - An AI-generated illustration will be created automatically

2. **View Stories**:
   - Browse all stories in the "My Stories" tab
   - View favorite stories in the "Favorites" tab
   - Click on a story card to view the full content with animated text reveal
   - Each story includes a unique AI-generated illustration

3. **Story Actions**:
   - Add/remove stories from favorites
   - Listen to stories with natural text-to-speech narration
   - Email stories with smart content management
   - Share stories directly to social media platforms
   - Print stories in a nicely formatted layout
   - Regenerate illustrations if desired

4. **Sharing Options**:
   - Email: Automatically formats stories for email clients
   - Social Media: Share directly to Twitter, Facebook, or WhatsApp
   - Web Share: Use native sharing on supported devices
   - Print: Generate a print-friendly version
   - Copy Link: Quick access to story URLs

## Environment Variables

- `DATABASE_URL`: SQLite database URL
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your Azure OpenAI deployment name
- `AZURE_OPENAI_API_VERSION`: Azure OpenAI API version
- `AZURE_DALLE_API_KEY`: Your Azure DALL-E API key
- `AZURE_DALLE_ENDPOINT`: Your Azure DALL-E endpoint URL
- `AZURE_DALLE_DEPLOYMENT_NAME`: Your Azure DALL-E deployment name
- `AZURE_DALLE_API_VERSION`: Azure DALL-E API version
- `AZURE_SPEECH_KEY`: Your Azure Speech Service API key
- `AZURE_SPEECH_REGION`: Your Azure Speech Service region
- `FLASK_APP`: Flask application entry point
- `FLASK_ENV`: Flask environment (development/production)

## License

MIT
