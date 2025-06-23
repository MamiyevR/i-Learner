# i-Learner

An AI-powered learning assistant that provides intelligent tutoring and assessment capabilities through document analysis and interactive chat.

## Core Implementation Details

### Backend Architecture

- REST API built with FastAPI
- Modular service layer design for business logic isolation
- Structured prompt engineering for consistent AI interactions
- SQLite with SQLAlchemy for persistent storage and session management
- Type safety across full stack

### Frontend Design

- React with TypeScript for type-safe component development
- Custom hooks for state management and API integration
- Responsive components (desktop-first approach)
- Real-time chat interface with error handling
- Vite for optimized build performance

### AI Integration

- OpenAI API integration with error handling and rate limiting
- Context management for meaningful AI interactions
- PDF processing pipeline for document analysis
- Structured prompt templates for consistent AI responses

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- OpenAI API key

### Local Development

1. Clone the repository:

```bash
git clone <repository-url>
cd project
```

2. Backend setup:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY=your_api_key

# Run the server
uvicorn app.main:app --reload
```

3. Frontend setup:

```bash
cd frontend
npm install
npm run dev
```

The application will be available at:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Docker Deployment

For containerized deployment:

```bash
docker-compose up --build
```

Access the application at http://localhost

## Project Structure

```
backend/
  ├── app/
  │   ├── ai/             # AI integration and prompts
  │   ├── db/             # Database models and queries
  │   ├── routers/        # API endpoints
  │   └── services/       # Business logic
  ├── requirements.txt
  ├── Dockerfile
  └── assessment.db


frontend/
  ├── src/
  │   ├── components/     # React components
  │   ├── services/       # API integration
  │   ├── types.ts
  │   └── App.tsx
  ├── Dockerfile
  └── package.json

k8s/

docket-compose.yml
README.md
```

## Known Limitations and Future Improvements

1. **Mobile Responsiveness**

   - Current UI is optimized for desktop use
   - Mobile-friendly design planned for future releases

2. **PDF Processing**

   - Basic text extraction using PyPDF2
   - Future improvements:
     - OCR integration for better text extraction
     - File size and page limits
     - Support for more document formats

3. **Document Processing**

   - RAG (Retrieval Augmented Generation) integration for handling larger documents
   - Improved context management for more accurate responses

4. **Chat Experience**
   - Current implementation uses basic request-response
   - Streaming support for more responsive chat

## Deployment Options

### Prerequisites

- Kubernetes cluster
- kubectl configured to your cluster
- Docker registry access

### Build and Push Docker Images

1. Build the images:

```bash
# Build backend
docker build -t your-registry/i-learner-backend:latest ./backend
docker push your-registry/i-learner-backend:latest

# Build frontend
docker build -t your-registry/i-learner-frontend:latest ./frontend
docker push your-registry/i-learner-frontend:latest
```

2. Update image references in k8s manifests:
   Edit `k8s/backend.yaml` and `k8s/frontend.yaml` to use your Docker registry paths.

### Deploy to Kubernetes

1. Apply the manifests:

```bash
kubectl apply -f k8s/
```

2. Verify the deployment:

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### Accessing the Application

Once deployed, the application will be available through your cluster's ingress controller. The exact URL will depend on your cluster configuration.
