import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client['anantha_lakshmi_db']

async def seed_products():
    """Seed database with all 56 products with proper images"""
    
    # Clear existing products
    await db.products.delete_many({})
    print("🗑️ Cleared existing products")
    
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
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 2}",
            "name": "Kobbari Laddu",
            "category": "laddus-chikkis",
            "description": "Traditional coconut laddus made with fresh coconut, jaggery, and cardamom. Soft and aromatic sweet delicacy.",
            "image": "https://images.unsplash.com/photo-1727018792817-2dae98db2294",
            "prices": [
                {"weight": "¼ kg", "price": 120},
                {"weight": "½ kg", "price": 230},
                {"weight": "1 kg", "price": 450}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 3}",
            "name": "Rava Laddu",
            "category": "laddus-chikkis",
            "description": "Semolina laddus roasted in ghee with cashews and raisins. Light and delicious traditional sweet.",
            "image": "https://images.pexels.com/photos/8887063/pexels-photo-8887063.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 4}",
            "name": "Boondi Laddu",
            "category": "laddus-chikkis",
            "description": "Golden yellow laddus made from tiny gram flour pearls. Classic festive sweet with perfect sweetness.",
            "image": "https://images.unsplash.com/photo-1635952346904-95f2ccfcd029",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 410}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 5}",
            "name": "Ariselu",
            "category": "laddus-chikkis",
            "description": "Traditional Telugu sweet made with rice flour, jaggery, and sesame seeds. Prepared during festivals.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/049/082/160/small/traditional-indian-sweets-laddu-and-pedha-ready-to-be-gifted-or-enjoyed-during-celebrations-like-diwali-and-raksha-bandhan-free-photo.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 130},
                {"weight": "½ kg", "price": 250},
                {"weight": "1 kg", "price": 490}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Traditional",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 6}",
            "name": "Peanut Chikki",
            "category": "laddus-chikkis",
            "description": "Crunchy groundnut brittle made with roasted peanuts and jaggery. Perfect healthy snack.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/053/781/239/small/orange-laddu-texture-closeup-side-view-of-indian-pakistani-and-bangladeshi-sweet-dessert-food-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Crunchy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 7}",
            "name": "Sesame Chikki",
            "category": "laddus-chikkis",
            "description": "Til chikki made with sesame seeds and jaggery. Rich in calcium and iron. Winter special.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/071/940/050/small/a-close-up-of-ladoo-indian-sweets-texture-of-ladoo-with-pieces-of-nuts-and-sesame-seeds-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Nutritious",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 8}",
            "name": "Coconut Burfi",
            "category": "laddus-chikkis",
            "description": "Square-shaped coconut fudge made with fresh coconut and condensed milk. Soft and creamy texture.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/007/133/657/small/coconut-burfi-squares-indian-sweet-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 125},
                {"weight": "½ kg", "price": 240},
                {"weight": "1 kg", "price": 470}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False
        },
        
        # SWEETS (10 products)
        {
            "id": f"product_{timestamp + 9}",
            "name": "Pootharekulu",
            "category": "sweets",
            "description": "Authentic Athreyapuram paper-thin sweet with layers of ghee and sugar. Traditional Andhra delicacy.",
            "image": "https://images.pexels.com/photos/8887054/pexels-photo-8887054.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 180},
                {"weight": "½ kg", "price": 350},
                {"weight": "1 kg", "price": 690}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 10}",
            "name": "Kaju Katli",
            "category": "sweets",
            "description": "Premium cashew fudge cut into diamond shapes. Rich, melt-in-mouth sweetness perfect for gifting.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/016/287/011/small/pista-roll-or-pistachio-rolls-mithai-or-sigar-indian-sweet-or-dessert-for-festivals-free-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 220},
                {"weight": "½ kg", "price": 430},
                {"weight": "1 kg", "price": 850}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 11}",
            "name": "Mysore Pak",
            "category": "sweets",
            "description": "Classic South Indian sweet made with besan, ghee, and sugar. Crumbly texture and rich flavor.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/069/774/906/small/wandouhuang-close-up-of-square-shaped-yellow-dessert-pieces-on-white-plate-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 140},
                {"weight": "½ kg", "price": 270},
                {"weight": "1 kg", "price": 530}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 12}",
            "name": "Gulab Jamun",
            "category": "sweets",
            "description": "Soft milk-solid balls soaked in rose-flavored sugar syrup. Classic Indian dessert loved by all.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/013/261/438/small/gulab-jamun-or-gulabjamun-is-an-indian-sweet-served-in-a-bowl-as-pile-closeup-view-free-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 410}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 13}",
            "name": "Rasgulla",
            "category": "sweets",
            "description": "Spongy white cottage cheese balls in light sugar syrup. Bengali specialty that's light and refreshing.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/052/116/046/small/indian-sweet-rasgulla-famous-bengali-sweet-in-clay-bowl-with-napkin-on-pink-background-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Light Sweet",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 14}",
            "name": "Jalebi",
            "category": "sweets",
            "description": "Crispy spiral-shaped sweet soaked in sugar syrup. Orange-colored festive treat with crunchy texture.",
            "image": "https://images.pexels.com/photos/8489737/pexels-photo-8489737.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Crispy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 15}",
            "name": "Badam Halwa",
            "category": "sweets",
            "description": "Rich almond pudding cooked in ghee and garnished with nuts. Premium dessert for special occasions.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/010/325/448/small/homemade-carrot-halwa-traditional-indian-sweet-on-white-plate-free-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 200},
                {"weight": "½ kg", "price": 390},
                {"weight": "1 kg", "price": 770}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 16}",
            "name": "Kova Mithai",
            "category": "sweets",
            "description": "Milk-based sweet with thick consistency. Traditional preparation that's rich and flavorful.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/053/237/252/small/assorted-indian-sweet-box-include-cream-gulab-jamun-motichoor-laddu-gurer-sondesh-cake-barfi-balushai-balushahi-top-view-of-pakistani-and-bangladeshi-mithai-dessert-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 130},
                {"weight": "½ kg", "price": 250},
                {"weight": "1 kg", "price": 490}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Traditional",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 17}",
            "name": "Dry Jamun",
            "category": "sweets",
            "description": "Dried milk-solid balls that can be stored longer. Convenient alternative to regular gulab jamun.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/037/916/855/small/ai-generated-jalebi-coated-in-sugar-syrup-traditional-indian-sweet-dish-delicious-oriental-sweets-concept-of-indian-cuisine-dessert-traditional-food-photo.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 120},
                {"weight": "½ kg", "price": 230},
                {"weight": "1 kg", "price": 450}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "Long Lasting",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 18}",
            "name": "Soan Papdi",
            "category": "sweets",
            "description": "Flaky, crispy sweet with layered texture. Melts in mouth instantly. Popular festive gift.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/071/940/140/small/a-close-up-of-barfi-indian-sweets-colorful-barfi-arranged-on-white-plate-with-dramatic-background-photo.jpg",
            "prices": [
                {"weight": "¼ kg", "price": 105},
                {"weight": "½ kg", "price": 200},
                {"weight": "1 kg", "price": 390}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Festive Special",
            "inventory_count": 100,
            "out_of_stock": False
        },
        
        # HOT ITEMS (10 products)
        {
            "id": f"product_{timestamp + 19}",
            "name": "Samosa",
            "category": "hot-items",
            "description": "Crispy triangular pastries filled with spiced potato mixture. Perfect tea-time snack.",
            "image": "https://images.unsplash.com/photo-1616813769023-d0557572ddbe",
            "prices": [
                {"weight": "250g (5 pcs)", "price": 80},
                {"weight": "500g (10 pcs)", "price": 150},
                {"weight": "1 kg (20 pcs)", "price": 290}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 20}",
            "name": "Mirchi Bajji",
            "category": "hot-items",
            "description": "Chili fritters with gram flour batter. Spicy and crispy street food favorite.",
            "image": "https://images.unsplash.com/photo-1760047550367-3d72fa3053c5",
            "prices": [
                {"weight": "250g (5 pcs)", "price": 70},
                {"weight": "500g (10 pcs)", "price": 130},
                {"weight": "1 kg (20 pcs)", "price": 250}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Spicy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 21}",
            "name": "Onion Pakoda",
            "category": "hot-items",
            "description": "Sliced onions mixed with chickpea flour and deep-fried. Crispy monsoon delight.",
            "image": "https://images.unsplash.com/photo-1680359939304-7e27ee183e7a",
            "prices": [
                {"weight": "250g", "price": 75},
                {"weight": "500g", "price": 140},
                {"weight": "1 kg", "price": 270}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 22}",
            "name": "Aloo Bonda",
            "category": "hot-items",
            "description": "Spicy potato balls coated with gram flour batter and fried. South Indian favorite.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/016/282/938/small/malai-chop-or-cream-sandwich-made-using-filling-rasgulla-or-gulab-jamun-sweet-is-a-bengali-sweet-free-photo.jpg",
            "prices": [
                {"weight": "250g (5 pcs)", "price": 70},
                {"weight": "500g (10 pcs)", "price": 130},
                {"weight": "1 kg (20 pcs)", "price": 250}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Filling",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 23}",
            "name": "Medu Vada",
            "category": "hot-items",
            "description": "Crispy savory donuts made from urad dal. Classic South Indian breakfast item.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/071/335/594/small/close-up-of-golden-baked-pastries-topped-with-sesame-seeds-and-shredded-coconut-a-delightful-sweet-treat-photo.jpg",
            "prices": [
                {"weight": "250g (5 pcs)", "price": 75},
                {"weight": "500g (10 pcs)", "price": 140},
                {"weight": "1 kg (20 pcs)", "price": 270}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 24}",
            "name": "Kachori",
            "category": "hot-items",
            "description": "Flaky fried bread stuffed with spiced lentil filling. North Indian street food delicacy.",
            "image": "https://images.unsplash.com/photo-1545668856-6eb87ce33b7a",
            "prices": [
                {"weight": "250g (5 pcs)", "price": 80},
                {"weight": "500g (10 pcs)", "price": 150},
                {"weight": "1 kg (20 pcs)", "price": 290}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Flaky",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 25}",
            "name": "Bread Pakoda",
            "category": "hot-items",
            "description": "Spiced potato sandwich coated with batter and deep-fried. Popular tea-time snack.",
            "image": "https://images.unsplash.com/photo-1727018427695-35a6048c91e7",
            "prices": [
                {"weight": "250g (4 pcs)", "price": 70},
                {"weight": "500g (8 pcs)", "price": 130},
                {"weight": "1 kg (16 pcs)", "price": 250}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 26}",
            "name": "Paneer Pakoda",
            "category": "hot-items",
            "description": "Cottage cheese cubes dipped in spiced batter and fried. Rich and crispy vegetarian snack.",
            "image": "https://static.vecteezy.com/system/resources/thumbnails/065/404/939/small/indonesia-traditional-market-snacks-or-jajanan-pasar-in-wooden-tray-photo.JPG",
            "prices": [
                {"weight": "250g", "price": 110},
                {"weight": "500g", "price": 210},
                {"weight": "1 kg", "price": 410}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 27}",
            "name": "Bonda",
            "category": "hot-items",
            "description": "Round potato fritters with perfect crispy coating. Traditional evening snack.",
            "image": "https://images.unsplash.com/photo-1680359939304-7e27ee183e7a",
            "prices": [
                {"weight": "250g (5 pcs)", "price": 65},
                {"weight": "500g (10 pcs)", "price": 120},
                {"weight": "1 kg (20 pcs)", "price": 230}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Comfort Food",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 28}",
            "name": "Mixed Bajji",
            "category": "hot-items",
            "description": "Assorted vegetable fritters including potato, chili, onion, and eggplant. Variety pack.",
            "image": "https://images.unsplash.com/photo-1760047550367-3d72fa3053c5",
            "prices": [
                {"weight": "250g", "price": 75},
                {"weight": "500g", "price": 140},
                {"weight": "1 kg", "price": 270}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Variety",
            "inventory_count": 100,
            "out_of_stock": False
        },
        
        # SNACKS (3 products)
        {
            "id": f"product_{timestamp + 29}",
            "name": "Atukullu Mixture",
            "category": "snacks",
            "description": "Crispy rice flakes mixture with peanuts, curry leaves, and spices. Perfect anytime snack.",
            "image": "https://images.unsplash.com/photo-1649777476920-0eef34169cdb",
            "prices": [
                {"weight": "¼ kg", "price": 70},
                {"weight": "½ kg", "price": 130},
                {"weight": "1 kg", "price": 250}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 30}",
            "name": "Masala Chekkalu",
            "category": "snacks",
            "description": "Spicy rice crackers with cumin and sesame. Traditional Telugu snack that's thin and crispy.",
            "image": "https://images.unsplash.com/photo-1671762520631-2506f7c48ef5",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Crunchy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 31}",
            "name": "Karapusa Janthikalu",
            "category": "snacks",
            "description": "Traditional spiral-shaped savory snack with spiced rice flour. Andhra specialty.",
            "image": "https://images.pexels.com/photos/7660475/pexels-photo-7660475.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False
        },
        
        # PICKLES (9 products)
        {
            "id": f"product_{timestamp + 32}",
            "name": "Mango Pickle",
            "category": "pickles",
            "description": "Spicy and tangy mango pickle with traditional spices. Classic accompaniment for rice and roti.",
            "image": "https://images.unsplash.com/photo-1617854307432-13950e24ba07",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 33}",
            "name": "Lemon Pickle",
            "category": "pickles",
            "description": "Tangy lemon pickle with mustard seeds and spices. Adds zest to every meal.",
            "image": "https://images.unsplash.com/photo-1550850584-455a131629e8",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 34}",
            "name": "Gongura Pickle",
            "category": "pickles",
            "description": "Famous Andhra gongura (sorrel leaves) pickle. Tangy and spicy Telugu delicacy.",
            "image": "https://images.unsplash.com/photo-1733714654311-102cb838ab2c",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Andhra Special",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 35}",
            "name": "Tomato Pickle",
            "category": "pickles",
            "description": "Spicy tomato pickle with garlic and red chili. Rich in flavor and aroma.",
            "image": "https://images.unsplash.com/photo-1632239108217-f6268b8d2622",
            "prices": [
                {"weight": "¼ kg", "price": 80},
                {"weight": "½ kg", "price": 150},
                {"weight": "1 kg", "price": 290}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Spicy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 36}",
            "name": "Mixed Vegetable Pickle",
            "category": "pickles",
            "description": "Assorted vegetable pickle with carrots, cauliflower, and green chili. Variety in every bite.",
            "image": "https://images.unsplash.com/photo-1632239108217-f6268b8d2622",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Variety",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 37}",
            "name": "Red Chili Pickle",
            "category": "pickles",
            "description": "Extra spicy red chili pickle for spice lovers. Use sparingly for intense heat.",
            "image": "https://images.unsplash.com/photo-1733714654311-102cb838ab2c",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Extra Spicy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 38}",
            "name": "Amla Pickle",
            "category": "pickles",
            "description": "Indian gooseberry pickle rich in Vitamin C. Healthy and tangy immunity booster.",
            "image": "https://images.unsplash.com/photo-1617854307432-13950e24ba07",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Healthy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 39}",
            "name": "Garlic Pickle",
            "category": "pickles",
            "description": "Pungent garlic pickle with health benefits. Strong flavor that enhances meals.",
            "image": "https://images.unsplash.com/photo-1550850584-455a131629e8",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": True,
            "tag": "New Arrival",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 40}",
            "name": "Ginger Pickle",
            "category": "pickles",
            "description": "Spicy ginger pickle that aids digestion. Warming and aromatic pickle.",
            "image": "https://images.unsplash.com/photo-1733714654311-102cb838ab2c",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Digestive",
            "inventory_count": 100,
            "out_of_stock": False
        },
        
        # POWDERS (12 products)
        {
            "id": f"product_{timestamp + 41}",
            "name": "Kandi Podi",
            "category": "powders",
            "description": "Traditional Telugu gunpowder made with roasted lentils and spices. Mix with ghee for rice.",
            "image": "https://images.unsplash.com/photo-1716816211590-c15a328a5ff0",
            "prices": [
                {"weight": "¼ kg", "price": 110},
                {"weight": "½ kg", "price": 210},
                {"weight": "1 kg", "price": 410}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 42}",
            "name": "Sambar Powder",
            "category": "powders",
            "description": "Authentic South Indian sambar masala. Essential for preparing flavorful sambar.",
            "image": "https://images.unsplash.com/photo-1675654871683-abf6524f68c6",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 43}",
            "name": "Rasam Powder",
            "category": "powders",
            "description": "Tangy rasam masala with cumin and pepper. Perfect for comforting South Indian soup.",
            "image": "https://images.unsplash.com/photo-1721934081798-34c4488fdd12",
            "prices": [
                {"weight": "¼ kg", "price": 85},
                {"weight": "½ kg", "price": 160},
                {"weight": "1 kg", "price": 310}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Best Seller",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 44}",
            "name": "Biryani Masala Powder",
            "category": "powders",
            "description": "Aromatic biryani spice blend with whole spices. Secret to restaurant-style biryani.",
            "image": "https://images.pexels.com/photos/6220707/pexels-photo-6220707.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 120},
                {"weight": "½ kg", "price": 230},
                {"weight": "1 kg", "price": 450}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 45}",
            "name": "Garam Masala Powder",
            "category": "powders",
            "description": "Warm spice blend essential for Indian cooking. Adds depth to curries and gravies.",
            "image": "https://images.unsplash.com/photo-1675654871683-abf6524f68c6",
            "prices": [
                {"weight": "¼ kg", "price": 100},
                {"weight": "½ kg", "price": 190},
                {"weight": "1 kg", "price": 370}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Essential",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 46}",
            "name": "Curry Powder",
            "category": "powders",
            "description": "Versatile yellow curry powder for everyday cooking. Balanced blend of spices.",
            "image": "https://images.unsplash.com/photo-1615485500834-bc10199bc727",
            "prices": [
                {"weight": "¼ kg", "price": 75},
                {"weight": "½ kg", "price": 140},
                {"weight": "1 kg", "price": 270}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Everyday Use",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 47}",
            "name": "Chaat Masala Powder",
            "category": "powders",
            "description": "Tangy and spicy chaat masala. Perfect for fruits, salads, and street food.",
            "image": "https://images.unsplash.com/photo-1721934081798-34c4488fdd12",
            "prices": [
                {"weight": "¼ kg", "price": 95},
                {"weight": "½ kg", "price": 180},
                {"weight": "1 kg", "price": 350}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Tangy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 48}",
            "name": "Pav Bhaji Masala Powder",
            "category": "powders",
            "description": "Special Mumbai-style pav bhaji masala. Rich red color and authentic flavor.",
            "image": "https://images.pexels.com/photos/6220707/pexels-photo-6220707.jpeg",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Mumbai Style",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 49}",
            "name": "Coriander Powder",
            "category": "powders",
            "description": "Pure ground coriander seeds. Basic spice for Indian cooking with mild flavor.",
            "image": "https://images.unsplash.com/photo-1716816211590-c15a328a5ff0",
            "prices": [
                {"weight": "¼ kg", "price": 60},
                {"weight": "½ kg", "price": 110},
                {"weight": "1 kg", "price": 210}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Basic Spice",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 50}",
            "name": "Red Chili Powder",
            "category": "powders",
            "description": "Hot and spicy red chili powder. Adds heat and color to dishes.",
            "image": "https://images.unsplash.com/photo-1675654871683-abf6524f68c6",
            "prices": [
                {"weight": "¼ kg", "price": 70},
                {"weight": "½ kg", "price": 130},
                {"weight": "1 kg", "price": 250}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Hot",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 51}",
            "name": "Turmeric Powder",
            "category": "powders",
            "description": "Pure ground turmeric with health benefits. Adds golden color and earthy flavor.",
            "image": "https://images.unsplash.com/photo-1615485500834-bc10199bc727",
            "prices": [
                {"weight": "¼ kg", "price": 65},
                {"weight": "½ kg", "price": 120},
                {"weight": "1 kg", "price": 230}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Healthy",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 52}",
            "name": "Cumin Powder",
            "category": "powders",
            "description": "Aromatic ground cumin seeds. Essential spice for tempering and curries.",
            "image": "https://images.unsplash.com/photo-1721934081798-34c4488fdd12",
            "prices": [
                {"weight": "¼ kg", "price": 90},
                {"weight": "½ kg", "price": 170},
                {"weight": "1 kg", "price": 330}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Aromatic",
            "inventory_count": 100,
            "out_of_stock": False
        },
        
        # SPICES (4 products)
        {
            "id": f"product_{timestamp + 53}",
            "name": "Black Pepper Whole",
            "category": "spices",
            "description": "Premium quality whole black peppercorns. Fresh and pungent for grinding.",
            "image": "https://images.unsplash.com/photo-1649951806971-ad0e00408773",
            "prices": [
                {"weight": "¼ kg", "price": 150},
                {"weight": "½ kg", "price": 290},
                {"weight": "1 kg", "price": 570}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 54}",
            "name": "Green Cardamom",
            "category": "spices",
            "description": "Aromatic green cardamom pods. Perfect for desserts, chai, and biryani.",
            "image": "https://images.unsplash.com/photo-1699859955036-fe4d7f173d15",
            "prices": [
                {"weight": "¼ kg", "price": 350},
                {"weight": "½ kg", "price": 690},
                {"weight": "1 kg", "price": 1350}
            ],
            "isBestSeller": True,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 55}",
            "name": "Cinnamon Sticks",
            "category": "spices",
            "description": "True Ceylon cinnamon sticks. Sweet and woody aroma for rice and curries.",
            "image": "https://images.unsplash.com/photo-1644057440075-3a5b077fe64d",
            "prices": [
                {"weight": "¼ kg", "price": 200},
                {"weight": "½ kg", "price": 390},
                {"weight": "1 kg", "price": 770}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Aromatic",
            "inventory_count": 100,
            "out_of_stock": False
        },
        {
            "id": f"product_{timestamp + 56}",
            "name": "Cloves Whole",
            "category": "spices",
            "description": "Premium quality whole cloves. Intense flavor for garam masala and rice dishes.",
            "image": "https://images.unsplash.com/photo-1633881614907-8587c9b93c2f",
            "prices": [
                {"weight": "¼ kg", "price": 250},
                {"weight": "½ kg", "price": 490},
                {"weight": "1 kg", "price": 970}
            ],
            "isBestSeller": False,
            "isNew": False,
            "tag": "Premium",
            "inventory_count": 100,
            "out_of_stock": False
        }
    ]
    
    # Insert all products
    if products:
        result = await db.products.insert_many(products)
        print(f"✅ Successfully added {len(result.inserted_ids)} products to database")
        
        # Print summary
        categories = {}
        for product in products:
            cat = product['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📊 Product Summary:")
        for category, count in categories.items():
            print(f"   {category}: {count} products")
    else:
        print("❌ No products to insert")

if __name__ == "__main__":
    asyncio.run(seed_products())
    print("\n🎉 Database seeding completed successfully!")
