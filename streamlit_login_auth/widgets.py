import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from streamlit_option_menu import option_menu

from .utils import register_new_usr
from .utils import check_unique_usr
from .utils import check_usr_role
from .utils import check_usr_pass


class __login__:
    # Builds the UI for the Login/ Sign Up page.
    
    def __init__(self):
        self.cookies = EncryptedCookieManager(
            prefix="streamlit_login_ui_yummy_cookies",
            password='9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b')
        
        if not self.cookies.ready():
            st.stop()
    
    def sign_up_widget(self) -> None:
        # Creates the sign-up widget and stores the user info in a database
        st.subheader('ลงทะเบียน')
        with st.form('Sign up form'):
            firstname_sign_up = st.text_input("ชื่อจริง *", placeholder = 'Please enter your firstname')
            lastname_sign_up = st.text_input("นามสกุล *", placeholder = 'Please enter your lastname')
            tel_sign_up = st.text_input("เบอร์โทรศัพท์ *", placeholder = 'Please enter your tel')
            password_sign_up = st.text_input("รหัสผ่าน *", placeholder = 'Create a strong password', type = 'password')
            
            role_sign_up = st.radio('บทบาทการเข้าใช้งาน', ['แพทย์', 'คนทั่วไป'], horizontal=True)
            
            sign_up_submit_button = st.form_submit_button(label = 'ลงทะเบียน')
            
            check_usr = check_unique_usr(firstname_sign_up, lastname_sign_up, role_sign_up)
            if sign_up_submit_button:
                if check_usr == False:
                    st.error("ชื่อผู้ใช้นี้เคยทำการลงทะเบียนไว้แล้ว!")
                elif check_usr == None:
                    st.error('กรุณากรอกข้อมูลให้ถูกต้อง!')
                elif check_usr == True:
                    register_new_usr(firstname_sign_up, lastname_sign_up, tel_sign_up, password_sign_up, role_sign_up)
                    st.success('ลงทะเบียนสำเร็จ!')
    
    def login_widget(self) -> None:
        # Creates the login widget, checks and sets cookies, authenticates the users
        # Checks if cookie exists
        st.subheader('เข้าสู่ระบบ')
        if st.session_state['LOGGED_IN'] == False:
            if st.session_state['LOGOUT_BUTTON_HIT'] == False:
                fetched_cookies = self.cookies
                if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                    if fetched_cookies['__streamlit_login_signup_ui_username__'] != '1c9a923f-fb21-4a91-b3f3-5f18e3f01182':
                        st.session_state['LOGGED_IN'] = True
        
        if st.session_state['LOGGED_IN'] == False:
            st.session_state['LOGOUT_BUTTON_HIT'] = False
            del_login = st.empty()
            with del_login.form("Login Form"):
                firstname = st.text_input("ชื่อจริง", placeholder = 'Your firstname')
                lastname = st.text_input("นามสกุล", placeholder = 'Your lastname')
                password = st.text_input("รหัสผ่าน", placeholder = 'Your password')
                
                login_submit_button = st.form_submit_button(label = 'เข้าสู่ระบบ')
                
                if login_submit_button:
                    role = check_usr_role(firstname, lastname)
                    
                    if role == False:
                        st.error("ไม่พบชื่อผู้ใช้นี้ในระบบ")
                    else:
                        authenticate_user_check = check_usr_pass(firstname, lastname, password, role)
                        if authenticate_user_check == False:
                            st.error("กรุณากรอกข้อมูลให้ถูกต้อง")
                        else:
                            st.session_state['LOGGED_IN'] = True
                            self.cookies['__streamlit_login_signup_ui_username__'] = firstname
                            self.cookies['__streamlit_login_signup_ui_lastname__'] = lastname
                            self.cookies['__streamlit_login_signup_ui_role__'] = role
                            self.cookies.save()
                            del_login.empty()
                            st.experimental_rerun()
    
    def get_name(self):
        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = self.cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                firstname = fetched_cookies['__streamlit_login_signup_ui_username__']
                if '__streamlit_login_signup_ui_lastname__' in fetched_cookies.keys():
                    lastname = fetched_cookies['__streamlit_login_signup_ui_lastname__']
                    if '__streamlit_login_signup_ui_role__' in fetched_cookies.keys():
                        role = fetched_cookies['__streamlit_login_signup_ui_role__']
                        return firstname, lastname, role
                
    def logout_widget(self):
        # Creates the logout widget in the sidebar only if the user is logged in
        if st.session_state['LOGGED_IN'] == True:
            # del_logout = st.sidebar.empty()
            with st.sidebar:
                logout_button = st.button(label = 'ออกจากระบบ')
            
            if logout_button:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                self.cookies['__streamlit_login_signup_ui_username__'] = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                # del_logout.empty()
                st.experimental_rerun()
       
    def nav_sidebar(self):
        # Creates the side navigaton bar
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title = 'Navigation',
                options = ['เข้าสู่ระบบ', 'ลงทะเบียน'])
        return main_page_sidebar, selected_option
    
    
    def build_login_ui(self):
        # Brings everything together, calls important functions
        firstname = ''
        lastname = ''
        role = ''
        
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False
        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False
        
        main_page_sidebar, selected_option = self.nav_sidebar()
        
        if selected_option == 'เข้าสู่ระบบ':
            self.login_widget()
            
            
        if selected_option == 'ลงทะเบียน':
            self.sign_up_widget()
            
        if st.session_state['LOGGED_IN'] == True:
            main_page_sidebar.empty()
            firstname, lastname, role = self.get_name()
        
        self.logout_widget()
        
        return (st.session_state['LOGGED_IN'], firstname, lastname, role)