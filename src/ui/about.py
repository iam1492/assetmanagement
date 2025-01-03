import streamlit as st
import assetmanagement.emoji as emoji

if st.session_state['authentication_status']:
    st.subheader("Ramus Company Members", divider="gray")
    st.write(f"Welcome :blue[{st.session_state['username']}] :sunglasses:")
    st.markdown(
        f"""    
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