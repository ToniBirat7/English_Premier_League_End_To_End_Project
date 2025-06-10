# Premier League Web Scraper v2.0

A comprehensive web scraping and data analysis system for Premier League match data. This project scrapes 2024-25 Premier League season data from a full-stack web application and stores detailed match statistics in a PostgreSQL database with extended analytics capabilities.

## 🎯 Overview

This scraper extracts complete Premier League match data including:
- Basic match information (teams, scores, results, dates)
- Extended statistics (possession, shots, corners, fouls, cards)
- All 38 matchweeks of the 2024-25 season
- Comprehensive data quality validation
- Advanced analytics and reporting

## 📋 Prerequisites

### System Requirements
- Python 3.8+ with virtual environment support
- PostgreSQL 15+ running on port 5434
- Docker (for PostgreSQL container)
- At least 1GB free disk space

### Required Services
1. **PostgreSQL Database** - Running on localhost:5434
2. **Django Backend API** - Running on localhost:8000 
3. **React Frontend** - Running on localhost:3000 (optional)

### Python Dependencies
```bash
# Core scraping libraries
requests>=2.31.0
psycopg2-binary>=2.9.7
pandas>=2.0.3

# Data analysis libraries
numpy>=1.24.3
matplotlib>=3.7.2
seaborn>=0.12.2

# Database utilities
SQLAlchemy>=2.0.19
```

## 🚀 Quick Start

### Step 1: Environment Setup

1. **Clone and navigate to the project:**
```bash
cd "/media/toni-birat/New Volume/English_Premier_League_Complete_Project"
```

2. **Activate your virtual environment:**
```bash
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r scraper_requirements.txt
```

### Step 2: Database Setup

1. **Start PostgreSQL container (if using Docker):**
```bash
docker run --name postgres-scraper \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5434:5432 \
  -d postgres:15
```

2. **Create the target database:**
```bash
python3 -c "
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        host='localhost',
        port='5434',
        user='postgres',
        password='postgres',
        database='postgres'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute(\"SELECT 1 FROM pg_database WHERE datname='weekly_scrapped_data'\")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute('CREATE DATABASE weekly_scrapped_data')
        print('✅ weekly_scrapped_data database created successfully')
    else:
        print('✅ weekly_scrapped_data database already exists')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Step 3: Start Required Services

1. **Start the Django backend:**
```bash
cd Full_Stack_WebApp/Backend
python manage.py runserver 0.0.0.0:8000
```

2. **Start the React frontend (optional):**
```bash
cd Full_Stack_WebApp/frontend
npm start
```

### Step 4: Run the Scraper

You can run the scraper in different modes:

#### Option A: Complete Pipeline (Recommended)
```bash
python run_scraper.py both
```

#### Option B: Scraping Only
```bash
python run_scraper.py scrape
```

#### Option C: Analysis Only
```bash
python run_scraper.py analyze
```

#### Option D: Direct Scraper Execution
```bash
python web_scraper.py
```

## 📊 Database Schema

The scraper creates a PostgreSQL table with the following structure:

```sql
CREATE TABLE PREMIER_LEAGUE_MATCHES (
    ID SERIAL PRIMARY KEY,
    DT DATE NOT NULL,                    -- Match Date
    HT VARCHAR(50) NOT NULL,             -- Home Team
    AT VARCHAR(50) NOT NULL,             -- Away Team
    FTHG INTEGER NOT NULL,               -- Full Time Home Goals
    FTAG INTEGER NOT NULL,               -- Full Time Away Goals
    FTR VARCHAR(1) NOT NULL,             -- Final Result (H/A/D)
    HP INTEGER,                          -- Home Possession (%)
    AP INTEGER,                          -- Away Possession (%)
    HS INTEGER,                          -- Home Shots
    AS_ INTEGER,                         -- Away Shots
    HST INTEGER,                         -- Home Shots on Target
    AST INTEGER,                         -- Away Shots on Target
    HC INTEGER,                          -- Home Corners
    AC INTEGER,                          -- Away Corners
    HF INTEGER,                          -- Home Fouls
    AF INTEGER,                          -- Away Fouls
    HY INTEGER,                          -- Home Yellow Cards
    AY INTEGER,                          -- Away Yellow Cards
    HR INTEGER,                          -- Home Red Cards
    AR INTEGER,                          -- Away Red Cards
    MW INTEGER,                          -- Match Week
    SEASON VARCHAR(7),                   -- Season
    SCRAPED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(DT, HT, AT)
);
```

## 🔧 Configuration

### Database Configuration
Edit the database connection settings in both `web_scraper.py` and `data_analyzer.py`:

```python
db_config = {
    'host': 'localhost',
    'port': '5434',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'weekly_scrapped_data'
}
```

### API Endpoints
The scraper connects to these endpoints:
- **Backend API**: `http://localhost:8000/api/matches/`
- **Frontend**: `http://localhost:3000` (for reference)

### Scraper Settings
Key configuration options in `web_scraper.py`:

```python
# Target season
current_season = "2024-25"

# Request timeout (seconds)
timeout = 30

# Delay between requests (seconds)
request_delay = 0.1

# Table name in PostgreSQL
table_name = "PREMIER_LEAGUE_MATCHES"
```

## 📈 Data Analysis Features

The built-in analyzer provides:

### Statistical Analysis
- Match result distributions
- Goal scoring patterns
- Home advantage analysis
- Team performance metrics
- Possession statistics
- Shot accuracy analysis
- Disciplinary records

### Data Quality Checks
- Missing value detection
- Data validity verification
- Duplicate match identification
- Matchweek consistency validation
- Possession percentage validation

### Export Capabilities
- CSV data export
- JSON analysis reports
- Comprehensive league tables
- Team performance rankings

## 🎯 Usage Examples

### Example 1: Basic Scraping
```bash
# Run complete scraping pipeline
python run_scraper.py scrape

# Expected output:
# ✅ 380 matches scraped and saved to PostgreSQL
# ✅ Database: weekly_scrapped_data
# ✅ All 38 matchweeks completed
```

### Example 2: Data Analysis
```bash
# Generate comprehensive analysis
python run_scraper.py analyze

# Expected output:
# 📊 380 matches analyzed
# 🏆 League table generated
# 📄 Data exported to CSV
# 📊 JSON report created
```

### Example 3: Database Verification
```bash
# Check database contents
PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d weekly_scrapped_data -c "
SELECT 
    COUNT(*) as total_matches,
    MIN(dt) as season_start,
    MAX(dt) as season_end,
    COUNT(DISTINCT ht) as unique_teams,
    MAX(mw) as max_matchweek
FROM premier_league_matches;
"
```

### Example 4: Team Performance Query
```bash
# Get top 5 teams by points
PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d weekly_scrapped_data -c "
SELECT 
    ht as team,
    COUNT(*) + (SELECT COUNT(*) FROM premier_league_matches p2 WHERE p2.at = p1.ht) as games_played,
    SUM(CASE WHEN ftr = 'H' THEN 3 WHEN ftr = 'D' THEN 1 ELSE 0 END) +
    (SELECT SUM(CASE WHEN ftr = 'A' THEN 3 WHEN ftr = 'D' THEN 1 ELSE 0 END) 
     FROM premier_league_matches p2 WHERE p2.at = p1.ht) as total_points
FROM premier_league_matches p1
GROUP BY ht
ORDER BY total_points DESC
LIMIT 5;
"
```

## 📁 Output Files

The scraper generates several output files:

### Data Files
- `premier_league_analysis_YYYYMMDD_HHMMSS.csv` - Complete match data
- `analysis_report_YYYYMMDD_HHMMSS.json` - Detailed analysis report

### Log Files
- `scraper.log` - Scraping operation logs
- `analyzer.log` - Analysis operation logs

### Generated Reports
- League table rankings
- Team performance statistics
- Match statistics summary
- Data quality assessment

## ⚠️ Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL container
docker restart postgres-scraper

# Verify connection
PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d weekly_scrapped_data -c "SELECT version();"
```

#### 2. Backend API Not Accessible
```bash
# Check if Django backend is running
curl -f http://localhost:8000/api/matches/ | head -5

# Start backend if needed
cd Full_Stack_WebApp/Backend
python manage.py runserver 0.0.0.0:8000
```

#### 3. Missing Dependencies
```bash
# Reinstall dependencies
pip install -r scraper_requirements.txt

# Check specific package
pip show psycopg2-binary requests pandas
```

#### 4. Permission Errors
```bash
# Ensure proper file permissions
chmod +x run_scraper.py web_scraper.py data_analyzer.py

# Check database permissions
PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d weekly_scrapped_data -c "
GRANT ALL PRIVILEGES ON DATABASE weekly_scrapped_data TO postgres;
"
```

### Performance Issues

#### 1. Slow Scraping
- Increase `request_delay` in `web_scraper.py`
- Check network connectivity to API endpoints
- Monitor database connection pool

#### 2. Memory Usage
- Process data in smaller batches
- Clear pandas DataFrames after use
- Monitor PostgreSQL memory usage

#### 3. Database Performance
```sql
-- Create additional indexes for better performance
CREATE INDEX IF NOT EXISTS idx_season_team ON premier_league_matches(season, ht, at);
CREATE INDEX IF NOT EXISTS idx_result ON premier_league_matches(ftr);
CREATE INDEX IF NOT EXISTS idx_goals ON premier_league_matches(fthg, ftag);
```

## 🔍 Data Validation

The scraper includes comprehensive data validation:

### Automatic Checks
- ✅ All 20 Premier League teams present
- ✅ Exactly 38 matchweeks per season
- ✅ 10 matches per matchweek (190 total per team)
- ✅ Possession percentages sum to ~100%
- ✅ No negative goals or impossible statistics
- ✅ Unique match identification (date + teams)
- ✅ Proper result codes (H/A/D)

### Manual Validation Commands
```bash
# Verify season completeness
PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d weekly_scrapped_data -c "
SELECT 
    season,
    COUNT(*) as total_matches,
    COUNT(DISTINCT mw) as matchweeks,
    COUNT(DISTINCT ht) + COUNT(DISTINCT at) as unique_teams_mentioned
FROM premier_league_matches 
GROUP BY season;
"

# Check data quality
python -c "
from data_analyzer import PremierLeagueDataAnalyzer
analyzer = PremierLeagueDataAnalyzer()
quality = analyzer.check_data_quality()
print(f'Data Quality Report: {quality}')
"
```

## 📚 Advanced Usage

### Custom Analysis Queries

#### Team Head-to-Head Records
```sql
SELECT 
    ht as home_team,
    at as away_team,
    COUNT(*) as matches_played,
    SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN ftr = 'A' THEN 1 ELSE 0 END) as away_wins,
    SUM(CASE WHEN ftr = 'D' THEN 1 ELSE 0 END) as draws,
    AVG(fthg) as avg_home_goals,
    AVG(ftag) as avg_away_goals
FROM premier_league_matches 
WHERE ht = 'Arsenal' AND at = 'Chelsea'
GROUP BY ht, at;
```

#### Monthly Performance Trends
```sql
SELECT 
    EXTRACT(MONTH FROM dt) as month,
    COUNT(*) as matches,
    AVG(fthg + ftag) as avg_goals_per_match,
    AVG(hs + as_) as avg_shots_per_match,
    SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as home_win_percentage
FROM premier_league_matches 
GROUP BY EXTRACT(MONTH FROM dt)
ORDER BY month;
```

### Extending the Scraper

#### Adding New Statistics
1. Update the database schema in `web_scraper.py`
2. Modify the `generate_extended_match_data()` method
3. Update the INSERT statement with new columns
4. Add validation rules in `check_data_quality()`

#### Custom Data Sources
1. Modify the `get_matches_from_api()` method
2. Update API endpoint configurations
3. Adjust data parsing logic for new source format
4. Update field mapping in `generate_extended_match_data()`

## 🚀 Production Deployment

### Environment Variables
```bash
# Set production database credentials
export POSTGRES_HOST=your-db-host
export POSTGRES_PORT=5432
export POSTGRES_USER=your-username
export POSTGRES_PASSWORD=your-password
export POSTGRES_DB=weekly_scrapped_data

# Set API endpoints
export BACKEND_API_URL=https://your-backend-api.com/api
export FRONTEND_URL=https://your-frontend.com
```

### Docker Deployment
```dockerfile
# Dockerfile for scraper
FROM python:3.11-slim

WORKDIR /app
COPY scraper_requirements.txt .
RUN pip install -r scraper_requirements.txt

COPY . .
CMD ["python", "run_scraper.py", "both"]
```

### Scheduled Execution
```bash
# Add to crontab for daily execution
0 2 * * * cd /path/to/scraper && python run_scraper.py scrape >> /var/log/scraper.log 2>&1
```

## 📞 Support

### Getting Help
- Check the troubleshooting section above
- Review log files in `scraper.log` and `analyzer.log`
- Verify all prerequisites are installed and running
- Test database connectivity independently

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏆 Acknowledgments

- Premier League for providing the data source
- PostgreSQL community for excellent database tools
- Python ecosystem for powerful data analysis libraries
- Full-stack web application providing the API endpoints

---

**Version**: 2.0  
**Last Updated**: June 10, 2025  
**Compatibility**: Python 3.8+, PostgreSQL 15+, Ubuntu 20.04+
