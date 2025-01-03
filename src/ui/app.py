import streamlit as st
import streamlit_authenticator as stauth

class AssetManagementUI:
    def __init__(self):
        st.set_page_config(page_title="Ramus", page_icon="👋")
        pg = st.navigation([
            st.Page("home.py", title="Stock Analysis", icon="🚀"),
            st.Page("my_records.py", title="My Records", icon="💾"),
        ])
        pg.run()
        
    def render(self):
        pass

if __name__ == "__main__":
    AssetManagementUI().render()

