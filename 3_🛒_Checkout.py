import streamlit as st

st.set_page_config(page_title="Secure Checkout", layout="centered")

# --- UI Header ---
st.title("🛡️ Secure Your Trademark")
st.subheader("Resolution Roadmap & Risk Audit")

# --- Service Details ---
with st.container():
    st.write("---")
    st.markdown("""
    ### What's included in your $299 Audit:
    * **Full Risk Analysis** of your current USPTO Status.
    * **Evidence Review** to prevent permanent refusal.
    * **Resolution Steps** tailored to your serial number.
    * **15-Minute Strategy Call** with our lead consultant.
    """)
    st.write("---")

# --- The "Handshake" to Stripe ---
st.info("You are being redirected to our secure Stripe checkout.")

# REPLACE THE URL BELOW WITH YOUR ACTUAL STRIPE LINK
stripe_url = "https://buy.stripe.com/YOUR_ACTUAL_LINK_HERE"

# Creating a high-visibility button
st.link_button("🚀 Proceed to Secure Checkout", stripe_url, use_container_width=True)

# --- Trust Signals ---
st.caption("🔒 Payments secured by Stripe. NovaSys LLC is a private consulting firm and is not affiliated with the USPTO.")