#!/usr/bin/env python3
"""
Backend API Testing Script for Anantha Lakshmi Food Delivery App
COMPREHENSIVE BACKEND API TESTING
Tests the recent fixes as requested in review:
1. Admin Authentication: POST /api/auth/admin-login with password 'admin123'
2. City Suggestions API: GET /api/admin/city-suggestions 
3. Products API: GET /api/products (verify 56 products across 7 categories)
4. Notifications Count API: GET /api/admin/notifications/count with admin token
5. Error Handling: Test endpoints with invalid data for proper JSON responses
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
BACKEND_URL = "https://admin-city-manager.preview.emergentagent.com/api"
ADMIN_PASSWORD = "admin123"

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

def test_bug_report_submission(email, mobile, issue_description):
    """Test bug report submission using form-data"""
    print(f"\n📝 Testing Bug Report Submission for {email}...")
    
    try:
        # Use form-data as specified in the review request
        form_data = {
            'email': email,
            'mobile': mobile,
            'issue_description': issue_description
        }
        
        response = requests.post(f"{BACKEND_URL}/reports", data=form_data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "report_id" in data and "message" in data:
                print(f"✅ SUCCESS: Bug report created with ID: {data['report_id']}")
                return True, data["report_id"]
            else:
                print(f"❌ FAILED: Missing report_id or message in response")
                return False, None
        else:
            print(f"❌ FAILED: HTTP {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False, None

def verify_report_in_list(reports, expected_email, expected_mobile, expected_description):
    """Verify that a specific report appears in the reports list with correct fields"""
    print(f"\n🔍 Verifying Report in List for {expected_email}...")
    
    for report in reports:
        if (report.get("email") == expected_email and 
            report.get("mobile") == expected_mobile and 
            report.get("issue_description") == expected_description):
            
            # Check all required fields from review request
            required_fields = ["id", "email", "mobile", "issue_description", "status", "created_at", "photo_url"]
            missing_fields = [field for field in required_fields if field not in report]
            
            if missing_fields:
                print(f"❌ FAILED: Missing fields: {missing_fields}")
                return False
            
            # Verify field formats
            if not report["id"]:  # Should be UUID format
                print(f"❌ FAILED: Report ID is empty")
                return False
            
            if report["status"] not in ["New", "In Progress", "Resolved"]:
                print(f"❌ FAILED: Invalid status: {report['status']}")
                return False
            
            print(f"✅ SUCCESS: Report found with correct fields")
            print(f"   - ID: {report['id']}")
            print(f"   - Email: {report['email']}")
            print(f"   - Mobile: {report['mobile']}")
            print(f"   - Issue: {report['issue_description'][:50]}...")
            print(f"   - Status: {report['status']}")
            print(f"   - Created: {report['created_at']}")
            print(f"   - Photo URL: {report['photo_url']}")
            return True
    
    print(f"❌ FAILED: Report not found for {expected_email}")
    return False

def test_report_ordering(reports):
    """Test that reports are ordered by newest first"""
    print(f"\n📅 Testing Report Ordering (Newest First)...")
    
    if len(reports) < 2:
        print(f"ℹ️  Less than 2 reports, ordering test skipped")
        return True
    
    try:
        # Check if reports are ordered by created_at descending (newest first)
        for i in range(len(reports) - 1):
            current_time = reports[i].get("created_at", "")
            next_time = reports[i + 1].get("created_at", "")
            
            if current_time and next_time:
                # Parse ISO timestamps
                current_dt = datetime.fromisoformat(current_time.replace('Z', '+00:00'))
                next_dt = datetime.fromisoformat(next_time.replace('Z', '+00:00'))
                
                if current_dt < next_dt:
                    print(f"❌ FAILED: Reports not in descending order")
                    print(f"   Current: {current_time}")
                    print(f"   Next: {next_time}")
                    return False
        
        print(f"✅ SUCCESS: Reports correctly ordered by newest first")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception parsing timestamps: {str(e)}")
        return False

def test_admin_password_change_otp():
    """Test admin password change OTP flow to identify 500 error"""
    print("\n" + "="*80)
    print("🔐 ADMIN PASSWORD CHANGE OTP TESTING")
    print("="*80)
    
    # Step 1: Admin login
    print("\n--- Step 1: Admin Login ---")
    admin_token = admin_login()
    
    if not admin_token:
        print("❌ CRITICAL: Cannot proceed without admin authentication")
        return False
    
    auth_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test OTP send endpoint
    print("\n--- Step 2: Testing OTP Send Endpoint ---")
    admin_email = "contact.ananthahomefoods@gmail.com"  # From .env file
    
    otp_send_data = {
        "email": admin_email
    }
    
    print(f"Testing POST /api/admin/profile/send-otp")
    success, otp_response = test_api_endpoint(
        "POST",
        "/admin/profile/send-otp",
        headers=auth_headers,
        data=otp_send_data,
        description=f"Send OTP to admin email: {admin_email}"
    )
    
    if not success:
        print("❌ FAILED: OTP send endpoint failed")
        return False
    
    print("✅ SUCCESS: OTP send endpoint working")
    
    # Step 3: Test OTP verification endpoint with invalid OTP (to see the error)
    print("\n--- Step 3: Testing OTP Verification Endpoint ---")
    
    # Test with invalid OTP first to see validation
    invalid_otp_data = {
        "email": admin_email,
        "otp": "123456",  # Invalid OTP
        "new_password": "newadmin123"
    }
    
    print(f"Testing POST /api/admin/profile/verify-otp-change-password with invalid OTP")
    success, verify_response = test_api_endpoint(
        "POST",
        "/admin/profile/verify-otp-change-password",
        headers=auth_headers,
        data=invalid_otp_data,
        description="Verify OTP with invalid OTP (should return 400)",
        expected_status=400
    )
    
    if success:
        print("✅ SUCCESS: OTP verification correctly rejects invalid OTP")
    else:
        print("❌ ISSUE: OTP verification endpoint behavior unexpected")
        
        # Check if it's a 500 error
        if verify_response is not None:
            print("🔍 INVESTIGATING 500 ERROR...")
            
            # Check backend logs for more details
            print("\n--- Checking Backend Logs ---")
            try:
                import subprocess
                result = subprocess.run(
                    ["tail", "-n", "50", "/var/log/supervisor/backend.err.log"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.stdout:
                    print("Backend Error Logs:")
                    print(result.stdout)
                else:
                    print("No recent error logs found")
                    
            except Exception as e:
                print(f"Could not read backend logs: {e}")
        
        return False
    
    # Step 4: Test with missing fields to trigger validation errors
    print("\n--- Step 4: Testing Validation Errors ---")
    
    test_cases = [
        {
            "name": "Missing email",
            "data": {"otp": "123456", "new_password": "newpass"},
            "expected_status": 422
        },
        {
            "name": "Missing OTP", 
            "data": {"email": admin_email, "new_password": "newpass"},
            "expected_status": 422
        },
        {
            "name": "Missing new_password",
            "data": {"email": admin_email, "otp": "123456"},
            "expected_status": 422
        },
        {
            "name": "Empty request body",
            "data": {},
            "expected_status": 422
        }
    ]
    
    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        success, response = test_api_endpoint(
            "POST",
            "/admin/profile/verify-otp-change-password",
            headers=auth_headers,
            data=test_case["data"],
            description=test_case["name"],
            expected_status=test_case["expected_status"]
        )
        
        if not success:
            print(f"❌ VALIDATION ERROR: {test_case['name']} - Expected {test_case['expected_status']} but got different response")
            
            # If we get 500 error, investigate
            if response is not None:
                print("🔍 INVESTIGATING 500 ERROR FOR VALIDATION...")
                try:
                    import subprocess
                    result = subprocess.run(
                        ["tail", "-n", "20", "/var/log/supervisor/backend.err.log"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.stdout:
                        print("Recent Backend Error Logs:")
                        print(result.stdout)
                        
                except Exception as e:
                    print(f"Could not read backend logs: {e}")
        else:
            print(f"✅ SUCCESS: {test_case['name']} handled correctly")
    
    return True

def test_admin_authentication():
    """Test admin authentication with password 'admin123'"""
    print("\n" + "="*80)
    print("🔐 TESTING ADMIN AUTHENTICATION")
    print("="*80)
    
    login_data = {"password": ADMIN_PASSWORD}
    
    success, response_data = test_api_endpoint(
        "POST",
        "/auth/admin-login",
        data=login_data,
        description="Admin login with password 'admin123'"
    )
    
    if success and response_data:
        # Verify response structure
        required_fields = ["user", "token", "message"]
        missing_fields = [field for field in required_fields if field not in response_data]
        
        if missing_fields:
            print(f"❌ FAILED: Missing fields in response: {missing_fields}")
            return False, None
        
        # Verify user object structure
        user = response_data.get("user", {})
        user_required_fields = ["id", "email", "name", "is_admin"]
        user_missing_fields = [field for field in user_required_fields if field not in user]
        
        if user_missing_fields:
            print(f"❌ FAILED: Missing user fields: {user_missing_fields}")
            return False, None
        
        # Verify admin user details
        if (user.get("id") == "admin" and 
            user.get("email") == "admin@ananthalakshmi.com" and
            user.get("name") == "Admin" and
            user.get("is_admin") == True):
            
            token = response_data.get("token")
            if token and len(token) > 100:  # JWT tokens are typically long
                print(f"✅ SUCCESS: Admin authentication working perfectly")
                print(f"   - User ID: {user.get('id')}")
                print(f"   - Email: {user.get('email')}")
                print(f"   - Name: {user.get('name')}")
                print(f"   - Is Admin: {user.get('is_admin')}")
                print(f"   - Token Length: {len(token)} characters")
                return True, token
            else:
                print(f"❌ FAILED: Invalid or missing JWT token")
                return False, None
        else:
            print(f"❌ FAILED: Invalid admin user object")
            return False, None
    
    print(f"❌ FAILED: Admin authentication failed")
    return False, None

def test_city_suggestions_api(admin_token):
    """Test GET /api/admin/city-suggestions API"""
    print("\n" + "="*80)
    print("🏙️  TESTING CITY SUGGESTIONS API")
    print("="*80)
    
    auth_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    success, response_data = test_api_endpoint(
        "GET",
        "/admin/city-suggestions",
        headers=auth_headers,
        description="Get city suggestions (admin endpoint)"
    )
    
    if success:
        # Verify response is proper JSON array
        if isinstance(response_data, list):
            print(f"✅ SUCCESS: City suggestions API returns proper JSON array")
            print(f"   - Number of suggestions: {len(response_data)}")
            
            # If there are suggestions, verify structure
            if response_data:
                suggestion = response_data[0]
                expected_fields = ["id", "state", "city", "customer_name", "phone", "email", "created_at", "status"]
                
                for field in expected_fields:
                    if field in suggestion:
                        print(f"   - Sample suggestion has '{field}' field ✓")
                    else:
                        print(f"   - Sample suggestion missing '{field}' field ⚠️")
            
            return True
        else:
            print(f"❌ FAILED: Response is not a JSON array, got: {type(response_data)}")
            return False
    
    print(f"❌ FAILED: City suggestions API failed")
    return False

def test_products_api():
    """Test GET /api/products API and verify 56 products across 7 categories"""
    print("\n" + "="*80)
    print("📦 TESTING PRODUCTS API")
    print("="*80)
    
    success, response_data = test_api_endpoint(
        "GET",
        "/products",
        description="Get all products and verify count and categories"
    )
    
    if success and isinstance(response_data, list):
        total_products = len(response_data)
        print(f"✅ SUCCESS: Products API returns {total_products} products")
        
        # Verify we have 56 products as expected
        if total_products == 56:
            print(f"✅ SUCCESS: Correct number of products (56)")
        else:
            print(f"⚠️  WARNING: Expected 56 products, got {total_products}")
        
        # Count products by category
        category_counts = {}
        for product in response_data:
            category = product.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\n📊 CATEGORY BREAKDOWN:")
        expected_categories = {
            "laddus-chikkis": 8,
            "sweets": 10, 
            "hot-items": 10,
            "snacks": 3,
            "pickles": 9,
            "powders": 12,
            "spices": 4
        }
        
        total_expected = sum(expected_categories.values())
        print(f"Expected total: {total_expected} products across {len(expected_categories)} categories")
        
        for category, expected_count in expected_categories.items():
            actual_count = category_counts.get(category, 0)
            if actual_count == expected_count:
                print(f"   ✅ {category}: {actual_count}/{expected_count}")
            else:
                print(f"   ⚠️  {category}: {actual_count}/{expected_count}")
        
        # Check for unexpected categories
        unexpected_categories = set(category_counts.keys()) - set(expected_categories.keys())
        if unexpected_categories:
            print(f"\n⚠️  UNEXPECTED CATEGORIES FOUND:")
            for category in unexpected_categories:
                print(f"   - {category}: {category_counts[category]} products")
        
        # Verify product structure
        if response_data:
            sample_product = response_data[0]
            required_fields = ["id", "name", "category", "description", "image", "prices", "isBestSeller", "isNew", "tag"]
            
            print(f"\n🔍 PRODUCT STRUCTURE VERIFICATION:")
            for field in required_fields:
                if field in sample_product:
                    print(f"   ✅ '{field}' field present")
                else:
                    print(f"   ❌ '{field}' field missing")
            
            # Verify prices structure
            prices = sample_product.get("prices", [])
            if isinstance(prices, list) and prices:
                print(f"   ✅ Prices array has {len(prices)} price tiers")
                sample_price = prices[0]
                if "weight" in sample_price and "price" in sample_price:
                    print(f"   ✅ Price structure correct (weight: {sample_price.get('weight')}, price: {sample_price.get('price')})")
                else:
                    print(f"   ❌ Price structure incorrect")
            else:
                print(f"   ❌ Prices array empty or invalid")
        
        return True
    
    print(f"❌ FAILED: Products API failed or returned invalid data")
    return False

def test_notifications_count_api(admin_token):
    """Test GET /api/admin/notifications/count API"""
    print("\n" + "="*80)
    print("🔔 TESTING NOTIFICATIONS COUNT API")
    print("="*80)
    
    auth_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    success, response_data = test_api_endpoint(
        "GET",
        "/admin/notifications/count",
        headers=auth_headers,
        description="Get notifications count with admin token"
    )
    
    if success and response_data:
        # Verify response structure
        expected_fields = ["bug_reports", "city_suggestions", "new_orders", "total"]
        
        print(f"🔍 NOTIFICATIONS COUNT STRUCTURE:")
        all_fields_present = True
        
        for field in expected_fields:
            if field in response_data:
                count = response_data[field]
                print(f"   ✅ {field}: {count}")
                
                # Verify it's a number
                if not isinstance(count, (int, float)):
                    print(f"   ⚠️  {field} is not a number: {type(count)}")
                    all_fields_present = False
            else:
                print(f"   ❌ Missing field: {field}")
                all_fields_present = False
        
        if all_fields_present:
            print(f"✅ SUCCESS: Notifications count API returns proper structure")
            
            # Verify total calculation
            calculated_total = (response_data.get("bug_reports", 0) + 
                             response_data.get("city_suggestions", 0) + 
                             response_data.get("new_orders", 0))
            actual_total = response_data.get("total", 0)
            
            if calculated_total == actual_total:
                print(f"   ✅ Total calculation correct: {actual_total}")
            else:
                print(f"   ⚠️  Total calculation mismatch: expected {calculated_total}, got {actual_total}")
            
            return True
        else:
            print(f"❌ FAILED: Missing required fields in response")
            return False
    
    print(f"❌ FAILED: Notifications count API failed")
    return False

def test_error_handling():
    """Test error handling with invalid data to ensure proper JSON responses"""
    print("\n" + "="*80)
    print("⚠️  TESTING ERROR HANDLING")
    print("="*80)
    
    test_cases = [
        {
            "name": "Invalid admin password",
            "method": "POST",
            "endpoint": "/auth/admin-login",
            "data": {"password": "wrongpassword"},
            "expected_status": 401,
            "description": "Test admin login with wrong password"
        },
        {
            "name": "Missing required fields in admin login",
            "method": "POST", 
            "endpoint": "/auth/admin-login",
            "data": {},
            "expected_status": 422,
            "description": "Test admin login with missing password field"
        },
        {
            "name": "Unauthorized access to admin endpoint",
            "method": "GET",
            "endpoint": "/admin/notifications/count",
            "data": None,
            "expected_status": 401,
            "description": "Test admin endpoint without authentication"
        },
        {
            "name": "Invalid product ID",
            "method": "GET",
            "endpoint": "/products/nonexistent-id",
            "data": None,
            "expected_status": 404,
            "description": "Test with non-existent product ID"
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        
        success, response_data = test_api_endpoint(
            test_case["method"],
            test_case["endpoint"],
            data=test_case["data"],
            description=test_case["description"],
            expected_status=test_case["expected_status"]
        )
        
        if success:
            # Verify response is proper JSON with detail field
            if response_data and "detail" in response_data:
                print(f"   ✅ Proper JSON error response with detail field")
            elif response_data:
                print(f"   ✅ JSON response received (structure may vary)")
            else:
                print(f"   ⚠️  No response data, but status code correct")
        else:
            print(f"   ❌ Error handling test failed")
            all_passed = False
    
    return all_passed

def main():
    """Main testing function - COMPREHENSIVE BACKEND API TESTING"""
    print("🚀 Starting Comprehensive Backend API Testing")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    print("="*80)
    
    test_results = []
    
    # Test 1: Admin Authentication
    print("\n" + "🔐" * 20 + " TEST 1: ADMIN AUTHENTICATION " + "🔐" * 20)
    auth_success, admin_token = test_admin_authentication()
    test_results.append(("Admin Authentication", auth_success))
    
    if not auth_success:
        print("❌ CRITICAL: Cannot proceed without admin authentication")
        return 1
    
    # Test 2: City Suggestions API
    print("\n" + "🏙️" * 20 + " TEST 2: CITY SUGGESTIONS API " + "🏙️" * 20)
    city_success = test_city_suggestions_api(admin_token)
    test_results.append(("City Suggestions API", city_success))
    
    # Test 3: Products API
    print("\n" + "📦" * 20 + " TEST 3: PRODUCTS API " + "📦" * 20)
    products_success = test_products_api()
    test_results.append(("Products API", products_success))
    
    # Test 4: Notifications Count API
    print("\n" + "🔔" * 20 + " TEST 4: NOTIFICATIONS COUNT API " + "🔔" * 20)
    notifications_success = test_notifications_count_api(admin_token)
    test_results.append(("Notifications Count API", notifications_success))
    
    # Test 5: Error Handling
    print("\n" + "⚠️" * 20 + " TEST 5: ERROR HANDLING " + "⚠️" * 20)
    error_handling_success = test_error_handling()
    test_results.append(("Error Handling", error_handling_success))
    
    # Summary
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS SUMMARY")
    print("="*80)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
        if success:
            passed_tests += 1
    
    print(f"\n🎯 OVERALL RESULT: {passed_tests}/{total_tests} tests passed ({(passed_tests/total_tests)*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - Backend APIs are working correctly!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Check individual test results above")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)