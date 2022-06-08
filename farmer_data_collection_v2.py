import streamlit as st
import pyrebase as pb
import datetime as dt
from streamlit_option_menu import option_menu as stmenu
import pandas as pd


connection={ "apiKey": "AIzaSyBGkwggRgEHzOFpYUQIKBTd8Cj0K7V4PRc",
              "authDomain": "sachinsfirstproject.firebaseapp.com",
              "projectId": "sachinsfirstproject",
              "storageBucket": "sachinsfirstproject.appspot.com",
              "messagingSenderId": "52484278756",
              "appId": "1:52484278756:web:91fedb26e3c9bc58cf9ff1",
              "measurementId": "G-VWVW88RDNP",
              "databaseURL":"https://sachinsfirstproject-default-rtdb.firebaseio.com"}
app=pb.initialize_app(connection)
auth=app.auth()
db=app.database()

#st.session_state={"status":2}
#st.session_state={}

def reg_user():
    auth.create_user_with_email_and_password(st.session_state["reg_email"], st.session_state["reg_password"])
    #auth.send_password_reset_email(st.session_state["reg_email"])

def change_state_0():
    st.session_state={}

def change_state_1():
    try:
        auth.sign_in_with_email_and_password(st.session_state["email"] , st.session_state["password"])
        st.session_state["status"]=1
    except:
        st.error("Invalid credentials, please try again")
        #st.button("Retry", on_click=change_state_0)

def change_state_2():
    data1={
        "user":st.session_state["email"],
        "aadhar":st.session_state["aadhar"],
        "first_name":st.session_state["first_name"],
        "last_name":st.session_state["last_name"],
        "gender":st.session_state["gender"],
        "dob":str(st.session_state["dob"]),
        "father_name":st.session_state["father_name"],
        "address_door_no":st.session_state["addr_door_no"],
        "address_area":st.session_state["addr_area"],
        "address_city":st.session_state["addr_city"],
        "address_pin":st.session_state["addr_pin"],
        "address_dist":st.session_state["addr_dist"],
        "address_state":st.session_state["addr_state"],
        "address_mobile":st.session_state["addr_mobile"],
        }
    st.session_state["push1"]=db.push(data1)
    st.session_state["status"]=2


def change_state_3():
    data2={"accomodation_type":st.session_state["accomodation_type"],
        "ammenities_list":st.session_state["ammenities_list"],
        "assets_list":st.session_state["assets"],
        "hh_mem_count":st.session_state["hh_member_count"]
        }
    st.session_state["push2"]=db.child(st.session_state["push1"]["name"]).update(data2)
    if st.session_state["hh_member_count"]>1:
        df_temp_val=1
        while df_temp_val<st.session_state["hh_member_count"]:
            mem_label="Name of Member " + str(df_temp_val)
            dob_label="DOB of Member " + str(df_temp_val)
            gender_label="Gender of Member " + str(df_temp_val)
            aadhar_label="Aadhar of Member " + str(df_temp_val)
            id_label="2nd ID Type of Member " + str(df_temp_val)
            id_num_label="2nd ID Number of Member " + str(df_temp_val)
            data3={
                mem_label:st.session_state[mem_label],
                dob_label:str(st.session_state[dob_label]),
                gender_label:st.session_state[gender_label],
                aadhar_label:st.session_state[aadhar_label],
                id_label:st.session_state[id_label],
                id_num_label:st.session_state[id_num_label]
                }
            st.session_state["push3"]=db.child(st.session_state["push1"]["name"]).update(data3)
            df_temp_val=df_temp_val+1
    st.session_state["status"]=3

if 'status' not in st.session_state:
    st.session_state["status"]="login"

if st.session_state["status"]=="login":
    st.session_state["email"]=st.text_input(label="email:")
    st.session_state["password"]=st.text_input(label="password:")
    but=st.button("Login", on_click=change_state_1)

if st.session_state["email"] != "admin@gmail.com":
    if 'status' not in st.session_state:
        pass

    elif st.session_state["status"]==1:
        #try:
        st.success("Logged in Successfully")
        st.header("Welcome to Farmer Registration Screen")
        st.subheader("Farmer Personal Details")
        st.session_state["aadhar"]=st.text_input("Aadhar Number:")
        if len(st.session_state["aadhar"]) != 12:
            st.warning("Aadhar Length Should be of 12 digits")
        st.session_state["first_name"]=st.text_input("First Name:")
        st.session_state["last_name"]=last_name=st.text_input("Last Name:")
        st.session_state["gender"]=st.radio(label="Gender:", options=("Male", "Female"))
        st.session_state["dob"]=st.date_input(label="Date of Birth:",value=dt.date(1995, 1, 1), min_value=dt.date(1940, 1, 1), max_value=dt.date(2010, 1, 1))
        st.session_state["father_name"]=st.text_input("Father Name:")
        st.subheader("Farmer Address Details")
        st.session_state["addr_door_no"]=st.text_input("Door No:")
        st.session_state["addr_area"]=st.text_input("Area:")
        st.session_state["addr_city"]=st.text_input("City:")
        st.session_state["addr_pin"]=st.text_input("PIN:")
        if len(st.session_state["addr_pin"]) != 6:
            st.warning("PIN Code Length Should be of 6 digits")
        st.session_state["addr_dist"]=st.text_input("District:")
        st.session_state["addr_state"]=st.text_input("State:")
        st.session_state["addr_mobile"]=st.text_input("Mobile:")
        if len(st.session_state["addr_mobile"]) != 10:
            st.warning("Mobile Number Should be of 10 digits")
        st.button("Save", on_click=change_state_2)
        st.button("Logout", on_click=change_state_0)


        #except:
        #    st.error("Invalid credentials, please try again")
        #    but=st.button("Retry", on_click=change_state_0)

    elif st.session_state["status"]==2:
        st.success("Logged in Successfully")
        st.subheader("House Hold Level Details: ")
        st.session_state["accomodation_type"]=st.radio(label="Type of Accomodation:", options=("Owned", "Rented"))
        st.session_state["ammenities_list"]=st.multiselect(label="Select Available Basic Ammenities:", options=("Electricity", "Water", "Toilet", "Sewage", "LPG Connection"))
        blank_str=""
        for i in st.session_state["ammenities_list"]:
            blank_str=blank_str + str(i) + ", "
        st.session_state["ammenities_list"]=blank_str
        st.session_state["assets"]=st.multiselect(label="Select Available Assets:", options=("Land", "Livestocks", "vehicle", "Smartphone", "Other Electronic Items"))
        blank_str=""
        for i in st.session_state["assets"]:
            blank_str=blank_str + str(i) + ", "
        st.session_state["assets"]=blank_str
        st.subheader("Member Details:")
        st.session_state["hh_member_count"]= st.slider("Select Count of House Hold Members", 0, 10,)
        st.info("House Hold Member Includes Applicant, Spouse and Unmarried Child")
        if st.session_state["hh_member_count"]==0:
            st.warning("No Member Selected")
        elif st.session_state["hh_member_count"]==1:
            st.info("Applicant Details Already Captured")
            st.button("Submit", on_click=change_state_3)
        elif st.session_state["hh_member_count"]>1:
            temp_val=1
            while temp_val<st.session_state["hh_member_count"]:
                header="Details of HH Member " + str(temp_val)
                st.subheader(header)
                mem_label="Name of Member " + str(temp_val)
                dob_label="DOB of Member " + str(temp_val)
                gender_label="Gender of Member " + str(temp_val)
                aadhar_label="Aadhar of Member " + str(temp_val)
                id_label="2nd ID Type of Member " + str(temp_val)
                id_num_label="2nd ID Number of Member " + str(temp_val)
                st.session_state[mem_label]=st.text_input(label=mem_label)
                st.session_state[dob_label]=st.date_input(label=dob_label, value=dt.date(1995, 1, 1), min_value=dt.date(1940, 1, 1), max_value=dt.date(2010, 1, 1))
                st.session_state[gender_label]=st.radio(label=gender_label, options=("Male", "Female"))
                st.session_state[aadhar_label]=st.text_input(label=aadhar_label)
                st.session_state[id_label]=st.radio(label=id_label, options=("PAN", "DL", "VOTER ID", "RATION CARD"))
                st.session_state[id_num_label]=st.text_input(label=id_num_label)
                temp_val=temp_val+1
            st.session_state["HH_expense"]=st.text_input("Total House Hold Expenses:", value="Enter in INR")
            st.button("Submit", on_click=change_state_3)
            st.button("Logout", on_click=change_state_0)


    elif st.session_state["status"]==3:
        st.success("Details Captured Successfully")
        st.balloons()
        st.button("Register Another Farmer", on_click=change_state_1)
        st.button("Logout", on_click=change_state_0)


if st.session_state["email"] == "admin@gmail.com":

    if 'status' not in st.session_state:
        pass
    #auth.sign_in_with_email_and_password(st.session_state["email"] , st.session_state["password"])
    elif st.session_state["status"]==1:
        with st.sidebar:
            select=stmenu(
                menu_title="Admin Panel",
                options=["Home", "Register User", "Extract Report", "Logout"],
                menu_icon="card-checklist", #icon names from https://icons.getbootstrap.com/
                icons=["fan", "exclude", "file-bar-graph-fill", "exclude"], #icon names from https://icons.getbootstrap.com/
                default_index=0, #default selection 0 for 1st option, 1 for 2nd option and so on
                )
        if select=="Home":
            st.success("Logged in Successfully")
            st.header("Welcome to Admin Panel!!!!")
        elif select=="Register User":
            st.header("Work In Progress......")
            #st.session_state["reg_email"]=st.text_input("Enter Email ID to Register User: ")
            #st.session_state["reg_password"]="yrhedbhsudifjal"
            #st.button("Register", on_click=reg_user)

        elif select=="Logout":
            st.button("Logout", on_click=change_state_0)

        elif select=="Extract Report":
            new_list=[]
            get=db.get()
            for i in get:
                new_list.append(i.val())
            data_base=pd.DataFrame(new_list)
            cols=list(data_base.columns)
            cols.reverse()
            data_base=data_base[cols]
            st.dataframe(data_base)
            filename="report" + str(dt.datetime.now()) + ".csv"
            st.download_button(label="Download Report", data=data_base.to_csv(), file_name=filename)
