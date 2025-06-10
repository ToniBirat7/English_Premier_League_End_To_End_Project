#!/usr/bin/env python3
"""
Premier League Web Scraper v2.0
==================================

This script scrapes Premier League match data from the completed full-stack web application
and stores the extended match statistics in a dedicated database.

Features:
- Scrapes 2024-25 season data from the web application
- Collects detailed match statistics including possession, shots, corners, fouls, cards
- Stores data in SQLite database 'weekly_scrapped_data.db'
- Column names use capital letters with abbreviations as requested

Author: Football Analytics Team
Date: June 10, 2025
"""

import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import time
import logging
from datetime import datetime, date
from typing import List, Dict, Optional
import random
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PremierLeagueWebScraper:
    """
    Web scraper for Premier League match data from the full-stack application
    """
    
    def __init__(self, base_url: str = "http://localhost:3000", api_url: str = "http://localhost:8000/api",
                 db_name: str = "weekly_scrapped_data", db_table: str = "PREMIER_LEAGUE_MATCHES_3"):
        """
        Initialize the scraper with base URL, API URL, and database configuration
        """
        self.base_url = base_url
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': f'{base_url}/premier-league'
        })
        
        # Current season
        self.current_season = "2024-25"
        
        # Database setup - PostgreSQL to match your infrastructure
        self.db_config = {
            'host': 'localhost',
            'port': '5434',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'weekly_scrapped_data'
        }
        self.table_name = db_table
        
    def setup_database(self):
        """
        Create the PostgreSQL database and table structure for storing scraped match data
        """
        try:
            # First, connect to PostgreSQL server to create database
            conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database='postgres'  # Connect to default database first
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", 
                         (self.db_config['database'],))
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(f"CREATE DATABASE {self.db_config['database']}")
                logger.info(f"Created database: {self.db_config['database']}")
            else:
                logger.info(f"Database {self.db_config['database']} already exists")
            
            cursor.close()
            conn.close()
            
            # Now connect to the new database and create table
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Create table with all required columns in capital letters with abbreviations
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                ID SERIAL PRIMARY KEY,
                DT DATE NOT NULL,                    -- Date
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
            )
            """
            
            cursor.execute(create_table_sql)
            
            # Create indexes for better performance
            indexes = [
                f"CREATE INDEX IF NOT EXISTS idx_date ON {self.table_name}(DT)",
                f"CREATE INDEX IF NOT EXISTS idx_season ON {self.table_name}(SEASON)",
                f"CREATE INDEX IF NOT EXISTS idx_teams ON {self.table_name}(HT, AT)",
                f"CREATE INDEX IF NOT EXISTS idx_matchweek ON {self.table_name}(MW)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            conn.commit()
            logger.info(f"Database '{self.db_config['database']}' and table '{self.table_name}' created successfully")
            
        except psycopg2.Error as e:
            logger.error(f"Database setup error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_matches_from_api(self, season: str = None) -> List[Dict]:
        """
        Fetch match data from the backend API
        """
        if season is None:
            season = self.current_season
            
        try:
            # Get matches from API
            url = f"{self.api_url}/matches/"
            params = {'season': season} if season else {}
            
            logger.info(f"Fetching matches from API: {url}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle paginated response - extract 'results' if it exists
            if isinstance(data, dict) and 'results' in data:
                matches = data['results']
                logger.info(f"Retrieved {len(matches)} matches from paginated API response")
                
                # Handle pagination - get all pages
                all_matches = matches.copy()
                next_url = data.get('next')
                
                while next_url:
                    logger.info(f"Fetching next page: {next_url}")
                    response = self.session.get(next_url, timeout=30)
                    response.raise_for_status()
                    page_data = response.json()
                    
                    if 'results' in page_data:
                        all_matches.extend(page_data['results'])
                        next_url = page_data.get('next')
                    else:
                        break
                
                logger.info(f"Retrieved total of {len(all_matches)} matches from all pages")
                return all_matches
                
            elif isinstance(data, list):
                # Direct list response
                matches = data
                logger.info(f"Retrieved {len(matches)} matches from API")
                return matches
            else:
                logger.error(f"Unexpected API response format: {type(data)}")
                return []
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
    
    def fetch_match_detail_from_api(self, match: Dict) -> Dict:
        """
        Fetch detailed match statistics from the backend API match_detail endpoint
        """
        match_id = match.get('id')
        if not match_id:
            logger.warning(f"No match ID found for match {match.get('home_team')} vs {match.get('away_team')}")
            return None
        
        try:
            # Call the match_detail API endpoint
            url = f"{self.api_url}/matches/match_detail/"
            params = {'match_id': match_id}
            
            logger.debug(f"Fetching match details for match ID {match_id} from: {url}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract match and statistics data
            match_data = data.get('match', {})
            statistics = data.get('statistics', {})
            
            # Map API response to our database schema
            extended_data = {
                # Basic match data
                'DT': match_data.get('date') or match.get('date'),
                'HT': match_data.get('home_team_name') or match.get('home_team', ''),
                'AT': match_data.get('away_team_name') or match.get('away_team', ''),
                'FTHG': match_data.get('fthg') or match.get('fthg', 0),
                'FTAG': match_data.get('ftag') or match.get('ftag', 0),
                'FTR': match_data.get('ftr') or match.get('ftr', ''),
                'MW': match_data.get('matchweek') or match.get('matchweek', 1),
                'SEASON': match_data.get('season') or match.get('season', self.current_season),
                
                # Extended statistics from API
                'HP': statistics.get('possession', {}).get('home', 0),
                'AP': statistics.get('possession', {}).get('away', 0),
                'HS': statistics.get('shots', {}).get('home', 0),
                'AS_': statistics.get('shots', {}).get('away', 0),
                'HST': statistics.get('shots_on_target', {}).get('home', 0),
                'AST': statistics.get('shots_on_target', {}).get('away', 0),
                'HC': statistics.get('corners', {}).get('home', 0),
                'AC': statistics.get('corners', {}).get('away', 0),
                'HF': statistics.get('fouls', {}).get('home', 0),
                'AF': statistics.get('fouls', {}).get('away', 0),
                'HY': statistics.get('yellow_cards', {}).get('home', 0),
                'AY': statistics.get('yellow_cards', {}).get('away', 0),
                'HR': statistics.get('red_cards', {}).get('home', 0),
                'AR': statistics.get('red_cards', {}).get('away', 0),
            }
            
            logger.debug(f"Successfully fetched match details for {extended_data['HT']} vs {extended_data['AT']}")
            return extended_data
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch match details for match ID {match_id}: {e}")
            return None
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing match detail response for match ID {match_id}: {e}")
            return None
    
    def scrape_season_data(self, season: str = None) -> List[Dict]:
        """
        Scrape all match data for a specific season
        """
        if season is None:
            season = self.current_season
            
        logger.info(f"Starting to scrape {season} season data...")
        
        # Get basic match data from API
        basic_matches = self.get_matches_from_api(season)
        
        if not basic_matches:
            logger.warning("No matches found from API, generating sample data for 2024-25 season")
        
        # Fetch extended statistics for each match from API
        extended_matches = []
        for match in basic_matches:
            try:
                extended_match = self.fetch_match_detail_from_api(match)
                if extended_match:
                    extended_matches.append(extended_match)
                else:
                    logger.warning(f"Failed to fetch extended data for match {match.get('id', 'unknown')}")
                
                # Add small delay to be respectful
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing match {match}: {e}")
                continue
        
        logger.info(f"Successfully processed {len(extended_matches)} matches")
        return extended_matches
    
    def save_to_database(self, matches: List[Dict]):
        """
        Save scraped match data to the PostgreSQL database
        """
        if not matches:
            logger.warning("No matches to save")
            return
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Insert matches with conflict resolution
            insert_sql = f"""
            INSERT INTO {self.table_name} 
            (DT, HT, AT, FTHG, FTAG, FTR, HP, AP, HS, AS_, HST, AST, HC, AC, HF, AF, HY, AY, HR, AR, MW, SEASON)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (DT, HT, AT) DO UPDATE SET
                FTHG = EXCLUDED.FTHG,
                FTAG = EXCLUDED.FTAG,
                FTR = EXCLUDED.FTR,
                HP = EXCLUDED.HP,
                AP = EXCLUDED.AP,
                HS = EXCLUDED.HS,
                AS_ = EXCLUDED.AS_,
                HST = EXCLUDED.HST,
                AST = EXCLUDED.AST,
                HC = EXCLUDED.HC,
                AC = EXCLUDED.AC,
                HF = EXCLUDED.HF,
                AF = EXCLUDED.AF,
                HY = EXCLUDED.HY,
                AY = EXCLUDED.AY,
                HR = EXCLUDED.HR,
                AR = EXCLUDED.AR,
                MW = EXCLUDED.MW,
                SEASON = EXCLUDED.SEASON
            """
            
            saved_count = 0
            for match in matches:
                try:
                    cursor.execute(insert_sql, (
                        match['DT'], match['HT'], match['AT'], match['FTHG'], match['FTAG'],
                        match['FTR'], match['HP'], match['AP'], match['HS'], match['AS_'],
                        match['HST'], match['AST'], match['HC'], match['AC'], match['HF'],
                        match['AF'], match['HY'], match['AY'], match['HR'], match['AR'],
                        match['MW'], match['SEASON']
                    ))
                    saved_count += 1
                except psycopg2.Error as e:
                    logger.error(f"Error saving match {match['HT']} vs {match['AT']}: {e}")
            
            conn.commit()
            logger.info(f"Successfully saved {saved_count} matches to database")
            
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_database_stats(self):
        """
        Get statistics about the scraped data in the PostgreSQL database
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Total matches
            cursor.execute(f"SELECT COUNT(*) as count FROM {self.table_name}")
            total_matches = cursor.fetchone()['count']
            
            # Matches by season
            cursor.execute(f"SELECT SEASON, COUNT(*) as count FROM {self.table_name} GROUP BY SEASON")
            season_stats = cursor.fetchall()
            
            # Latest matches
            cursor.execute(f"""
                SELECT DT, HT, AT, FTHG, FTAG, FTR 
                FROM {self.table_name} 
                ORDER BY DT DESC 
                LIMIT 5
            """)
            latest_matches = cursor.fetchall()
            
            logger.info(f"Database Statistics:")
            logger.info(f"Total matches: {total_matches}")
            logger.info(f"Matches by season: {season_stats}")
            logger.info(f"Latest matches: {latest_matches}")
            
            return {
                'total_matches': total_matches,
                'season_stats': season_stats,
                'latest_matches': latest_matches
            }
            
        except psycopg2.Error as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
        finally:
            if conn:
                conn.close()
    
    def run_scraper(self, season: str = None):
        """
        Main method to run the complete scraping process
        """
        if season is None:
            season = self.current_season
            
        try:
            logger.info(f"Starting Premier League Web Scraper v2.0")
            logger.info(f"Target season: {season}")
            logger.info(f"Website URL: {self.base_url}")
            logger.info(f"API URL: {self.api_url}")
            
            # Setup database
            self.setup_database()
            
            # Scrape season data
            matches = self.scrape_season_data(season)
            
            if matches:
                # Save to database
                self.save_to_database(matches)
                
                # Show statistics
                self.get_database_stats()
                
                logger.info("Scraping completed successfully!")
                return True
            else:
                logger.error("No matches were scraped")
                return False
                
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return False


def main():
    """
    Main function to run the scraper
    """
    print("=" * 60)
    print("Premier League Web Scraper v2.0")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: 2024-25 Premier League Season")
    print(f"Database: weekly_scrapped_data.db")
    print("=" * 60)
    
    # Initialize scraper
    scraper = PremierLeagueWebScraper()
    
    # Run scraping process
    success = scraper.run_scraper("2024-25")
    
    if success:
        print("\n✅ Scraping completed successfully!")
        print(f"✅ Data saved to PostgreSQL database '{scraper.db_config['database']}'")
        print(f"✅ Table name: '{scraper.table_name}'")
        print(f"✅ Database running on: {scraper.db_config['host']}:{scraper.db_config['port']}")
    else:
        print("\n❌ Scraping failed. Check logs for details.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
