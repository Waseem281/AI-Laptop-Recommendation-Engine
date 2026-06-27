import streamlit as st
from ai.ai_explainer import explain_recommendation


def product_card(product):

    with st.container(border=True):

        # ===================================
        # Laptop Name
        # ===================================

        st.subheader(f"💻 {product['name']}")

        # ===================================
        # AI Match Score
        # ===================================

        if "similarity" in product.index:

            score = float(product["similarity"])

            if score >= 90:
                st.success(f"🎯 Excellent Match: {score:.1f}%")

            elif score >= 75:
                st.warning(f"🎯 Good Match: {score:.1f}%")

            else:
                st.info(f"🎯 Match Score: {score:.1f}%")

        st.divider()

        # ===================================
        # Layout
        # ===================================

        left, right = st.columns([2, 1])

        with left:

            st.write(f"🏷 **Brand:** {product['brand']}")

            st.write(
                f"🧠 **Processor:** {product['processor_brand']} {product['processor']}"
            )

            st.write(f"💾 **RAM:** {product['ram']} GB")

            st.write(f"💽 **Storage:** {product['memory_size']} GB")

            st.write(
                f"🎮 **GPU:** {product['gpu_brand']} {product['gpu_type']}"
            )

            st.write(f"🪟 **OS:** {product['os']}")

        with right:

            st.metric(
                "💰 Price",
                f"₹{int(product['price']):,}"
            )

            st.metric(
                "⭐ Rating",
                f"{product['rating']}"
            )

            st.metric(
                "🖥 Display",
                f"{product['display_size']}\""
            )

        st.divider()

        st.caption(f"🛡 Warranty: {product['warrenty']}")

        # ===================================
        # AI Explanation
        # ===================================

        if st.button(
            "🤖 Why Recommended?",
            key=f"why_{product.name}"
        ):

            with st.spinner("Generating explanation..."):

                explanation = explain_recommendation(
                    product,
                    st.session_state.get(
                        "last_query",
                        ""
                    )
                )

            st.info(explanation)