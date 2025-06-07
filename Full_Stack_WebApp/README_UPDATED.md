# ⚽ Premier League Full-Stack Web Application

A comprehensive, modern web application for exploring Premier League data, featuring real-time league tables, match fixtures, team statistics, and historical data analysis.

## 🚀 Quick Start

### Prerequisites

- Node.js (v18+)
- Python (3.8+)
- npm or yarn

### 1. Backend Setup (Django)

```bash
cd Backend_WebApp
pip install -r requirements.txt
python manage.py runserver 8000
```

### 2. Frontend Setup (React)

```bash
cd Frontend_WebApp/premier-league-app
npm install
npm start
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000/api/

## ✨ Features

### 📊 League Table

- Interactive, sortable league table
- Real-time position calculations
- Qualification indicators (Champions League, Europa League, etc.)
- Multi-season support (2019-20 to 2024-25)

### ⚽ Match Data

- 2,280+ Premier League matches
- Complete fixture history
- Match results and statistics
- Season filtering

### 🏆 Team Statistics

- 20 Premier League teams
- Detailed performance metrics
- Win/draw/loss records
- Goals for/against analysis

### 📱 Modern UI/UX

- SofaScore-inspired design
- Fully responsive layout
- Smooth animations and transitions
- Professional styling with modern CSS

## 🔧 Technology Stack

### Frontend

- **React 18** with TypeScript
- **React Router** for navigation
- **CSS3** with modern styling
- **Responsive Design**

### Backend

- **Django** with REST Framework
- **SQLite** database
- **CORS** enabled
- **Pagination** support

## 📊 API Endpoints

- `GET /api/teams/` - Team information
- `GET /api/matches/` - Match data with filtering
- `GET /api/teams/league_table/` - League table generation
- `GET /api/stats/overview/` - Season statistics
- `GET /api/stats/seasons/` - Available seasons

## 🧪 Testing

Run the comprehensive test suite:

```bash
./test_application.sh
```

## 📈 Data Coverage

- **6 Seasons**: 2019-20 to 2024-25
- **20 Teams**: All current Premier League clubs
- **2,280+ Matches**: Complete fixture history
- **Real-time Calculations**: Points, positions, goal difference

## 🚀 Production Deployment

Ready for deployment on:

- **AWS** (EC2, RDS, CloudFront)
- **Heroku** (Quick deployment)
- **DigitalOcean** (Cost-effective)
- **Vercel + Railway** (Modern stack)

## 📝 License

This project is licensed under the MIT License.

## 🎯 Status

✅ **FULLY FUNCTIONAL** - Ready for production use!

---

**Built with ❤️ for Premier League fans and football data enthusiasts**
