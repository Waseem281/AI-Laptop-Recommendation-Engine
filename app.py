import streamlit as st

from services.product_service import ProductService
from services.recommendation_service import RecommendationService
from ai.query_parser import parse_query
from utils.product_card import product_card


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Laptop Recommendation Engine",
    page_icon="💻",
    layout="wide"
)


# =====================================================
# LOAD CSS
# =====================================================

def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css()


# =====================================================
# LOAD DATA
# =====================================================

product_service = ProductService()

df = product_service.get_all_products()

recommendation_service = RecommendationService(df)


# =====================================================
# HERO
# =====================================================

st.title("💻 AI Laptop Recommendation Engine")

st.write(
    "Find the perfect laptop using Artificial Intelligence."
)

st.caption(
    "Search naturally • Compare laptops • Get AI recommendations"
)

st.divider()


# =====================================================
# DASHBOARD
# =====================================================

stats = product_service.get_statistics()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💻 Laptops", stats["total_laptops"])
c2.metric("🏷 Brands", stats["total_brands"])
c3.metric("⭐ Avg Rating", f"{stats['average_rating']:.2f}")
c4.metric("💰 Avg Price", f"₹{stats['average_price']:,.0f}")

st.divider()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🔍 Filters")

brand = st.sidebar.selectbox(
    "Brand",
    ["All"] + product_service.get_brands()
)

processor_brand = st.sidebar.selectbox(
    "Processor Brand",
    ["All"] + sorted(df["processor_brand"].astype(str).unique())
)

ram = st.sidebar.selectbox(
    "RAM",
    ["All"] + sorted(df["ram"].dropna().astype(int).astype(str).unique())
)

max_price = st.sidebar.slider(
    "Maximum Price",
    int(df["price"].min()),
    int(df["price"].max()),
    int(df["price"].max())
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    5.0,
    0.0,
    0.1
)

sort_option = st.sidebar.selectbox(
    "Sort By",
    [
        "AI Recommendation",
        "Price Low to High",
        "Price High to Low",
        "Highest Rating"
    ]
)


# =====================================================
# SEARCH
# =====================================================

query = st.text_input(
    "",
    placeholder="🔍 Example: Gaming laptop under ₹70000"
)

st.session_state["last_query"] = query


# =====================================================
# QUICK SEARCHES
# =====================================================

st.markdown("### 🔥 Popular Searches")

a, b, c, d = st.columns(4)

if a.button("🎮 Gaming"):
    query = "Gaming laptop"

if b.button("👨‍💻 Coding"):
    query = "Laptop for programming"

if c.button("🤖 AI/ML"):
    query = "Machine Learning Laptop"

if d.button("📚 Student"):
    query = "Student Laptop"


# =====================================================
# FILTER PRODUCTS
# =====================================================

filtered = product_service.filter_products(
    brand=brand,
    processor_brand=processor_brand,
    ram=ram,
    max_price=max_price,
    min_rating=min_rating
)


# =====================================================
# AI SEARCH
# =====================================================

if query:

    with st.spinner("🤖 AI is understanding your query..."):

        ai = parse_query(query)

    with st.expander("AI Analysis"):
        st.json(ai)

    search_text = " ".join(
        [
            str(ai["purpose"]),
            str(ai["processor"]),
            str(ai["gpu"]),
            str(ai["brand"])
        ]
    ).strip()

    if search_text == "":
        search_text = query

    recommendations = recommendation_service.recommend(
        search_text,
        top_n=20
    )

    if ai["budget"] != "":
        recommendations = recommendations[
            recommendations["price"] <= float(ai["budget"])
        ]

    if ai["brand"] != "":
        recommendations = recommendations[
            recommendations["brand"].str.lower()
            ==
            ai["brand"].lower()
        ]

    filtered = recommendations


# =====================================================
# SORTING
# =====================================================

if sort_option == "Price Low to High":
    filtered = filtered.sort_values("price")

elif sort_option == "Price High to Low":
    filtered = filtered.sort_values(
        "price",
        ascending=False
    )

elif sort_option == "Highest Rating":
    filtered = filtered.sort_values(
        "rating",
        ascending=False
    )


# =====================================================
# RESULTS
# =====================================================

filtered = filtered.head(10)

st.divider()

st.subheader(f"🏆 Top Recommendations ({len(filtered)})")

if filtered.empty:
    st.warning("No laptops found.")

else:

    col1, col2 = st.columns(2)

    for i, (_, laptop) in enumerate(filtered.iterrows()):

        with col1 if i % 2 == 0 else col2:
            product_card(laptop)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
<center>

### 🚀 AI Laptop Recommendation Engine

Built using

**Python • Streamlit • Groq • Scikit-learn • Pandas**

</center>
""",
    unsafe_allow_html=True
)