# Premier League Full-Stack Web Application

## 🎯 Project Overview

A production-ready full-stack web application that simulates real-world football data scraping and displays Premier League match data with a SofaScore-inspired UI. The application consists of a Django REST API backend, React frontend, and PostgreSQL database with integrated web scraping capabilities.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  Django Backend │    │   PostgreSQL    │
│   (JavaScript)   │◄──►│   (REST API)    │◄──►│   (Docker)      │
│   + CSS Styling  │    │  + Web Scraper  │    │   Port: 5434    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Features

### Frontend (React + CSS)

- **Home Page**: Match listings with SofaScore-inspired design
- **Fixtures Page**: Upcoming matches display
- **League Table**: Current season standings
- **Team Details**: Individual team statistics and match history
- **Responsive Design**: Mobile-friendly layout
- **Real Team Logos**: Official Premier League team logos
- **Elegant UI**: Clean, attractive, production-ready interface

### Backend (Django REST API)

- **Match Management**: CRUD operations for matches
- **Team Management**: Team data and statistics
- **League Table Generation**: Dynamic standings calculation
- **Data Pagination**: Chunked data delivery for performance
- **Web Scraping Service**: Integrated scraper for frontend data
- **RESTful Endpoints**: Well-structured API design

### Database (PostgreSQL)

- **Docker Container**: `postgres:15-alpine` on port 5434
- **Schema**: Simplified match data storage
- **Data Persistence**: Reliable data storage and retrieval

## 🗄️ Database Schema

### Match Model

```python
class Match(models.Model):
    date = models.DateField()           # Match date
    home_team = models.CharField()      # Home team name
    away_team = models.CharField()      # Away team name
    fthg = models.IntegerField()        # Full Time Home Goals
    ftag = models.IntegerField()        # Full Time Away Goals
    ftr = models.CharField()            # Full Time Result (H/A/D)
    season = models.CharField()         # Season (e.g., "2023-24")
    matchweek = models.IntegerField()   # Match week number
```

## 🚀 API Endpoints

### Matches

- `GET /api/matches/` - List matches with pagination
- `GET /api/matches/recent/` - Get recent matches
- `GET /api/matches/by_season/?season=2023-24` - Filter by season
- `GET /api/matches/fixtures/` - Upcoming fixtures

### Teams

- `GET /api/teams/` - List all teams
- `GET /api/teams/{id}/` - Team details
- `GET /api/teams/{id}/matches/` - Team's matches
- `GET /api/teams/league_table/` - Current league table

### Statistics

- `GET /api/stats/overview/` - General statistics
- `GET /api/stats/seasons/` - Available seasons

## 🛠️ Technology Stack

### Backend

- **Framework**: Django 5.2.1
- **API**: Django REST Framework
- **Database**: PostgreSQL 15 (Docker)
- **Web Scraping**: Beautiful Soup 4 + Requests
- **Environment**: Python Virtual Environment (.venv)

### Frontend

- **Framework**: React 18 (JavaScript)
- **Styling**: Pure CSS (No Tailwind)
- **HTTP Client**: Axios
- **Routing**: React Router
- **Build Tool**: Create React App

### Database

- **Engine**: PostgreSQL 15-alpine
- **Container**: Docker
- **Port**: 5434
- **Database Name**: epl_postgres

## 📁 Project Structure

```
Full_Stack_WebApp/
├── README.md
├── Backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── football_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── football_api/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── scraper.py
│   └── fixtures/
│       └── premier_league_data.json
├── Frontend/
│   ├── package.json
│   ├── public/
│   │   ├── index.html
│   │   └── team_logos/
│   └── src/
│       ├── components/
│       │   ├── MatchCard.js
│       │   ├── TeamCard.js
│       │   ├── LeagueTable.js
│       │   └── Navigation.js
│       ├── pages/
│       │   ├── Home.js
│       │   ├── Fixtures.js
│       │   ├── Table.js
│       │   └── Teams.js
│       ├── services/
│       │   └── api.js
│       ├── styles/
│       │   ├── App.css
│       │   ├── components/
│       │   └── pages/
│       └── App.js
└── docker-compose.yml
```

## 🔄 Data Flow

1. **Data Ingestion**: CSV data (`premier_league_6_seasons_complete.csv`) loaded into Django
2. **API Serving**: Django serves data via REST API endpoints
3. **Frontend Display**: React frontend fetches and displays data with SofaScore-inspired UI
4. **Web Scraping**: Django scraper extracts data from React frontend
5. **Data Storage**: Scraped data stored in PostgreSQL container

## 🎨 UI Design Principles

### SofaScore-Inspired Design

- **Color Scheme**: Professional sports website colors
- **Layout**: Clean, grid-based match cards
- **Typography**: Modern, readable fonts
- **Icons**: Official team logos and sports icons
- **Navigation**: Intuitive menu structure
- **Responsiveness**: Mobile-first design approach

### Key UI Components

- **Match Cards**: Attractive match result displays
- **League Table**: Professional standings table
- **Team Logos**: Real Premier League team logos
- **Navigation Bar**: Clean, accessible menu
- **Loading States**: Smooth loading animations
- **Error Handling**: User-friendly error messages

## 📦 Dependencies

### Backend Requirements

```
Django==5.2.1
djangorestframework==3.15.1
django-cors-headers==4.1.0
psycopg2-binary==2.9.6
beautifulsoup4==4.12.2
requests==2.31.0
django-filter==23.2
```

### Frontend Requirements

```
React: ^18.2.0
axios: ^1.4.0
react-router-dom: ^6.14.0
```

## 🚀 Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL Docker container (running on port 5434)

### Backend Setup

```bash
cd Backend/
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata premier_league_data.json
python manage.py runserver
```

### Frontend Setup

```bash
cd Frontend/
npm install
npm start
```

### Database Setup

```bash
# PostgreSQL container already running on port 5434
docker ps | grep postgres
```

## 🧪 Testing Strategy

### Backend Testing

- Model validation tests
- API endpoint tests
- Scraper functionality tests
- Database integration tests

### Frontend Testing

- Component rendering tests
- API integration tests
- UI interaction tests
- Responsive design tests

## 🔒 Security Considerations

- CORS configuration for frontend-backend communication
- Input validation and sanitization
- Rate limiting for API endpoints
- Secure database connection strings
- Environment variable management

## 📈 Performance Optimization

- Database query optimization
- API response pagination
- Frontend code splitting
- Image optimization for team logos
- Caching strategies for frequently accessed data

## 🚢 Deployment Strategy

### Development

- Local Django development server
- React development server
- Docker PostgreSQL container

### Production (Future)

- Docker containerization
- Nginx reverse proxy
- Gunicorn WSGI server
- PostgreSQL production database
- Static file serving

## 📋 Development Phases

### Phase 1: Backend Foundation

1. Django project setup
2. Database models and migrations
3. REST API endpoints
4. Data loading from CSV
5. Basic testing

### Phase 2: Frontend Development

1. React project initialization
2. Component structure setup
3. API service integration
4. SofaScore-inspired UI implementation
5. Responsive design

### Phase 3: Integration & Scraping

1. Frontend-backend integration
2. Web scraping service implementation
3. Data flow validation
4. Performance optimization
5. Error handling

### Phase 4: Polish & Production

1. UI refinement and team logos
2. Comprehensive testing
3. Documentation completion
4. Performance tuning
5. Deployment preparation

## 🤝 Contributing

1. Follow Python PEP 8 coding standards
2. Use semantic commit messages
3. Write comprehensive tests
4. Update documentation
5. Follow React best practices

## 📝 License

This project is for educational and demonstration purposes.

---

**Note**: This application simulates real-world football data scraping for educational purposes. Official Premier League data should be obtained through proper licensing agreements.
