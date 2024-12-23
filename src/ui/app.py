import streamlit as st

import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent))
from assetmanagement.crew import Assetmanagement

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
            with st.container():
                st.markdown("### Final Report")
                st.markdown(st.session_state.final_report)
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
            """
            ### Ramus Company is the world best company
            * CEO - Ramus Jung
            * CSO - Sunny Park
            """
        )
        
        self.sidebar();
        self.report_generation();
    
if __name__ == "__main__":
    StockReportGenUI().render()
