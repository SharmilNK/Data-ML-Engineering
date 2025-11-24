#!/usr/bin/env python3
"""
Test script for the From Air to Care API
Usage: python test_api.py [API_URL]
"""
import sys
import requests
import json

# Default API URL
DEFAULT_API_URL = "http://localhost:8000"

def test_health(api_url):
    """Test health check endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{api_url}/health")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_root(api_url):
    """Test root endpoint."""
    print("\nTesting / endpoint...")
    try:
        response = requests.get(f"{api_url}/")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_predict(api_url):
    """Test prediction endpoint."""
    print("\nTesting /predict endpoint...")
    
    # Sample prediction request
    test_data = {
        "Temp_Max_C": 25.0,
        "Temp_Min_C": 15.0,
        "Humidity_Avg": 70.0,
        "Precip_mm": 0.0,
        "month": 6,
        "day": 15,
        "day_of_week": 5,
        "quarter": 2,
        "season": 3,
        "borough": "brooklyn"
    }
    
    try:
        response = requests.post(
            f"{api_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"  Status: {response.status_code}")
        print(f"  Request: {json.dumps(test_data, indent=2)}")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response text: {e.response.text}")
        return False

def main():
    """Run all tests."""
    api_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_API_URL
    print(f"=" * 60)
    print(f"Testing From Air to Care API")
    print(f"API URL: {api_url}")
    print(f"=" * 60)
    
    results = []
    results.append(("Health Check", test_health(api_url)))
    results.append(("Root Endpoint", test_root(api_url)))
    results.append(("Prediction", test_predict(api_url)))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed! ✓")
    else:
        print("Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

