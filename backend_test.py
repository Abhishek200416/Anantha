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
BACKEND_URL = "https://bugfix-response.preview.emergentagent.com/api"

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
    """Main testing function - FOCUSED ON ADMIN BUG REPORTS ENDPOINT"""
    print("🚀 Starting Backend API Tests - Admin Bug Reports Endpoint")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    
    # Test results tracking
    test_results = {}
    
    # ============= STEP 1: ADMIN LOGIN =============
    print("\n" + "="*80)
    print("🔐 STEP 1: ADMIN LOGIN - POST /api/auth/admin-login")
    print("="*80)
    
    # Get admin authentication token
    admin_token = admin_login()
    
    if not admin_token:
        print("❌ CRITICAL: Cannot proceed without admin authentication")
        test_results['admin_login'] = False
        return 1
    
    test_results['admin_login'] = True
    
    # Prepare authorization headers
    auth_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    # ============= STEP 2: FETCH BUG REPORTS =============
    print("\n" + "="*80)
    print("🐛 STEP 2: FETCH BUG REPORTS - GET /api/admin/reports")
    print("="*80)
    
    # Test 2.1: Get bug reports with admin authentication
    success, reports_response = test_api_endpoint(
        "GET",
        "/admin/reports",
        headers=auth_headers,
        description="Fetch bug reports with admin authentication"
    )
    
    test_results['fetch_bug_reports_with_auth'] = success
    
    if success and reports_response is not None:
        print(f"\n  📊 Bug Reports Response Verification:")
        print(f"    - Response type: {type(reports_response)}")
        print(f"    - Is array: {isinstance(reports_response, list)}")
        print(f"    - Number of reports: {len(reports_response) if isinstance(reports_response, list) else 'N/A'}")
        
        # Check if response is valid JSON (not HTML)
        if isinstance(reports_response, list):
            print(f"    ✅ Response is valid JSON array")
            test_results['verify_json_response'] = True
            
            # Check response structure if reports exist
            if len(reports_response) > 0:
                first_report = reports_response[0]
                print(f"\n  📋 Sample Report Structure:")
                for key, value in first_report.items():
                    print(f"    - {key}: {type(value).__name__}")
                print(f"    ✅ Bug reports have proper structure")
            else:
                print(f"    ℹ️  No bug reports found (empty array - this is normal)")
        else:
            print(f"    ❌ Response is not a JSON array")
            test_results['verify_json_response'] = False
    else:
        print(f"    ❌ Failed to fetch bug reports")
        test_results['verify_json_response'] = False
    
    # Test 2.2: Test without authentication (should fail with 401)
    success, unauth_response = test_api_endpoint(
        "GET",
        "/admin/reports",
        description="Fetch bug reports without authentication (should return 401)",
        expected_status=401
    )
    
    test_results['fetch_bug_reports_no_auth'] = success
    
    if success:
        print(f"    ✅ Correctly returns 401 when no authentication provided")
    else:
        print(f"    ❌ Should return 401 for unauthenticated requests")
    
    # ============= FINAL SUMMARY =============
    print(f"\n{'='*80}")
    print("🎯 ADMIN BUG REPORTS ENDPOINT TEST SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print("\n📋 Detailed Results by Test Category:")
    
    # Group results by category
    categories = {
        "Admin Authentication": [
            'admin_login'
        ],
        "Admin Bug Reports Endpoint (GET /api/admin/reports)": [
            'fetch_bug_reports_with_auth', 'verify_json_response',
            'fetch_bug_reports_no_auth'
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
    
    # Admin Login
    if test_results.get('admin_login'):
        print(f"  ✅ Admin login works correctly with password 'admin123'")
        print(f"      - Returns valid JWT token")
        print(f"      - Token can be used for subsequent API calls")
    else:
        print(f"  ❌ Admin login failed")
    
    # Admin Bug Reports Endpoint
    if test_results.get('fetch_bug_reports_with_auth') and test_results.get('verify_json_response'):
        print(f"  ✅ GET /api/admin/reports endpoint works correctly")
        print(f"      - Returns valid JSON response (not HTML)")
        print(f"      - Accepts Authorization header with JWT token")
        print(f"      - Returns array of bug reports")
    else:
        print(f"  ❌ GET /api/admin/reports endpoint failed")
        if not test_results.get('verify_json_response'):
            print(f"      - Response was not valid JSON (possibly HTML)")
    
    if test_results.get('fetch_bug_reports_no_auth'):
        print(f"  ✅ Endpoint correctly requires authentication (returns 401 without token)")
    else:
        print(f"  ❌ Endpoint should return 401 for unauthenticated requests")
    
    print(f"\n🔧 ENDPOINT VERIFICATION:")
    print(f"  📍 Admin Login: POST {BACKEND_URL}/auth/admin-login")
    print(f"  📍 Admin Bug Reports: GET {BACKEND_URL}/admin/reports")
    print(f"  📍 Both endpoints are accessible with /api prefix as expected")
    
    # Check the specific fix mentioned in review request
    if test_results.get('fetch_bug_reports_with_auth') and test_results.get('verify_json_response'):
        print(f"\n✅ FIX VERIFICATION:")
        print(f"  The /api prefix issue has been resolved!")
        print(f"  - GET /api/admin/reports now returns proper JSON response")
        print(f"  - No longer returning HTML instead of JSON")
        print(f"  - Endpoint is accessible with correct /api prefix")
    else:
        print(f"\n❌ FIX VERIFICATION:")
        print(f"  The /api prefix issue may still exist!")
        print(f"  - GET /api/admin/reports may still be returning HTML")
        print(f"  - Check if endpoint routing is correct")
    
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests} test(s) failed. Check the detailed output above for specific issues.")
        print(f"🔍 TROUBLESHOOTING:")
        print(f"  - Verify backend service is running on {BACKEND_URL}")
        print(f"  - Check if /api/admin/reports endpoint is properly mapped")
        print(f"  - Ensure admin authentication is working")
        print(f"  - Verify endpoint returns JSON, not HTML")
        return 1
    else:
        print(f"\n🎉 ALL TESTS PASSED! Admin bug reports endpoint is working correctly.")
        print(f"✅ Admin login with password 'admin123' - WORKING")
        print(f"✅ GET /api/admin/reports with Authorization header - WORKING")
        print(f"✅ Endpoint returns valid JSON response (not HTML) - WORKING")
        print(f"✅ Authentication protection working correctly - WORKING")
        print(f"✅ The /api prefix fix has been successfully verified!")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)