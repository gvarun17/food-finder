"""Fake dev data. Every restaurant here is invented and inserted with is_fake = TRUE.
Replace with real, verified data before any real user sees results.

Dish tuple: (name, description, price_inr, is_veg, spice_level 0-3, course)
"""

RESTAURANTS = [
    {
        "name": "Dev Dum House", "area": "Gachibowli", "cuisines": ["Hyderabadi", "Biryani"], "price_band": 2,
        "dishes": [
            ("Chicken Dum Biryani", "Slow-cooked basmati rice layered with marinated chicken, served with mirchi ka salan", 280, False, 2, "main"),
            ("Mutton Dum Biryani", "Tender mutton pieces cooked dum style with saffron and fried onions", 380, False, 2, "main"),
            ("Veg Dum Biryani", "Seasonal vegetables and paneer cooked with fragrant rice and mint", 220, True, 1, "main"),
            ("Chicken 65", "Crispy fried chicken tossed with curry leaves and green chilli, very spicy", 240, False, 3, "starter"),
            ("Paneer 65", "Crispy fried paneer cubes with a spicy curd and curry leaf coating", 220, True, 3, "starter"),
            ("Mirchi Ka Salan", "Tangy peanut and sesame gravy with green chillies", 90, True, 2, "side"),
            ("Double Ka Meetha", "Fried bread pudding soaked in saffron milk and dry fruits", 120, True, 0, "dessert"),
            ("Irani Chai", "Strong milky tea with a hint of cardamom", 40, True, 0, "drink"),
        ],
    },
    {
        "name": "Dev Green Leaf", "area": "Gachibowli", "cuisines": ["South Indian", "Vegetarian"], "price_band": 1,
        "dishes": [
            ("Masala Dosa", "Crisp rice crepe filled with spiced potato, served with chutneys and sambar", 110, True, 1, "main"),
            ("Ghee Podi Idli", "Mini idlis tossed in spicy gunpowder and ghee", 120, True, 2, "starter"),
            ("Medu Vada", "Crispy lentil donuts, soft inside, with sambar and coconut chutney", 80, True, 0, "starter"),
            ("Pesarattu Upma", "Green gram dosa stuffed with upma, an Andhra breakfast favourite", 120, True, 1, "main"),
            ("Mini Meals", "Rice, sambar, rasam, two curries, curd and papad, light lunch", 180, True, 1, "main"),
            ("Filter Coffee", "Strong South Indian decoction coffee with frothy milk", 50, True, 0, "drink"),
            ("Rava Kesari", "Sweet semolina pudding with ghee and cashew", 70, True, 0, "dessert"),
            ("Gongura Rice", "Tangy sorrel leaf rice with peanuts, spicy and sour", 150, True, 3, "main"),
        ],
    },
    {
        "name": "Dev Wok Express", "area": "Gachibowli", "cuisines": ["Chinese", "Indo-Chinese"], "price_band": 2,
        "dishes": [
            ("Veg Manchurian Dry", "Crispy vegetable balls tossed in a garlicky soy sauce", 190, True, 2, "starter"),
            ("Chilli Paneer", "Paneer cubes with peppers and onions in a hot chilli sauce", 230, True, 3, "starter"),
            ("Chicken Lollipop", "Fried chicken winglets with a spicy red coating", 260, False, 2, "starter"),
            ("Schezwan Fried Rice", "Wok-tossed rice with vegetables in fiery schezwan sauce", 200, True, 3, "main"),
            ("Chicken Hakka Noodles", "Stir-fried noodles with chicken, cabbage and spring onion", 240, False, 1, "main"),
            ("Hot and Sour Soup", "Peppery tangy soup with mushrooms and vegetables", 130, True, 2, "soup"),
            ("Sweet Corn Soup", "Mild, creamy sweet corn soup, light and comforting", 120, True, 0, "soup"),
            ("Honey Chilli Potato", "Crispy potato fingers glazed in honey and chilli, sweet and spicy", 170, True, 2, "starter"),
        ],
    },
    {
        "name": "Dev Kebab Corner", "area": "Madhapur", "cuisines": ["North Indian", "Mughlai", "Kebabs"], "price_band": 3,
        "dishes": [
            ("Chicken Tikka", "Charcoal-grilled chicken marinated in yogurt and spices", 290, False, 2, "starter"),
            ("Mutton Seekh Kebab", "Minced mutton skewers grilled in the tandoor, juicy and smoky", 340, False, 2, "starter"),
            ("Paneer Tikka", "Tandoor-grilled paneer with bell peppers and onions", 250, True, 1, "starter"),
            ("Hara Bhara Kebab", "Spinach and green pea patties, pan-fried, mild and light", 210, True, 0, "starter"),
            ("Butter Chicken", "Creamy tomato gravy with tender tandoori chicken", 330, False, 1, "main"),
            ("Dal Makhani", "Slow-cooked black lentils with butter and cream", 220, True, 0, "main"),
            ("Butter Naan", "Soft tandoor-baked bread brushed with butter", 60, True, 0, "bread"),
            ("Phirni", "Chilled ground-rice pudding with cardamom in a clay bowl", 110, True, 0, "dessert"),
        ],
    },
    {
        "name": "Dev Andhra Mess", "area": "Madhapur", "cuisines": ["Andhra", "Telugu"], "price_band": 1,
        "dishes": [
            ("Andhra Chicken Fry", "Chicken fried with red chillies and curry leaves, very spicy", 220, False, 3, "starter"),
            ("Natu Kodi Pulusu", "Country chicken stew in a tangy tamarind gravy", 290, False, 3, "main"),
            ("Gongura Mutton", "Mutton cooked with tangy sorrel leaves, a signature Andhra dish", 360, False, 3, "main"),
            ("Veg Meals", "Unlimited rice with dal, three curries, pickle, curd and papad", 160, True, 2, "main"),
            ("Pappu Charu", "Comforting lentil and tamarind soup served with rice", 100, True, 1, "main"),
            ("Gutti Vankaya Curry", "Stuffed brinjal in a peanut and sesame masala", 170, True, 2, "main"),
            ("Bobbatlu", "Sweet flatbread stuffed with lentil and jaggery", 80, True, 0, "dessert"),
            ("Buttermilk", "Spiced, cooling buttermilk with ginger and curry leaves", 30, True, 0, "drink"),
        ],
    },
    {
        "name": "Dev Pizza Yard", "area": "Madhapur", "cuisines": ["Italian", "Pizza"], "price_band": 3,
        "dishes": [
            ("Margherita Pizza", "Classic tomato, mozzarella and basil on a thin crust", 320, True, 0, "main"),
            ("Paneer Tikka Pizza", "Tandoori paneer, onion and capsicum with a spicy sauce", 380, True, 2, "main"),
            ("Chicken Pepperoni Pizza", "Chicken pepperoni and mozzarella on a hand-tossed base", 420, False, 1, "main"),
            ("Penne Arrabbiata", "Penne in a spicy tomato and garlic sauce", 290, True, 2, "main"),
            ("Alfredo Pasta with Chicken", "Creamy white sauce pasta with grilled chicken", 350, False, 0, "main"),
            ("Garlic Bread with Cheese", "Toasted bread with garlic butter and melted cheese", 170, True, 0, "starter"),
            ("Tiramisu", "Coffee-soaked sponge layered with mascarpone", 240, True, 0, "dessert"),
            ("Caesar Salad", "Romaine with parmesan, croutons and a light dressing", 260, True, 0, "starter"),
        ],
    },
    {
        "name": "Dev Charminar Haleem", "area": "Banjara Hills", "cuisines": ["Hyderabadi", "Mughlai"], "price_band": 2,
        "dishes": [
            ("Mutton Haleem", "Slow-cooked wheat, lentils and mutton, pounded smooth, topped with fried onions", 260, False, 2, "main"),
            ("Chicken Haleem", "A lighter chicken version of the Ramzan classic with ghee and lime", 220, False, 2, "main"),
            ("Veg Haleem", "Wheat, lentils and vegetables slow-cooked in the haleem style", 180, True, 1, "main"),
            ("Paya Shorba", "Rich trotter soup with warm spices", 190, False, 2, "soup"),
            ("Pathar Ka Gosht", "Mutton grilled on a hot stone with Hyderabadi spices", 380, False, 2, "starter"),
            ("Khubani Ka Meetha", "Stewed dried apricots with cream, a Hyderabadi dessert", 140, True, 0, "dessert"),
            ("Lukhmi", "Flaky pastry stuffed with spiced minced meat", 150, False, 1, "starter"),
            ("Sheer Khurma", "Vermicelli cooked in milk with dates and nuts", 130, True, 0, "dessert"),
        ],
    },
    {
        "name": "Dev Terrace Grill", "area": "Banjara Hills", "cuisines": ["Continental", "Grill", "Bar"], "price_band": 4,
        "dishes": [
            ("Grilled Chicken Steak", "Herb-marinated chicken breast with pepper sauce and mash", 560, False, 1, "main"),
            ("Mushroom Stroganoff", "Mushrooms in a creamy paprika sauce with buttered rice", 440, True, 0, "main"),
            ("Grilled Fish with Lemon Butter", "Fresh fish fillet grilled with lemon butter and vegetables", 620, False, 0, "main"),
            ("Peri Peri Paneer Skewers", "Paneer and vegetables grilled with a spicy peri peri glaze", 420, True, 2, "starter"),
            ("Loaded Nachos", "Corn chips with cheese, jalapenos, salsa and beans", 340, True, 1, "starter"),
            ("Lamb Chops", "Pan-seared lamb chops with rosemary jus", 780, False, 1, "main"),
            ("Chocolate Lava Cake", "Warm chocolate cake with a molten centre and ice cream", 280, True, 0, "dessert"),
            ("Virgin Mojito", "Mint, lime and soda, cold and refreshing", 180, True, 0, "drink"),
        ],
    },
    {
        "name": "Dev Chaat Street", "area": "Banjara Hills", "cuisines": ["Chaat", "Street Food", "Vegetarian"], "price_band": 1,
        "dishes": [
            ("Pani Puri", "Crisp hollow puris with spicy mint water, potato and chickpeas", 60, True, 2, "starter"),
            ("Dahi Papdi Chaat", "Crisp papdi with yogurt, tamarind and mint chutney, sweet and tangy", 90, True, 1, "starter"),
            ("Pav Bhaji", "Spiced mashed vegetable curry with buttered pav", 130, True, 1, "main"),
            ("Samosa Chaat", "Crushed samosa topped with chole, yogurt and chutneys", 100, True, 2, "starter"),
            ("Dabeli", "Gujarati potato filling with peanuts and pomegranate in a bun", 70, True, 1, "starter"),
            ("Kulfi Falooda", "Creamy kulfi over falooda noodles and rose syrup", 140, True, 0, "dessert"),
            ("Masala Soda", "Fizzy lemon soda with chaat masala and black salt", 50, True, 0, "drink"),
            ("Bhel Puri", "Puffed rice, sev, onions and chutneys, light and crunchy", 80, True, 1, "starter"),
        ],
    },
]
