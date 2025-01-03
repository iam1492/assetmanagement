from pathlib import Path
from google.cloud import firestore
import streamlit as st
import os
import pandas as pd
from itables.streamlit import interactive_table
import markdown
class MyRecord():
    
    db = None
    stock_records = []
    
    def __init__(self):
        root_path = Path(__file__).parent.parent.parent
        firestore_key_path = os.path.join(root_path,"firestore-key.json" )
        self.db = firestore.Client.from_service_account_json(firestore_key_path)
        
    def get_records(self):
        records = []
        user_doc = self.db.collection("users").document(st.session_state['username'])
        for record in user_doc.collection('companies').stream():
            records.append(record.to_dict())
        return records
    
    def render(self):
        st.subheader("Stock Records", divider="gray")
        if st.session_state['authentication_status']:
            self.stock_records = self.get_records()
            
            if self.stock_records.__len__() == 0:
                st.warning("There is no record to show")
                return
            
            df = pd.DataFrame(self.stock_records)[['company', 'ticker', 'rating', 'created_at']]
            table = interactive_table(df, select=True, column_filter=True, column_sort=True, column_width=200)
            st.markdown("### Select a row to view the final result")
            
            if table and table['selected_rows']:
                st.write("\n")
                final_result = self.stock_records[table['selected_rows'][0]].get('final_result')
                st.html(final_result)
        else:
            st.error("Please login to view your records")

MyRecord().render()