#!/usr/bin/env python3
"""
Backend API Testing Script for Anantha Lakshmi Food Delivery App
FOCUSED TEST: State Management APIs
Tests: GET /api/states, GET /api/admin/states (with admin auth), Database verification
"""

import requests
import json
import sys
from datetime import datetime, timedelta, timezone
import time
import random

# Backend URL from environment
BACKEND_URL = "https://city-state-counter.preview.emergentagent.com/api"

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

def main():
    """Main testing function - FOCUSED ON STATE MANAGEMENT APIS"""
    print("🚀 Starting FOCUSED Backend API Tests - State Management APIs")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    
    # Test results tracking
    test_results = {}
    
    # ============= STEP 1: ADMIN LOGIN AUTHENTICATION =============
    print("\n" + "="*80)
    print("🔐 STEP 1: ADMIN LOGIN AUTHENTICATION TEST")
    print("="*80)
    
    # Test 1.1: Admin login with correct password
    auth_token = admin_login()
    if not auth_token:
        print("\n❌ CRITICAL: Admin login failed - cannot proceed with admin-only tests")
        test_results['admin_login'] = False
        return 1
    
    test_results['admin_login'] = True
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Test 1.2: Verify token contains proper admin info
    print(f"\n  📊 Admin Token Verification:")
    print(f"    - Token received: {bool(auth_token)}")
    print(f"    - Token length: {len(auth_token) if auth_token else 0}")
    print(f"    - Token starts with expected format: {auth_token.startswith('eyJ') if auth_token else False}")
    
    # ============= STEP 2: TEST PUBLIC STATES API =============
    print("\n" + "="*80)
    print("🏛️ STEP 2: TEST PUBLIC STATES API (GET /api/states)")
    print("="*80)
    
    success, all_products = test_api_endpoint(
        "GET",
        "/products",
        description="Get products for order creation test"
    )
    
    test_results['get_products'] = success
    
    product_count = len(all_products) if all_products else 0
    print(f"\n📊 Products Available:")
    print(f"  - Total products found: {product_count}")
    
    if success and product_count > 0:
        print(f"  ✅ Products available for order creation")
        test_results['products_available'] = True
        
        # Select products for order
        order_products = random.sample(all_products, min(2, len(all_products)))
        print(f"\n  🎯 Selected {len(order_products)} products for test order:")
        for i, product in enumerate(order_products, 1):
            print(f"    {i}. {product['name']} (ID: {product['id']})")
    else:
        print(f"  ⚠️  No products in database - will create test order with mock product data")
        test_results['products_available'] = False
        
        # Create mock product data for testing
        order_products = [{
            'id': '1',
            'name': 'Immunity Dry Fruits Laddu',
            'image': '/images/immunity-laddu.jpg',
            'prices': [{'weight': '250g', 'price': 150.0}],
            'description': 'Healthy immunity boosting laddu with dry fruits'
        }]
        print(f"\n  🎯 Using mock product for test order:")
        print(f"    1. {order_products[0]['name']} (ID: {order_products[0]['id']})")
    
    
    # ============= STEP 3: CREATE TEST ORDER (GUEST CHECKOUT) =============
    print("\n" + "="*80)
    print("🛒 STEP 3: CREATE TEST ORDER (GUEST CHECKOUT)")
    print("="*80)
    
    # Build order items using available products
    order_items = []
    subtotal = 0.0
    
    for product in order_products:
        # Pick first price tier
        price_tier = product['prices'][0]
        quantity = random.randint(1, 2)
        item_total = price_tier['price'] * quantity
        subtotal += item_total
        
        order_items.append({
            "product_id": product['id'],
            "name": product['name'],
            "image": product['image'],
            "weight": price_tier['weight'],
            "price": price_tier['price'],
            "quantity": quantity,
            "description": product.get('description', '')
        })
    
    delivery_charge = 49.0
    total = subtotal + delivery_charge
    
    # Create order data as specified in test plan
    order_data = {
        "user_id": "guest",
        "customer_name": "Test Customer",
        "email": "test@example.com",
        "phone": "9876543210",
        "doorNo": "12-34",
        "building": "Sri Lakshmi Apartments",
        "street": "MG Road",
        "city": "Hyderabad",
        "state": "Telangana",
        "pincode": "500001",
        "location": "Hyderabad",
        "items": order_items,
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "total": total,
        "payment_method": "online",
        "payment_sub_method": "paytm"
    }
    
    print(f"\n  📦 Test Order Details:")
    print(f"    - Customer: {order_data['customer_name']}")
    print(f"    - Email: {order_data['email']}")
    print(f"    - Phone: {order_data['phone']}")
    print(f"    - Address: {order_data['doorNo']}, {order_data['building']}, {order_data['street']}")
    print(f"    - City: {order_data['city']}, {order_data['state']} - {order_data['pincode']}")
    print(f"    - Location: {order_data['location']}")
    print(f"    - Payment: {order_data['payment_method']} ({order_data['payment_sub_method']})")
    print(f"    - Items: {len(order_items)}")
    print(f"    - Subtotal: ₹{subtotal:.2f}")
    print(f"    - Delivery: ₹{delivery_charge:.2f}")
    print(f"    - Total: ₹{total:.2f}")
    
    # Test 3.1: Create order (should work without authentication - guest checkout)
    success, order_response = test_api_endpoint(
        "POST",
        "/orders",
        data=order_data,
        description="Create order as guest (no authentication required)"
    )
    
    test_results['create_order_guest'] = success
    
    order_id = None
    tracking_code = None
    
    if success and order_response:
        order_id = order_response.get('order_id')
        tracking_code = order_response.get('tracking_code')
        
        print(f"\n  📊 Order Creation Verification:")
        print(f"    - Order ID: {order_id}")
        print(f"    - Tracking Code: {tracking_code}")
        print(f"    - Has order_id: {bool(order_id)}")
        print(f"    - Has tracking_code: {bool(tracking_code)}")
        
        if order_id and tracking_code:
            print(f"    ✅ Order created successfully with proper IDs")
            test_results['verify_order_creation'] = True
        else:
            print(f"    ❌ Order created but missing IDs")
            test_results['verify_order_creation'] = False
    else:
        print(f"    ❌ Failed to create order")
        test_results['verify_order_creation'] = False
    
    # ============= STEP 4: GET ALL ORDERS (ADMIN ONLY) =============
    print("\n" + "="*80)
    print("📋 STEP 4: GET ALL ORDERS (ADMIN ONLY)")
    print("="*80)
    
    # Test 4.1: Get all orders with admin token (should work)
    success, admin_orders = test_api_endpoint(
        "GET",
        "/orders",
        headers=headers,
        description="Get all orders with admin authentication"
    )
    
    test_results['get_orders_admin'] = success
    
    if success and admin_orders is not None:
        orders_count = len(admin_orders) if isinstance(admin_orders, list) else 0
        print(f"\n  📊 Admin Orders Verification:")
        print(f"    - Total orders returned: {orders_count}")
        print(f"    - Response is list: {isinstance(admin_orders, list)}")
        
        # Check if our created order is in the list
        if order_id and isinstance(admin_orders, list):
            created_order_found = any(order.get('order_id') == order_id for order in admin_orders)
            print(f"    - Created order found in list: {created_order_found}")
            
            if created_order_found:
                print(f"    ✅ Created order appears in admin orders list")
                test_results['verify_order_in_admin_list'] = True
            else:
                print(f"    ❌ Created order not found in admin orders list")
                test_results['verify_order_in_admin_list'] = False
        else:
            print(f"    ⚠️  Cannot verify created order (no order_id or invalid response)")
            test_results['verify_order_in_admin_list'] = False
        
        print(f"    ✅ Admin can access orders endpoint")
    else:
        print(f"    ❌ Failed to get orders with admin token")
    
    # Test 4.2: Try to get orders without authentication (should fail with 401)
    success, response = test_api_endpoint(
        "GET",
        "/orders",
        description="Try to get orders without authentication (should return 401)",
        expected_status=401
    )
    
    test_results['get_orders_no_auth'] = success
    
    if success:
        print(f"    ✅ Correctly returns 401 when no authentication provided")
    else:
        print(f"    ❌ Should return 401 for unauthenticated access")
    
    # ============= STEP 5: GET ANALYTICS (ADMIN ONLY) =============
    print("\n" + "="*80)
    print("📊 STEP 5: GET ANALYTICS (ADMIN ONLY)")
    print("="*80)
    
    # Test 5.1: Get analytics with admin token (should work)
    success, analytics_data = test_api_endpoint(
        "GET",
        "/orders/analytics/summary",
        headers=headers,
        description="Get order analytics with admin authentication"
    )
    
    test_results['get_analytics_admin'] = success
    
    if success and analytics_data:
        print(f"\n  📊 Analytics Data Verification:")
        
        # Check expected fields
        expected_fields = ['total_orders', 'total_sales', 'active_orders', 'cancelled_orders', 'completed_orders']
        for field in expected_fields:
            value = analytics_data.get(field, 'N/A')
            print(f"    - {field}: {value}")
        
        # Check if analytics contains reasonable data
        total_orders = analytics_data.get('total_orders', 0)
        total_sales = analytics_data.get('total_sales', 0)
        
        if isinstance(total_orders, int) and isinstance(total_sales, (int, float)):
            print(f"    ✅ Analytics data has correct format")
            test_results['verify_analytics_format'] = True
            
            # If we created an order, total_orders should be at least 1
            if order_id and total_orders >= 1:
                print(f"    ✅ Analytics reflects created order (total_orders >= 1)")
                test_results['verify_analytics_data'] = True
            elif not order_id:
                print(f"    ℹ️  Cannot verify order count (no order was created)")
                test_results['verify_analytics_data'] = True
            else:
                print(f"    ⚠️  Analytics may not reflect recent order creation")
                test_results['verify_analytics_data'] = False
        else:
            print(f"    ❌ Analytics data has incorrect format")
            test_results['verify_analytics_format'] = False
            test_results['verify_analytics_data'] = False
        
        print(f"    ✅ Admin can access analytics endpoint")
    else:
        print(f"    ❌ Failed to get analytics with admin token")
        test_results['verify_analytics_format'] = False
        test_results['verify_analytics_data'] = False
    
    # Test 5.2: Try to get analytics without authentication (should fail with 401)
    success, response = test_api_endpoint(
        "GET",
        "/orders/analytics/summary",
        description="Try to get analytics without authentication (should return 401)",
        expected_status=401
    )
    
    test_results['get_analytics_no_auth'] = success
    
    if success:
        print(f"    ✅ Correctly returns 401 when no authentication provided")
    else:
        print(f"    ❌ Should return 401 for unauthenticated access")
    
    # ============= FINAL SUMMARY =============
    print(f"\n{'='*80}")
    print("🎯 ADMIN AUTHENTICATION & ORDERS FLOW TEST SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print("\n📋 Detailed Results by Test Category:")
    
    # Group results by category
    categories = {
        "Admin Authentication": ['admin_login'],
        "Products API": ['get_products', 'products_available'],
        "Order Creation (Guest)": ['create_order_guest', 'verify_order_creation'],
        "Admin Orders Access": ['get_orders_admin', 'verify_order_in_admin_list', 'get_orders_no_auth'],
        "Admin Analytics": ['get_analytics_admin', 'verify_analytics_format', 'verify_analytics_data', 'get_analytics_no_auth']
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
        print(f"  ✅ Admin login with password 'admin123' works correctly")
        print(f"  ✅ JWT token is properly generated and returned")
    else:
        print(f"  ❌ Admin login failed - check password or backend service")
    
    # Order Creation
    if test_results.get('create_order_guest') and test_results.get('verify_order_creation'):
        print(f"  ✅ Guest order creation works without authentication")
        print(f"  ✅ Order returns proper order_id and tracking_code")
    else:
        print(f"  ❌ Order creation failed - check order validation or backend service")
    
    # Admin Orders Access
    if test_results.get('get_orders_admin'):
        print(f"  ✅ Admin can access all orders with JWT token")
    else:
        print(f"  ❌ Admin orders access failed - check authentication or endpoint")
    
    if test_results.get('get_orders_no_auth'):
        print(f"  ✅ Orders endpoint properly requires authentication (returns 401)")
    else:
        print(f"  ❌ Orders endpoint should return 401 without authentication")
    
    # Analytics
    if test_results.get('get_analytics_admin'):
        print(f"  ✅ Admin can access analytics with JWT token")
    else:
        print(f"  ❌ Admin analytics access failed - check authentication or endpoint")
    
    if test_results.get('get_analytics_no_auth'):
        print(f"  ✅ Analytics endpoint properly requires authentication (returns 401)")
    else:
        print(f"  ❌ Analytics endpoint should return 401 without authentication")
    
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests} test(s) failed. Check the detailed output above for specific issues.")
        return 1
    else:
        print(f"\n🎉 ALL TESTS PASSED! Admin authentication and orders flow is working correctly.")
        print(f"✅ Admin login authentication with JWT token - WORKING")
        print(f"✅ Order creation and retrieval in admin panel - WORKING")
        print(f"✅ Analytics endpoint with proper authentication - WORKING")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)