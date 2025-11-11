#!/usr/bin/env python3
"""
Backend API Testing Script for Anantha Lakshmi Food Delivery App
COMPREHENSIVE BUG REPORTING FLOW TEST
Tests the complete bug reporting flow from submission to admin viewing:
1. Bug report submission (POST /api/reports)
2. Admin login (POST /api/auth/admin-login) 
3. Admin fetch bug reports (GET /api/admin/reports)
4. Update report status (PUT /api/admin/reports/{report_id}/status)
5. Verify complete flow: Submit report → Admin sees it in panel
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
BACKEND_URL = "https://otp-repair-1.preview.emergentagent.com/api"
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

def main():
    """Main testing function - ADMIN PASSWORD CHANGE OTP TESTING"""
    print("🚀 Starting Admin Password Change OTP Testing")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    print("="*80)
    
    # Test the admin password change OTP flow
    success = test_admin_password_change_otp()
    
    if success:
        print(f"\n🎉 OVERALL RESULT: OTP TESTING COMPLETED")
        print(f"✅ Admin password change OTP endpoints tested")
        print(f"✅ Any 500 errors have been identified and logged")
        return 0
    else:
        print(f"\n⚠️  OVERALL RESULT: ISSUES FOUND IN OTP FLOW")
        print(f"❌ 500 errors detected - check logs above for details")
        return 1
    
    # Prepare authorization headers
    auth_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    # ============= STEP 2: SUBMIT BUG REPORTS =============
    print("\n" + "="*80)
    print("📝 STEP 2: SUBMIT BUG REPORTS - POST /api/reports")
    print("="*80)
    
    # Test scenarios from review request
    test_reports = [
        {
            "email": "test@example.com",
            "mobile": "9876543210", 
            "issue_description": "Testing mobile bug report feature - dropdown menu issue"
        },
        {
            "email": "user2@example.com",
            "mobile": "9876543211",
            "issue_description": "Admin panel not loading properly on mobile devices"
        },
        {
            "email": "user3@example.com", 
            "mobile": "9876543212",
            "issue_description": "Product images not displaying correctly in cart"
        }
    ]
    
    submitted_reports = []
    for i, report_data in enumerate(test_reports):
        print(f"\n--- Submitting Report {i+1}/3 ---")
        success, report_id = test_bug_report_submission(
            report_data["email"],
            report_data["mobile"], 
            report_data["issue_description"]
        )
        
        test_results[f'submit_report_{i+1}'] = success
        
        if success and report_id:
            submitted_reports.append((report_id, report_data))
            created_report_ids.append(report_id)
    
    # ============= STEP 3: FETCH BUG REPORTS (ADMIN) =============
    print("\n" + "="*80)
    print("🐛 STEP 3: FETCH BUG REPORTS - GET /api/admin/reports")
    print("="*80)
    
    # Test 3.1: Get bug reports with admin authentication
    success, reports_response = test_api_endpoint(
        "GET",
        "/admin/reports",
        headers=auth_headers,
        description="Fetch bug reports with admin authentication"
    )
    
    test_results['fetch_bug_reports_with_auth'] = success
    
    if success and isinstance(reports_response, list):
        print(f"\n📊 Bug Reports Retrieved: {len(reports_response)}")
        test_results['verify_json_response'] = True
        
        # ============= STEP 4: VERIFY SUBMITTED REPORTS =============
        print("\n" + "="*80)
        print("🔍 STEP 4: VERIFY SUBMITTED REPORTS IN LIST")
        print("="*80)
        
        for i, (report_id, report_data) in enumerate(submitted_reports):
            print(f"\n--- Verifying Report {i+1} ---")
            success = verify_report_in_list(
                reports_response,
                report_data["email"],
                report_data["mobile"],
                report_data["issue_description"]
            )
            test_results[f'verify_report_{i+1}'] = success
        
        # ============= STEP 5: TEST REPORT ORDERING =============
        print("\n" + "="*80)
        print("📅 STEP 5: TEST REPORT ORDERING")
        print("="*80)
        
        ordering_success = test_report_ordering(reports_response)
        test_results['report_ordering'] = ordering_success
        
    else:
        print(f"❌ Failed to fetch bug reports or invalid response")
        test_results['verify_json_response'] = False
    
    # Test 3.2: Test without authentication (should fail with 401)
    print(f"\n--- Testing Without Authentication ---")
    success, unauth_response = test_api_endpoint(
        "GET",
        "/admin/reports",
        description="Fetch bug reports without authentication (should return 401)",
        expected_status=401
    )
    
    test_results['fetch_bug_reports_no_auth'] = success
    
    # ============= STEP 6: UPDATE REPORT STATUS =============
    print("\n" + "="*80)
    print("🔄 STEP 6: UPDATE REPORT STATUS - PUT /api/admin/reports/{id}/status")
    print("="*80)
    
    if created_report_ids:
        first_report_id = created_report_ids[0]
        
        # Test updating status to "In Progress"
        success, status_response = test_api_endpoint(
            "PUT",
            f"/admin/reports/{first_report_id}/status",
            headers=auth_headers,
            data={"status": "In Progress"},
            description="Update report status to 'In Progress'"
        )
        
        test_results['update_report_status'] = success
        
        if success:
            # Verify status change by fetching reports again
            print(f"\n--- Verifying Status Update ---")
            success, updated_reports = test_api_endpoint(
                "GET",
                "/admin/reports",
                headers=auth_headers,
                description="Fetch reports to verify status update"
            )
            
            if success and isinstance(updated_reports, list):
                # Find the updated report
                for report in updated_reports:
                    if report.get("id") == first_report_id:
                        if report.get("status") == "In Progress":
                            print(f"✅ SUCCESS: Status successfully updated to 'In Progress'")
                            test_results['verify_status_update'] = True
                        else:
                            print(f"❌ FAILED: Status not updated, still: {report.get('status')}")
                            test_results['verify_status_update'] = False
                        break
                else:
                    print(f"❌ FAILED: Updated report not found in list")
                    test_results['verify_status_update'] = False
            else:
                print(f"❌ FAILED: Could not fetch reports to verify status update")
                test_results['verify_status_update'] = False
    else:
        print(f"⚠️  No report IDs available for status update test")
        test_results['update_report_status'] = False
        test_results['verify_status_update'] = False
    
    # ============= FINAL SUMMARY =============
    print(f"\n{'='*80}")
    print("🎯 COMPREHENSIVE BUG REPORTING FLOW TEST SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n📊 Overall Test Statistics:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Success Rate: {success_rate:.1f}%")
    
    # Group results by test phase
    print(f"\n📋 Detailed Results by Test Phase:")
    
    phases = {
        "1. Admin Authentication": ['admin_login'],
        "2. Bug Report Submission": ['submit_report_1', 'submit_report_2', 'submit_report_3'],
        "3. Admin Fetch Reports": ['fetch_bug_reports_with_auth', 'verify_json_response', 'fetch_bug_reports_no_auth'],
        "4. Report Verification": ['verify_report_1', 'verify_report_2', 'verify_report_3'],
        "5. Report Ordering": ['report_ordering'],
        "6. Status Management": ['update_report_status', 'verify_status_update']
    }
    
    for phase, test_keys in phases.items():
        phase_tests = {k: v for k, v in test_results.items() if k in test_keys}
        if phase_tests:
            phase_passed = sum(1 for v in phase_tests.values() if v)
            phase_total = len(phase_tests)
            print(f"\n  {phase} ({phase_passed}/{phase_total} passed):")
            for test_name, result in phase_tests.items():
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"    {test_name}: {status}")
    
    print(f"\n🎯 KEY FINDINGS:")
    
    # Critical flow verification
    critical_tests = ['admin_login', 'submit_report_1', 'fetch_bug_reports_with_auth', 'verify_report_1']
    critical_passed = sum(1 for test in critical_tests if test_results.get(test, False))
    
    if critical_passed == len(critical_tests):
        print(f"  ✅ CRITICAL FLOW WORKING: Submit report → Admin sees it in panel")
        print(f"      - Bug report submission works (POST /api/reports)")
        print(f"      - Admin can fetch bug reports (GET /api/admin/reports)")
        print(f"      - Submitted reports appear in admin panel")
        print(f"      - All required fields present and correct")
    else:
        print(f"  ❌ CRITICAL FLOW BROKEN: {critical_passed}/{len(critical_tests)} critical tests passed")
    
    # Authentication verification
    if test_results.get('admin_login') and test_results.get('fetch_bug_reports_no_auth'):
        print(f"  ✅ AUTHENTICATION WORKING: Admin endpoints properly protected")
    else:
        print(f"  ❌ AUTHENTICATION ISSUES: Admin endpoints may not be properly protected")
    
    # Status management verification
    if test_results.get('update_report_status') and test_results.get('verify_status_update'):
        print(f"  ✅ STATUS MANAGEMENT WORKING: Can update and verify report status")
    else:
        print(f"  ❌ STATUS MANAGEMENT ISSUES: Status updates may not be working")
    
    print(f"\n🔧 ENDPOINT VERIFICATION:")
    print(f"  📍 Bug Report Submission: POST {BACKEND_URL}/reports")
    print(f"  📍 Admin Login: POST {BACKEND_URL}/auth/admin-login")
    print(f"  📍 Admin Fetch Reports: GET {BACKEND_URL}/admin/reports")
    print(f"  📍 Update Report Status: PUT {BACKEND_URL}/admin/reports/{{id}}/status")
    
    if success_rate >= 80:
        print(f"\n🎉 OVERALL RESULT: SUCCESS - Bug reporting flow is working correctly!")
        print(f"✅ Users can submit bug reports from mobile dropdown menu")
        print(f"✅ Admin can view all bug reports in admin panel")
        print(f"✅ Complete flow: Submit report → Admin sees it → Can manage status")
        return 0
    else:
        print(f"\n⚠️  OVERALL RESULT: ISSUES FOUND - Bug reporting flow needs attention!")
        print(f"🔍 TROUBLESHOOTING:")
        print(f"  - Check if backend service is running properly")
        print(f"  - Verify all endpoints have correct /api prefix")
        print(f"  - Ensure database is accessible and working")
        print(f"  - Check admin authentication and permissions")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)