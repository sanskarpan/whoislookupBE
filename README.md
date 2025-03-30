# Whois Domain Lookup Application

A full-stack application that provides domain and contact information using the Whois API. The application consists of a FastAPI backend and a React frontend.

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm
- Docker and Docker Compose (optional, for containerized deployment)
- A Whois API key from [whoisxmlapi.com](https://www.whoisxmlapi.com/)

### Backend Setup

1. Clone the repository and navigate to the backend directory
   ```bash
   git clone https://github.com/sanskarpan/whoislookupBE.git
   cd whoislookupBE
   ```

2. Set up the backend
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. Configure environment variables
   ```bash
   # Create .env file from example
   cp .env.example .env
   
   # Edit the .env file to add your Whois API key
   # API_KEY=your_whois_api_key_here
   ```

4. Start the backend server
   ```bash
   # Run the FastAPI server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
   ```

5. Verify the backend is running by accessing:
   - API documentation: http://localhost:5000/api/docs
   - Health check: http://localhost:5000/api/health

### Frontend Setup

1. Clone the repository and navigate to the frontend directory
   ```bash
   git clone https://github.com/sanskarpan/whoislookupFE.git
   cd whoislookupFE
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Configure environment variables
   ```bash
   # Create .env file
   echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
   ```

4. Initialize Tailwind CSS
   ```bash
   npx tailwindcss init -p
   ```

5. Start the frontend development server
   ```bash
   npm start
   ```

6. Access the application at:
   - http://localhost:3000

## Running with Docker

If you prefer to use Docker, you can set up and run both services with Docker Compose:

1. Configure environment variables
   ```bash
   # Create backend .env file
   cp backend/.env.example backend/.env
   
   # Edit backend/.env to add your Whois API key
   ```

2. Build and start the containers
   ```bash
   docker-compose up -d
   ```

3. Access the application at:
   - http://localhost:3000

## Deployment Instructions

### Deploy using Docker

For a production deployment, you can use the included Docker configuration:

1. Configure production environment variables
   ```bash
   # In backend/.env
   DEBUG=False
   ```

2. Build and deploy using Docker Compose
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

## Troubleshooting

### Common Issues

1. **No response from server error**
   - Verify the backend is running
   - Check your API key in backend/.env
   - Ensure CORS is properly configured

2. **Tailwind CSS not working**
   - Run `npx tailwindcss init -p` in the frontend directory
   - Check that your `index.css` contains the Tailwind directives
   - Try using the CDN version in `index.html` as a fallback

3. **Date/Time Errors**
   - This is fixed in the latest code, but ensure your WhoisService file is updated

### Getting Help

If you encounter any issues not covered here, please:
1. Check the browser console for error messages
2. Look at the backend logs for any errors
3. Create an issue in the GitHub repository with details of the problem

## Testing

Test the application with a domain like "amazon.com" to verify both domain and contact information retrieval are working correctly.