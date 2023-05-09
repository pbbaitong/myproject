import pickle
import joblib
import imblearn
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_login_auth.widgets import __login__

from datetime import datetime
import pandas as pd

# --- STREAMLIT EXTRAS ---


# --- IMPORT FOR FILTER ---
from function import *

# --- TEST MODAL ---
import hydralit_components as hc

hc.hydralit_experimental(True)

modal_code = """
<div>
<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
Hydralit Components Experimental Demo!
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
<div class="modal-dialog" role="document">
<div class="modal-content">
<div class="modal-header">
  <h5 class="modal-title" id="exampleModalLabel">Modal Popup Form!</h5>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>
<div class="modal-body">
  <div class="container">
<h2>Pure JS+HTML Form</h2>
<form class="form-horizontal" action="/">
<div class="form-group">
<label class="control-label col-sm-2" for="email">Email:</label>
<div class="col-sm-10">
  <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
</div>
</div>
<div class="form-group">
<label class="control-label col-sm-2" for="pwd">Password:</label>
<div class="col-sm-10">          
  <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pwd">
</div>
</div>
<div class="form-group">        
<div class="col-sm-offset-2 col-sm-10">
  <div class="checkbox">
    <label><input type="checkbox" name="remember"> Remember me</label>
  </div>
</div>
</div>
<div class="form-group">        
<div class="col-sm-offset-2 col-sm-10">
  <button type="submit" class="btn btn-default">Submit</button>
</div>
</div>
</form>
</div>
</div>
<div class="modal-footer">
  <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
  <button type="button" class="btn btn-primary">Save changes</button>
</div>
</div>
</div>
</div>
</div>
"""


st.markdown(modal_code, unsafe_allow_html=True)
query_param = st.experimental_get_query_params()

if query_param:
    st.write('We caputred these values from the experimental modal form using Javascript + HTML + Streamlit + Hydralit Components.')
    st.write(query_param)



import mysql.connector
# --- CONNECT DATABASE ---
# Initialize connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

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
                    options = ['Home', 'Profile'])
          
          role = role_login
          general_firstname = doctor_firstname = firstname_login
          general_lastname = doctor_lastname = lastname_login
          
          # --------------------------------------------------------------------------------------------------------------------
          if selected == 'Home':
               
               # role = st.radio('บทบาทการเข้าใช้งาน', ['แพทย์', 'คนทั่วไป'], horizontal=True)
               # '---'

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
                         
                         submit_button = st.form_submit_button(label= 'บันทึก')
                         
                         if submit_button:
                              st.success('บันทึกข้อมูลเรียบร้อยแล้ว')
                         
               analyze_button = st.button(label= 'วิเคราะห์ผล')
               
               if analyze_button:
                    # --------------------------------------------------------------------------------------------------------------------
                    # --- MACHINE LEARNING ---
                    gender, bmi, cong_label, ht, dlp, dm, heart, kidney, blood, breathe, others, fit_result = format_data(gender, weight, height, congenital, fit_result)
                    if role == 'คนทั่วไป':
                         prediction = normal_model.predict([[gender, weight, age, ht, dlp, dm, heart, kidney, blood, breathe, others, cong_label, fit_result]])
                         st.write(prediction[0])
                         risk_score = prediction[0]
                    else:
                         prediction = med_model.predict_proba([[gender, weight, age, ht, dm, heart, kidney, breathe, cong_label, fit_result, hct, hb, mch, mchc, rbc, wbc]])
                         st.write('prediction', prediction)
                         risk_score = prediction[0][1]
                         hyperplastic_pc = hyper_model.predict_proba([[gender, weight, age, ht, dm, heart, kidney, breathe, cong_label, fit_result, hct, hb, mch, mchc, rbc, wbc]])
                         st.write('hyperplastic_pc', hyperplastic_pc)
                         tubular_pc = tubular_model.predict_proba([[gender, weight, age, ht, dm, heart, kidney, breathe, cong_label, fit_result, hct, hb, mch, mchc, rbc, wbc]])
                         st.write('tubular_pc', tubular_pc)
                         
                    # --- SHOW RESULTS ---
                    # st.markdown(popup_html, unsafe_allow_html=True)
                    
                    # st.markdown(f'<style>{popup_css}</style>', unsafe_allow_html=True)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    # if risk_score >= 0.5:
                         # st.markdown('<h3 style="text-align: center; color: black;">ผลการวิเคราะห์</h3>', unsafe_allow_html=True)
                         # text_alignment = '<style> text-align: center; color: black;</style>'
                         # st.markdown(text_alignment, unsafe_allow_html=True)
                         # st.write('มีความเสี่ยงในการมีติ่งเนื้อในลำไส้ใหญ่สูง ร้อยละ %s' %(float(f'{prediction[0][1]:.2f}')*100))
                    # else:
                         # st.write('มีความเสี่ยงในการมีติ่งเนื้อในลำไส้ใหญ่ต่ำ')
                         
                    # if role == 'แพทย์':
                         
                         # st.write('ความเสี่ยงในการเกิดติ่งเนื้อชนิด hyperplastic คือ ร้อยละ %s' %float(f'{hyperplastic_pc[0][1]:.2f}'))
                         # st.write('ความเสี่ยงในการเกิดติ่งเนื้อชนิด tubular adenoma คือ ร้อยละ %s' %float(f'{tubular_pc[0][1]:.2f}'))
                         # '---'
                    
                    # --- SAVE TO GENERAL DATABASE ---
                    """general_name = run_query_val("SELECT COUNT(*) FROM general WHERE general_firstname = %s AND general_lastname = %s", (general_firstname, general_lastname))
                    
                    if f'{general_name[0][0]}' == '0':
                         mycursor = conn.cursor()
                         mycursor.execute("INSERT INTO general (general_firstname, general_lastname) VALUES (%s,%s)", (general_firstname, general_lastname))
                         conn.commit()
                    
                    # --- SAVE TO RESULT DATABASE ---
                    mycursor = conn.cursor()
                    if role == 'คนทั่วไป':
                         mycursor.execute("INSERT INTO result (result) VALUES (%s)", (float(prediction[0]),))
                    else:
                         mycursor.execute("INSERT INTO result (result, hyperplastic_pc, tubular_pc) VALUES (%s, %s, %s)", (float(f'{prediction[0][1]:.2f}'), float(f'{hyperplastic_pc[0][1]:.2f}'), float(f'{tubular_pc[0][1]:.2f}')))
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
                    conn.commit()"""

          
          else:
               st.subheader('Profile')

               def format_data_profile(gender, fit_test, result):
                    # --- GENDER ---
                    gender = 'ชาย' if gender == 1 else 'หญิง'
                    
                    # --- FIT TEST ---
                    fit_test = 'มี' if fit_test == 1 else 'ไม่มี'
                    
                    # --- RESULT ---
                    result = 'เสี่ยง' if result >= 0.5 else 'ไม่เสี่ยง'
                    
                    return gender, fit_test, result
               
               
               if role == 'แพทย์':
                    current_doctor_id = run_query_val("SELECT doctor_id FROM doctor WHERE doctor_firstname = %s AND doctor_lastname = %s", (doctor_firstname, doctor_lastname))
                    doctor_id = f'{current_doctor_id[0][0]}'
                    
                    df_general_name = pd.read_sql("SELECT * FROM general", con=conn)
                    df_general_name['general_full_name'] = df_general_name.general_firstname.str.cat(df_general_name.general_lastname, sep=' ')
                    name_options = df_general_name['general_full_name'].tolist()
                    name_options.append('ทั้งหมด')
                    
                    # col1, col2 = st.columns(2)
                    # with col1:
                         # selected_name = st.selectbox("Select a name", name_options)
                    selected_name = st.text_input('Search name')
                    

                    df_record_result = pd.read_sql("SELECT rec.record_id, gen.general_firstname, gen.general_lastname, rec.date, rec.gender, rec.age, rec.weight, rec.height, rec.congenital, rec.fit_test, rec.hb, rec.hct, rec.rbc, rec.mch, rec.mchc, rec.wbc, res.result, res.hyperplastic_pc, res.tubular_pc FROM general gen, record rec, result res WHERE rec.result_id = res.result_id and gen.general_id = rec.general_id and rec.doctor_id = %s"%(doctor_id), con=conn)
                    df_record_result['general_full_name'] = df_record_result.general_firstname.str.cat(df_record_result.general_lastname, sep=' ')
                    
                    # Search name
                    if selected_name:
                         df_record_result = df_record_result[df_record_result['general_full_name'].astype(str).str.contains(selected_name)]
                    df_record_result.drop(['general_full_name'], axis=1, inplace=True)
                    
                    # Format data
                    for i in range(len(df_record_result.index)):
                         gender, fit_test, result = format_data_profile(int(df_record_result.iloc[i].gender), int(df_record_result.iloc[i].fit_test), float(df_record_result.iloc[i].result))
                         fit_test = 'Positive' if fit_test == 'มี' else 'Negative'
                         df_record_result.iloc[[i],[4,9]] = gender, fit_test               
                         
                    # Rename columns
                    df_record_result.rename(columns={'record_id':'Record ID', 'general_firstname':'ชื่อจริง', 'general_lastname':'นามสกุล', 'date': 'วันที่ตรวจ', 'gender':'เพศ', 'age':'อายุ', 'weight':'น้ำหนัก', 'height':'ส่วนสูง', 'congenital':'โรคประจำตัว', 'fit_test':'Fit Test',
                                                     'hb':'HB', 'hct':'HCT', 'rbc':'RBC', 'mch':'MCH', 'mchc':'MCHC', 'wbc':'WBC', 'result':'ผลการวิเคราะห์', 'hyperplastic_pc':'% hyperplastic', 'tubular_pc':'% tubular'}, inplace=True)
                         
               else:
                    current_general_id = run_query_val("SELECT general_id FROM general WHERE general_firstname = %s AND general_lastname = %s", (general_firstname, general_lastname))
                    general_id = f'{current_general_id[0][0]}'
                    
                    col1, col2 = st.columns(2)
                              
                    df_record_result = pd.read_sql("SELECT rec.record_id, gen.general_firstname, gen.general_lastname, rec.date, rec.gender, rec.age, rec.weight, rec.height, rec.congenital, rec.fit_test, res.result FROM general gen, record rec, result res WHERE rec.result_id = res.result_id and gen.general_id = rec.general_id and gen.general_id = %s" %(general_id), con=conn)
                    
                    # Format data
                    for i in range(len(df_record_result.index)):
                         gender, fit_test, result = format_data_profile(int(df_record_result.iloc[i].gender), int(df_record_result.iloc[i].fit_test), float(df_record_result.iloc[i].result))
                         df_record_result.iloc[[i],[4,9,10]] = gender, fit_test, result
                    
                    # Rename columns
                    df_record_result.rename(columns={'record_id':'Record ID', 'general_firstname':'ชื่อจริง', 'general_lastname':'นามสกุล', 'date':'วันที่ตรวจ', 'gender':'เพศ', 'age':'อายุ', 'weight':'น้ำหนัก', 'height':'ส่วนสูง', 'congenital':'โรคประจำตัว', 'fit_test':'Fit Test', 'result':'ผลการวิเคราะห์'}, inplace=True)
               
               filtered_df = filter_dataframe(df_record_result)
               st.dataframe(filtered_df)

     if __name__ == '__main__':
          main(firstname_login, lastname_login, role_login)
