import streamlit as st
st.title("📊 USPTO Status Intelligence")
st.info("Status 641: High-Risk Alert")
st.write("Current data shows a surge in Status 641 delays for DIY filers. Vanessa can help.")
if st.button("Check My Serial Number"):
    st.switch_page("pages/3_🔍_Instant_Check.py")