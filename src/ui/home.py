import streamlit as st
import sys
import pathlib
import markdown
import os
from dotenv import load_dotenv
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from assetmanagement.crew import Assetmanagement
from crewai.crew import CrewOutput
import assetmanagement.emoji as emoji
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
            if isinstance(st.session_state.final_report, CrewOutput):
                self.send_email(st.session_state.final_report.raw, st.session_state.company)
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.markdown("## Menu")
            company = st.text_input("Enter name of company", key='company', placeholder="Apple, Adobe, etc")
            if st.button("WORK FOR ME!!!"):
                print("Button Clicked")
                st.session_state.generating = True
    
    def render(self):
        st.set_page_config(page_title="Ramus", page_icon="👋")
        
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

    def send_email(self, markdown_text: str, company: str):
        load_dotenv()
        
        smtp_server = os.getenv('SMTP_SERVER')
        smtp = smtplib.SMTP(smtp_server, 587)
        smtp.starttls()
        smtp.login(os.getenv('GMAIL_SENDER'), os.getenv('GMAIL_PASSWORD'))
        
        sender = os.getenv('GMAIL_SENDER')
        receiver = os.getenv('EMAIL_RECEIVER')
        
        multipart_msg = MIMEMultipart("alternative")
        multipart_msg["Subject"] = f"{company} Stock Analysis Report"
        multipart_msg["From"] = sender
        multipart_msg["To"] = receiver

        html = markdown.markdown(markdown_text)
        part1 = MIMEText(markdown_text, "plain")
        part2 = MIMEText(html, "html")
        multipart_msg.attach(part1)
        multipart_msg.attach(part2)
        
        smtp.sendmail(sender, receiver, multipart_msg.as_string())
        smtp.quit()
    
if __name__ == "__main__":
    StockReportGenUI().render()