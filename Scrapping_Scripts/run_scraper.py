#!/usr/bin/env python3
"""
Premier League Scraper Runner
============================

Simple script to run the web scraper and data analyzer.

Usage:
    python run_scraper.py [scrape|analyze|both]

Author: Football Analytics Team  
Date: June 10, 2025
"""

import sys
import subprocess
import os
from datetime import datetime

def install_requirements():
    """
    Install required packages
    """
    print("Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "scraper_requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def run_scraper():
    """
    Run the web scraper
    """
    print("\n" + "="*50)
    print("RUNNING WEB SCRAPER")
    print("="*50)
    
    try:
        result = subprocess.run([sys.executable, "web_scraper.py"], 
                              capture_output=True, text=True, timeout=300)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        if result.returncode == 0:
            print("✅ Scraper completed successfully")
            return True
        else:
            print("❌ Scraper failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Scraper timed out")
        return False
    except Exception as e:
        print(f"❌ Error running scraper: {e}")
        return False

def run_analyzer():
    """
    Run the data analyzer
    """
    print("\n" + "="*50)
    print("RUNNING DATA ANALYZER")
    print("="*50)
    
    try:
        result = subprocess.run([sys.executable, "data_analyzer.py"], 
                              capture_output=True, text=True, timeout=120)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        if result.returncode == 0:
            print("✅ Analyzer completed successfully")
            return True
        else:
            print("❌ Analyzer failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Analyzer timed out")
        return False
    except Exception as e:
        print(f"❌ Error running analyzer: {e}")
        return False

def check_database_connection():
    """
    Check if PostgreSQL database is accessible
    """
    try:
        import psycopg2
        
        # Test connection to the target database
        db_config = {
            'host': 'localhost',
            'port': '5434',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'weekly_scrapped_data'
        }
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        
        print(f"✅ PostgreSQL connection successful!")
        print(f"   Database: weekly_scrapped_data")
        print(f"   Version: {version[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Installing requirements...")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure PostgreSQL is running on port 5434")
        print("   and weekly_scrapped_data database exists")
        return False

def check_backend_status():
    """
    Check if the backend server is running
    """
    try:
        import requests
        response = requests.get("http://localhost:8000/api", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print("⚠️  Backend server responded with status:", response.status_code)
            return False
    except requests.RequestException:
        print("❌ Backend server is not accessible at http://localhost:8000")
        print("   Please make sure your Django backend is running")
        return False

def check_frontend_status():
    """
    Check if the frontend server is running
    """
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server is running")
            return True
        else:
            print("⚠️  Frontend server responded with status:", response.status_code)
            return False
    except requests.RequestException:
        print("❌ Frontend server is not accessible at http://localhost:3000")
        print("   Please make sure your React frontend is running")
        return False

def main():
    """
    Main function
    """
    print("🏆 Premier League Web Scraper Runner")
    print("="*50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: 2024-25 Premier League Season")
    print("="*50)
    
    # Parse command line arguments
    mode = "both"  # default
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if mode not in ["scrape", "analyze", "both"]:
        print("Usage: python run_scraper.py [scrape|analyze|both]")
        sys.exit(1)
    
    print(f"🚀 Mode: {mode}")
    
    # Check if requirements are installed
    try:
        import requests
        import pandas
    except ImportError:
        print("📦 Installing requirements...")
        if not install_requirements():
            sys.exit(1)
    
    # Check server status if scraping
    if mode in ["scrape", "both"]:
        print("\n🔍 Checking server status...")
        db_ok = check_database_connection()
        backend_ok = check_backend_status()
        frontend_ok = check_frontend_status()
        
        if not db_ok:
            print("\n❌ Database connection failed. Cannot proceed.")
            sys.exit(1)
        
        if not backend_ok:
            print("\n⚠️  Warning: Backend server not accessible.")
            print("   The scraper will use sample data instead.")
        
        if not frontend_ok:
            print("\n⚠️  Warning: Frontend server not accessible.")
            print("   The scraper will use API data or sample data.")
    
    # Run tasks based on mode
    success = True
    
    if mode in ["scrape", "both"]:
        success &= run_scraper()
    
    if mode in ["analyze", "both"]:
        # Check if PostgreSQL database has data
        try:
            import psycopg2
            conn = psycopg2.connect(
                host='localhost',
                port='5434',
                user='postgres',
                password='postgres',
                database='weekly_scrapped_data'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'premier_league_matches'")
            table_exists = cursor.fetchone()[0] > 0
            cursor.close()
            conn.close()
            
            if table_exists:
                success &= run_analyzer()
            else:
                print("❌ No data found in database. Please run scraper first.")
                success = False
        except Exception as e:
            print(f"❌ Database check failed: {e}. Please run scraper first.")
            success = False
    
    # Final status
    print("\n" + "="*50)
    if success:
        print("🎉 All tasks completed successfully!")
        print("\n📊 Results:")
        
        # Check PostgreSQL database
        try:
            import psycopg2
            conn = psycopg2.connect(
                host='localhost', port='5434', user='postgres', 
                password='postgres', database='weekly_scrapped_data'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM premier_league_matches")
            count = cursor.fetchone()[0]
            print(f"   Database: weekly_scrapped_data ({count} matches)")
            cursor.close()
            conn.close()
        except:
            print("   Database: weekly_scrapped_data (connection failed)")
            
        if os.path.exists("scraper.log"):
            print("   Logs: scraper.log")
        csv_files = [f for f in os.listdir('.') if f.startswith('premier_league_data_') and f.endswith('.csv')]
        if csv_files:
            print(f"   CSV Export: {csv_files[-1]}")
    else:
        print("❌ Some tasks failed. Check logs for details.")
    
    print("="*50)

if __name__ == "__main__":
    main()
