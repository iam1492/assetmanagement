import streamlit as st
import streamlit_authenticator as stauth
import yaml
import os
from pyaml_env import parse_config

class AssetManagementUI:
    
    def __init__(self):
        st.set_page_config(page_title="Ramus", page_icon="👋")
        
        page_home = st.Page("home.py", title="Stock Analysis", icon="🚀")
        page_my_records = st.Page("my_records.py", title="My Records", icon="💾")
        page_about = st.Page("zbout.py", title="About", icon="🧐")

        dir = os.path.dirname(__file__)
        self.config_path = os.path.join(dir, "config/authentication.yaml")
        self.config = parse_config(self.config_path)
        self.authenticator = stauth.Authenticate(
                self.config['credentials'],
                self.config['cookie']['name'],
                self.config['cookie']['key'],
                self.config['cookie']['expiry_days'],
                auto_hash=False
            )
        
        if self.is_logged_in():
            pg = st.navigation(
                {
                    "Stock Analysis": [page_home, page_my_records],
                    "More": [page_about]
                }
            ) 
        else:
            pg = st.navigation(pages=[page_about], position="hidden")
        pg.run()
    
    def render(self):
        self.authenticate()
        if st.session_state['authentication_status']:
            self.authenticator.logout(location="sidebar")
        
    def authenticate(self):
        if st.session_state['authentication_status'] is False:
            st.error('Username/password is incorrect')
        elif st.session_state['authentication_status'] is None:
            self.authenticator.login(location="main")
            st.warning('Please enter your username and password')
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)

    def is_logged_in(self):
        return st.session_state['authentication_status']
    
if __name__ == "__main__":
    AssetManagementUI().render()


