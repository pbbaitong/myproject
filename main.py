import pickle
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth

import mysql.connector
# --- CONNECT DATABASE ---
# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# --- USER AUTHENTICATION ---
names = ['Peter Parker', 'Rebecca Miller']
usernames = ['pparker', 'rmiller']

# Load hashed passwords
file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)
    
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'web_app', 'auth', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')

if authentication_status == None:
    st.warning('Please enter your username and password')

# --- MAIN PAGE ---
if authentication_status:
    def main():
     # st.title('Questionnaire')
     menu = ['Home', 'Profile']
     
     # --- SIDEBAR ---
     authenticator.logout('Logout', 'sidebar')
     st.sidebar.title(f'Welcome {name}')
     
     with st.sidebar:
          selected = option_menu(
               menu_title = 'Main Menu',
               options = ['Home', 'Profile'])
          
     # --------------------------------------------------------------------------------------------------------------------
     if selected == 'Home':
          
          role = st.radio('บทบาทการเข้าใช้งาน', ['แพทย์', 'คนทั่วไป'], horizontal=True)
          '---'

          if role == 'แพทย์':
               st.subheader('Patient\'s Name')
               with st.form(key = 'pateinform'):
                    col1, col2, col3 = st.columns([2,2,1])
                    
                    with col1:
                         firstname = st.text_input('ชื่อจริง')
                    
                    with col2:
                         lastname = st.text_input('นามสกุล')
                         
                    with col3:
                         submit_button = st.form_submit_button(label= 'บันทึก')
                    
                    if submit_button:
                         st.success('บันทึกข้อมูลเรียบร้อยแล้ว')
                         # rows = run_query("SELECT * from mytable;")
                         rows = run_query('INSERT INTO general (general_firstname, general_lastname) VALUES (%s, %s)' %(firstname, lastname))
                         for row in rows:
                              st.write(f"{row[0]} has a :{row[1]}:")
                    
          # Demographics
          st.subheader('Demographics')
          with st.form(key = 'demographicsform'):
               col1, col2 = st.columns(2)
               
               with col1:
                    sex = st.radio('เพศ', ['ชาย', 'หญิง'], horizontal=True)
               
               with col2:
                    age = st.number_input('อายุ (ปี)', min_value=0.00)
               
               col3, col4 = st.columns(2)
               
               with col3:
                    weight = st.number_input('น้ำหนัก (กิโลกรัม)', min_value=0.00)
                    
               with col4:
                    height = st.number_input('ส่วนสูง (เซนติเมตร)', min_value=0.00)
               
               if role == 'คนทั่วไป':
                    '---'
                    stool_blood = st.radio('ภายใน 30 วันที่ผ่านมา มีเลือดปนในอุจจาระหรือไม่', ['No', 'Yes'], horizontal=True)
                    '---'
               congenital = st.multiselect('โรคประจำตัว', ['UD', 'HT', 'DLP', 'DM', 'Heart', 'Kidney', 'Blood', 'Breathe', 'Other'])
               
               submit_button = st.form_submit_button(label= 'บันทึก')
               
               if submit_button:
                    st.success('บันทึกข้อมูลเรียบร้อยแล้ว')
          
          # --------------------------------------------------------------------------------------------------------------------
          # Medical Record
          if role == 'แพทย์':
               st.subheader('Medical Record')
               with st.form(key = 'medicalform'):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                         systolic = st.number_input('Systolic Blood Pressure', min_value=0.00)
                    
                    with col2:
                         diastolic = st.number_input('Diastolic Blood Pressure', min_value=0.00)
                    
                    '---'
                    fit_result = st.radio('FIT Result', ['Negative', 'Positive'], horizontal=True)
                    '---'
                    # st.write('Clinical Microscopy')
                    hb = st.number_input('Hemoglobin', min_value=0.00)
                    hct = st.number_input('Hematocrit', min_value=0.00)
                    rbc = st.number_input('Red Blood Cell', min_value=0.00)
                    mcv = st.number_input('Mean Cell Volumn', min_value=0.00)
                    mch = st.number_input('Mean Cell Hemoglobin', min_value=0.00)
                    mchc = st.number_input('Mean Cell Hemoglobin Concentration', min_value=0.00)
                    rdw = st.number_input('Red Blood Cell Distribution Width', min_value=0.00)
                    plt = st.number_input('Platelet', min_value=0.00)
                    wbc = st.number_input('White Blood Cell', min_value=0.00)
                    n = st.number_input('Neutrophil', min_value=0.00)
                    l = st.number_input('Lymphocyte', min_value=0.00)
                    m = st.number_input('Monocyte', min_value=0.00)
                    e = st.number_input('Eosinophil', min_value=0.00)
                    b =st.number_input('Basophil', min_value=0.00)
                    
                    submit_button = st.form_submit_button(label= 'บันทึก')
                    
                    if submit_button:
                         st.success('บันทึกข้อมูลเรียบร้อยแล้ว')
                    
          analyze_button = st.button(label= 'วิเคราะห์ผล')
          
     else:
          st.subheader('Profile')

    if __name__ == '__main__':
        main()