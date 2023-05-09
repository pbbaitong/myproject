import streamlit as st
from streamlit_login_auth.widgets import __login__

__login__obj = __login__()
# LOGGED_IN = __login__obj.sign_up_widget()
LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")