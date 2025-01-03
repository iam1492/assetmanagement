import streamlit as st
import sys
from pathlib import Path
import markdown
import os
import traceback
from dotenv import load_dotenv
sys.path.append(str(Path(__file__).parent.parent))
from assetmanagement.crew import Assetmanagement
from crewai.crew import CrewOutput
import assetmanagement.emoji as emoji
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re
import streamlit_authenticator as stauth
from pyaml_env import parse_config
import yaml
from google.cloud import firestore
from streamlit_extras.add_vertical_space import add_vertical_space

load_dotenv()

class StockReportGenUI:
    authenticator = None
    config = None
    config_path = None
    db = None
    
    def __init__(self):
        #load database
        root_path = Path(__file__).parent.parent.parent
        firestore_key_path = os.path.join(root_path,"firestore-key.json" )
        self.db = firestore.Client.from_service_account_json(firestore_key_path)
        
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
    
    def start_analysing(self, company):
        inputs = {
            'company': company,
        }
        return Assetmanagement().crew().kickoff(inputs)
    
    def report_generation(self):
        if st.session_state.generating:
            st.session_state.final_report = self.start_analysing(st.session_state.company)
        if st.session_state.final_report and st.session_state.final_report != "":
            st.session_state.generating = False
            if isinstance(st.session_state.final_report, CrewOutput):
                try:
                    final_result = st.session_state.final_report.raw
                    self.save_to_firestore(final_result)
                    self.send_email()
                    st.session_state.final_report = ""
                except Exception as e:
                    print(traceback.format_exc())
                    st.error(f"An error occurred: {e}")
                    st.session_state.final_report = ""
    
    def save_to_firestore(self, final_result):
        json_object = eval(final_result)
        user_doc = self.db.collection("users").document(st.session_state['username'])
        company_doc = user_doc.collection("companies").document(json_object['ticker'])
        company_doc.set({
                        "company": json_object['company'],
                        "ticker": json_object['ticker'],
                        "rating": json_object['rating'],
                        "final_result": json_object['final_result'],
                        "created_at":firestore.SERVER_TIMESTAMP
                    })

    def is_valid_email(self, email: str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def sidebar(self):
        
        with st.sidebar:
            st.text_input("Enter name of company", key='company', placeholder="Apple, Adobe, etc")
            st.checkbox("Send final report to my email", key='send_email')
            
            if st.button("Start Analysis"):
                st.session_state.generating = True
            
            add_vertical_space(10)
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
    
    def render(self):
        
        self.authenticate()
        
        if st.session_state['authentication_status']:
            if "company" not in st.session_state:
                st.session_state.company = ""
                
            if "final_report" not in st.session_state:
                st.session_state.final_report = ""
                
            if "generating" not in st.session_state:
                st.session_state.generating = ""
            
            st.subheader("Ramus Stock Analysis", divider="gray")
            st.write(f"Welcome :blue[{st.session_state['username']}] :sunglasses:")
            st.markdown(
                f"""    
                ### Members
                ### {emoji.RAMUS} CEO - Ramus Jung
                ### {emoji.SUNNY} CSO - Sunny Park
                * {emoji.SANTA} Research Head - Santa Claus
                * {emoji.RUDOLF} Technical Analyst - Rudolf
                * {emoji.SNOWMAN} Financial Analyst - Snowman
                * {emoji.ELSA} Macro Analyst - Elsa
                * {emoji.PENGSU} Translator - Pengsu
                * {emoji.KEVIN} Hedge Fund Manager - Kevin
                """
            )
            
            self.sidebar();
            self.report_generation();

    def send_email(self):
        
        markdown_text = None
        
        with open(self.get_report_path("investment_recommendation_kr.md"), "r", encoding='utf-8') as f:
            markdown_text = f.read()
            
        print(f"##### markdown_text: {markdown_text}")
        
        if st.session_state.send_email and markdown_text:
            receiver = st.session_state['email']
            sender = os.getenv('GMAIL_SENDER')
            smtp_server = os.getenv('SMTP_SERVER')
            smtp = smtplib.SMTP(smtp_server, 587)
            smtp.starttls()
            smtp.login(os.getenv('GMAIL_SENDER'), os.getenv('GMAIL_PASSWORD'))
            
            multipart_msg = MIMEMultipart("alternative")
            multipart_msg["Subject"] = f"{st.session_state.company} Stock Analysis Report"
            multipart_msg["From"] = sender
            multipart_msg["To"] = receiver

            html = markdown.markdown(markdown_text)
            part1 = MIMEText(markdown_text, "plain")
            part2 = MIMEText(html, "html")
            multipart_msg.attach(part1)
            multipart_msg.attach(part2)
            
            with open(self.get_report_path("macro_report.md"), "r", encoding='utf-8') as f:
                multipart_msg.attach(MIMEApplication(f.read(), Name="macro_report.md"))
                
            with open(self.get_report_path("financial_report.md"), "r", encoding='utf-8') as f:
                multipart_msg.attach(MIMEApplication(f.read(), Name="financial_report.md"))
            
            with open(self.get_report_path("technical_report.md"), "r", encoding='utf-8') as f:
                multipart_msg.attach(MIMEApplication(f.read(), Name="technical_report.md"))

            smtp.sendmail(sender, receiver, multipart_msg.as_string())
            smtp.quit()
    
    def get_report_path(self, file_name: str):
        root_path = Path(__file__).parent.parent.parent
        return os.path.join(root_path,f"reports/{file_name}" )
    
StockReportGenUI().render()