import pickle
import joblib
import imblearn
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_login_auth.widgets import __login__

from datetime import datetime
import pandas as pd
# import base64
from PIL import Image

# --- IMPORT FOR DASHBOARD ---
import plotly.graph_objects as go
import plotly.express as px

# --- IMPORT FOR FILTER ---
from function import *
                              
import mysql.connector
# --- CONNECT DATABASE ---
# Initialize connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

# conn = init_connection()
conn = st.experimental_connection('db', type='sql')

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def run_query_val(query, val):
    with conn.cursor() as cur:
        cur.execute(query, val)
        return cur.fetchall()
   
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

st.set_page_config(layout='wide')

# --- USER AUTHENTICATION ---------------------------------------------------------------------------------------------------
__login__obj = __login__()
LOGGED_IN, firstname_login, lastname_login, role_login = __login__obj.build_login_ui()

# -- LOADING MODEL ---
normal_model = joblib.load('model/model_normal.sav')
med_model = joblib.load('model/model_med_check.sav')
hyper_model = joblib.load('model/model_med_hyper.sav')
tubular_model = joblib.load('model/model_med_tub.sav')


# --------------------------------------------------------------------------------------------------------------------
# --- MAIN PAGE ---
if LOGGED_IN == True:
     # --------------------------------------------------------------------------------------------------------------------
     # --- FORMAT DATA ---
     def format_data(gender, weight, height, congenital, fit_result):
          # --- GENDER ---
          gender = 1 if gender == 'ชาย' else 0
          
          # --- BMI ---     
          bmi = float(f'{weight/((height*0.01)**2):.2f}')
          
          # --- CONGENITAL ---
          cong_label = 0 if congenital == [] else 1
          
          # --- HT ---
          ht = 1 if 'ความดันโลหิต' in congenital else 0
          
          # --- DLP ---
          dlp = 1 if 'ไขมันในเลือดสูง' in congenital else 0
          
          # --- DM ---
          dm = 1 if 'เบาหวาน' in congenital else 0
          
          # --- HEART ---
          heart = 1 if 'ลิ้นหัวใจรั่ว โรคหัวใจ' in congenital else 0
          
          # --- KIDNEY ---
          kidney = 1 if 'ไตวาย ภาวะไตอักเสบ' in congenital else 0
          
          # --- BLOOD ---
          blood = 1 if 'โลหิตจาง มะเร็งเม็ดเลือด' in congenital else 0
          
          # --- BREATHE ---
          breathe = 1 if 'หอบหืด จมูกอักเสบ' in congenital else 0
          
          # --- OTHERS ---
          others = 1 if 'อื่น ๆ' in congenital else 0
          
          # --- FIT TEST ---
          fit_result = 1 if fit_result == 'Positive' else 0
          
          return (gender, bmi, cong_label, ht, dlp, dm, heart, kidney, blood, breathe, others, fit_result)
     
     # --------------------------------------------------------------------------------------------------------------------
     # --- MAIN PAGE ---
     def main(firstname_login, lastname_login, role_login):
          # --- SIDEBAR ---
          # authenticator.logout('Logout', 'sidebar')
          # st.sidebar.title(f'Welcome {name}')
          
          
          with st.sidebar:
               selected = option_menu(
                    menu_title = 'Main Menu',
                    options = ['แบบสอบถาม', 'ประวัติการตรวจ'])
          
          role = role_login
          general_firstname = doctor_firstname = firstname_login
          general_lastname = doctor_lastname = lastname_login


          button_style = """
                    <style>
                    .stButton > button {
                         text-align: center;
                         
                         width: 130px;
                    }
                    </style>
                    """
          text_style = """
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Anuphan:wght@300&display=swap');
                    html, body, [class*="css"], .st-cn, [type*="number"], .st-eg, #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 > div:nth-child(1) > div > div:nth-child(21) > div:nth-child(1) > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v4 > div:nth-child(2) > div:nth-child(1) > div > div > div > div > div > div.st-be.st-ef.st-eo.st-ep.st-eq.st-b3.st-cm.st-fe.st-bf.st-cd.st-ce.st-cf.st-cg, #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 > div:nth-child(1) > div > div:nth-child(23) > div:nth-child(1) > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v4 > div:nth-child(2) > div:nth-child(1) > div > div > div > div > div > div.st-be.st-ee.st-en.st-eo.st-ep.st-b3.st-cm.st-fd.st-bf.st-cd.st-ce.st-cf.st-cg {
                         font-family: 'Anuphan', sans-serif;
                         color: #091747;
                    }
                    </style>
                    """
          multiselect_style = """
          <style>
                    @import url('https://fonts.googleapis.com/css2?family=Anuphan:wght@300&display=swap');
                    .st-fn, .st-gn, .st-ho, .st-cn, .st-dt{
                         font-family: 'Anuphan', sans-serif;
                         color: #ffffff;
                    }
                    </style>
                    """
                    
          dataframe_style = """
          <style>
                    @import url('https://fonts.googleapis.com/css2?family=Anuphan:wght@300&display=swap');
                    .dataframe td {
                         font-family: 'Anuphan', sans-serif;
                         color: #ffffff;
                    } 
                    </style>
          
          """

          st.markdown(button_style, unsafe_allow_html=True)
          st.markdown(text_style, unsafe_allow_html=True)
          st.markdown(multiselect_style, unsafe_allow_html=True)
          st.markdown(dataframe_style, unsafe_allow_html=True)
          
          reduce_header_height_style = """
                    <style>
                        .appview-container .main .block-container {padding-top: 5rem;}
                    </style>
                    """
          st.markdown(reduce_header_height_style, unsafe_allow_html=True)
          
          show_header()
          
          
          # --------------------------------------------------------------------------------------------------------------------
          if selected == 'แบบสอบถาม':
               # role = st.radio('บทบาทการเข้าใช้งาน', ['แพทย์', 'คนทั่วไป'], horizontal=True)
               # '---'
               
               col1, col2, col3 = st.columns([1,2,1])
               with col2:

                    if role == 'แพทย์':
                         # doctor_firstname = firstname_login
                         # doctor_lastname = lastname_login
                         
                         st.subheader('Patient\'s Name')
                         with st.form(key = 'pateinform'):
                              col1, col2, col3 = st.columns([2,2,1])
                              # col1, col2 = st.columns([2,1])
                              
                              with col1:
                                   # df_general_name = pd.read_sql("SELECT general_firstname, general_lastname FROM general", con=conn)
                                   # df_general_name['general_full_name'] = df_general_name.general_firstname.str.cat(df_general_name.general_lastname, sep=' ')
                                   # name_list = df_general_name['general_full_name'].tolist()
                                   # selected_patient_name = st.selectbox('ชื่อจริง', name_list)
                                   # st.write(type(selected_firstname))
                                   # general_fullname = selected_patient_name.split(' ', 1)
                                   # general_firstname = general_fullname[0]
                                   # general_lastname = general_fullname[1]
                                   # st.write(general_firstname)
                                   # st.write(general_lastname)

                                   general_firstname = st.text_input('ชื่อจริง')
                              
                              with col2:
                                   general_lastname = st.text_input('นามสกุล')
                                   
                              with col3:
                                   ' '
                                   ' '
                                   submit_button = st.form_submit_button(label= 'บันทึก')
                              
                              if submit_button:
                                   st.success('บันทึกข้อมูลเรียบร้อยแล้ว')

                    # --------------------------------------------------------------------------------------------------------------------
                    # --- DEMOGRAPHICS ---
                    placeholder3 = st.empty()
                    
                    st.subheader('Demographics')
                    with st.form(key = 'demographicsform'):
                         col1, col2 = st.columns(2)
                         
                         with col1:
                              gender = st.radio('เพศ', ['ชาย', 'หญิง'], horizontal=True)
                         
                         with col2:
                              age = st.number_input('อายุ (ปี)', min_value=0.00)
                         
                         col3, col4 = st.columns(2)
                         
                         with col3:
                              weight = st.number_input('น้ำหนัก (กิโลกรัม)', min_value=0.00)
                              
                         with col4:
                              height = st.number_input('ส่วนสูง (เซนติเมตร)', min_value=0.00)
                         
                         if role == 'คนทั่วไป':
                              '---'
                              fit_result = st.radio('ภายใน 30 วันที่ผ่านมา มีเลือดปนในอุจจาระหรือไม่', ['ไม่มี', 'มี'], horizontal=True)
                              '---'
                         congenital = st.multiselect('โรคประจำตัว', ['ความดันโลหิต', 'ไขมันในเลือดสูง', 'เบาหวาน', 'ลิ้นหัวใจรั่ว โรคหัวใจ', 'ไตวาย ภาวะไตอักเสบ', 'โลหิตจาง มะเร็งเม็ดเลือด', 'หอบหืด จมูกอักเสบ', 'อื่น ๆ'])
                         
                         col1, col2, col3, col4, col5 = st.columns(5)
                         with col3:
                              submit_button = st.form_submit_button(label= 'บันทึก')
                         
                         if submit_button:
                              st.success('บันทึกข้อมูลเรียบร้อยแล้ว')

                    # --------------------------------------------------------------------------------------------------------------------
                    # --- MEDICAL RECORD ---
                    if role == 'แพทย์':
                         st.subheader('Medical Record')
                         with st.form(key = 'medicalform'):
                              # col1, col2 = st.columns(2)
                              
                              # with col1:
                                   # systolic = st.number_input('Systolic Blood Pressure', min_value=0.00)
                              
                              # with col2:
                                   # diastolic = st.number_input('Diastolic Blood Pressure', min_value=0.00)
                              
                              # '---'
                              fit_result = st.radio('FIT Result', ['Negative', 'Positive'], horizontal=True)
                              '---'
                              # st.write('Clinical Microscopy')
                              hb = st.number_input('Hemoglobin', min_value=0.00)
                              hct = st.number_input('Hematocrit', min_value=0.00)
                              rbc = st.number_input('Red Blood Cell', min_value=0.00)
                              # mcv = st.number_input('Mean Cell Volumn', min_value=0.00)
                              mch = st.number_input('Mean Cell Hemoglobin', min_value=0.00)
                              mchc = st.number_input('Mean Cell Hemoglobin Concentration', min_value=0.00)
                              # rdw = st.number_input('Red Blood Cell Distribution Width', min_value=0.00)
                              # plt = st.number_input('Platelet', min_value=0.00)
                              wbc = st.number_input('White Blood Cell', min_value=0.00)
                              # n = st.number_input('Neutrophil', min_value=0.00)
                              # l = st.number_input('Lymphocyte', min_value=0.00)
                              # m = st.number_input('Monocyte', min_value=0.00)
                              # e = st.number_input('Eosinophil', min_value=0.00)
                              # b =st.number_input('Basophil', min_value=0.00)
                              
                              col1, col2, col3, col4, col5 = st.columns(5)
                              with col3:
                                   submit_button = st.form_submit_button(label= 'บันทึก')
                              
                              if submit_button:
                                   st.success('บันทึกข้อมูลเรียบร้อยแล้ว')
                    
                    placeholder = st.empty()
                    
                    col6,col7 = st.columns(2)
                    with col7:
                         analyze_button = placeholder.button(label= 'วิเคราะห์ผล')
                    
                    if analyze_button:
                         # --------------------------------------------------------------------------------------------------------------------
                         # --- MACHINE LEARNING ---
                         gender, bmi, cong_label, ht, dlp, dm, heart, kidney, blood, breathe, others, fit_result = format_data(gender, weight, height, congenital, fit_result)
                         if role == 'คนทั่วไป':
                              prediction = normal_model.predict([[gender, weight, age, ht, dlp, dm, heart, kidney, blood, breathe, others, cong_label, fit_result]])
                              # st.write(prediction[0])
                              risk_score = float(f'{prediction[0]*100:.2f}')
                         else:
                              prediction = med_model.predict_proba([[gender, weight, age, ht, dm, heart, kidney, breathe, cong_label, fit_result, hct, hb, mch, mchc, rbc, wbc]])
                              # st.write('prediction', prediction)
                              risk_score = float(f'{prediction[0][1]*100:.2f}')
                              hyperplastic_pc = hyper_model.predict_proba([[gender, weight, age, ht, dm, heart, kidney, breathe, cong_label, fit_result, hct, hb, mch, mchc, rbc, wbc]])
                              # st.write('hyperplastic_pc', hyperplastic_pc)
                              hyperplastic_pc_score = float(f'{hyperplastic_pc[0][1]*100:.2f}')
                              tubular_pc = tubular_model.predict_proba([[gender, weight, age, ht, dm, heart, kidney, breathe, cong_label, fit_result, hct, hb, mch, mchc, rbc, wbc]])
                              # st.write('tubular_pc', tubular_pc)
                              tubular_pc_score = float(f'{tubular_pc[0][1]*100:.2f}')
                              
                         # --- SHOW RESULTS ---
                         placeholder.empty()
                         
                         st.subheader('Result')
                         with st.form(key = 'resultform'):
                              # st.write('REsulttttt')
                              if role == 'แพทย์':
                                   if hyperplastic_pc_score >= tubular_pc_score:
                                        ' '
                                        ' '
                                        html_string = f'''
                                                  <h5>มีความเสี่ยงในการมีติ่งเนื้อในลำไส้ใหญ่ {risk_score}%</h5>
                                                  <p>โดยที่มีโอกาสในการเกิดติ่งเนื้อแต่ละชนิด ดังนี้</p>
                                                  <p>Hyperplastic {hyperplastic_pc_score}%</p>
                                                  <p>Tubular Adenoma {tubular_pc_score}%</p>
                                                  '''
                                   else:
                                        ' '
                                        ' '
                                        html_string = f'''
                                                  <h5>มีความเสี่ยงในการมีติ่งเนื้อในลำไส้ใหญ่ {risk_score}%</h5>
                                                  <p>โดยที่มีโอกาสในการเกิดติ่งเนื้อแต่ละชนิด ดังนี้</p>
                                                  <p>Hyperplastic {hyperplastic_pc_score}%</p>
                                                  <p>Tubular Adenoma {tubular_pc_score}%</p>
                                                  '''
                                        # focus = st.error('Tubular Adenoma %s'%tubular_pc_score)
                                   css_string = '''
                                             <style>
                                             h5 {
                                                  text-align: center;
                                                  font-weight: bold;
                                             }
                                             p {
                                                  text-align: center;
                                             }
                                             </style>
                                             '''
                              else:
                                   if risk_score < 50:
                                        ' '
                                        ' '
                                        html_string = '''
                                                  <h5>มีความเสี่ยงในการมีติ่งเนื้อในลำไส้ใหญ่ต่ำ</h5>
                                                  '''
                                        css_string = '''
                                                  <style>
                                                  h5 {
                                                       text-align: center;
                                                       color: green;
                                                  }
                                                  </style>
                                                  '''
                                   else:
                                        ' '
                                        ' '
                                        html_string = '''
                                                  <h5>มีความเสี่ยงในการมีติ่งเนื้อในลำไส้ใหญ่สูง</h5>
                                                  '''
                                        css_string = '''
                                                  <style>
                                                  h5 {
                                                       text-align: center;
                                                       color: red;
                                                  }
                                                  </style>
                                                  '''
                              st.markdown(html_string, unsafe_allow_html=True)
                              st.markdown(css_string, unsafe_allow_html=True)
                              
                              
                              
                              col1, col2, col3, col4, col5 = st.columns(5)
                              with col3:
                                   reload_button = st.form_submit_button(label= 'กลับไปที่หน้าหลัก')
                              
                              if reload_button:
                                   
                                   st.experimental_memo.clear()
                              
                         
                         # --- SAVE TO GENERAL DATABASE ---
                         general_name = run_query_val("SELECT COUNT(*) FROM general WHERE general_firstname = %s AND general_lastname = %s", (general_firstname, general_lastname))
                         
                         if f'{general_name[0][0]}' == '0':
                              mycursor = conn.cursor()
                              mycursor.execute("INSERT INTO general (general_firstname, general_lastname) VALUES (%s,%s)", (general_firstname, general_lastname))
                              conn.commit()
                         
                         # --- SAVE TO RESULT DATABASE ---
                         mycursor = conn.cursor()
                         if role == 'คนทั่วไป':
                              mycursor.execute("INSERT INTO result (result) VALUES (%s)", (risk_score,))
                         else:
                              mycursor.execute("INSERT INTO result (result, hyperplastic_pc, tubular_pc) VALUES (%s, %s, %s)", (risk_score, hyperplastic_pc_score, tubular_pc_score))
                         conn.commit()
                         
                         # --- SAVE TO RECORD DATABASE ---
                         result_id = mycursor.lastrowid
                         current_general_id = run_query_val("SELECT general_id FROM general WHERE general_firstname = %s AND general_lastname = %s", (general_firstname, general_lastname))
                         general_id = f'{current_general_id[0][0]}'
                         if role == 'แพทย์':
                              current_doctor_id = run_query_val("SELECT doctor_id FROM doctor WHERE doctor_firstname = %s AND doctor_lastname = %s", (doctor_firstname, doctor_lastname))
                              doctor_id = f'{current_doctor_id[0][0]}'
                         
                         mycursor = conn.cursor()
                         if role == 'คนทั่วไป':
                              mycursor.execute("INSERT INTO record (general_id, date, gender, age, weight, height, congenital, fit_test, result_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                                             (general_id,  datetime.now(), gender, age, weight, height, str(congenital), fit_result, result_id))
                         else:
                              mycursor.execute("INSERT INTO record (general_id, doctor_id, date, gender, age, weight, height, congenital, fit_test, hb, hct, rbc, mch, mchc, wbc, result_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                                             (general_id, doctor_id, datetime.now(), gender, age, weight, height, str(congenital), fit_result, hb, hct, rbc, mch, mchc, wbc, result_id))
                         conn.commit()
          
          else:
               doctor_image = Image.open('images/doctor.jpg')
               general_image = Image.open('images/general.jpg')
               
               col1, col2, col3 = st.columns([1,3,2])
               with col1:
                    if role == 'คนทั่วไป':
                         st.image(general_image, width=170)
                    else:
                         st.image(doctor_image, width=170)
                    
                    st.write('สวัสดีคุณ', doctor_firstname, doctor_lastname)
               with col2:
                    st.subheader('ประวัติการตรวจ')

                    def format_data_profile(gender, fit_test, result, congenital):
                         # --- GENDER ---
                         gender = 'ชาย' if gender == 1 else 'หญิง'
                         
                         # --- FIT TEST ---
                         fit_test = 'มี' if fit_test == 1 else 'ไม่มี'
                         
                         # --- RESULT ---
                         result = 'เสี่ยง' if result >= 50 else 'ไม่เสี่ยง'
                         
                         # --- HT ---
                         ht = 1 if 'ความดันโลหิต' in congenital else 0
                         
                         # --- DLP ---
                         dlp = 1 if 'ไขมันในเลือดสูง' in congenital else 0
                         
                         # --- DM ---
                         dm = 1 if 'เบาหวาน' in congenital else 0
                         
                         # --- HEART ---
                         heart = 1 if 'ลิ้นหัวใจรั่ว โรคหัวใจ' in congenital else 0
                         
                         # --- KIDNEY ---
                         kidney = 1 if 'ไตวาย ภาวะไตอักเสบ' in congenital else 0
                         
                         # --- BLOOD ---
                         blood = 1 if 'โลหิตจาง มะเร็งเม็ดเลือด' in congenital else 0
                         
                         # --- BREATHE ---
                         breathe = 1 if 'หอบหืด จมูกอักเสบ' in congenital else 0
                         
                         # --- OTHERS ---
                         others = 1 if 'อื่น ๆ' in congenital else 0
    
                         
                         
                         return gender, fit_test, result, ht, dlp, dm, heart, kidney, blood, breathe, others
                    
                    
                    if role == 'แพทย์':
                         current_doctor_id = run_query_val("SELECT doctor_id FROM doctor WHERE doctor_firstname = %s AND doctor_lastname = %s", (doctor_firstname, doctor_lastname))
                         doctor_id = f'{current_doctor_id[0][0]}'
                         
                         df_general_name = pd.read_sql("SELECT * FROM general", con=conn)
                         df_general_name['general_full_name'] = df_general_name.general_firstname.str.cat(df_general_name.general_lastname, sep=' ')
                         name_options = df_general_name['general_full_name'].tolist()
                         name_options.append('ทั้งหมด')
                         
                         col1, col2 = st.columns([4,1])
                         with col1:
                              selected_name = st.text_input('ค้นหา', placeholder = 'ตัวอย่าง "สมชาย"')
                         
                         

                         df_record_result = pd.read_sql("SELECT rec.record_id, gen.general_firstname, gen.general_lastname, rec.date, rec.gender, rec.age, rec.weight, rec.height, rec.congenital, rec.fit_test, rec.hb, rec.hct, rec.rbc, rec.mch, rec.mchc, rec.wbc, res.result, res.hyperplastic_pc, res.tubular_pc FROM general gen, record rec, result res WHERE rec.result_id = res.result_id and gen.general_id = rec.general_id and rec.doctor_id = %s"%(doctor_id), con=conn)
                         df_record_result['general_full_name'] = df_record_result.general_firstname.str.cat(df_record_result.general_lastname, sep=' ')
                         
                         # Search name
                         if selected_name:
                              df_record_result = df_record_result[df_record_result['general_full_name'].astype(str).str.contains(selected_name)]
                         df_record_result.drop(['general_full_name'], axis=1, inplace=True)
                         
                         # Format data
                         for i in range(len(df_record_result.index)):
                              gender, fit_test, result, ht, dlp, dm, heart, kidney, blood, breathe, others = format_data_profile(int(df_record_result.iloc[i].gender), int(df_record_result.iloc[i].fit_test), float(df_record_result.iloc[i].result), df_record_result.iloc[i].congenital)
                              fit_test = 'Positive' if fit_test == 'มี' else 'Negative'
                              df_record_result.loc[df_record_result.index[i], 'ht'] = ht
                              df_record_result.loc[df_record_result.index[i], 'dlp'] = dlp
                              df_record_result.loc[df_record_result.index[i], 'dm'] = dm
                              df_record_result.loc[df_record_result.index[i], 'heart'] = heart
                              df_record_result.loc[df_record_result.index[i], 'kidney'] = kidney
                              df_record_result.loc[df_record_result.index[i], 'blood'] = blood
                              df_record_result.loc[df_record_result.index[i], 'breathe'] = breathe
                              df_record_result.loc[df_record_result.index[i], 'others'] = others
                              if ht + dlp + dm + heart + kidney + blood + breathe + others >= 1:
                                   df_record_result.loc[df_record_result.index[i], 'cong'] = 'มีโรคประจำตัว'
                              else:
                                   df_record_result.loc[df_record_result.index[i], 'cong'] = 'ไม่มีโรคประจำตัว'

                              df_record_result.iloc[[i],[4,9]] = gender, fit_test
                              
                              # ht, dlp, dm, heart, kidney, blood, breathe, others = format_congenital(df_record_result.iloc[i].congenital)
                              # st.write(ht)
                              # df_record_result['HT'] = 2
                              # df_record_result['DLP'] = 2
                              # df_record_result.iloc[[0], [1]] = ht
                              
                              # df_record_result.iloc[[i], []] = ht
                              
                         # Rename columns
                         df_record_result.rename(columns={'record_id':'Record ID', 'general_firstname':'ชื่อจริง', 'general_lastname':'นามสกุล', 'date': 'วันที่ตรวจ', 'gender':'เพศ', 'age':'อายุ', 'weight':'น้ำหนัก', 'height':'ส่วนสูง', 'congenital':'โรคประจำตัว', 'fit_test':'Fit Test',
                                                       'hb':'HB', 'hct':'HCT', 'rbc':'RBC', 'mch':'MCH', 'mchc':'MCHC', 'wbc':'WBC', 'result':'% ผลการวิเคราะห์', 'hyperplastic_pc':'% hyperplastic', 'tubular_pc':'% tubular'}, inplace=True)
                         
                         filtered_df = filter_dataframe(df_record_result)
                         filtered_df_show = filtered_df.drop(['ht', 'dlp', 'dm', 'heart', 'kidney', 'blood', 'breathe', 'others', 'cong'], axis=1)
                         
                    else:
                         current_general_id = run_query_val("SELECT general_id FROM general WHERE general_firstname = %s AND general_lastname = %s", (general_firstname, general_lastname))
                         general_id = f'{current_general_id[0][0]}'
                         
                         col1, col2 = st.columns(2)
                         
                         # df_record_result_no_doctor = pd.read_sql("SELECT rec.record_id, gen.general_firstname, gen.general_lastname, rec.date, rec.gender, rec.age, rec.weight, rec.height, rec.congenital, rec.fit_test, res.result FROM general gen, doctor doc, record rec, result res WHERE rec.result_id = res.result_id and gen.general_id = rec.general_id and rec.doctor_id = %s and gen.general_id = %s" %('1000', general_id), con=conn)
                         df_record_result = pd.read_sql("SELECT rec.record_id, gen.general_firstname, gen.general_lastname, rec.date, rec.gender, rec.age, rec.weight, rec.height, rec.congenital, rec.fit_test, res.result, doc.doctor_firstname, doc.doctor_lastname FROM general gen, doctor doc, record rec, result res WHERE rec.result_id = res.result_id and gen.general_id = rec.general_id and rec.doctor_id = doc.doctor_id and gen.general_id = %s" %(general_id), con=conn)
                         
                         # df_record_result_no_doctor.drop_duplicates()
                         # df_record_result_no_doctor
                         # Format data
                         for i in range(len(df_record_result.index)):
                              gender, fit_test, result, ht, dlp, dm, heart, kidney, blood, breathe, others = format_data_profile(int(df_record_result.iloc[i].gender), int(df_record_result.iloc[i].fit_test), float(df_record_result.iloc[i].result), df_record_result.iloc[i].congenital)
                              df_record_result.iloc[[i],[4,9,10]] = gender, fit_test, result
                         
                         df_record_result['doctor_full_name'] = df_record_result.doctor_firstname.str.cat(df_record_result.doctor_lastname, sep=' ')
                         # df = df.drop('column_name', axis=1)
                         df_record_result.drop(['doctor_firstname', 'doctor_lastname'], axis=1, inplace=True)
                         
                         # Rename columns
                         df_record_result.rename(columns={'record_id':'Record ID', 'general_firstname':'ชื่อจริง', 'general_lastname':'นามสกุล', 'date':'วันที่ตรวจ', 'gender':'เพศ', 'age':'อายุ', 'weight':'น้ำหนัก', 'height':'ส่วนสูง', 'congenital':'โรคประจำตัว', 'fit_test':'Fit Test', 'result':'ผลการวิเคราะห์', 'doctor_full_name':'แพทย์ผู้รับผิดชอบ'}, inplace=True)

                         filtered_df_show = filtered_df = filter_dataframe(df_record_result)
               ' '
               st.dataframe(filtered_df_show)
               
               
               
               # --- DASHBOARD ---
               ' '
               ' '
               st.markdown("""
                    <style>
                    div[data-testid="metric-container"] {
                    background-color: rgba(28, 131, 225, 0.1);
                    border: 1px solid rgba(28, 131, 225, 0.1);
                    padding: 5% 5% 5% 10%;
                    border-radius: 5px;
                    color: rgb(30, 103, 119);
                    overflow-wrap: break-word;
                    }

                    /* breakline for metric text         */
                    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
                    overflow-wrap: break-word;
                    white-space: break-spaces;
                    color: red;
                    }
                    </style>
                    """, unsafe_allow_html=True)
               
               if role == 'แพทย์':
                    col1, col2 = st.columns(2)
                    with col1:
                         ' '
                         ' '
                         ' '
                         ' '
                         ' '
                         
                         
                         
                         
                         col3, col4 = st.columns(2)
                         with col3:
                              # filtered_df_unique = filtered_df.drop_duplicates(subset=['ชื่อจริง', 'นามสกุล'])
                              # record_amount = str(filtered_df_unique.shape[0]) + ' คน'
                              # st.metric(label='จำนวนทั้งหมด', value=record_amount)
                              
                              record_amount = str(filtered_df.shape[0]) + ' records'
                              st.metric(label='จำนวนทั้งหมด', value=record_amount)
                              
                              polyp_amount = str((filtered_df['% ผลการวิเคราะห์'] >= 50).sum()) + ' records'
                              st.metric(label='มีความเสี่ยงสูง', value=polyp_amount)
                              
                              no_polyp_amount = str((filtered_df['% ผลการวิเคราะห์'] < 50).sum()) + ' records'
                              st.metric(label='มีความเสี่ยงตำ่', value=no_polyp_amount)
                         with col4:
                              result_labels = ['Hyperplastic', 'Tubular adenomas', 'มีความเสี่ยงตำ่']
                              hyperplastic_amount = (filtered_df['% hyperplastic'] > 50).sum()
                              tubular_amount = (filtered_df['% tubular'] > 50).sum()
                              no_polyp_amount = (filtered_df['% ผลการวิเคราะห์'] < 50).sum()
                              result_values = [hyperplastic_amount, tubular_amount, no_polyp_amount]
                              
                              result_fig = go.Figure(data=[go.Pie(labels=result_labels, values=result_values, textposition='outside', textinfo='percent+label')])
                              result_fig.update_layout(showlegend=False)
                              result_fig.update_layout(
                                             font=dict(
                                             family='Anuphan',
                                             size=13
                                             )                         
                                             )
                              result_fig.update_layout(margin=dict(l=50,t=70,b=140))
                              st.plotly_chart(result_fig, theme="streamlit", use_container_width=True)
                              
                              
                              
                         
                         
                         
                         
                    with col2:
                         ' '
                         ' '
                         ' '
                         ' '
                         ' '
                         ' '
                         
                         congenital_values = [filtered_df['ht'].sum(), filtered_df['dlp'].sum(), filtered_df['dm'].sum(), filtered_df['heart'].sum(), filtered_df['kidney'].sum(), filtered_df['blood'].sum(), filtered_df['breathe'].sum(), filtered_df['others'].sum()]
                         fig = go.Figure()
                         fig.add_trace(go.Bar(x=['HT', 'dlp', 'dm', 'heart', 'kidney', 'blood', 'breathe', 'others'], y=congenital_values))
                         # st.plotly_chart(fig, theme="streamlit")
                    
                         filtered_polyp_df = filtered_df[filtered_df['% ผลการวิเคราะห์'] >= 50]
                         # filtered_polyp_df
                         congenital_values = [filtered_polyp_df['ht'].sum(), filtered_polyp_df['dlp'].sum(), filtered_polyp_df['dm'].sum(), filtered_polyp_df['heart'].sum(), filtered_polyp_df['kidney'].sum(), filtered_polyp_df['blood'].sum(), filtered_polyp_df['breathe'].sum(), filtered_polyp_df['others'].sum()]
                         fig.add_trace(go.Bar(x=['HT', 'dlp', 'dm', 'heart', 'kidney', 'blood', 'breathe', 'others'], y=congenital_values))
                         # st.plotly_chart(fig, theme="streamlit")
                         
                         filtered_no_polyp_df = filtered_df[filtered_df['% ผลการวิเคราะห์'] < 50]
                         congenital_values = [filtered_no_polyp_df['ht'].sum(), filtered_no_polyp_df['dlp'].sum(), filtered_no_polyp_df['dm'].sum(), filtered_no_polyp_df['heart'].sum(), filtered_no_polyp_df['kidney'].sum(), filtered_no_polyp_df['blood'].sum(), filtered_no_polyp_df['breathe'].sum(), filtered_no_polyp_df['others'].sum()]
                         fig.add_trace(go.Bar(x=['HT', 'dlp', 'dm', 'heart', 'kidney', 'blood', 'breathe', 'others'], y=congenital_values))
                         
                         fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              ))
                         fig.update_layout(margin=dict(l=100))
                         
                         fig.update_layout(title={
                                   'text': 'กราฟแสดงความถี่จำนวนคนที่มีโรคประจำตัว',
                                   'font_family': 'Anuphan',
                                   'font_size':25,
                                   'font_color': '#091747',
                                   'y':0.95,
                                   'x':0.55,
                                   'xanchor': 'center',
                                   'yanchor': 'top'})
                         
                         st.plotly_chart(fig, theme="streamlit",  use_container_width=True)
                              
                              
                              
                              
                              
                    
                    col5, col6 = st.columns(2)
                    with col5:
                         col7, col8 = st.columns(2)
                         with col7:
                              ' '
                              ' '
                              st.subheader('การกระจายของข้อมูลฟีเจอร์และ')
                         with col8:
                              y_label = st.selectbox('เลือก', ['% ผลการวิเคราะห์', '% hyperplastic', '% tubular'])
                         
                         
                         tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(['อายุ', 'น้ำหนัก', 'ส่วนสูง', 'HB', 'HCT', 'RBC', 'MCH', 'MCHC', 'WBC'])
                         with tab1:
                              fig = px.scatter(filtered_df, x='อายุ', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab2:
                              fig = px.scatter(filtered_df, x='น้ำหนัก', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab3:
                              fig = px.scatter(filtered_df, x='ส่วนสูง', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab4:
                              fig = px.scatter(filtered_df, x='HB', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab5:
                              fig = px.scatter(filtered_df, x='HCT', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab6:
                              fig = px.scatter(filtered_df, x='RBC', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab7:
                              fig = px.scatter(filtered_df, x='MCH', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab8:
                              fig = px.scatter(filtered_df, x='MCHC', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                         with tab9:
                              fig = px.scatter(filtered_df, x='WBC', y=y_label, color='เพศ', size=[1]*filtered_df.shape[0])
                              fig.update_layout(legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              ),
                              font=dict(
                              family='Anuphan',
                              size=13
                              )                         
                              )
                              st.plotly_chart(fig, theme="streamlit", use_container_width=True)



                    with col6:
                         with st.container():
                              gender_fig = horizontal_chart(list(filtered_df['เพศ'].unique()), [[((filtered_df['เพศ']=='ชาย').sum()*100)/filtered_df.shape[0], ((filtered_df['เพศ']=='หญิง').sum()*100)/filtered_df.shape[0]]], ['เพศ'])
                              st.plotly_chart(gender_fig, use_container_width=True)

                         with st.container():
                              congenital_fig = horizontal_chart(list(filtered_df['cong'].unique()), [[((filtered_df['cong']=='มีโรคประจำตัว').sum()*100)/filtered_df.shape[0], ((filtered_df['cong']=='ไม่มีโรคประจำตัว').sum()*100)/filtered_df.shape[0]]], ['โรคประจำตัว'])
                              st.plotly_chart(congenital_fig, use_container_width=True)
                              
                         with st.container():
                              fit_fig = horizontal_chart(['Positive', 'Negative'], [[((filtered_df['Fit Test']=='Positive').sum()*100)/filtered_df.shape[0], ((filtered_df['Fit Test']=='Negative').sum()*100)/filtered_df.shape[0]]], ['Fit Test'])
                              st.plotly_chart(fit_fig, use_container_width=True)
                     
               else:
                    col1, col2 = st.columns([1,3])
                    with col1:
                         record_amount = str(filtered_df.shape[0]) + ' ครั้ง'
                         st.metric(label='ประวัติการตรวจ', value=record_amount)
                         
                         polyp_amount = str((filtered_df['ผลการวิเคราะห์'] == 'เสี่ยง').sum()) + ' ครั้ง'
                         st.metric(label='มีความเสี่ยงสูง', value=polyp_amount)
                         
                         no_polyp_amount = str((filtered_df['ผลการวิเคราะห์'] == 'ไม่เสี่ยง').sum()) + ' ครั้ง'
                         st.metric(label='มีความเสี่ยงตำ่', value=no_polyp_amount)
                          
                    with col2:
                         col3, col4 = st.columns([1,8])
                         # st.line_chart(filtered_df, x='วันที่ตรวจ', y='อายุ')
                         with col4:
                              line_chart = filtered_df.copy()
                              tab1, tab2, tab3 = st.tabs(['น้ำหนัก-ส่วนสูง', 'น้ำหนัก-วันที่ตรวจ', 'ส่วนสูง-วันที่ตรวจ'])
                              with tab1:
                                   age_fig = px.line(line_chart, x='น้ำหนัก', y='ส่วนสูง', markers=True)
                                   age_fig.update_layout(xaxis=dict(tickformat='%d-%m-%Y'))
                                   age_fig.update_layout(title={
                                        'text': 'กราฟแสดงความสัมพันธ์ระหว่างน้ำหนักและส่วนสูง',
                                        'font_family': 'Anuphan',
                                        'font_size':25,
                                        'font_color': '#091747',
                                        'y':0.95,
                                        'x':0.55,
                                        'xanchor': 'center',
                                        'yanchor': 'top'})
                                   age_fig.update_layout(
                                                  font=dict(
                                                  family='Anuphan',
                                                  size=13))
                                   age_fig.update_layout(margin=dict(l=50,t=70,b=140))
                                   
                                   st.plotly_chart(age_fig, use_container_width=True)
                              with tab2:
                                   weight_fig = px.line(line_chart, x='วันที่ตรวจ', y='น้ำหนัก', markers=True)
                                   weight_fig.update_layout(xaxis=dict(tickformat='%d-%m-%Y'))
                                   weight_fig.update_layout(title={
                                        'text': 'กราฟแสดงความสัมพันธ์ระหว่างน้ำหนักและส่วนสูง',
                                        'font_family': 'Anuphan',
                                        'font_size':25,
                                        'font_color': '#091747',
                                        'y':0.95,
                                        'x':0.55,
                                        'xanchor': 'center',
                                        'yanchor': 'top'})
                                   weight_fig.update_layout(
                                                  font=dict(
                                                  family='Anuphan',
                                                  size=13))
                                   weight_fig.update_layout(margin=dict(l=50,t=70,b=140))
                                   st.plotly_chart(weight_fig, use_container_width=True)
                              with tab3:
                                   height_fig = px.line(line_chart, x='วันที่ตรวจ', y='ส่วนสูง', markers=True)
                                   height_fig.update_layout(xaxis=dict(tickformat='%d-%m-%Y'))
                                   height_fig.update_layout(title={
                                        'text': 'กราฟแสดงความสัมพันธ์ระหว่างน้ำหนักและส่วนสูง',
                                        'font_family': 'Anuphan',
                                        'font_size':25,
                                        'font_color': '#091747',
                                        'y':0.95,
                                        'x':0.55,
                                        'xanchor': 'center',
                                        'yanchor': 'top'})
                                   height_fig.update_layout(
                                                  font=dict(
                                                  family='Anuphan',
                                                  size=13))
                                   height_fig.update_layout(margin=dict(l=50,t=70,b=140))
                                   st.plotly_chart(height_fig, use_container_width=True)
                    
                    
                    
                    
                    
                    
               

     if __name__ == '__main__':
          main(firstname_login, lastname_login, role_login)
