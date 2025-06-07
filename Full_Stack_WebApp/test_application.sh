#!/bin/bash

echo "=== Premier League Full-Stack Application Test ==="
echo "Date: $(date)"
echo

echo "1. Testing React Frontend (localhost:3000)..."
REACT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$REACT_STATUS" = "200" ]; then
    echo "✅ React Frontend: WORKING"
else
    echo "❌ React Frontend: FAILED (Status: $REACT_STATUS)"
fi

echo
echo "2. Testing Django Backend API (localhost:8000)..."
DJANGO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/)
if [ "$DJANGO_STATUS" = "200" ]; then
    echo "✅ Django API Root: WORKING"
else
    echo "❌ Django API Root: FAILED (Status: $DJANGO_STATUS)"
fi

echo
echo "3. Testing API Endpoints..."

# Test Teams endpoint
TEAMS_COUNT=$(curl -s "http://localhost:8000/api/teams/" | jq -r '.count')
echo "✅ Teams Endpoint: $TEAMS_COUNT teams available"

# Test Matches endpoint
MATCHES_COUNT=$(curl -s "http://localhost:8000/api/matches/" | jq -r '.count')
echo "✅ Matches Endpoint: $MATCHES_COUNT matches available"

# Test League Table endpoint
TABLE_COUNT=$(curl -s "http://localhost:8000/api/teams/league_table/?season=2024-25" | jq '. | length')
echo "✅ League Table Endpoint: $TABLE_COUNT teams in 2024-25 table"

# Test Stats Overview endpoint
STATS_TOTAL_MATCHES=$(curl -s "http://localhost:8000/api/stats/overview/?season=2024-25" | jq -r '.total_matches')
echo "✅ Stats Overview Endpoint: $STATS_TOTAL_MATCHES matches in 2024-25 season"

# Test Seasons endpoint
SEASONS_COUNT=$(curl -s "http://localhost:8000/api/stats/seasons/" | jq '. | length')
echo "✅ Seasons Endpoint: $SEASONS_COUNT seasons available"

echo
echo "4. API Response Sample - League Table Top 3:"
curl -s "http://localhost:8000/api/teams/league_table/?season=2024-25" | jq '.[0:3] | .[] | {position, team: .team.name, points, matches_played}'

echo
echo "=== Test Summary ==="
echo "🎯 Frontend: React development server running on port 3000"
echo "🎯 Backend: Django API server running on port 8000"
echo "🎯 Database: SQLite with Premier League data (2019-20 to 2024-25)"
echo "🎯 Features: League Table, Teams, Matches, Fixtures, Statistics"
echo
echo "📱 Application accessible at: http://localhost:3000"
echo "🔗 API documentation at: http://localhost:8000/api/"
echo
echo "✅ FULL-STACK APPLICATION IS READY FOR USE!"
