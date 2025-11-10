#!/usr/bin/env python3
"""
Seed database with mock products from frontend
This script imports the mock products and adds them to MongoDB
"""

import asyncio
import os
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Mock products data (from frontend/src/mock.js)
MOCK_PRODUCTS = [
    # Laddus & Chikkis
    {
        "id": "1",
        "name": "Immunity Dry Fruits Laddu",
        "category": "laddus-chikkis",
        "description": "Boost immunity with dry fruits",
        "image": "https://images.unsplash.com/photo-1635952346904-95f2ccfcd029?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 399},
            {"weight": "1kg", "price": 1499}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Healthy Choice",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "2",
        "name": "Ragi Dry Fruits Laddu",
        "category": "laddus-chikkis",
        "description": "Healthy ragi with dry fruits",
        "image": "https://images.unsplash.com/photo-1605194000384-439c3ced8d15?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 299},
            {"weight": "1kg", "price": 1199}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Nutritious",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "3",
        "name": "Ground Nut Laddu",
        "category": "laddus-chikkis",
        "description": "Traditional groundnut laddu",
        "image": "https://images.unsplash.com/photo-1610508500445-a4592435e27e?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 299},
            {"weight": "1kg", "price": 1099}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Classic Taste",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "4",
        "name": "Oats Laddu",
        "category": "laddus-chikkis",
        "description": "Healthy oats laddu",
        "image": "https://images.unsplash.com/photo-1699708263762-00ca477760bd?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 299}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "New Arrival",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "5",
        "name": "Dry Fruits Chikki",
        "category": "laddus-chikkis",
        "description": "Crunchy dry fruits chikki",
        "image": "https://images.unsplash.com/photo-1695568181747-f54dff1d4654?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 299}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Crispy Delight",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "6",
        "name": "Palli Chikki",
        "category": "laddus-chikkis",
        "description": "Groundnut chikki",
        "image": "https://images.unsplash.com/photo-1695568180070-8b5acead5cf4?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 169}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Best Value",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "7",
        "name": "Nuvvulu Chikki",
        "category": "laddus-chikkis",
        "description": "Sesame chikki",
        "image": "https://images.unsplash.com/photo-1695568181747-f54dff1d4654?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 169}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Traditional",
        "inventory_count": None,
        "out_of_stock": False
    },
    {
        "id": "8",
        "name": "Kaju Katli Chikki",
        "category": "laddus-chikkis",
        "description": "Premium cashew chikki",
        "image": "https://images.unsplash.com/photo-1695568180070-8b5acead5cf4?w=500",
        "prices": [
            {"weight": "¼ kg", "price": 349}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Premium",
        "inventory_count": None,
        "out_of_stock": False
    }
]

async def seed_products():
    """Seed products into MongoDB database"""
    print("🌱 Starting database seeding...")
    print(f"📊 Database: {db_name}")
    print(f"🔗 MongoDB URL: {mongo_url[:30]}...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Check if products already exist
        existing_count = await db.products.count_documents({})
        print(f"📦 Existing products in database: {existing_count}")
        
        if existing_count > 0:
            response = input("⚠️  Products already exist. Do you want to replace them? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return
            
            # Clear existing products
            result = await db.products.delete_many({})
            print(f"🗑️  Deleted {result.deleted_count} existing products")
        
        # Insert mock products
        result = await db.products.insert_many(MOCK_PRODUCTS)
        print(f"✅ Successfully seeded {len(result.inserted_ids)} products!")
        
        # Verify products
        final_count = await db.products.count_documents({})
        print(f"📊 Total products in database: {final_count}")
        
        # Show sample products
        print("\n📋 Sample products:")
        async for product in db.products.find({}, {"_id": 0, "id": 1, "name": 1}).limit(5):
            print(f"  - ID: {product['id']}, Name: {product['name']}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        sys.exit(1)
    finally:
        client.close()
        print("\n✅ Database connection closed")

if __name__ == "__main__":
    print("="*60)
    print("   ANANTHA LAKSHMI - DATABASE SEEDER")
    print("="*60)
    asyncio.run(seed_products())
