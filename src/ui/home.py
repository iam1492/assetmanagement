import streamlit as st
import sys
import pathlib
import markdown
import os
import traceback
from dotenv import load_dotenv
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from assetmanagement.crew import Assetmanagement
from crewai.crew import CrewOutput
import assetmanagement.emoji as emoji
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

class StockReportGenUI:
    
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
                    self.send_email(st.session_state.final_report.raw, st.session_state.company, st.session_state.email)
                    st.session_state.final_report = ""
                except Exception as e:
                    print(traceback.format_exc())
                    st.error(f"An error occurred: {e}")
                    st.session_state.final_report = ""

    def is_valid_email(self, email: str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def sidebar(self):
        with st.sidebar:
            st.markdown("## Menu")
            st.text_input("Enter name of company", key='company', placeholder="Apple, Adobe, etc")
            email = st.text_input("Enter email for the final Report", key='email', placeholder="abc@def.com")

            if (not email):
                disabled = False
            else:
                disabled = not self.is_valid_email(email)
            
            if st.button("Start Analysis", disabled=disabled):
                st.session_state.generating = True

    def authenticate(self):
        
        dir = os.path.dirname(__file__)
        config_path = os.path.join(dir, "config/authentication.yaml")
    
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)
        print(config)
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        authenticator.login(location="main")
        
        if st.session_state['authentication_status']:
            authenticator.logout(location="sidebar")
            return True
        elif st.session_state['authentication_status'] is False:
            st.error('Username/password is incorrect')
            return False
        elif st.session_state['authentication_status'] is None:
            st.warning('Please enter your username and password')
            return False
    
    def render(self):
        st.set_page_config(page_title="Ramus", page_icon="👋")
        
        if self.authenticate():
            if "company" not in st.session_state:
                st.session_state.company = ""
                
            if "final_report" not in st.session_state:
                st.session_state.final_report = ""
                
            if "generating" not in st.session_state:
                st.session_state.generating = ""
            st.write("# Welcome to Ramus Corp")
            st.markdown(
                f"""
                ## Members
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

    def send_email(self, markdown_text: str, company: str, email: str):
        load_dotenv()
        
        if email and email != "":
            receiver = email
        else:
            receiver = os.getenv('EMAIL_RECEIVER')

        sender = os.getenv('GMAIL_SENDER')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp = smtplib.SMTP(smtp_server, 587)
        smtp.starttls()
        smtp.login(os.getenv('GMAIL_SENDER'), os.getenv('GMAIL_PASSWORD'))
        
        multipart_msg = MIMEMultipart("alternative")
        multipart_msg["Subject"] = f"{company} Stock Analysis Report"
        multipart_msg["From"] = sender
        multipart_msg["To"] = receiver

        html = markdown.markdown(markdown_text)
        part1 = MIMEText(markdown_text, "plain")
        part2 = MIMEText(html, "html")
        multipart_msg.attach(part1)
        multipart_msg.attach(part2)
        
        script_dir = os.path.dirname(__file__)
        financial_report_path = os.path.join(script_dir, "reports/financial_report.md")
        with open(financial_report_path, "r", encoding='utf-8') as f:
            multipart_msg.attach(MIMEApplication(f.read(), Name="financial_report.md"))

        technical_report_path = os.path.join(script_dir, "reports/technical_report.md")
        with open(technical_report_path, "r", encoding='utf-8') as f:
            multipart_msg.attach(MIMEApplication(f.read(), Name="technical_report.md"))

        smtp.sendmail(sender, receiver, multipart_msg.as_string())
        smtp.quit()
    
if __name__ == "__main__":
    StockReportGenUI().render()