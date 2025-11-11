#!/usr/bin/env python3
"""
Backend API Testing Script for Anantha Lakshmi Food Delivery App
FOCUSED TEST: Bug Reporting and City Suggestion Endpoints
Tests: POST /api/report-issue and POST /api/suggest-city endpoints that were just fixed
"""

import requests
import json
import sys
from datetime import datetime, timedelta, timezone
import time
import random
import os
import tempfile

# Backend URL from environment
BACKEND_URL = "https://report-submission.preview.emergentagent.com/api"

def test_api_endpoint(method, endpoint, headers=None, data=None, description="", expected_status=None):
    """Test a single API endpoint"""
    url = f"{BACKEND_URL}{endpoint}"
    
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"Description: {description}")
    print(f"URL: {url}")
    if data:
        print(f"Request Data: {json.dumps(data, indent=2)}")
    print(f"{'='*60}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return False, None
            
        print(f"Status Code: {response.status_code}")
        
        # Try to parse JSON response
        response_data = None
        try:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        # Check if request was successful
        if expected_status:
            success = response.status_code == expected_status
        else:
            success = 200 <= response.status_code < 300
            
        if success:
            print("✅ SUCCESS: API endpoint is working as expected")
            return True, response_data
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            return False, response_data
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False, None
    except requests.exceptions.Timeout as e:
        print(f"❌ TIMEOUT ERROR: {str(e)}")
        return False, None
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False, None

def admin_login():
    """Login as admin and get auth token"""
    print("\n" + "="*80)
    print("🔐 ADMIN AUTHENTICATION")
    print("="*80)
    
    # Admin login with password
    login_data = {
        "password": "admin123"
    }
    
    success, response_data = test_api_endpoint(
        "POST",
        "/auth/admin-login",
        data=login_data,
        description="Admin login with password 'admin123'"
    )
    
    if success and response_data and "token" in response_data:
        token = response_data["token"]
        print(f"✅ Successfully logged in as admin and got JWT token")
        return token
    
    print("❌ Failed to get admin authentication token")
    return None

def test_api_endpoint_form_data(method, endpoint, headers=None, form_data=None, files=None, description="", expected_status=None):
    """Test API endpoint with form data (for file uploads)"""
    url = f"{BACKEND_URL}{endpoint}"
    
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"Description: {description}")
    print(f"URL: {url}")
    if form_data:
        print(f"Form Data: {form_data}")
    if files:
        print(f"Files: {list(files.keys())}")
    print(f"{'='*60}")
    
    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers, data=form_data, files=files, timeout=30)
        else:
            print(f"❌ Unsupported method for form data: {method}")
            return False, None
            
        print(f"Status Code: {response.status_code}")
        
        # Try to parse JSON response
        response_data = None
        try:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        # Check if request was successful
        if expected_status:
            success = response.status_code == expected_status
        else:
            success = 200 <= response.status_code < 300
            
        if success:
            print("✅ SUCCESS: API endpoint is working as expected")
            return True, response_data
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            return False, response_data
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False, None
    except requests.exceptions.Timeout as e:
        print(f"❌ TIMEOUT ERROR: {str(e)}")
        return False, None
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False, None

def create_test_image():
    """Create a small test image file for upload testing"""
    try:
        # Create a simple 1x1 pixel PNG image
        import base64
        
        # Minimal PNG data (1x1 transparent pixel)
        png_data = base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU8'
            'IQAAAAABJRU5ErkJggg=='
        )
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.write(png_data)
        temp_file.close()
        
        return temp_file.name
    except Exception as e:
        print(f"Warning: Could not create test image: {e}")
        return None

def main():
    """Main testing function - FOCUSED ON BUG REPORTING AND CITY SUGGESTION ENDPOINTS"""
    print("🚀 Starting Backend API Tests - Bug Reporting and City Suggestion Endpoints")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    
    # Test results tracking
    test_results = {}
    
    # ============= STEP 1: BUG REPORT ENDPOINT TEST =============
    print("\n" + "="*80)
    print("🐛 STEP 1: BUG REPORT ENDPOINT TEST - POST /api/reports")
    print("="*80)
    
    # Test 1.1: Create bug report with form-data fields as specified in review request
    bug_report_data = {
        "issue_title": "Test Issue",
        "description": "This is a test bug report",
        "name": "Test User",
        "email": "test@test.com",
        "phone": "9876543210",
        "page": "Home"
    }
    
    success, bug_response = test_api_endpoint_form_data(
        "POST",
        "/report-issue",
        form_data=bug_report_data,
        description="Create bug report with form-data fields (issue_title, description, name, email, phone, page)"
    )
    
    test_results['create_bug_report_form_data'] = success
    
    report_id_1 = None
    if success and bug_response:
        report_id_1 = bug_response.get('report_id')
        print(f"\n  📊 Bug Report Creation Verification:")
        print(f"    - Report ID: {report_id_1}")
        print(f"    - Has report_id: {bool(report_id_1)}")
        print(f"    - Message: {bug_response.get('message', 'N/A')}")
        print(f"    - Response structure valid: {isinstance(bug_response, dict)}")
        
        if report_id_1:
            print(f"    ✅ Bug report created successfully with proper response structure")
            test_results['verify_bug_report_creation'] = True
        else:
            print(f"    ❌ Bug report created but missing report_id")
            test_results['verify_bug_report_creation'] = False
    else:
        print(f"    ❌ Failed to create bug report")
        test_results['verify_bug_report_creation'] = False
    
    # Test 1.2: Test with minimal required fields only
    minimal_bug_report_data = {
        "issue_title": "Test Issue",
        "description": "This is a test bug report"
    }
    
    success, minimal_response = test_api_endpoint_form_data(
        "POST",
        "/report-issue",
        form_data=minimal_bug_report_data,
        description="Create bug report with minimal required fields only"
    )
    
    test_results['create_bug_report_minimal'] = success
    
    if success and minimal_response:
        print(f"\n  📊 Minimal Bug Report Verification:")
        print(f"    - Report ID: {minimal_response.get('report_id')}")
        print(f"    - Message: {minimal_response.get('message', 'N/A')}")
        print(f"    ✅ Bug report created with minimal fields")
    else:
        print(f"    ❌ Failed to create bug report with minimal fields")
    
    # ============= STEP 2: CITY SUGGESTION ENDPOINT TEST =============
    print("\n" + "="*80)
    print("🏙️ STEP 2: CITY SUGGESTION ENDPOINT TEST - POST /api/suggest-city")
    print("="*80)
    
    # Test 2.1: Create city suggestion with JSON body as specified in review request
    city_suggestion_data = {
        "state": "Andhra Pradesh",
        "city": "Kadapa",
        "customer_name": "Test Customer",
        "phone": "9876543210",
        "email": "customer@test.com"
    }
    
    success, city_response = test_api_endpoint(
        "POST",
        "/suggest-city",
        data=city_suggestion_data,
        description="Create city suggestion with JSON body (state, city, customer_name, phone, email)"
    )
    
    test_results['create_city_suggestion'] = success
    
    suggestion_id_1 = None
    if success and city_response:
        suggestion_id_1 = city_response.get('suggestion_id')
        print(f"\n  📊 City Suggestion Creation Verification:")
        print(f"    - Suggestion ID: {suggestion_id_1}")
        print(f"    - Has suggestion_id: {bool(suggestion_id_1)}")
        print(f"    - Message: {city_response.get('message', 'N/A')}")
        print(f"    - Response structure valid: {isinstance(city_response, dict)}")
        
        if suggestion_id_1:
            print(f"    ✅ City suggestion created successfully with proper response structure")
            test_results['verify_city_suggestion_creation'] = True
        else:
            print(f"    ❌ City suggestion created but missing suggestion_id")
            test_results['verify_city_suggestion_creation'] = False
    else:
        print(f"    ❌ Failed to create city suggestion")
        test_results['verify_city_suggestion_creation'] = False
    
    # Test 2.2: Test with different state and city
    city_suggestion_data_2 = {
        "state": "Telangana",
        "city": "Warangal",
        "customer_name": "Another Customer",
        "phone": "9999888777",
        "email": "another@test.com"
    }
    
    success, city_response_2 = test_api_endpoint(
        "POST",
        "/suggest-city",
        data=city_suggestion_data_2,
        description="Create city suggestion with different state and city (Telangana, Warangal)"
    )
    
    test_results['create_city_suggestion_2'] = success
    
    if success and city_response_2:
        suggestion_id_2 = city_response_2.get('suggestion_id')
        print(f"\n  📊 Second City Suggestion Verification:")
        print(f"    - Suggestion ID: {suggestion_id_2}")
        print(f"    - Message: {city_response_2.get('message', 'N/A')}")
        print(f"    ✅ Second city suggestion created successfully")
    else:
        print(f"    ❌ Failed to create second city suggestion")
    
    # Test 2.3: Test with missing required fields (should handle gracefully)
    incomplete_city_data = {
        "state": "Karnataka",
        "city": "Bangalore"
        # Missing customer_name, phone, email
    }
    
    success, incomplete_response = test_api_endpoint(
        "POST",
        "/suggest-city",
        data=incomplete_city_data,
        description="Test city suggestion with missing optional fields"
    )
    
    test_results['create_city_suggestion_incomplete'] = success
    
    if success and incomplete_response:
        print(f"\n  📊 Incomplete City Suggestion Verification:")
        print(f"    - Suggestion ID: {incomplete_response.get('suggestion_id')}")
        print(f"    - Message: {incomplete_response.get('message', 'N/A')}")
        print(f"    ✅ City suggestion created even with missing optional fields")
    else:
        print(f"    ❌ Failed to create city suggestion with missing optional fields")
    
    # ============= FINAL SUMMARY =============
    print(f"\n{'='*80}")
    print("🎯 BUG REPORTING AND CITY SUGGESTION ENDPOINTS TEST SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print("\n📋 Detailed Results by Test Category:")
    
    # Group results by category
    categories = {
        "Bug Report Endpoint (POST /api/report-issue)": [
            'create_bug_report_form_data', 'verify_bug_report_creation',
            'create_bug_report_minimal'
        ],
        "City Suggestion Endpoint (POST /api/suggest-city)": [
            'create_city_suggestion', 'verify_city_suggestion_creation',
            'create_city_suggestion_2', 'create_city_suggestion_incomplete'
        ]
    }
    
    for category, test_keys in categories.items():
        category_tests = {k: v for k, v in test_results.items() if k in test_keys}
        if category_tests:
            category_passed = sum(1 for v in category_tests.values() if v)
            category_total = len(category_tests)
            print(f"\n  {category} ({category_passed}/{category_total} passed):")
            for test_name, result in category_tests.items():
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"    {test_name}: {status}")
    
    print(f"\n📊 Overall Test Statistics:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n🎯 KEY FINDINGS:")
    
    # Bug Report Endpoint
    if test_results.get('create_bug_report_form_data') and test_results.get('verify_bug_report_creation'):
        print(f"  ✅ POST /api/report-issue endpoint works correctly with form-data")
        print(f"      - Accepts issue_title, description, name, email, phone, page fields")
        print(f"      - Returns success response with report_id")
        print(f"      - Response structure is valid")
    else:
        print(f"  ❌ POST /api/report-issue endpoint failed")
    
    if test_results.get('create_bug_report_minimal'):
        print(f"  ✅ Bug report endpoint works with minimal required fields")
    else:
        print(f"  ❌ Bug report endpoint failed with minimal fields")
    
    # City Suggestion Endpoint
    if test_results.get('create_city_suggestion') and test_results.get('verify_city_suggestion_creation'):
        print(f"  ✅ POST /api/suggest-city endpoint works correctly with JSON body")
        print(f"      - Accepts state, city, customer_name, phone, email fields")
        print(f"      - Returns success response with suggestion_id")
        print(f"      - Response structure is valid")
    else:
        print(f"  ❌ POST /api/suggest-city endpoint failed")
    
    if test_results.get('create_city_suggestion_2'):
        print(f"  ✅ City suggestion endpoint works with different state/city combinations")
    else:
        print(f"  ❌ City suggestion endpoint failed with different combinations")
    
    if test_results.get('create_city_suggestion_incomplete'):
        print(f"  ✅ City suggestion endpoint handles missing optional fields gracefully")
    else:
        print(f"  ❌ City suggestion endpoint failed with missing optional fields")
    
    print(f"\n🔧 ENDPOINT VERIFICATION:")
    print(f"  📍 Bug Report Endpoint: POST {BACKEND_URL}/reports")
    print(f"  📍 City Suggestion Endpoint: POST {BACKEND_URL}/suggest-city")
    print(f"  📍 Both endpoints are accessible with /api prefix as expected")
    
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests} test(s) failed. Check the detailed output above for specific issues.")
        print(f"🔍 TROUBLESHOOTING:")
        print(f"  - Verify backend service is running on {BACKEND_URL}")
        print(f"  - Check if endpoints are properly mapped with /api prefix")
        print(f"  - Ensure MongoDB is accessible and collections are created")
        return 1
    else:
        print(f"\n🎉 ALL TESTS PASSED! Bug reporting and city suggestion endpoints are working correctly.")
        print(f"✅ POST /api/report-issue - Bug report endpoint WORKING")
        print(f"✅ POST /api/suggest-city - City suggestion endpoint WORKING")
        print(f"✅ Both endpoints return proper response structure with IDs")
        print(f"✅ Frontend can now call these endpoints with /api prefix successfully")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)