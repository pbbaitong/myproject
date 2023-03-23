import streamlit as st
from streamlit_option_menu import option_menu

def main():
     # st.title('Questionnaire')
     menu = ['Home', 'Profile']
     
     # Sidebar menu
     with st.sidebar:
          selected = option_menu(
               menu_title = 'Main Menu',
               options = ['Home', 'Profile', 'Sign out'])
     
     if selected == 'Home':
          
          st.subheader('Patient\'s Name')
          with st.form(key = 'pateinform'):
               col1, col2, col3 = st.columns([2,2,1])
               
               with col1:
                    firstname = st.text_input('First name')
               
               with col2:
                    lastname = st.text_input('Last name')
                    
               with col3:
                    submit_button = st.form_submit_button(label= 'Save')
               
               if submit_button:
                    st.success('The patient\'s information is saved.')
                    
          # Demographics
          st.subheader('Demographics')
          with st.form(key = 'demographicsform'):
               col1, col2 = st.columns(2)
               
               with col1:
                    sex = st.radio('Gender', ['Male', 'Female'], horizontal=True)
               
               with col2:
                    age = st.number_input('Age (years)', min_value=0.00)
               
               col3, col4 = st.columns(2)
               
               with col3:
                    weight = st.number_input('Weight (kg.)', min_value=0.00)
                    
               with col4:
                    height = st.number_input('Height (cm.)', min_value=0.00)
               
               '---'
               stool_blood = st.radio('During the past 30 days, did the patient has blood in the stool?', ['No', 'Yes'], horizontal=True)
               '---'
               congenital = st.multiselect('What is the patient\'s medical condition?', ['UD', 'HT', 'DLP', 'DM', 'Heart', 'Kidney', 'Blood', 'Breathe', 'Other'])
               
               submit_button = st.form_submit_button(label= 'Save')
               
               if submit_button:
                    st.success('The patient\'s information is saved.')
          
          # --------------------------------------------------------------------------------------------------------------------
          # Medical Record
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
               
               submit_button = st.form_submit_button(label= 'Save')
               
               if submit_button:
                    st.success('The patient\'s information is saved.')
                    
          analyze_button = st.button(label= 'Analyze')
          
     elif selected == 'Profile':
          st.subheader('Profile')
     else:
          st.subheader('Sign out')

if __name__ == '__main__':
     main()