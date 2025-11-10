from fastapi import FastAPI, APIRouter, HTTPException, Depends, File, UploadFile, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr, ConfigDict, ValidationError
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import aiofiles
import base64
from auth import create_access_token, decode_token, get_password_hash, verify_password
from email_service import send_order_confirmation_email
from gmail_service import send_order_confirmation_email_gmail
from cities_data import ALL_CITIES, DEFAULT_DELIVERY_CHARGES, DEFAULT_OTHER_CITY_CHARGE, ANDHRA_PRADESH_CITIES, TELANGANA_CITIES
import random
import string
from math import radians, sin, cos, sqrt, atan2

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()

# Create API router
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add validation error handler to log details
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"VALIDATION ERROR on {request.url.path}")
    print(f"Request body: {await request.body()}")
    print(f"Validation errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# ============= MODELS =============

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleAuth(BaseModel):
    id_token: str
    
class PhoneAuth(BaseModel):
    phone: str
    otp: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    phone: Optional[str] = None
    auth_provider: str = "email"  # email, google, phone
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    category: str
    description: str
    image: str
    prices: List[dict]
    isBestSeller: bool = False
    isNew: bool = False
    tag: str = "Traditional"
    discount_percentage: Optional[float] = None
    discount_expiry_date: Optional[str] = None
    inventory_count: Optional[int] = None
    out_of_stock: bool = False
    available_cities: Optional[List[str]] = None  # Cities where product can be delivered

class DiscountUpdate(BaseModel):
    discount_percentage: float
    discount_expiry_date: str

class OrderItem(BaseModel):
    product_id: str
    name: str
    image: str
    weight: str
    price: float
    quantity: int
    description: Optional[str] = None

class OrderCreate(BaseModel):
    user_id: Optional[str] = "guest"
    customer_name: str
    email: str  # Changed from EmailStr to str for more flexibility
    phone: str
    address: Optional[str] = ""
    doorNo: Optional[str] = ""
    building: Optional[str] = ""
    street: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    pincode: Optional[str] = ""
    location: Optional[str] = ""  # Made optional, will use city as fallback
    items: List[OrderItem]
    subtotal: float
    delivery_charge: float
    total: float
    payment_method: str = "online"
    payment_sub_method: Optional[str] = None

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str
    tracking_code: str
    user_id: str
    customer_name: str
    email: str  # Changed from EmailStr to str
    phone: str
    address: str
    doorNo: Optional[str] = None
    building: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    location: str
    items: List[OrderItem]
    subtotal: float
    delivery_charge: float
    total: float
    payment_method: str
    payment_sub_method: Optional[str] = None
    payment_status: str = "pending"
    order_status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estimated_delivery: Optional[str] = None
    admin_notes: Optional[str] = None
    delivery_days: Optional[int] = None
    cancelled: bool = False
    cancel_reason: Optional[str] = None

class Location(BaseModel):
    name: str
    charge: float
    free_delivery_threshold: Optional[float] = None  # City-specific free delivery threshold
    state: Optional[str] = None

class State(BaseModel):
    name: str
    enabled: bool = True

class AdminLogin(BaseModel):
    password: str

class SavedUserDetails(BaseModel):
    identifier: str  # phone or email
    customer_name: str
    email: EmailStr
    phone: str
    doorNo: Optional[str] = None
    building: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    location: str

# ============= HELPER FUNCTIONS =============

def generate_order_id():
    """Generate unique order ID"""
    return f"AL{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"

def generate_tracking_code():
    """Generate tracking code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

async def get_current_user(authorization: Optional[str] = Header(None)):
    """Dependency to get current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check if it's an admin user
        if payload.get("is_admin") or payload.get("sub") == "admin":
            return {
                "id": "admin",
                "email": "admin@ananthalakshmi.com",
                "name": "Admin",
                "is_admin": True
            }
        
        user = await db.users.find_one({"id": payload.get("sub")}, {"_id": 0, "password": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")

async def get_current_user_optional(authorization: Optional[str] = Header(None)):
    """Dependency to get current user from JWT token - allows guest users"""
    if not authorization:
        # Return guest user
        return {
            "id": "guest",
            "email": "guest@ananthalakshmi.com",
            "name": "Guest",
            "is_admin": False
        }
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if not payload:
            # Return guest user if token is invalid
            return {
                "id": "guest",
                "email": "guest@ananthalakshmi.com",
                "name": "Guest",
                "is_admin": False
            }
        
        # Check if it's an admin user
        if payload.get("is_admin") or payload.get("sub") == "admin":
            return {
                "id": "admin",
                "email": "admin@ananthalakshmi.com",
                "name": "Admin",
                "is_admin": True
            }
        
        user = await db.users.find_one({"id": payload.get("sub")}, {"_id": 0, "password": 0})
        if not user:
            # Return guest user if user not found
            return {
                "id": "guest",
                "email": "guest@ananthalakshmi.com",
                "name": "Guest",
                "is_admin": False
            }
        
        return user
    except Exception as e:
        # Return guest user for any authentication error
        return {
            "id": "guest",
            "email": "guest@ananthalakshmi.com",
            "name": "Guest",
            "is_admin": False
        }

# ============= AUTHENTICATION APIS =============

@api_router.post("/auth/register")
async def register(user_data: UserRegister):
    """Register new user with email and password"""
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    user = {
        "id": str(uuid.uuid4()),
        "email": user_data.email,
        "name": user_data.name,
        "phone": user_data.phone,
        "password": hashed_password,
        "auth_provider": "email",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.users.insert_one(user)
    
    # Create token
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    
    # Remove password and _id from response
    user.pop("password", None)
    user.pop("_id", None)
    
    return {
        "user": user,
        "token": token,
        "message": "Registration successful"
    }

@api_router.post("/auth/login")
async def login(user_data: UserLogin):
    """Login with email and password"""
    user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    
    if not user or not verify_password(user_data.password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    
    # Remove password from response
    user.pop("password", None)
    
    return {
        "user": user,
        "token": token,
        "message": "Login successful"
    }

@api_router.post("/auth/google")
async def google_auth(auth_data: GoogleAuth):
    """Google OAuth authentication (mock implementation)"""
    # In production, verify the id_token with Google
    # For now, this is a mock implementation
    
    # Mock user data
    user_email = f"user{random.randint(1000, 9999)}@gmail.com"
    user_name = "Google User"
    
    # Check if user exists
    user = await db.users.find_one({"email": user_email}, {"_id": 0})
    
    if not user:
        # Create new user
        user = {
            "id": str(uuid.uuid4()),
            "email": user_email,
            "name": user_name,
            "auth_provider": "google",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(user)
        user.pop("_id", None)
    
    # Create token
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    
    return {
        "user": user,
        "token": token,
        "message": "Google authentication successful"
    }

@api_router.post("/auth/phone")
async def phone_auth(auth_data: PhoneAuth):
    """Phone OTP authentication (mock implementation)"""
    # In production, verify OTP
    # For now, this is a mock implementation
    
    # Mock OTP verification (assume OTP is correct)
    user = await db.users.find_one({"phone": auth_data.phone}, {"_id": 0})
    
    if not user:
        # Create new user
        user = {
            "id": str(uuid.uuid4()),
            "email": f"{auth_data.phone}@phone.user",
            "name": f"User {auth_data.phone}",
            "phone": auth_data.phone,
            "auth_provider": "phone",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(user)
        user.pop("_id", None)
    
    # Create token
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    
    return {
        "user": user,
        "token": token,
        "message": "Phone authentication successful"
    }

@api_router.post("/auth/admin-login")
async def admin_login(login_data: AdminLogin):
    """Admin login with password - returns JWT token"""
    # Check admin password (stored in environment or hardcoded for now)
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    if login_data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    # Create admin user object
    admin_user = {
        "id": "admin",
        "email": "admin@ananthalakshmi.com",
        "name": "Admin",
        "is_admin": True
    }
    
    # Create token with long expiration for admin
    token = create_access_token({"sub": admin_user["id"], "email": admin_user["email"], "is_admin": True})
    
    return {
        "user": admin_user,
        "token": token,
        "message": "Admin login successful"
    }

@api_router.get("/user-details/{identifier}")
async def get_saved_user_details(identifier: str):
    """Get saved user details by phone or email"""
    details = await db.saved_user_details.find_one({"identifier": identifier}, {"_id": 0})
    
    if not details:
        return None
    
    return details

# ============= PRODUCTS APIS =============

@api_router.get("/products")
async def get_products(city: Optional[str] = None):
    """Get all products with discount calculation, optionally filtered by city availability"""
    # Build query filter
    query_filter = {}
    if city:
        # Filter products that either have no city restriction or include the requested city
        query_filter = {
            "$or": [
                {"available_cities": None},
                {"available_cities": []},
                {"available_cities": city}
            ]
        }
    
    products = await db.products.find(query_filter, {"_id": 0}).to_list(1000)
    
    # Calculate discounted prices for each product
    for product in products:
        discount_percentage = product.get('discount_percentage')
        discount_expiry = product.get('discount_expiry_date')
        
        # Check if discount is valid
        discount_active = False
        if discount_percentage and discount_expiry:
            try:
                # Parse the date string
                expiry_date_str = discount_expiry.replace('Z', '+00:00')
                if 'T' in expiry_date_str:
                    expiry_date = datetime.fromisoformat(expiry_date_str)
                else:
                    # If only date is provided (YYYY-MM-DD), add time and timezone
                    expiry_date = datetime.fromisoformat(expiry_date_str + "T23:59:59+00:00")
                
                # Ensure timezone awareness for comparison
                if expiry_date.tzinfo is None:
                    expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                
                if expiry_date > datetime.now(timezone.utc):
                    discount_active = True
            except:
                pass
        
        product['discount_active'] = discount_active
        
        # Calculate discounted prices if discount is active
        if discount_active and discount_percentage:
            discounted_prices = []
            for price_item in product.get('prices', []):
                original_price = price_item['price']
                discounted_price = round(original_price * (1 - discount_percentage / 100), 2)
                discounted_prices.append({
                    **price_item,
                    'original_price': original_price,
                    'discounted_price': discounted_price
                })
            product['discounted_prices'] = discounted_prices
    
    return products

@api_router.post("/products")
async def create_product(product: Product, current_user: dict = Depends(get_current_user)):
    """Create new product (Admin only)"""
    product_dict = product.model_dump()
    await db.products.insert_one(product_dict)
    product_dict.pop("_id", None)
    return {"message": "Product created successfully", "product": product_dict}

@api_router.put("/products/{product_id}")
async def update_product(product_id: str, product: Product, current_user: dict = Depends(get_current_user)):
    """Update product (Admin only)"""
    product_dict = product.model_dump()
    result = await db.products.update_one({"id": product_id}, {"$set": product_dict})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product updated successfully"}

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user: dict = Depends(get_current_user)):
    """Delete product (Admin only)"""
    result = await db.products.delete_one({"id": product_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product deleted successfully"}

# ============= DISCOUNT APIS =============

@api_router.post("/admin/products/{product_id}/discount")
async def add_discount(product_id: str, discount: DiscountUpdate, current_user: dict = Depends(get_current_user)):
    """Add or update discount for a product (Admin only)"""
    # Validate discount percentage
    if discount.discount_percentage < 0 or discount.discount_percentage > 70:
        raise HTTPException(status_code=400, detail="Discount must be between 0% and 70%")
    
    # Validate expiry date is in the future
    try:
        # Parse the date string
        expiry_date_str = discount.discount_expiry_date.replace('Z', '+00:00')
        if 'T' in expiry_date_str:
            expiry_date = datetime.fromisoformat(expiry_date_str)
        else:
            # If only date is provided (YYYY-MM-DD), add time and timezone
            expiry_date = datetime.fromisoformat(expiry_date_str + "T23:59:59+00:00")
        
        # Ensure timezone awareness for comparison
        if expiry_date.tzinfo is None:
            expiry_date = expiry_date.replace(tzinfo=timezone.utc)
        
        if expiry_date <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Expiry date must be in the future")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    # Update product
    result = await db.products.update_one(
        {"id": product_id},
        {"$set": {
            "discount_percentage": discount.discount_percentage,
            "discount_expiry_date": discount.discount_expiry_date
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Discount added successfully"}

@api_router.delete("/admin/products/{product_id}/discount")
async def remove_discount(product_id: str, current_user: dict = Depends(get_current_user)):
    """Remove discount from a product (Admin only)"""
    result = await db.products.update_one(
        {"id": product_id},
        {"$unset": {"discount_percentage": "", "discount_expiry_date": ""}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Discount removed successfully"}

@api_router.get("/admin/products/discounts")
async def get_products_with_discounts(current_user: dict = Depends(get_current_user)):
    """Get all products with discount information (Admin only)"""
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    return products

# ============= INVENTORY MANAGEMENT APIS =============

@api_router.put("/admin/products/{product_id}/inventory")
async def update_inventory(product_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    """Update product inventory (Admin only)"""
    inventory_count = data.get("inventory_count")
    
    if inventory_count is None:
        raise HTTPException(status_code=400, detail="inventory_count is required")
    
    if inventory_count < 0:
        raise HTTPException(status_code=400, detail="Inventory count cannot be negative")
    
    update_data = {
        "inventory_count": inventory_count,
        "out_of_stock": inventory_count == 0
    }
    
    result = await db.products.update_one(
        {"id": product_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Inventory updated successfully"}

@api_router.get("/admin/products/{product_id}/stock-status")
async def get_stock_status(product_id: str, current_user: dict = Depends(get_current_user)):
    """Get product stock status (Admin only)"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0, "out_of_stock": 1, "inventory_count": 1})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "out_of_stock": product.get("out_of_stock", False),
        "inventory_count": product.get("inventory_count")
    }

@api_router.put("/admin/products/{product_id}/stock-status")
async def toggle_stock_status(product_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    """Toggle out of stock status (Admin only)"""
    out_of_stock = data.get("out_of_stock", False)
    
    result = await db.products.update_one(
        {"id": product_id},
        {"$set": {"out_of_stock": out_of_stock}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Stock status updated successfully"}

@api_router.put("/admin/products/{product_id}/available-cities")
async def update_available_cities(product_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    """Update product available cities (Admin only)"""
    available_cities = data.get("available_cities", [])
    
    # Validate available_cities is a list
    if not isinstance(available_cities, list):
        raise HTTPException(status_code=400, detail="available_cities must be an array")
    
    result = await db.products.update_one(
        {"id": product_id},
        {"$set": {"available_cities": available_cities if available_cities else None}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Available cities updated successfully"}

# ============= BEST SELLER APIS =============

@api_router.post("/admin/best-sellers")
async def update_best_sellers(data: dict, current_user: dict = Depends(get_current_user)):
    """Bulk update best sellers (Admin only)"""
    product_ids = data.get("product_ids", [])
    
    # Remove best seller flag from all products
    await db.products.update_many({}, {"$set": {"isBestSeller": False}})
    
    # Set best seller flag for selected products
    if product_ids:
        await db.products.update_many(
            {"id": {"$in": product_ids}},
            {"$set": {"isBestSeller": True}}
        )
    
    return {"message": "Best sellers updated successfully"}

@api_router.get("/admin/best-sellers")
async def get_best_sellers(current_user: dict = Depends(get_current_user)):
    """Get all best seller products (Admin only)"""
    products = await db.products.find({"isBestSeller": True}, {"_id": 0}).to_list(1000)
    return products

# ============= FESTIVAL PRODUCT APIS =============

@api_router.post("/admin/festival-product")
async def set_festival_product(data: dict, current_user: dict = Depends(get_current_user)):
    """Set festival product (Admin only)"""
    product_id = data.get("product_id")
    
    if product_id:
        # Store festival product ID in settings collection
        await db.settings.update_one(
            {"key": "festival_product"},
            {"$set": {"key": "festival_product", "product_id": product_id}},
            upsert=True
        )
        return {"message": "Festival product set successfully"}
    else:
        # Remove festival product
        await db.settings.delete_one({"key": "festival_product"})
        return {"message": "Festival product removed successfully"}

@api_router.get("/admin/festival-product")
async def get_festival_product():
    """Get current festival product (Public API)"""
    setting = await db.settings.find_one({"key": "festival_product"}, {"_id": 0})
    
    if not setting:
        return None
    
    product_id = setting.get("product_id")
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    
    return product

# ============= FREE DELIVERY SETTINGS API =============

@api_router.post("/admin/settings/free-delivery")
async def set_free_delivery_threshold(data: dict, current_user: dict = Depends(get_current_user)):
    """Set free delivery threshold (Admin only)"""
    # Verify admin access
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    threshold = data.get("threshold", 0)
    enabled = data.get("enabled", False)
    
    await db.settings.update_one(
        {"key": "free_delivery"},
        {"$set": {"key": "free_delivery", "threshold": float(threshold), "enabled": bool(enabled)}},
        upsert=True
    )
    return {"message": "Free delivery settings updated successfully", "threshold": threshold, "enabled": enabled}

@api_router.get("/settings/free-delivery")
async def get_free_delivery_settings():
    """Get free delivery settings (Public API)"""
    setting = await db.settings.find_one({"key": "free_delivery"}, {"_id": 0})
    
    if not setting:
        # Default: Free delivery enabled for orders >= ₹1000
        return {"enabled": True, "threshold": 1000}
    
    return {"enabled": setting.get("enabled", True), "threshold": setting.get("threshold", 1000)}

# ============= IMAGE UPLOAD API =============

@api_router.post("/upload/image")
async def upload_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """Upload product image from desktop"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Create uploads directory if not exists
        uploads_dir = ROOT_DIR.parent / "frontend" / "public" / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = uploads_dir / filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Return URL
        image_url = f"/uploads/{filename}"
        return {"url": image_url, "message": "Image uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

# Alias for frontend compatibility
@api_router.post("/upload-image")
async def upload_image_alias(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """Upload product image from desktop (alias endpoint)"""
    return await upload_image(file, current_user)

# ============= ORDERS APIS =============

@api_router.post("/orders")
async def create_order(order_data: OrderCreate, current_user: dict = Depends(get_current_user_optional)):
    """Create new order - allows guest checkout"""
    try:
        print(f"DEBUG: Received order data: {order_data.model_dump()}")
        print(f"DEBUG: Current user: {current_user}")
        # Check inventory for all items
        for item in order_data.items:
            product = await db.products.find_one({"id": item.product_id})
            if product:
                if product.get("out_of_stock", False):
                    raise HTTPException(status_code=400, detail=f"Product {item.name} is out of stock")
                
                inventory_count = product.get("inventory_count")
                if inventory_count is not None and inventory_count < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Insufficient inventory for {item.name}")
        
        # Generate order ID and tracking code
        order_id = generate_order_id()
        tracking_code = generate_tracking_code()
        
        # Use city as location if location is not provided
        location_value = order_data.location or order_data.city or ""
        
        # SERVER-SIDE DELIVERY CHARGE CALCULATION
        # Find the city's delivery settings from database
        city_location = await db.locations.find_one({"name": order_data.city})
        
        # Calculate delivery charge based on city's free delivery threshold
        calculated_delivery_charge = 0.0
        
        if city_location:
            base_charge = city_location.get("charge", 99.0)
            free_delivery_threshold = city_location.get("free_delivery_threshold")
            
            # Check if order qualifies for free delivery
            if free_delivery_threshold and order_data.subtotal >= free_delivery_threshold:
                calculated_delivery_charge = 0.0
                print(f"🎁 FREE DELIVERY APPLIED: {order_data.city} - Subtotal ₹{order_data.subtotal} >= Threshold ₹{free_delivery_threshold}")
            else:
                calculated_delivery_charge = base_charge
                print(f"💰 DELIVERY CHARGE APPLIED: {order_data.city} - ₹{base_charge}")
        else:
            # City not found in database, use default charge
            calculated_delivery_charge = 99.0
            print(f"⚠️ CITY NOT FOUND: {order_data.city} - Using default charge ₹99")
        
        # Calculate correct total
        calculated_total = order_data.subtotal + calculated_delivery_charge
        
        # Create order with SERVER-CALCULATED values
        order = {
            "id": str(uuid.uuid4()),
            "order_id": order_id,
            "tracking_code": tracking_code,
            "user_id": current_user["id"],
            "customer_name": order_data.customer_name,
            "email": order_data.email,
            "phone": order_data.phone,
            "address": order_data.address,
            "doorNo": order_data.doorNo,
            "building": order_data.building,
            "street": order_data.street,
            "city": order_data.city,
            "state": order_data.state,
            "pincode": order_data.pincode,
            "location": location_value,
            "items": [item.model_dump() for item in order_data.items],
            "subtotal": order_data.subtotal,
            "delivery_charge": calculated_delivery_charge,
            "total": calculated_total,
            "payment_method": order_data.payment_method,
            "payment_sub_method": order_data.payment_sub_method,
            "payment_status": "completed",
            "order_status": "confirmed",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "estimated_delivery": (datetime.now(timezone.utc)).isoformat(),
            "admin_notes": None,
            "delivery_days": None,
            "cancelled": False,
            "cancel_reason": None
        }
        
        await db.orders.insert_one(order)
        
        # Update inventory for each item
        for item in order_data.items:
            product = await db.products.find_one({"id": item.product_id})
            if product and product.get("inventory_count") is not None:
                new_count = product["inventory_count"] - item.quantity
                update_data = {"inventory_count": max(0, new_count)}
                
                # Mark as out of stock if inventory reaches 0
                if new_count <= 0:
                    update_data["out_of_stock"] = True
                
                await db.products.update_one(
                    {"id": item.product_id},
                    {"$set": update_data}
                )
        
        # Save user details for future orders
        saved_details = {
            "identifier": order_data.phone,  # Use phone as primary identifier
            "customer_name": order_data.customer_name,
            "email": order_data.email,
            "phone": order_data.phone,
            "doorNo": order_data.doorNo,
            "building": order_data.building,
            "street": order_data.street,
            "city": order_data.city,
            "state": order_data.state,
            "pincode": order_data.pincode,
            "location": location_value,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.saved_user_details.update_one(
            {"identifier": order_data.phone},
            {"$set": saved_details},
            upsert=True
        )
        
        # Also save with email as identifier
        await db.saved_user_details.update_one(
            {"identifier": order_data.email},
            {"$set": {**saved_details, "identifier": order_data.email}},
            upsert=True
        )
        
        # Prepare email content
        items_list = []
        for item in order_data.items:
            items_list.append({
                "name": item.name,
                "weight": item.weight,
                "quantity": item.quantity,
                "price": item.price
            })
        
        email_data = {
            "order_id": order_id,
            "tracking_code": tracking_code,
            "customer_name": order_data.customer_name,
            "order_date": datetime.now().strftime("%B %d, %Y"),
            "total": calculated_total,
            "address": order_data.address,
            "doorNo": order_data.doorNo,
            "building": order_data.building,
            "street": order_data.street,
            "city": order_data.city,
            "state": order_data.state,
            "pincode": order_data.pincode,
            "location": order_data.location,
            "phone": order_data.phone,
            "items": items_list
        }
        
        # Send confirmation email via Gmail
        await send_order_confirmation_email_gmail(order_data.email, email_data)
        
        # Remove MongoDB _id field before returning
        order.pop("_id", None)
        
        return {
            "message": "Order created successfully",
            "order_id": order_id,
            "tracking_code": tracking_code,
            "subtotal": order_data.subtotal,
            "delivery_charge": calculated_delivery_charge,
            "total": calculated_total,
            "order": order
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@api_router.get("/orders/track/{identifier}")
async def track_order(identifier: str):
    """Track order by order_id, tracking_code, phone number, or email (public API)"""
    # Search by order_id, tracking_code, phone number, or email
    order = await db.orders.find_one(
        {"$or": [
            {"order_id": identifier}, 
            {"tracking_code": identifier}, 
            {"phone": identifier},
            {"email": identifier}
        ]},
        {"_id": 0}
    )
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@api_router.get("/orders/user/{user_id}")
async def get_user_orders(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get all orders for a user"""
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    orders = await db.orders.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return orders

@api_router.get("/orders")
async def get_all_orders(current_user: dict = Depends(get_current_user)):
    """Get all orders (Admin only)"""
    orders = await db.orders.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return orders

@api_router.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    """Update order status (Admin only)"""
    status = data.get("status")
    if not status:
        raise HTTPException(status_code=400, detail="Status is required")
    
    result = await db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"order_status": status}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order status updated successfully"}

@api_router.put("/orders/{order_id}/cancel")
async def cancel_order(order_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    """Cancel order (Admin only)"""
    cancel_reason = data.get("cancel_reason", "")
    
    result = await db.orders.update_one(
        {"order_id": order_id},
        {"$set": {
            "cancelled": True,
            "cancel_reason": cancel_reason,
            "order_status": "cancelled"
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order cancelled successfully"}

@api_router.put("/orders/{order_id}/admin-update")
async def update_order_admin_fields(order_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    """Update admin fields like notes and delivery days"""
    update_fields = {}
    
    if "admin_notes" in data:
        update_fields["admin_notes"] = data["admin_notes"]
    if "delivery_days" in data:
        update_fields["delivery_days"] = data["delivery_days"]
    if "order_status" in data:
        update_fields["order_status"] = data["order_status"]
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.orders.update_one(
        {"order_id": order_id},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order updated successfully"}

@api_router.get("/orders/analytics/summary")
async def get_orders_analytics(current_user: dict = Depends(get_current_user)):
    """Get order analytics and statistics"""
    try:
        # Get all orders
        all_orders = await db.orders.find({}, {"_id": 0}).to_list(10000)
        
        # Calculate statistics
        total_orders = len(all_orders)
        total_sales = sum(order.get("total", 0) for order in all_orders)
        active_orders = len([o for o in all_orders if not o.get("cancelled", False) and o.get("order_status") != "delivered"])
        cancelled_orders = len([o for o in all_orders if o.get("cancelled", False)])
        completed_orders = len([o for o in all_orders if o.get("order_status") == "delivered"])
        
        # Monthly sales
        from collections import defaultdict
        monthly_sales = defaultdict(float)
        monthly_orders = defaultdict(int)
        
        for order in all_orders:
            created_at = order.get("created_at", "")
            if created_at:
                try:
                    order_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    month_key = order_date.strftime("%Y-%m")
                    monthly_sales[month_key] += order.get("total", 0)
                    monthly_orders[month_key] += 1
                except:
                    pass
        
        # Top products
        product_counts = defaultdict(int)
        for order in all_orders:
            for item in order.get("items", []):
                product_counts[item.get("name", "Unknown")] += item.get("quantity", 0)
        
        top_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_orders": total_orders,
            "total_sales": total_sales,
            "active_orders": active_orders,
            "cancelled_orders": cancelled_orders,
            "completed_orders": completed_orders,
            "monthly_sales": dict(monthly_sales),
            "monthly_orders": dict(monthly_orders),
            "top_products": [{"name": name, "count": count} for name, count in top_products]
        }
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

# ============= USER DETAILS API =============

@api_router.get("/user-details/{identifier}")
async def get_user_details(identifier: str):
    """Get user details by phone or email from most recent order"""
    # Search for the most recent order with this phone or email
    order = await db.orders.find_one(
        {"$or": [
            {"phone": identifier},
            {"email": identifier}
        ]},
        {"_id": 0},
        sort=[("created_at", -1)]  # Get most recent order
    )
    
    if not order:
        raise HTTPException(status_code=404, detail="No details found")
    
    # Return relevant customer details
    return {
        "customer_name": order.get("customer_name"),
        "email": order.get("email"),
        "phone": order.get("phone"),
        "doorNo": order.get("doorNo"),
        "building": order.get("building"),
        "street": order.get("street"),
        "city": order.get("city"),
        "state": order.get("state"),
        "pincode": order.get("pincode"),
        "location": order.get("location")
    }

# ============= LOCATIONS API =============

@api_router.get("/locations")
async def get_locations():
    """Get delivery locations with state information"""
    # Check if custom locations exist in database
    locations = await db.locations.find({}, {"_id": 0}).to_list(1000)
    
    if not locations:
        # Return default cities with charges and state information
        locations = []
        
        # Add default cities with charges
        for city, charge in DEFAULT_DELIVERY_CHARGES.items():
            state = "Andhra Pradesh" if city in ANDHRA_PRADESH_CITIES else "Telangana"
            locations.append({"name": city, "charge": charge, "state": state})
        
        # Add remaining AP cities with default charge
        for city in ANDHRA_PRADESH_CITIES:
            if city not in DEFAULT_DELIVERY_CHARGES:
                locations.append({"name": city, "charge": DEFAULT_OTHER_CITY_CHARGE, "state": "Andhra Pradesh"})
        
        # Add remaining Telangana cities with default charge
        for city in TELANGANA_CITIES:
            if city not in DEFAULT_DELIVERY_CHARGES:
                locations.append({"name": city, "charge": DEFAULT_OTHER_CITY_CHARGE, "state": "Telangana"})
    else:
        # For database locations, add state information if not present
        for loc in locations:
            if "state" not in loc or not loc["state"]:
                # Determine state based on city name
                city_name = loc["name"]
                if city_name in ANDHRA_PRADESH_CITIES:
                    loc["state"] = "Andhra Pradesh"
                elif city_name in TELANGANA_CITIES:
                    loc["state"] = "Telangana"
                else:
                    loc["state"] = "Andhra Pradesh"  # Default
    
    return locations

@api_router.post("/admin/locations")
async def update_locations(locations: List[Location], current_user: dict = Depends(get_current_user)):
    """Update delivery locations (Admin only)"""
    # Clear existing locations
    await db.locations.delete_many({})
    
    # Insert new locations
    if locations:
        location_dicts = [loc.model_dump() for loc in locations]
        await db.locations.insert_many(location_dicts)
    
    return {"message": "Locations updated successfully"}

@api_router.put("/admin/locations/{city_name}")
async def update_city_settings(
    city_name: str, 
    charge: Optional[float] = None,
    free_delivery_threshold: Optional[float] = None,
    current_user: dict = Depends(get_current_user)
):
    """Update city delivery settings including charge and free delivery threshold"""
    
    # Check if city exists in database
    existing = await db.locations.find_one({"name": city_name})
    
    if existing:
        # Update existing city
        update_data = {}
        if charge is not None:
            update_data["charge"] = charge
        if free_delivery_threshold is not None:
            update_data["free_delivery_threshold"] = free_delivery_threshold
        
        if update_data:
            await db.locations.update_one({"name": city_name}, {"$set": update_data})
    else:
        # Create new city entry
        city_data = {"name": city_name}
        if charge is not None:
            city_data["charge"] = charge
        if free_delivery_threshold is not None:
            city_data["free_delivery_threshold"] = free_delivery_threshold
        
        # Determine state
        if city_name in ANDHRA_PRADESH_CITIES:
            city_data["state"] = "Andhra Pradesh"
        elif city_name in TELANGANA_CITIES:
            city_data["state"] = "Telangana"
        else:
            city_data["state"] = "Andhra Pradesh"
        
        await db.locations.insert_one(city_data)
    
    return {"message": f"Settings updated for {city_name}"}

@api_router.delete("/admin/locations/{city_name}")
async def delete_location(city_name: str, current_user: dict = Depends(get_current_user)):
    """Delete a delivery location (Admin only)"""
    result = await db.locations.delete_one({"name": city_name})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    
    return {"message": f"Location '{city_name}' deleted successfully"}

# ============= STATES API =============

@api_router.get("/states")
async def get_states():
    """Get available states"""
    # Check if custom states exist in database
    states = await db.states.find({}, {"_id": 0}).to_list(1000)
    
    if not states:
        # Return default states
        default_states = [
            {"name": "Andhra Pradesh", "enabled": True},
            {"name": "Telangana", "enabled": True},
            {"name": "Karnataka", "enabled": False},
            {"name": "Tamil Nadu", "enabled": False},
            {"name": "Maharashtra", "enabled": False}
        ]
        return default_states
    
    return states

@api_router.get("/admin/states")
async def get_admin_states(current_user: dict = Depends(get_current_user)):
    """Get all states for admin management"""
    states = await db.states.find({}, {"_id": 0}).to_list(1000)
    
    if not states:
        # Return default states
        default_states = [
            {"name": "Andhra Pradesh", "enabled": True},
            {"name": "Telangana", "enabled": True},
            {"name": "Karnataka", "enabled": False},
            {"name": "Tamil Nadu", "enabled": False},
            {"name": "Maharashtra", "enabled": False},
            {"name": "Kerala", "enabled": False},
            {"name": "Odisha", "enabled": False},
            {"name": "West Bengal", "enabled": False},
            {"name": "Gujarat", "enabled": False},
            {"name": "Rajasthan", "enabled": False}
        ]
        return default_states
    
    return states

@api_router.post("/admin/states")
async def add_state(state: State, current_user: dict = Depends(get_current_user)):
    """Add a new state (Admin only)"""
    # Check if state already exists
    existing = await db.states.find_one({"name": state.name})
    if existing:
        raise HTTPException(status_code=400, detail="State already exists")
    
    await db.states.insert_one(state.model_dump())
    return {"message": f"State '{state.name}' added successfully"}

@api_router.put("/admin/states/{state_name}")
async def update_state(state_name: str, state: State, current_user: dict = Depends(get_current_user)):
    """Update state status (Admin only)"""
    result = await db.states.update_one(
        {"name": state_name},
        {"$set": {"enabled": state.enabled}}
    )
    
    if result.matched_count == 0:
        # If state doesn't exist, create it
        await db.states.insert_one({"name": state_name, "enabled": state.enabled})
    
    return {"message": f"State '{state_name}' updated successfully"}

@api_router.delete("/admin/states/{state_name}")
async def delete_state(state_name: str, current_user: dict = Depends(get_current_user)):
    """Delete a state (Admin only)"""
    result = await db.states.delete_one({"name": state_name})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="State not found")
    
    return {"message": f"State '{state_name}' deleted successfully"}


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Anantha Lakshmi API Server", "status": "running"}
