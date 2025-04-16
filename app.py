import streamlit as st
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="E-Commerce Demo",
    page_icon="🛒",
    layout="centered"
)

# -----------------------------
# Session State Setup
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "cart" not in st.session_state:
    st.session_state.cart = {}

# -----------------------------
# Dummy User Login Info
# -----------------------------
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "customer"}
}

# -----------------------------
# Login System (Centered)
# -----------------------------
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>Login to Your Account</h2>", unsafe_allow_html=True)
    st.markdown("###")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = users[username]["role"]
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()
else:
    st.sidebar.success(f"Logged in as {st.session_state.user_role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()

# -----------------------------
# Sample Product Data
# -----------------------------
products = [
    {
        "name": "Wireless Headphones",
        "price": 50,
        "image": "assets/headphones.jpeg",
        "description": "High-quality wireless headphones with noise cancellation.",
        "category": "Electronics"
    },
    {
        "name": "Smart Watch",
        "price": 120,
        "image": "assets/smart_watch.jpeg",
        "description": "Fitness tracking smart watch with long battery life.",
        "category": "Wearables"
    },
    {
        "name": "Laptop",
        "price": 800,
        "image": "assets/laptop.jpeg",
        "description": "Sleek laptop with powerful performance for work and play.",
        "category": "Computers"
    },
    {
        "name": "Bluetooth Speaker",
        "price": 40,
        "image": "assets/speaker.jpeg",
        "description": "Compact speaker with impressive sound quality.",
        "category": "Electronics"
    },
    {
        "name": "DSLR Camera",
        "price": 650,
        "image": "assets/camera.jpeg",
        "description": "Professional DSLR camera for photography enthusiasts.",
        "category": "Electronics"
    }
]

deal_products = [
    {
        "name": "Gaming Mouse",
        "price": 30,
        "original_price": 45,
        "image": "assets/gaming.jpeg",
        "description": "High DPI gaming mouse with colorful lighting.",
    },
    {
        "name": "Noise Cancelling Earbuds",
        "price": 25,
        "original_price": 50,
        "image": "assets/buds.jpeg",
        "description": "In-ear buds with active noise cancelling technology.",
    }
]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
search_term = st.sidebar.text_input("Search")
cost_range = st.sidebar.slider("Price Range", 0, 1000, (0, 1000))
category = st.sidebar.selectbox("Category", ["All", "Electronics", "Wearables", "Computers"])

# -----------------------------
# Product Filtering
# -----------------------------
filtered_products = [p for p in products if cost_range[0] <= p["price"] <= cost_range[1]]
if category != "All":
    filtered_products = [p for p in filtered_products if p["category"] == category]
if search_term:
    filtered_products = [p for p in filtered_products if search_term.lower() in p["name"].lower()]

# -----------------------------
# Add to Cart
# -----------------------------
def add_to_cart(product_name, quantity=1):
    if product_name in st.session_state.cart:
        st.session_state.cart[product_name] += quantity
    else:
        st.session_state.cart[product_name] = quantity

# -----------------------------
# Display Products
# -----------------------------
def display_products(product_list):
    for product in product_list:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image(product["image"], width=120)
        with col2:
            st.subheader(product["name"])
            st.write(product["description"])
            st.write(f"*Price:* ${product['price']}")
            qty = st.number_input("Qty", 0, 5, 0, key=f"qty_{product['name']}")
        with col3:
            if st.button("Add to Cart 🛒", key=f"add_{product['name']}"):
                if qty > 0:
                    add_to_cart(product["name"], qty)
                    st.success(f"Added {qty} x {product['name']} to cart!")
                else:
                    st.warning("Please select a quantity greater than 0.")
        st.markdown("---")

# -----------------------------
# Display Cart
# -----------------------------
def show_cart():
    st.subheader("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Cart is empty.")
        return

    total = 0
    for name, qty in st.session_state.cart.items():
        product = next((p for p in products if p["name"] == name), None) or \
                  next((p for p in deal_products if p["name"] == name), None)
        if product:
            line_total = product["price"] * qty
            total += line_total
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(product["image"], width=80)
            with col2:
                st.write(f"{name}")
                st.write(f"Quantity: {qty}")
                st.write(f"Total: ${line_total}")
    st.write(f"### Grand Total: ${total}")
    if st.button("Checkout"):
        st.success("Proceeding to payment gateway...")

# -----------------------------
# Admin Panel
# -----------------------------
def admin_controls():
    st.subheader("🛠 Admin Panel")

    with st.expander("➕ Add New Product"):
        name = st.text_input("Product Name")
        desc = st.text_area("Description")
        price = st.number_input("Price", min_value=1, step=1)
        cat = st.selectbox("Category", ["Electronics", "Wearables", "Computers"])
        img = st.text_input("Image Path (e.g., assets/your_image.jpeg)")
        if st.button("Add Product"):
            new_prod = {
                "name": name,
                "price": price,
                "image": img,
                "description": desc,
                "category": cat
            }
            products.append(new_prod)
            st.success(f"Product '{name}' added.")

    with st.expander("✏ Update Product Price"):
        prod_names = [p["name"] for p in products]
        selected = st.selectbox("Select Product", prod_names)
        new_price = st.number_input("New Price", min_value=1, step=1)
        if st.button("Update Price"):
            for p in products:
                if p["name"] == selected:
                    p["price"] = new_price
                    st.success(f"Updated price of {selected} to ${new_price}")

# -----------------------------
# Top Header and Logo
# -----------------------------
st.image("assets/logo.jpeg", width=800)
st.markdown("<h1 style='text-align:center;'>Welcome to Our E-Commerce Store</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Shop the best products at the best prices!</p>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# Main Tabs
# -----------------------------
tabs = st.tabs(["🏠 Home", "🔥 Today's Deal", "📦 Cart", "📞 Support"] + (["🛠 Admin"] if st.session_state.user_role == "admin" else []))

# Home Tab
with tabs[0]:
    st.subheader("🛍 Products")
    if filtered_products:
        display_products(filtered_products)
    else:
        st.warning("No matching products found.")

# Deal Tab
with tabs[1]:
    st.subheader("🔥 Limited Time Deals")
    for dp in deal_products:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image(dp["image"], width=100)
        with col2:
            st.subheader(dp["name"])
            st.write(dp["description"])
            st.markdown(
                f"<span style='color:red; font-size:28px;'>${dp['price']} "
                f"${dp['original_price']}",
                unsafe_allow_html=True
            )
            qty = st.number_input("Qty", 0, 5, 0, key=f"deal_{dp['name']}")
        with col3:
            if st.button("Add to Cart", key=f"btn_deal_{dp['name']}"):
                if qty > 0:
                    add_to_cart(dp["name"], qty)
                    st.success(f"Added {qty} x {dp['name']}")
        st.markdown("---")

# Cart Tab
with tabs[2]:
    show_cart()

# Support Tab
with tabs[3]:
    st.subheader("📞 Customer Support")
    st.markdown(""" 
    - 📦 *Shipping:* Ships within 2-3 business days.
    - 🔁 *Returns:* 30-day hassle-free returns.
    - 📧 *Contact:* support@ecommerce.com
    """)

# Admin Tab
if st.session_state.user_role == "admin":
    with tabs[4]:
        admin_controls()

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>© 2025 E-Commerce Demo. Built with ❤ using Streamlit.</p>", unsafe_allow_html=True)
