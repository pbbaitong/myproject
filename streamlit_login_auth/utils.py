import streamlit as st
import mysql.connector

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])
conn = init_connection()

def register_new_usr(firstname_sign_up: str, lastname_sign_up: str, tel_sign_up: str, password_sign_up: str, role_sign_up) -> None:
    # Save the infoamation of the new user in the database
    mycursor = conn.cursor()
    if role_sign_up == 'คนทั่วไป':
        mycursor.execute("INSERT INTO general (general_firstname, general_lastname, general_tel, general_password) VALUES (%s, %s, %s, %s)", (firstname_sign_up, lastname_sign_up, tel_sign_up, password_sign_up))
    else:
        mycursor.execute("INSERT INTO doctor (doctor_firstname, doctor_lastname, doctor_tel, doctor_password) VALUES (%s, %s, %s, %s)", (firstname_sign_up, lastname_sign_up, tel_sign_up, password_sign_up))
    conn.commit()

def non_empty_str_check(firstname_sign_up: str, lastname_sign_up: str):
    # Checks for non-empty strings
    if not firstname_sign_up:
        return False
    if not lastname_sign_up:
        return False
    return True

def check_unique_usr(firstname_sign_up: str, lastname_sign_up: str, role_sign_up):
    # Checks if the account already exists
    mycursor = conn.cursor(buffered=True)
    if role_sign_up == 'คนทั่วไป':
        mycursor.execute("SELECT * FROM general WHERE general_firstname = %s AND general_lastname = %s", (firstname_sign_up, lastname_sign_up))
        # mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM doctor WHERE doctor_firstname = %s AND doctor_lastname = %s", (firstname_sign_up, lastname_sign_up))
        # mycursor.fetchall()
    name_existed = mycursor.fetchone()
    conn.commit()
    if name_existed is not None:
        return False
    non_empty_check = non_empty_str_check(firstname_sign_up, lastname_sign_up)
    if non_empty_check == False:
        return None
    return True

def check_usr_role(firstname_login: str, lastname_login: str):
    # Find the role
    mycursor = conn.cursor(buffered=True)
    general = mycursor.execute("SELECT * FROM general WHERE general_firstname = %s AND general_lastname = %s", (firstname_login, lastname_login))
    general_existed = mycursor.fetchone()
    conn.commit()
    if general_existed is None:
        doctor = mycursor.execute("SELECT * FROM doctor WHERE doctor_firstname = %s AND doctor_lastname = %s", (firstname_login, lastname_login))
        doctor_existed = mycursor.fetchone()
        if doctor_existed is None:
            return False
        else:
            role_sign_up = 'แพทย์'
    else:
        role_sign_up = 'คนทั่วไป'
    return role_sign_up

def check_usr_pass(firstname_login: str, lastname_login: str, password_login: str, role_sign_up) -> bool:
    # Authenticates the name and password
    mycursor = conn.cursor(buffered=True)
    if role_sign_up == 'คนทั่วไป':
        general_password = mycursor.execute("SELECT general_password FROM general WHERE general_firstname = %s AND general_lastname = %s", (firstname_login, lastname_login))
        general_password_existed = mycursor.fetchone()
        if password_login == general_password_existed[0]:
            return True
    else:
        doctor_password = mycursor.execute("SELECT doctor_password FROM doctor WHERE doctor_firstname = %s AND doctor_lastname = %s", (firstname_login, lastname_login))
        doctor_password_existed = mycursor.fetchone()
        if password_login == doctor_password_existed[0]:
            return True
    return False
