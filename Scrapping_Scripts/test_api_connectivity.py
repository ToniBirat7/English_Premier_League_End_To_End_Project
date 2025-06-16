#!/usr/bin/env python3
"""
Script to test API connectivity before running the web scraper
"""

import requests
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_connectivity(api_url=None):
    """Test connectivity to the API endpoint"""
    
    # Try multiple possible URLs for the API
    possible_urls = [
        'http://127.0.0.1:8000/api',          # Local development
        'http://localhost:8000/api',          # Local development alternative
        'http://host.docker.internal:8000/api' # Docker container accessing host
    ]
    
    if not api_url:
        # Get API URL from environment variables
        # api_url = os.getenv('api_url', 'http://192.168.1.79:8000/api')
        # Use the first URL by default, but we'll test all of them
        api_url = possible_urls[0]

    # Strip any trailing whitespace
    api_url = api_url.strip()
    
    print(f"Testing connectivity to API: {api_url}")
    
    # Test endpoints
    endpoints = [
        "",  # Base API URL
        "/matches/",  # Matches endpoint
        "/teams/"  # Teams endpoint (if available)
    ]
    
    all_success = True
    successful_url = None
    
    # First, try all possible URLs if we're using the default
    if api_url in possible_urls and len(possible_urls) > 1:
        print("Testing multiple possible API URLs:")
        for url in possible_urls:
            try:
                print(f"Trying: {url}")
                response = requests.get(
                    url, 
                    timeout=3,
                    headers={
                        'User-Agent': 'API-Connectivity-Test/1.0',
                        'Accept': 'application/json'
                    }
                )
                
                if response.status_code == 200:
                    print(f"✅ Success! Status code: {response.status_code}")
                    try:
                        data = response.json()
                        print(f"  Response: {str(data)[:100]}...")
                        api_url = url  # Use this URL for further tests
                        successful_url = url
                        break
                    except:
                        print(f"  Response is not JSON. Content: {response.text[:100]}...")
                else:
                    print(f"❌ Failed! Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"❌ Error: {e}")
    
    # Now test the endpoints with the selected URL
    print(f"\nTesting endpoints with URL: {api_url}")
    for endpoint in endpoints:
        try:
            url = f"{api_url}{endpoint}"
            print(f"Testing endpoint: {url}")
            
            response = requests.get(
                url, 
                timeout=5,
                headers={
                    'User-Agent': 'API-Connectivity-Test/1.0',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code == 200:
                print(f"✅ Success! Status code: {response.status_code}")
                try:
                    # Try to parse as JSON
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        print(f"  Found {len(data['results'])} results")
                    elif isinstance(data, list):
                        print(f"  Found {len(data)} items")
                    print(f"  Response: {str(data)[:100]}...")
                except:
                    print(f"  Response is not JSON. Content: {response.text[:100]}...")
            else:
                print(f"❌ Failed! Status code: {response.status_code}")
                print(f"  Response: {response.text[:100]}...")
                all_success = False
                
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: {e}")
            all_success = False
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout Error: {e}")
            all_success = False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            all_success = False
    
    # Return success status
    if all_success:
        print("\n✅ API connectivity test passed for all endpoints!")
        return True
    else:
        print("\n❌ API connectivity test failed for one or more endpoints!")
        return False

if __name__ == "__main__":
    # If URL is passed as argument, use it
    api_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    success = test_api_connectivity(api_url)
    
    # Exit with status code
    sys.exit(0 if success else 1)
