#!/usr/bin/env python3
"""
Seed script to add new products from user's list
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

# New products data based on user's list
new_products = [
    # ========== 🍬 Laddus & Chikkis ==========
    {
        "name": "Immunity Dry Fruits Laddu",
        "category": "laddus-chikkis",
        "description": "Boost your immunity with this nutritious blend of premium dry fruits and natural ingredients",
        "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 400},
            {"weight": "1 kg", "price": 1500}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Healthy Choice"
    },
    {
        "name": "Ragi Dry Fruits Laddu",
        "category": "laddus-chikkis",
        "description": "Healthy ragi combined with nutritious dry fruits for a wholesome treat",
        "image": "https://images.pexels.com/photos/8887148/pexels-photo-8887148.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 300},
            {"weight": "1 kg", "price": 1200}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Nutritious"
    },
    {
        "name": "Ground Nut Laddu",
        "category": "laddus-chikkis",
        "description": "Traditional groundnut laddu made with authentic recipes",
        "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 300},
            {"weight": "1 kg", "price": 1100}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Classic Taste"
    },
    {
        "name": "Oats Laddu",
        "category": "laddus-chikkis",
        "description": "Healthy oats laddu perfect for health-conscious food lovers",
        "image": "https://images.pexels.com/photos/12571183/pexels-photo-12571183.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 300}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "New Arrival"
    },
    {
        "name": "Dry Fruits Chikki",
        "category": "laddus-chikkis",
        "description": "Crunchy dry fruits chikki with premium ingredients",
        "image": "https://images.pexels.com/photos/29184393/pexels-photo-29184393.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 300}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Crispy Delight"
    },
    {
        "name": "Palli Chikki",
        "category": "laddus-chikkis",
        "description": "Traditional groundnut chikki with perfect sweetness",
        "image": "https://images.pexels.com/photos/29184389/pexels-photo-29184389.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 170}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Best Value"
    },
    {
        "name": "Nuvvulu Chikki",
        "category": "laddus-chikkis",
        "description": "Sesame seed chikki with authentic traditional taste",
        "image": "https://images.pexels.com/photos/33104648/pexels-photo-33104648.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 170},
            {"weight": "1 kg", "price": 650}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Traditional"
    },
    {
        "name": "Kaju Chikki",
        "category": "laddus-chikkis",
        "description": "Premium cashew chikki for special occasions",
        "image": "https://images.pexels.com/photos/8887148/pexels-photo-8887148.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 300}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Premium Quality"
    },
    
    # ========== 🍰 Sweets ==========
    {
        "name": "Kobbari Laddu",
        "category": "sweets",
        "description": "Delicious coconut laddu made with fresh coconut",
        "image": "https://images.unsplash.com/photo-1642744901889-9efbec703430?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxpbmRpYW4lMjBzd2VldHN8ZW58MHx8fG9yYW5nZXwxNzYyNjcyNjA5fDA&ixlib=rb-4.1.0&q=85",
        "prices": [
            {"weight": "½ kg", "price": 385},
            {"weight": "1 kg", "price": 680}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Festival Special"
    },
    {
        "name": "Ariselu",
        "category": "sweets",
        "description": "Traditional rice sweet for festivals and celebrations",
        "image": "https://images.pexels.com/photos/12571183/pexels-photo-12571183.jpeg",
        "prices": [
            {"weight": "½ kg", "price": 320},
            {"weight": "1 kg", "price": 640}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Traditional Sweet"
    },
    {
        "name": "Kobbari Burellu",
        "category": "sweets",
        "description": "Coconut-filled sweet delight perfect for festivals",
        "image": "https://images.pexels.com/photos/8887055/pexels-photo-8887055.jpeg",
        "prices": [
            {"weight": "½ kg", "price": 320},
            {"weight": "1 kg", "price": 640}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Traditional"
    },
    {
        "name": "Kajjikayalu",
        "category": "sweets",
        "description": "Crescent-shaped sweet with sweet filling inside",
        "image": "https://images.pexels.com/photos/29184393/pexels-photo-29184393.jpeg",
        "prices": [
            {"weight": "½ kg", "price": 400},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Festival Favorite"
    },
    {
        "name": "Pottu Minapa Sunnundalu",
        "category": "sweets",
        "description": "Traditional urad dal sweet balls with authentic taste",
        "image": "https://images.pexels.com/photos/8887148/pexels-photo-8887148.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 875}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Authentic"
    },
    {
        "name": "Nuvvulu (Sesame) Laddu",
        "category": "sweets",
        "description": "Healthy sesame seed laddu packed with nutrition",
        "image": "https://images.pexels.com/photos/29184389/pexels-photo-29184389.jpeg",
        "prices": [
            {"weight": "½ kg", "price": 400},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Nutritious"
    },
    {
        "name": "Bhoondi Chekka",
        "category": "sweets",
        "description": "Sweet boondi packed in traditional style",
        "image": "https://images.pexels.com/photos/8858693/pexels-photo-8858693.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 170},
            {"weight": "½ kg", "price": 330}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Sweet Treat"
    },
    {
        "name": "Chalimidi",
        "category": "sweets",
        "description": "Traditional sweet with unique taste and texture",
        "image": "https://images.pexels.com/photos/1343537/pexels-photo-1343537.jpeg",
        "prices": [
            {"weight": "½ kg", "price": 300},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Unique Taste"
    },
    {
        "name": "Sweet Gavvalu",
        "category": "sweets",
        "description": "Shell-shaped sweet snack perfect for festivals",
        "image": "https://images.pexels.com/photos/5947065/pexels-photo-5947065.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 160},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Crispy Sweet"
    },
    {
        "name": "Flax Seeds Laddu",
        "category": "sweets",
        "description": "Healthy flax seeds laddu with omega-3 benefits",
        "image": "https://images.pexels.com/photos/23614250/pexels-photo-23614250.jpeg",
        "prices": [
            {"weight": "½ kg", "price": 400},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Healthy Choice"
    },
    
    # ========== 🍘 Hot Items ==========
    {
        "name": "Atukullu Mixture",
        "category": "hot-items",
        "description": "Crispy poha mixture with perfect spice blend",
        "image": "https://images.pexels.com/photos/9832685/pexels-photo-9832685.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Crispy Snack"
    },
    {
        "name": "Hot Gavvalu",
        "category": "hot-items",
        "description": "Shell-shaped spicy snack with authentic masala",
        "image": "https://images.pexels.com/photos/33104648/pexels-photo-33104648.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Spicy Delight"
    },
    {
        "name": "Hot Kajalu",
        "category": "hot-items",
        "description": "Crunchy spicy kajalu perfect for tea time",
        "image": "https://images.pexels.com/photos/5947065/pexels-photo-5947065.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Tea Time"
    },
    {
        "name": "Karapusa",
        "category": "hot-items",
        "description": "Traditional spicy puffed snack with authentic flavor",
        "image": "https://images.pexels.com/photos/9832685/pexels-photo-9832685.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Traditional"
    },
    {
        "name": "Palli Pakodi",
        "category": "hot-items",
        "description": "Crispy groundnut pakoda with perfect crunch",
        "image": "https://images.pexels.com/photos/33104648/pexels-photo-33104648.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 160},
            {"weight": "1 kg", "price": 640}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Crunchy"
    },
    {
        "name": "Ragi Chakralu",
        "category": "hot-items",
        "description": "Healthy ragi-based crispy wheels with spicy coating",
        "image": "https://images.pexels.com/photos/5947065/pexels-photo-5947065.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Healthy Snack"
    },
    {
        "name": "Ragi Kara Bundhi",
        "category": "hot-items",
        "description": "Spicy ragi boondi perfect for health-conscious snackers",
        "image": "https://images.pexels.com/photos/9832685/pexels-photo-9832685.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 175},
            {"weight": "1 kg", "price": 700}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Healthy & Spicy"
    },
    {
        "name": "Ragi Ribbon Pakodi",
        "category": "hot-items",
        "description": "Healthy ragi ribbon pakodi with authentic spices",
        "image": "https://images.pexels.com/photos/33104648/pexels-photo-33104648.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Premium Healthy"
    },
    {
        "name": "Ribbon Pakodi",
        "category": "hot-items",
        "description": "Classic ribbon pakodi with perfect texture and spice",
        "image": "https://images.pexels.com/photos/5947065/pexels-photo-5947065.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Classic Favorite"
    },
    {
        "name": "Kaju Masala",
        "category": "hot-items",
        "description": "Premium cashews coated with special masala blend",
        "image": "https://images.pexels.com/photos/23614250/pexels-photo-23614250.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 350},
            {"weight": "1 kg", "price": 1400}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Premium"
    },
    
    # ========== 🍪 Snacks ==========
    {
        "name": "Bhondi",
        "category": "snacks",
        "description": "Crispy boondi snack perfect for munching anytime",
        "image": "https://images.pexels.com/photos/9832685/pexels-photo-9832685.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Crispy Snack"
    },
    {
        "name": "Masala Chekkalu / Pappu Chekkalu",
        "category": "snacks",
        "description": "Traditional rice crackers with masala coating",
        "image": "https://images.pexels.com/photos/33104648/pexels-photo-33104648.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Traditional Snack"
    },
    {
        "name": "Ragi Masala Chekkalu",
        "category": "snacks",
        "description": "Healthy ragi crackers with authentic masala flavor",
        "image": "https://images.pexels.com/photos/5947065/pexels-photo-5947065.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "½ kg", "price": 500}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Healthy Cracker"
    },
    
    # ========== 🥒 Veg Pickles ==========
    {
        "name": "Tomato Pickle",
        "category": "pickles",
        "description": "Tangy tomato pickle made with authentic spices",
        "image": "https://images.pexels.com/photos/30174012/pexels-photo-30174012.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Tangy & Spicy"
    },
    {
        "name": "Allam Pickle",
        "category": "pickles",
        "description": "Fresh ginger pickle with perfect heat and tang",
        "image": "https://images.pexels.com/photos/28915087/pexels-photo-28915087.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Spicy Ginger"
    },
    {
        "name": "Mango Pickle",
        "category": "pickles",
        "description": "Traditional mango pickle with authentic taste",
        "image": "https://images.pexels.com/photos/4023132/pexels-photo-4023132.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Classic Favorite"
    },
    {
        "name": "Pandu Mirchi",
        "category": "pickles",
        "description": "Spicy green chili pickle with authentic flavor",
        "image": "https://images.pexels.com/photos/30174012/pexels-photo-30174012.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Extra Hot"
    },
    {
        "name": "Gongura Pickle",
        "category": "pickles",
        "description": "Traditional Andhra gongura pickle with authentic taste",
        "image": "https://images.pexels.com/photos/28915087/pexels-photo-28915087.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Andhra Special"
    },
    {
        "name": "Pandu Mirchi Gongura",
        "category": "pickles",
        "description": "Spicy blend of green chili and gongura pickle",
        "image": "https://images.pexels.com/photos/30174012/pexels-photo-30174012.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Fusion Pickle"
    },
    {
        "name": "Lemon Pickle",
        "category": "pickles",
        "description": "Tangy lemon pickle made with fresh ingredients",
        "image": "https://images.pexels.com/photos/28915087/pexels-photo-28915087.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Tangy Delight"
    },
    {
        "name": "Amla Pickle",
        "category": "pickles",
        "description": "Healthy amla pickle rich in vitamin C",
        "image": "https://images.pexels.com/photos/14627741/pexels-photo-14627741.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Healthy Choice"
    },
    {
        "name": "Amla Tokku",
        "category": "pickles",
        "description": "Thick amla chutney style pickle with unique taste",
        "image": "https://images.pexels.com/photos/14627741/pexels-photo-14627741.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Chutney Style"
    },
    
    # ========== 🌶️ Powders ==========
    {
        "name": "Kandi Podi",
        "category": "powders",
        "description": "Traditional dal powder perfect for rice and dosa",
        "image": "https://images.unsplash.com/photo-1608554208766-8198d5536b46",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Traditional"
    },
    {
        "name": "Kakarakaya Karam",
        "category": "powders",
        "description": "Bitter gourd spice powder with health benefits",
        "image": "https://images.pexels.com/photos/6808985/pexels-photo-6808985.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Healthy Spice"
    },
    {
        "name": "Kobbari Karam",
        "category": "powders",
        "description": "Coconut-based spice powder with authentic flavor",
        "image": "https://images.unsplash.com/photo-1611960555774-35f9d21c7e25",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Coconut Flavor"
    },
    {
        "name": "Flax Seeds Powder",
        "category": "powders",
        "description": "Healthy flax seeds powder rich in omega-3",
        "image": "https://images.pexels.com/photos/7038148/pexels-photo-7038148.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Superfood"
    },
    {
        "name": "Munagaku Karam Podi",
        "category": "powders",
        "description": "Drumstick leaves powder packed with nutrition",
        "image": "https://images.pexels.com/photos/6808985/pexels-photo-6808985.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Nutrient Rich"
    },
    {
        "name": "Nalla Karam Podi",
        "category": "powders",
        "description": "Aromatic sesame spice powder for rice",
        "image": "https://images.unsplash.com/photo-1608554208766-8198d5536b46",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Aromatic"
    },
    {
        "name": "Pudina Podi",
        "category": "powders",
        "description": "Refreshing mint powder perfect for rice and curries",
        "image": "https://images.pexels.com/photos/7038184/pexels-photo-7038184.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Refreshing"
    },
    {
        "name": "Dhaniyala Podi",
        "category": "powders",
        "description": "Fresh coriander powder with authentic aroma",
        "image": "https://images.unsplash.com/photo-1611960555774-35f9d21c7e25",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Aromatic"
    },
    {
        "name": "Karuvepaku Podi (Curry Leaves)",
        "category": "powders",
        "description": "Curry leaves powder with health benefits and aroma",
        "image": "https://images.pexels.com/photos/6808985/pexels-photo-6808985.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Healthy"
    },
    {
        "name": "Nuvvula Podi",
        "category": "powders",
        "description": "Nutritious sesame seed powder for daily use",
        "image": "https://images.pexels.com/photos/7038148/pexels-photo-7038148.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Nutritious"
    },
    {
        "name": "Idly Karam Podi",
        "category": "powders",
        "description": "Classic idly powder with perfect spice blend",
        "image": "https://images.unsplash.com/photo-1608554208766-8198d5536b46",
        "prices": [
            {"weight": "¼ kg", "price": 250},
            {"weight": "1 kg", "price": 1000}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Breakfast Essential"
    },
    {
        "name": "Sprouted Ragi Powder",
        "category": "powders",
        "description": "Healthy sprouted ragi powder for health-conscious",
        "image": "https://images.pexels.com/photos/7038184/pexels-photo-7038184.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 600}
        ],
        "isBestSeller": False,
        "isNew": True,
        "tag": "Health Powder"
    },
    
    # ========== 🌶️ Spices ==========
    {
        "name": "Sambar Powder",
        "category": "spices",
        "description": "Authentic sambar powder with perfect blend of spices",
        "image": "https://images.unsplash.com/photo-1523112784166-c04db3a3bb7c",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Essential Spice"
    },
    {
        "name": "Special Rasam Powder",
        "category": "spices",
        "description": "Special rasam powder for authentic South Indian taste",
        "image": "https://images.pexels.com/photos/6808985/pexels-photo-6808985.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 200},
            {"weight": "1 kg", "price": 800}
        ],
        "isBestSeller": True,
        "isNew": False,
        "tag": "Rasam Essential"
    },
    {
        "name": "Dhaniya Powder",
        "category": "spices",
        "description": "Fresh coriander powder for daily cooking",
        "image": "https://images.unsplash.com/photo-1611960555774-35f9d21c7e25",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 500}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Daily Essential"
    },
    {
        "name": "Pulusu Podi",
        "category": "spices",
        "description": "Tangy curry powder for traditional Andhra dishes",
        "image": "https://images.pexels.com/photos/7038148/pexels-photo-7038148.jpeg",
        "prices": [
            {"weight": "¼ kg", "price": 150},
            {"weight": "1 kg", "price": 500}
        ],
        "isBestSeller": False,
        "isNew": False,
        "tag": "Andhra Special"
    }
]

def seed_new_products():
    """Seed new products into MongoDB with proper UUID-format IDs"""
    print(f"🌱 Starting product seeding...")
    print(f"📦 Found {len(new_products)} new products to seed")
    
    success_count = 0
    error_count = 0
    
    # Get the count of existing products to display
    existing_count = products_collection.count_documents({})
    print(f"📊 Current products in database: {existing_count}")
    
    for idx, product_data in enumerate(new_products, 1):
        try:
            # Generate proper UUID-format ID
            timestamp = int(datetime.now().timestamp() * 1000) + idx
            product_id = f"product_{timestamp}"
            
            # Convert to database format
            db_product = {
                "id": product_id,
                "name": product_data["name"],
                "category": product_data["category"],
                "description": product_data["description"],
                "image": product_data["image"],
                "prices": product_data["prices"],
                "isBestSeller": product_data.get("isBestSeller", False),
                "isNew": product_data.get("isNew", False),
                "tag": product_data.get("tag", ""),
                "discount_percentage": None,
                "discount_expiry_date": None,
                "inventory_count": 100,  # Default stock
                "out_of_stock": False,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Insert into database
            products_collection.insert_one(db_product)
            success_count += 1
            print(f"✅ [{success_count}/{len(new_products)}] Added: {product_data['name']} (ID: {product_id})")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error adding {product_data['name']}: {str(e)}")
    
    # Show final statistics
    print(f"\n{'='*60}")
    print(f"✅ Successfully added: {success_count} products")
    if error_count > 0:
        print(f"❌ Failed to add: {error_count} products")
    
    total = products_collection.count_documents({})
    print(f"📊 Total products in database now: {total}")
    print(f"{'='*60}")
    
    # Show category breakdown
    print(f"\n📋 Category Breakdown:")
    categories = products_collection.distinct("category")
    for category in sorted(categories):
        count = products_collection.count_documents({"category": category})
        print(f"   {category}: {count} products")

if __name__ == "__main__":
    try:
        seed_new_products()
        print("\n🎉 Product seeding completed successfully!")
        client.close()
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        sys.exit(1)
