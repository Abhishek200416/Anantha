#!/usr/bin/env python3
"""
Seed all products synchronously into MongoDB database
"""
import os
from pymongo import MongoClient
from datetime import datetime

def seed_all_products():
    """Seed database with all 56 products"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_url)
    db = client['food_delivery']
    products_collection = db.products
    
    print("=" * 60)
    print("SEEDING ALL PRODUCTS TO DATABASE")
    print("=" * 60)
    
    # Clear existing products
    delete_result = products_collection.delete_many({})
    print(f"\n✓ Cleared {delete_result.deleted_count} existing products")
    
    timestamp = int(datetime.now().timestamp())
    
    products = [
        # LADDUS & CHIKKIS (8 products)
        {
            "id": f"product_{timestamp + 1}",
            "name": "Immunity Dry Fruits Laddu",
            "category": "laddus-chikkis",
            "description": "Nutritious laddus packed with dry fruits like almonds, cashews, dates, and figs. Boosts immunity and energy naturally.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 150},
                {"weight": "½ kg", "price": 280},
                {"weight": "1 kg", "price": 550}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 2}",
            "name": "Ragi Laddu",
            "category": "laddus-chikkis",
            "description": "Healthy ragi (finger millet) laddus with jaggery and ghee. Rich in calcium and iron, perfect for growing kids.",
            "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087",
            "prices": [
                {"weight": "¼ kg", "price": 130},
                {"weight": "½ kg", "price": 250},
                {"weight": "1 kg", "price": 480}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 3}",
            "name": "Groundnut Laddu",
            "category": "laddus-chikkis",
            "description": "Crunchy groundnut laddus made with roasted peanuts and jaggery. High in protein and absolutely delicious.",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 4}",
            "name": "Sesame Laddu (Nuvvula Undalu)",
            "category": "laddus-chikkis",
            "description": "Traditional sesame seed laddus with jaggery. Rich in antioxidants and keeps you warm in winter.",
            "image": "https://images.unsplash.com/photo-1606312619070-d48b4cff2c0b",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 400}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 5}",
            "name": "Dates Laddu (Kharjura Undalu)",
            "category": "laddus-chikkis",
            "description": "Sugar-free laddus made with dates and dry fruits. Natural sweetness and extremely healthy.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 140},
                {"weight": "½ kg", "price": 270},
                {"weight": "1 kg", "price": 520}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 6}",
            "name": "Rava Laddu",
            "category": "laddus-chikkis",
            "description": "Soft and melt-in-mouth rava laddus with cashews and raisins. A traditional favorite for all occasions.",
            "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
            "prices": [
                {"weight": "¼ kg", "price": 120},
                {"weight": "½ kg", "price": 230},
                {"weight": "1 kg", "price": 440}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 7}",
            "name": "Peanut Chikki",
            "category": "laddus-chikkis",
            "description": "Crispy peanut chikki with jaggery. Traditional winter sweet that's crunchy and wholesome.",
            "image": "https://images.pexels.com/photos/7937472/pexels-photo-7937472.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 8}",
            "name": "Mixed Dry Fruits Chikki",
            "category": "laddus-chikkis",
            "description": "Premium chikki loaded with almonds, cashews, pistachios, and dates. Healthy snacking redefined.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 160},
                {"weight": "½ kg", "price": 310},
                {"weight": "1 kg", "price": 600}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        
        # SWEETS (10 products)
        {
            "id": f"product_{timestamp + 9}",
            "name": "Ariselu",
            "category": "sweets",
            "description": "Traditional Telugu festival sweet made with rice flour and jaggery. Soft, aromatic, and absolutely divine.",
            "image": "https://images.unsplash.com/photo-1606312619070-d48b4cff2c0b",
            "prices": [
                {"weight": "¼ kg", "price": 140},
                {"weight": "½ kg", "price": 270},
                {"weight": "1 kg", "price": 520}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 10}",
            "name": "Kobbari Burellu (Coconut Burfi)",
            "category": "sweets",
            "description": "Premium coconut burfi with fresh coconut and sugar. Soft texture with rich coconut flavor.",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 130},
                {"weight": "½ kg", "price": 250},
                {"weight": "1 kg", "price": 480}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 11}",
            "name": "Kajjikayalu",
            "category": "sweets",
            "description": "Crescent-shaped sweet dumplings filled with coconut and jaggery. A Sankranti special delicacy.",
            "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
            "prices": [
                {"weight": "¼ kg", "price": 150},
                {"weight": "½ kg", "price": 290},
                {"weight": "1 kg", "price": 560}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Festival Special",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 12}",
            "name": "Sunnundalu (Urad Dal Laddu)",
            "category": "sweets",
            "description": "Protein-rich laddus made with roasted urad dal and ghee. Melts in mouth with aromatic flavor.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 140},
                {"weight": "½ kg", "price": 270},
                {"weight": "1 kg", "price": 520}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 13}",
            "name": "Pootharekulu",
            "category": "sweets",
            "description": "Paper-thin rice wafers layered with pure ghee and sugar. The famous Atreyapuram delicacy.",
            "image": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62",
            "prices": [
                {"weight": "¼ kg", "price": 180},
                {"weight": "½ kg", "price": 350},
                {"weight": "1 kg", "price": 680}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 14}",
            "name": "Kaja",
            "category": "sweets",
            "description": "Crispy layered sweet made with refined flour and sugar syrup. A Kakinada specialty.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 160},
                {"weight": "½ kg", "price": 310},
                {"weight": "1 kg", "price": 600}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 15}",
            "name": "Mysore Pak",
            "category": "sweets",
            "description": "Rich and buttery sweet made with gram flour, ghee, and sugar. Soft, melt-in-mouth texture.",
            "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087",
            "prices": [
                {"weight": "¼ kg", "price": 170},
                {"weight": "½ kg", "price": 330},
                {"weight": "1 kg", "price": 640}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 16}",
            "name": "Kova (Khoya) Mithai",
            "category": "sweets",
            "description": "Premium milk-based sweet with rich, creamy texture. Traditional favorite for celebrations.",
            "image": "https://images.pexels.com/photos/7937472/pexels-photo-7937472.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 190},
                {"weight": "½ kg", "price": 370},
                {"weight": "1 kg", "price": 720}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 17}",
            "name": "Boorelu (Sweet Bonda)",
            "category": "sweets",
            "description": "Fried sweet balls filled with Bengal gram and jaggery. Crispy outside, soft and sweet inside.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 140},
                {"weight": "½ kg", "price": 270},
                {"weight": "1 kg", "price": 520}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 18}",
            "name": "Badam Halwa",
            "category": "sweets",
            "description": "Luxurious almond halwa made with pure ghee. Rich, smooth, and absolutely indulgent.",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 220},
                {"weight": "½ kg", "price": 430},
                {"weight": "1 kg", "price": 840}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        
        # HOT ITEMS (10 products)
        {
            "id": f"product_{timestamp + 19}",
            "name": "Atukullu Mixture",
            "category": "hot-items",
            "description": "Spicy and crunchy mixture with rice flakes, peanuts, curry leaves, and spices. Perfect tea-time snack.",
            "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 20}",
            "name": "Hot Gavvalu (Sev)",
            "category": "hot-items",
            "description": "Crispy shell-shaped savory snack made with gram flour. Spicy and addictive.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 21}",
            "name": "Ribbon Pakodi",
            "category": "hot-items",
            "description": "Crispy ribbon-shaped snack with perfect spice blend. Great for snacking anytime.",
            "image": "https://images.unsplash.com/photo-1606312619070-d48b4cff2c0b",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 22}",
            "name": "Murukku",
            "category": "hot-items",
            "description": "Traditional spiral-shaped crispy snack made with rice and urad dal flour. Classic South Indian favorite.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 23}",
            "name": "Chegodilu (Ring Murukku)",
            "category": "hot-items",
            "description": "Ring-shaped spicy snack made with rice flour and cumin. Sankranti special savory.",
            "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Festival Special",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 24}",
            "name": "Karam Dosa",
            "category": "hot-items",
            "description": "Thin crispy wafers with spicy chili powder coating. Extremely hot and crunchy.",
            "image": "https://images.pexels.com/photos/7937472/pexels-photo-7937472.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 25}",
            "name": "Boondi (Spicy)",
            "category": "hot-items",
            "description": "Tiny crispy balls made from gram flour with spicy masala. Perfect accompaniment with meals.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 26}",
            "name": "Nippattu (Rice Crackers)",
            "category": "hot-items",
            "description": "Crispy rice crackers with sesame and peanuts. Traditional Karnataka-style snack.",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 27}",
            "name": "Garlic Murukku",
            "category": "hot-items",
            "description": "Spicy murukku with garlic flavor. Extra crispy and aromatic, perfect with tea.",
            "image": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 400}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 28}",
            "name": "Cornflakes Mixture",
            "category": "hot-items",
            "description": "Crunchy mixture with cornflakes, peanuts, and cashews. Modern twist to traditional mixture.",
            "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        
        # SNACKS (3 products)
        {
            "id": f"product_{timestamp + 29}",
            "name": "Masala Chekkalu",
            "category": "snacks",
            "description": "Crispy rice crackers with spicy masala coating. Thin, light, and perfectly seasoned.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 30}",
            "name": "Kaju Masala (Spiced Cashews)",
            "category": "snacks",
            "description": "Premium cashews roasted with aromatic spices. Healthy and delicious snacking option.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 180},
                {"weight": "½ kg", "price": 350},
                {"weight": "1 kg", "price": 680}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 31}",
            "name": "Karapusa Janthikalu (Hot Sticks)",
            "category": "snacks",
            "description": "Extra spicy stick-shaped snack made with gram flour. Thin, crispy, and fiery hot.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        
        # PICKLES (9 products)
        {
            "id": f"product_{timestamp + 32}",
            "name": "Mango Pickle (Avakaya)",
            "category": "pickles",
            "description": "Traditional Andhra-style mango pickle with mustard and red chili. Spicy, tangy, and finger-licking good.",
            "image": "https://images.unsplash.com/photo-1606312619070-d48b4cff2c0b",
            "prices": [
                {"weight": "¼ kg", "price": 70},
                {"weight": "½ kg", "price": 130},
                {"weight": "1 kg", "price": 250}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 33}",
            "name": "Gongura Pickle",
            "category": "pickles",
            "description": "Iconic Andhra pickle made with sorrel leaves. Tangy, spicy, and absolutely authentic.",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 34}",
            "name": "Tomato Pickle",
            "category": "pickles",
            "description": "Tangy tomato pickle with garlic and spices. Perfect accompaniment with rice and chapati.",
            "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
            "prices": [
                {"weight": "¼ kg", "price": 65},
                {"weight": "½ kg", "price": 120},
                {"weight": "1 kg", "price": 230}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 35}",
            "name": "Allam (Ginger) Pickle",
            "category": "pickles",
            "description": "Spicy ginger pickle that aids digestion. Hot, tangy, and therapeutic.",
            "image": "https://images.pexels.com/photos/7937472/pexels-photo-7937472.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 75},
                {"weight": "½ kg", "price": 140},
                {"weight": "1 kg", "price": 270}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 36}",
            "name": "Lemon Pickle (Nimmakaaya)",
            "category": "pickles",
            "description": "Tangy lemon pickle with fenugreek and mustard. Classic taste that never gets old.",
            "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087",
            "prices": [
                {"weight": "¼ kg", "price": 70},
                {"weight": "½ kg", "price": 130},
                {"weight": "1 kg", "price": 250}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 37}",
            "name": "Amla (Gooseberry) Pickle",
            "category": "pickles",
            "description": "Healthy amla pickle rich in Vitamin C. Tangy, slightly sweet, and immunity-boosting.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 38}",
            "name": "Mixed Veg Pickle",
            "category": "pickles",
            "description": "Assorted vegetables in spicy oil. Carrot, cauliflower, green chili, and more in one jar.",
            "image": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62",
            "prices": [
                {"weight": "¼ kg", "price": 75},
                {"weight": "½ kg", "price": 140},
                {"weight": "1 kg", "price": 270}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 39}",
            "name": "Garlic Pickle (Vellulli)",
            "category": "pickles",
            "description": "Spicy garlic pickle with red chili. Strong flavor that enhances any meal.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 40}",
            "name": "Red Chili Pickle (Mirchi)",
            "category": "pickles",
            "description": "Extra hot red chili pickle for spice lovers. Extremely fiery and addictive.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 70},
                {"weight": "½ kg", "price": 130},
                {"weight": "1 kg", "price": 250}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        
        # POWDERS (12 products)
        {
            "id": f"product_{timestamp + 41}",
            "name": "Kandi Podi (Dal Powder)",
            "category": "powders",
            "description": "Roasted toor dal powder with spices. Mix with ghee and eat with hot rice - heaven!",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 42}",
            "name": "Idly Karam (Idli Powder)",
            "category": "powders",
            "description": "Spicy powder for idli and dosa. Made with lentils, dry red chilies, and curry leaves.",
            "image": "https://images.unsplash.com/photo-1606312619070-d48b4cff2c0b",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 43}",
            "name": "Pudina Podi (Mint Powder)",
            "category": "powders",
            "description": "Refreshing mint powder with roasted gram. Aromatic and cooling effect.",
            "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 44}",
            "name": "Curry Leaves Powder (Karivepaku)",
            "category": "powders",
            "description": "Aromatic curry leaves powder with lentils. Healthy and flavorful addition to meals.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 45}",
            "name": "Nalla Karam (Sesame Powder)",
            "category": "powders",
            "description": "Roasted sesame powder with red chilies. Rich, nutty flavor perfect with hot rice.",
            "image": "https://images.pexels.com/photos/7937472/pexels-photo-7937472.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 400}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 46}",
            "name": "Flax Seeds Powder (Avise Ginjalu)",
            "category": "powders",
            "description": "Roasted flax seeds powder. Rich in Omega-3, fiber, and extremely healthy.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 120},
                {"weight": "½ kg", "price": 230},
                {"weight": "1 kg", "price": 440}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 47}",
            "name": "Peanut Powder (Verusanaga)",
            "category": "powders",
            "description": "Roasted peanut powder with spices. High protein content and delicious taste.",
            "image": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 48}",
            "name": "Coconut Powder (Kobbari)",
            "category": "powders",
            "description": "Roasted coconut powder with red chilies. Sweet and spicy combination.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 105},
                {"weight": "½ kg", "price": 200},
                {"weight": "1 kg", "price": 380}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 49}",
            "name": "Garlic Powder (Vellulli)",
            "category": "powders",
            "description": "Spicy garlic powder mix. Aromatic and flavorful, great health benefits.",
            "image": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 50}",
            "name": "Gongura Powder",
            "category": "powders",
            "description": "Dried sorrel leaves powder. Tangy flavor that's quintessentially Andhra.",
            "image": "https://images.pexels.com/photos/4686819/pexels-photo-4686819.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 400}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 51}",
            "name": "Dondakaya Powder (Tindora)",
            "category": "powders",
            "description": "Dried ivy gourd powder with spices. Unique taste and medicinal properties.",
            "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
            "prices": [
                {"weight": "¼ kg", "price": 105},
                {"weight": "½ kg", "price": 200},
                {"weight": "1 kg", "price": 380}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 52}",
            "name": "Tomato Powder (Tamata)",
            "category": "powders",
            "description": "Dried tomato powder with spices. Tangy and versatile for various dishes.",
            "image": "https://images.pexels.com/photos/5949888/pexels-photo-5949888.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        
        # SPICES (4 products)
        {
            "id": f"product_{timestamp + 53}",
            "name": "Sambar Powder",
            "category": "spices",
            "description": "Authentic South Indian sambar powder. Perfect blend of spices for aromatic sambar.",
            "image": "https://images.pexels.com/photos/7937472/pexels-photo-7937472.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 54}",
            "name": "Rasam Powder",
            "category": "spices",
            "description": "Traditional rasam powder with tamarind tang. Essential for authentic South Indian rasam.",
            "image": "https://images.unsplash.com/photo-1608797178974-15b35a64ede9",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 55}",
            "name": "Dhaniya Powder (Coriander)",
            "category": "spices",
            "description": "Pure coriander powder. Freshly ground with authentic aroma and flavor.",
            "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 60},
                {"weight": "½ kg", "price": 110},
                {"weight": "1 kg", "price": 210}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        },
        {
            "id": f"product_{timestamp + 56}",
            "name": "Pulusu Podi (Tamarind Curry Powder)",
            "category": "spices",
            "description": "Tangy tamarind-based curry powder. Perfect for quick and tasty vegetable curries.",
            "image": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "",
            "inventory_count": 100,
            "out_of_stock": False,
            "discount_percentage": None,
            "discount_expiry_date": None
        }
    ]
    
    # Insert all products
    products_collection.insert_many(products)
    print(f"\n✅ Successfully added {len(products)} products to database")
    
    # Get category breakdown
    categories = products_collection.distinct('category')
    print(f"\n📊 Product Summary:")
    for cat in sorted(categories):
        count = products_collection.count_documents({'category': cat})
        print(f"   {cat}: {count} products")
    
    # Show sample products
    print(f"\n🍱 Sample Products:")
    sample_products = list(products_collection.find({}, {'name': 1, 'category': 1, 'prices': 1, '_id': 0}).limit(10))
    for p in sample_products:
        prices_str = ', '.join([f"₹{price['price']}" for price in p.get('prices', [])])
        print(f"   • {p['name']} ({p['category']}) - {prices_str}")
    
    print("\n" + "=" * 60)
    print("✅ PRODUCTS SEEDING COMPLETE!")
    print("=" * 60)
    print("\nAll products are now available in:")
    print("  1. Home page - Product catalog")
    print("  2. Admin panel - Products tab")
    print("  3. Checkout page - Product selection")
    print("\n" + "=" * 60)
    
    client.close()

if __name__ == "__main__":
    try:
        seed_all_products()
    except Exception as e:
        print(f"\n❌ Error seeding products: {str(e)}")
        import traceback
        traceback.print_exc()
