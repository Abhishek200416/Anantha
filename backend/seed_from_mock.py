#!/usr/bin/env python3
"""
Seed script to convert frontend mock products to real database products
"""
import os
import sys
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'anantha_lakshmi_db')
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
products_collection = db['products']

# Mock products data (from frontend/src/mock.js)
mock_products = [
    # Laddus & Chikkis
    {"id": 1, "name": "Immunity Dry Fruits Laddu", "category": "laddus-chikkis", "description": "Boost immunity with dry fruits", "image": "https://images.unsplash.com/photo-1635952346904-95f2ccfcd029?w=500", "prices": [{"weight": "¼ kg", "price": 399}, {"weight": "1kg", "price": 1499}], "isBestSeller": True, "isNew": False, "tag": "Healthy Choice"},
    {"id": 2, "name": "Ragi Dry Fruits Laddu", "category": "laddus-chikkis", "description": "Healthy ragi with dry fruits", "image": "https://images.unsplash.com/photo-1605194000384-439c3ced8d15?w=500", "prices": [{"weight": "¼ kg", "price": 299}, {"weight": "1kg", "price": 1199}], "isBestSeller": False, "isNew": False, "tag": "Nutritious"},
    {"id": 3, "name": "Ground Nut Laddu", "category": "laddus-chikkis", "description": "Traditional groundnut laddu", "image": "https://images.unsplash.com/photo-1610508500445-a4592435e27e?w=500", "prices": [{"weight": "¼ kg", "price": 299}, {"weight": "1kg", "price": 1099}], "isBestSeller": False, "isNew": False, "tag": "Classic Taste"},
    {"id": 4, "name": "Oats Laddu", "category": "laddus-chikkis", "description": "Healthy oats laddu", "image": "https://images.unsplash.com/photo-1699708263762-00ca477760bd?w=500", "prices": [{"weight": "¼ kg", "price": 299}], "isBestSeller": False, "isNew": True, "tag": "New Arrival"},
    {"id": 5, "name": "Dry Fruits Chikki", "category": "laddus-chikkis", "description": "Crunchy dry fruits chikki", "image": "https://images.unsplash.com/photo-1695568181747-f54dff1d4654?w=500", "prices": [{"weight": "¼ kg", "price": 299}], "isBestSeller": False, "isNew": False, "tag": "Crispy Delight"},
    {"id": 6, "name": "Palli Chikki", "category": "laddus-chikkis", "description": "Groundnut chikki", "image": "https://images.unsplash.com/photo-1695568180070-8b5acead5cf4?w=500", "prices": [{"weight": "¼ kg", "price": 169}], "isBestSeller": True, "isNew": False, "tag": "Best Value"},
    {"id": 7, "name": "Nuvvulu Chikki", "category": "laddus-chikkis", "description": "Sesame chikki", "image": "https://images.pexels.com/photos/3026811/pexels-photo-3026811.jpeg?w=500", "prices": [{"weight": "¼ kg", "price": 169}, {"weight": "1kg", "price": 649}], "isBestSeller": False, "isNew": False, "tag": "Traditional"},
    {"id": 8, "name": "Kaju Chikki", "category": "laddus-chikkis", "description": "Premium cashew chikki", "image": "https://images.unsplash.com/photo-1662490880176-5d248d9b979a?w=500", "prices": [{"weight": "¼ kg", "price": 299}], "isBestSeller": False, "isNew": False, "tag": "Premium Quality"},
    
    # Sweets
    {"id": 9, "name": "Kobbari Laddu", "category": "sweets", "description": "Coconut laddu", "image": "https://images.unsplash.com/photo-1727018427695-35a6048c91e7?w=500", "prices": [{"weight": "½ kg", "price": 399}, {"weight": "1kg", "price": 699}], "isBestSeller": True, "isNew": False, "tag": "Festival Special"},
    {"id": 10, "name": "Ariselu", "category": "sweets", "description": "Traditional rice sweet", "image": "https://images.unsplash.com/photo-1727018792817-2dae98db2294?w=500", "prices": [{"weight": "½ kg", "price": 319}, {"weight": "1kg", "price": 639}], "isBestSeller": False, "isNew": False, "tag": "Traditional Sweet"},
    {"id": 11, "name": "Ravva Laddu", "category": "sweets", "description": "Semolina sweet balls", "image": "https://images.unsplash.com/photo-1697643448353-e95a9b8ab9c8?w=500", "prices": [{"weight": "½ kg", "price": 339}, {"weight": "1kg", "price": 669}], "isBestSeller": False, "isNew": False, "tag": "Classic"},
    {"id": 12, "name": "Boondi Laddu", "category": "sweets", "description": "Sweet boondi balls", "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500", "prices": [{"weight": "½ kg", "price": 359}, {"weight": "1kg", "price": 699}], "isBestSeller": True, "isNew": False, "tag": "Popular Choice"},
    {"id": 13, "name": "Kaju Katli", "category": "sweets", "description": "Premium cashew sweet", "image": "https://images.unsplash.com/photo-1610496427557-8dd676a7e2c2?w=500", "prices": [{"weight": "½ kg", "price": 599}, {"weight": "1kg", "price": 1199}], "isBestSeller": True, "isNew": False, "tag": "Premium"},
    {"id": 14, "name": "Gulab Jamun", "category": "sweets", "description": "Soft milk sweet", "image": "https://images.unsplash.com/photo-1697643509237-a2f9e55e3370?w=500", "prices": [{"weight": "1kg", "price": 499}], "isBestSeller": False, "isNew": False, "tag": "Soft & Sweet"},
    {"id": 15, "name": "Jangri", "category": "sweets", "description": "Traditional spiral sweet", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500", "prices": [{"weight": "½ kg", "price": 329}, {"weight": "1kg", "price": 649}], "isBestSeller": False, "isNew": False, "tag": "Festival Favorite"},
    {"id": 16, "name": "Badam Burfi", "category": "sweets", "description": "Almond fudge", "image": "https://images.unsplash.com/photo-1598175988905-94d3b3c24696?w=500", "prices": [{"weight": "½ kg", "price": 559}, {"weight": "1kg", "price": 1099}], "isBestSeller": False, "isNew": True, "tag": "Rich & Creamy"},
    {"id": 17, "name": "Mysore Pak", "category": "sweets", "description": "Ghee-rich sweet", "image": "https://images.unsplash.com/photo-1573919808537-fc9c196f5d41?w=500", "prices": [{"weight": "½ kg", "price": 399}, {"weight": "1kg", "price": 799}], "isBestSeller": False, "isNew": False, "tag": "South Special"},
    {"id": 18, "name": "Milk Peda", "category": "sweets", "description": "Soft milk sweet", "image": "https://images.unsplash.com/photo-1595777216528-071e0127ccbf?w=500", "prices": [{"weight": "½ kg", "price": 379}], "isBestSeller": False, "isNew": False, "tag": "Melt in Mouth"},
    
    # Hot Items
    {"id": 19, "name": "Samosa", "category": "hot-items", "description": "Crispy potato samosa", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500", "prices": [{"weight": "6 pcs", "price": 120}, {"weight": "12 pcs", "price": 220}], "isBestSeller": True, "isNew": False, "tag": "Crispy & Hot"},
    {"id": 20, "name": "Onion Pakoda", "category": "hot-items", "description": "Crispy onion fritters", "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500", "prices": [{"weight": "¼ kg", "price": 99}, {"weight": "½ kg", "price": 189}], "isBestSeller": False, "isNew": False, "tag": "Tea Time"},
    {"id": 21, "name": "Mirchi Bajji", "category": "hot-items", "description": "Spicy chili fritters", "image": "https://images.unsplash.com/photo-1626074353765-517a65aced42?w=500", "prices": [{"weight": "6 pcs", "price": 99}], "isBestSeller": False, "isNew": False, "tag": "Spicy"},
    {"id": 22, "name": "Punugulu", "category": "hot-items", "description": "Crispy savory balls", "image": "https://images.unsplash.com/photo-1630409346060-e3bf06df0b7a?w=500", "prices": [{"weight": "¼ kg", "price": 99}], "isBestSeller": False, "isNew": False, "tag": "Crispy Bites"},
    {"id": 23, "name": "Bonda", "category": "hot-items", "description": "Potato fritters", "image": "https://images.unsplash.com/photo-1601050690566-dd5427ba63e7?w=500", "prices": [{"weight": "6 pcs", "price": 110}], "isBestSeller": False, "isNew": False, "tag": "Savory"},
    {"id": 24, "name": "Dosa", "category": "hot-items", "description": "Crispy rice crepe", "image": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=500", "prices": [{"weight": "2 pcs", "price": 80}, {"weight": "4 pcs", "price": 150}], "isBestSeller": True, "isNew": False, "tag": "South Classic"},
    {"id": 25, "name": "Idli", "category": "hot-items", "description": "Steamed rice cakes", "image": "https://images.unsplash.com/photo-1630383249896-424e482df921?w=500", "prices": [{"weight": "4 pcs", "price": 60}, {"weight": "8 pcs", "price": 110}], "isBestSeller": False, "isNew": False, "tag": "Healthy"},
    {"id": 26, "name": "Vada", "category": "hot-items", "description": "Crispy lentil donuts", "image": "https://images.unsplash.com/photo-1626074353765-517a65aced42?w=500", "prices": [{"weight": "4 pcs", "price": 80}], "isBestSeller": False, "isNew": False, "tag": "Crispy"},
    
    # Snacks
    {"id": 27, "name": "Mixture", "category": "snacks", "description": "Spicy namkeen mix", "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=500", "prices": [{"weight": "¼ kg", "price": 119}, {"weight": "1kg", "price": 449}], "isBestSeller": True, "isNew": False, "tag": "Crunchy Mix"},
    {"id": 28, "name": "Chegodilu", "category": "snacks", "description": "Crunchy ring murukku", "image": "https://images.unsplash.com/photo-1601050689830-7180f6b1bdb6?w=500", "prices": [{"weight": "¼ kg", "price": 129}], "isBestSeller": False, "isNew": False, "tag": "Traditional"},
    {"id": 29, "name": "Karapusa", "category": "snacks", "description": "Spicy rice snack", "image": "https://images.unsplash.com/photo-1632207699891-e085c0a2c587?w=500", "prices": [{"weight": "¼ kg", "price": 109}], "isBestSeller": False, "isNew": False, "tag": "Crispy"},
    {"id": 30, "name": "Boondi", "category": "snacks", "description": "Crispy chickpea pearls", "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=500", "prices": [{"weight": "¼ kg", "price": 99}], "isBestSeller": False, "isNew": False, "tag": "Light Snack"},
    {"id": 31, "name": "Murukku", "category": "snacks", "description": "Spiral savory snack", "image": "https://images.unsplash.com/photo-1601050690830-7180f6b1bdb6?w=500", "prices": [{"weight": "¼ kg", "price": 129}, {"weight": "1kg", "price": 489}], "isBestSeller": True, "isNew": False, "tag": "Classic Snack"},
    {"id": 32, "name": "Janthikalu", "category": "snacks", "description": "Crunchy savory sticks", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500", "prices": [{"weight": "¼ kg", "price": 119}], "isBestSeller": False, "isNew": False, "tag": "Crunchy"},
    {"id": 33, "name": "Ribbon Pakodi", "category": "snacks", "description": "Ribbon-shaped snack", "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=500", "prices": [{"weight": "¼ kg", "price": 139}], "isBestSeller": False, "isNew": True, "tag": "Crispy Delight"},
    {"id": 34, "name": "Aloo Bhujia", "category": "snacks", "description": "Potato crispy sev", "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500", "prices": [{"weight": "¼ kg", "price": 109}], "isBestSeller": False, "isNew": False, "tag": "Spicy"},
    
    # Pickles
    {"id": 35, "name": "Mango Pickle", "category": "pickles", "description": "Tangy mango pickle", "image": "https://images.unsplash.com/photo-1628173930763-34c68a8e0b2e?w=500", "prices": [{"weight": "½ kg", "price": 199}, {"weight": "1kg", "price": 379}], "isBestSeller": True, "isNew": False, "tag": "Tangy & Spicy"},
    {"id": 36, "name": "Tomato Pickle", "category": "pickles", "description": "Spicy tomato pickle", "image": "https://images.unsplash.com/photo-1606491956391-ba70a43b2c9f?w=500", "prices": [{"weight": "½ kg", "price": 189}], "isBestSeller": False, "isNew": False, "tag": "Flavorful"},
    {"id": 37, "name": "Gongura Pickle", "category": "pickles", "description": "Tangy sorrel leaves", "image": "https://images.unsplash.com/photo-1628173930763-34c68a8e0b2e?w=500", "prices": [{"weight": "½ kg", "price": 229}, {"weight": "1kg", "price": 439}], "isBestSeller": True, "isNew": False, "tag": "Regional Favorite"},
    {"id": 38, "name": "Lemon Pickle", "category": "pickles", "description": "Zesty lemon pickle", "image": "https://images.unsplash.com/photo-1606491956391-ba70a43b2c9f?w=500", "prices": [{"weight": "½ kg", "price": 199}], "isBestSeller": False, "isNew": False, "tag": "Zesty"},
    {"id": 39, "name": "Mixed Veg Pickle", "category": "pickles", "description": "Assorted vegetables", "image": "https://images.unsplash.com/photo-1628173930763-34c68a8e0b2e?w=500", "prices": [{"weight": "½ kg", "price": 209}], "isBestSeller": False, "isNew": False, "tag": "Variety"},
    {"id": 40, "name": "Garlic Pickle", "category": "pickles", "description": "Spicy garlic pickle", "image": "https://images.unsplash.com/photo-1606491956391-ba70a43b2c9f?w=500", "prices": [{"weight": "½ kg", "price": 249}], "isBestSeller": False, "isNew": True, "tag": "Strong Flavor"},
    
    # Powders
    {"id": 41, "name": "Sambar Powder", "category": "powders", "description": "Traditional sambar spice", "image": "https://images.unsplash.com/photo-1596040033229-a0b3b1c1e79c?w=500", "prices": [{"weight": "100g", "price": 79}, {"weight": "250g", "price": 189}], "isBestSeller": True, "isNew": False, "tag": "Authentic"},
    {"id": 42, "name": "Rasam Powder", "category": "powders", "description": "Tangy rasam spice", "image": "https://images.unsplash.com/photo-1596040033229-a0b3b1c1e79c?w=500", "prices": [{"weight": "100g", "price": 79}], "isBestSeller": False, "isNew": False, "tag": "Traditional"},
    {"id": 43, "name": "Curry Powder", "category": "powders", "description": "Aromatic curry blend", "image": "https://images.unsplash.com/photo-1599909533604-b34e5157f4d1?w=500", "prices": [{"weight": "100g", "price": 89}, {"weight": "250g", "price": 209}], "isBestSeller": False, "isNew": False, "tag": "Flavorful"},
    {"id": 44, "name": "Idli Podi", "category": "powders", "description": "Spicy lentil powder", "image": "https://images.unsplash.com/photo-1596040033229-a0b3b1c1e79c?w=500", "prices": [{"weight": "100g", "price": 89}], "isBestSeller": True, "isNew": False, "tag": "Breakfast Companion"},
    {"id": 45, "name": "Pulusu Powder", "category": "powders", "description": "Tangy curry powder", "image": "https://images.unsplash.com/photo-1599909533604-b34e5157f4d1?w=500", "prices": [{"weight": "100g", "price": 79}], "isBestSeller": False, "isNew": False, "tag": "Tangy"},
    
    # Spices
    {"id": 46, "name": "Red Chilli Powder", "category": "spices", "description": "Hot red chilli", "image": "https://images.unsplash.com/photo-1582440522680-79bf4430a5f0?w=500", "prices": [{"weight": "100g", "price": 69}, {"weight": "250g", "price": 159}], "isBestSeller": True, "isNew": False, "tag": "Spicy"},
    {"id": 47, "name": "Turmeric Powder", "category": "spices", "description": "Pure turmeric", "image": "https://images.unsplash.com/photo-1615485290234-4aa49e3a530b?w=500", "prices": [{"weight": "100g", "price": 49}, {"weight": "250g", "price": 109}], "isBestSeller": False, "isNew": False, "tag": "Pure & Natural"},
    {"id": 48, "name": "Coriander Powder", "category": "spices", "description": "Fresh coriander", "image": "https://images.unsplash.com/photo-1596040033229-a0b3b1c1e79c?w=500", "prices": [{"weight": "100g", "price": 59}], "isBestSeller": False, "isNew": False, "tag": "Aromatic"},
    {"id": 49, "name": "Garam Masala", "category": "spices", "description": "Warming spice blend", "image": "https://images.unsplash.com/photo-1599909533604-b34e5157f4d1?w=500", "prices": [{"weight": "50g", "price": 89}], "isBestSeller": False, "isNew": False, "tag": "Aromatic Blend"},
    {"id": 50, "name": "Cumin Powder", "category": "spices", "description": "Ground cumin seeds", "image": "https://images.unsplash.com/photo-1596040033229-a0b3b1c1e79c?w=500", "prices": [{"weight": "100g", "price": 69}], "isBestSeller": False, "isNew": False, "tag": "Essential Spice"},
    
    # Other
    {"id": 51, "name": "Cashew Nuts", "category": "other", "description": "Premium cashews", "image": "https://images.unsplash.com/photo-1585515662115-33ec36ba0215?w=500", "prices": [{"weight": "250g", "price": 299}, {"weight": "500g", "price": 579}], "isBestSeller": True, "isNew": False, "tag": "Premium Quality"},
    {"id": 52, "name": "Almonds", "category": "other", "description": "Healthy almonds", "image": "https://images.unsplash.com/photo-1508258872933-31c7f764c1bc?w=500", "prices": [{"weight": "250g", "price": 349}], "isBestSeller": False, "isNew": False, "tag": "Nutritious"},
    {"id": 53, "name": "Raisins", "category": "other", "description": "Sweet dry grapes", "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9?w=500", "prices": [{"weight": "250g", "price": 199}], "isBestSeller": False, "isNew": False, "tag": "Sweet & Healthy"},
    {"id": 54, "name": "Dates", "category": "other", "description": "Natural sweetener", "image": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=500", "prices": [{"weight": "250g", "price": 179}], "isBestSeller": False, "isNew": False, "tag": "Energy Booster"},
    {"id": 55, "name": "Ghee", "category": "other", "description": "Pure cow ghee", "image": "https://images.unsplash.com/photo-1627662168682-fce1e47d91e0?w=500", "prices": [{"weight": "500ml", "price": 599}, {"weight": "1L", "price": 1149}], "isBestSeller": True, "isNew": False, "tag": "Pure & Fresh"},
    {"id": 56, "name": "Honey", "category": "other", "description": "Natural honey", "image": "https://images.unsplash.com/photo-1587049352846-4a222e784343?w=500", "prices": [{"weight": "500g", "price": 399}], "isBestSeller": False, "isNew": False, "tag": "Pure Honey"},
    {"id": 57, "name": "Jaggery", "category": "other", "description": "Organic jaggery", "image": "https://images.unsplash.com/photo-1620476807083-f5e08e8d6d00?w=500", "prices": [{"weight": "500g", "price": 99}, {"weight": "1kg", "price": 189}], "isBestSeller": False, "isNew": False, "tag": "Natural Sweetener"},
    {"id": 58, "name": "Rice Flour", "category": "other", "description": "Fresh rice flour", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500", "prices": [{"weight": "1kg", "price": 89}], "isBestSeller": False, "isNew": False, "tag": "Fresh Ground"},
]

def seed_products():
    """Seed mock products into MongoDB with proper UUID-format IDs"""
    print(f"🌱 Starting product seeding...")
    print(f"📦 Found {len(mock_products)} products to seed")
    
    # Clear existing products (optional - comment out to keep existing)
    # products_collection.delete_many({})
    # print("🗑️  Cleared existing products")
    
    success_count = 0
    error_count = 0
    
    for idx, mock_product in enumerate(mock_products, 1):
        try:
            # Generate proper UUID-format ID
            timestamp = int(datetime.now().timestamp() * 1000) + idx
            product_id = f"product_{timestamp}"
            
            # Convert mock product to database format
            db_product = {
                "id": product_id,
                "name": mock_product["name"],
                "category": mock_product["category"],
                "description": mock_product["description"],
                "image": mock_product["image"],
                "prices": mock_product["prices"],
                "isBestSeller": mock_product.get("isBestSeller", False),
                "isNew": mock_product.get("isNew", False),
                "tag": mock_product.get("tag", ""),
                "discount": 0,
                "inventory_count": 100,  # Default stock
                "out_of_stock": False,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Insert into database
            products_collection.insert_one(db_product)
            success_count += 1
            print(f"✅ [{success_count}/{len(mock_products)}] Added: {mock_product['name']}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error adding {mock_product['name']}: {e}")
    
    print(f"\n🎉 Seeding Complete!")
    print(f"✅ Successfully added: {success_count} products")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    
    # Verify count
    total_count = products_collection.count_documents({})
    print(f"📊 Total products in database: {total_count}")

if __name__ == "__main__":
    try:
        seed_products()
        print("\n✨ Database seeding successful!")
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        sys.exit(1)
