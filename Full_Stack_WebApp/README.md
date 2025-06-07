# Premier League Full-Stack Football Data Application

## 🎯 Project Overview

This project simulates a real-world football data ecosystem by creating a full-stack application that mimics data scraping workflows. The system consists of three main components that work together to demonstrate data flow from generation to consumption and back to storage.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Source   │    │   Frontend UI   │    │  Scraping Bot   │
│   (Django API)  │────┤   (React App)   │────┤  (Python Bot)   │
│                 │    │                 │    │                 │
│ Serves 6 seasons│    │ SofaScore-like  │    │ Scrapes Frontend│
│ of PL data via  │    │ UI with elegant │    │ data and stores │
│ REST API in     │    │ CSS styling     │    │ in PostgreSQL   │
│ chunks          │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                   ┌─────────────────┐
                   │   PostgreSQL    │
                   │   (Docker)      │
                   │                 │
                   │ Stores scraped  │
                   │ football data   │
                   └─────────────────┘
```

## 📊 Data Flow

1. **Data Generation**: Use existing `generate_data.py` to create 6 seasons of Premier League data (2019-2025)
2. **API Service**: Django backend serves this data via REST API endpoints in paginated chunks
3. **Frontend Display**: React application consumes API and displays data with SofaScore-inspired UI
4. **Data Scraping**: Python scraping service scrapes the frontend pages and extracts data
5. **Data Storage**: Scraped data is stored in PostgreSQL database running in Docker

## 🛠️ Technology Stack

### Backend (Django)

- **Framework**: Django 4.x + Django REST Framework
- **Database**: SQLite (for Django data storage)
- **Environment**: Existing `.venv` virtual environment
- **Features**:
  - REST API endpoints with pagination
  - CORS enabled for React frontend
  - Chunked data delivery for performance
  - Rate limiting for realistic API behavior

### Frontend (React)

- **Framework**: React 18.x
- **Styling**: Pure CSS (No Tailwind or CSS frameworks)
- **State Management**: React hooks (useState, useEffect)
- **HTTP Client**: Axios for API calls
- **Features**:
  - SofaScore-inspired design
  - Responsive layout
  - Real-time data loading with pagination
  - Loading states and error handling

### Scraping Service

- **Language**: Python 3.x
- **Libraries**: Selenium/BeautifulSoup + Requests
- **Database**: PostgreSQL (Docker container)
- **Features**:
  - Automated scraping of React frontend
  - Data extraction and validation
  - Batch processing and storage

### Database (PostgreSQL)

- **Container**: Docker PostgreSQL 15
- **Purpose**: Store scraped data
- **Schema**: Replicate frontend data structure

## 📁 Project Structure

```
Full_Stack_WebApp/
├── README.md                 # This file
├── Backend/                  # Django API Server
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── football_api/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── management/
│   │       └── commands/
│   │           └── load_data.py
│   └── data/
│       └── premier_league_data.csv
├── Frontend_WebApp/          # React Application
│   ├── package.json
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MatchCard/
│   │   │   ├── MatchList/
│   │   │   ├── Navigation/
│   │   │   ├── LeagueTable/
│   │   │   └── TeamStats/
│   │   ├── pages/
│   │   │   ├── Home/
│   │   │   ├── Fixtures/
│   │   │   ├── Table/
│   │   │   └── Teams/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── global.css
│   │   │   └── components/
│   │   └── utils/
│   └── build/
├── Scraping_Service/         # Web Scraping Bot
│   ├── requirements.txt
│   ├── scraper.py
│   ├── models.py
│   ├── database.py
│   ├── config.py
│   └── logs/
├── Database/                 # PostgreSQL Docker Setup
│   ├── docker-compose.yml
│   ├── init.sql
│   └── data/
├── Dummy_Datasets/           # Data Generation
│   ├── generate_data.py      # Existing file
│   └── generated_data/
└── docs/                     # Documentation
    ├── api_documentation.md
    ├── frontend_guide.md
    └── deployment_guide.md
```

## 🚀 Development Phases

### Phase 1: Backend Development (Django API)

1. **Setup Django Project**

   - Initialize Django project in existing `.venv`
   - Configure Django REST Framework
   - Setup CORS for React integration

2. **Data Models & API**

   - Create models for Premier League data
   - Load generated data from `generate_data.py`
   - Create REST API endpoints with pagination
   - Implement filtering and sorting

3. **API Endpoints**
   ```
   GET /api/matches/              # All matches with pagination
   GET /api/matches/{id}/         # Match details
   GET /api/teams/                # Team list
   GET /api/teams/{id}/matches/   # Team's matches
   GET /api/seasons/              # Available seasons
   GET /api/table/{season}/       # League table
   ```

### Phase 2: Frontend Development (React)

1. **Project Setup**

   - Create React application
   - Setup routing (React Router)
   - Configure API service layer

2. **Core Components**

   - Navigation header (SofaScore-style)
   - Match cards with team logos and scores
   - League table component
   - Team statistics displays

3. **Pages Implementation**

   - **Home**: Live scores and recent matches
   - **Fixtures**: Upcoming and past matches
   - **Table**: League standings
   - **Teams**: Team profiles and statistics

4. **Styling (Pure CSS)**
   - SofaScore-inspired color scheme
   - Responsive grid layouts
   - Hover effects and animations
   - Loading skeletons

### Phase 3: PostgreSQL Database Setup

1. **Docker Configuration**

   - Create docker-compose.yml for PostgreSQL
   - Setup initialization scripts
   - Configure volume persistence

2. **Database Schema**
   - Mirror frontend data structure
   - Create indexes for performance
   - Setup constraints and relationships

### Phase 4: Scraping Service Development

1. **Web Scraper Implementation**

   - Setup Selenium for React scraping
   - Create data extraction logic
   - Implement error handling and retries

2. **Data Processing**

   - Parse scraped HTML/JSON data
   - Validate data integrity
   - Transform data for PostgreSQL storage

3. **Database Integration**
   - Connect to PostgreSQL container
   - Implement batch insert operations
   - Create data synchronization logic

### Phase 5: Integration & Testing

1. **End-to-End Testing**

   - Test complete data flow
   - Verify data consistency
   - Performance optimization

2. **Documentation**
   - API documentation
   - Frontend component guide
   - Deployment instructions

## 🎨 Frontend Design Guidelines

### SofaScore-Inspired Features

- **Color Scheme**: Dark theme with accent colors
- **Typography**: Clean, modern fonts
- **Match Cards**: Team logos, scores, match time
- **League Table**: Interactive sorting and filtering
- **Responsive Design**: Mobile-first approach

### Pages Structure

1. **Home Page**: Featured matches, live scores, recent results
2. **Fixtures Page**: Calendar view of all matches
3. **Table Page**: League standings with team statistics
4. **Teams Page**: Individual team profiles and match history

## 🔧 Development Setup

### Prerequisites

- Python 3.8+ (with existing `.venv`)
- Node.js 16+
- Docker & Docker Compose
- Git

### Quick Start

```bash
# 1. Activate existing virtual environment
source .venv/bin/activate

# 2. Setup Backend (Django)
cd Backend/
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata premier_league_data
python manage.py runserver 8000

# 3. Setup Frontend (React)
cd ../Frontend_WebApp/
npm install
npm start  # Runs on port 3000

# 4. Setup Database (PostgreSQL)
cd ../Database/
docker-compose up -d

# 5. Run Scraping Service
cd ../Scraping_Service/
pip install -r requirements.txt
python scraper.py
```

## 📝 API Documentation

### Match Data Structure

```json
{
  "id": 1,
  "season": "2024-25",
  "matchweek": 1,
  "date": "17/08/24",
  "home_team": "Arsenal",
  "away_team": "Wolves",
  "home_goals": 2,
  "away_goals": 0,
  "result": "H",
  "stats": {
    "home_shots": 15,
    "away_shots": 8,
    "home_possession": 68,
    "away_possession": 32
  }
}
```

## 🚀 Deployment Considerations

### Production Setup

- Django with Gunicorn + Nginx
- React build served by Nginx
- PostgreSQL with persistent volumes
- Docker Compose for orchestration

### Environment Variables

- Database credentials
- API keys and secrets
- CORS origins
- Debug settings

## 🔄 Future Enhancements

1. **Real-time Updates**: WebSocket integration
2. **Advanced Analytics**: Player statistics and predictions
3. **Mobile App**: React Native version
4. **API Caching**: Redis implementation
5. **Machine Learning**: Match prediction models

---

## 🏁 Getting Started

Ready to begin development? Let's start with Phase 1 - Backend Development!

```bash
# Generate the data first
cd Dummy_Datasets/
python generate_data.py

# Then proceed with Django backend setup
cd ../Backend/
# ... (setup instructions will be provided)
```

This README serves as our project roadmap. Each phase will be implemented step-by-step with detailed instructions and best practices.
