import streamlit as st
from streamlit_option_menu import option_menu as stmenu
from PIL import Image

def change_state():
    st.session_state["status"]=2
def change_state2():
    st.session_state["status"]=3
def change_state3():
    st.session_state["status"]=4
def change_state4():
    st.session_state["status"]=5
def change_state5():
    st.session_state["status"]=6
#st.session_state["status"]=5
#status=1
with st.sidebar:
    select=stmenu(menu_title="Kisan Pay Mobile App",
        options=["Registration", "Digital KYC", "Loan Application", "Credit Assessment", "Fact Sheet"],
        menu_icon="card-checklist", #icon names from https://icons.getbootstrap.com/
        icons=["fan", "exclude", "file-bar-graph-fill"], #icon names from https://icons.getbootstrap.com/
        default_index=0, #default selection 0 for 1st option, 1 for 2nd option and so on
        )
if select=="Digital KYC":
    st.subheader("As Per Existing Flow")

elif select=="Loan Application":
    st.subheader("As Per Existing Flow")

elif select=="Registration":
    if 'status' not in st.session_state:
        st.title("Welcome to Kisan Pay Mobile Application Simulation!!!!!")
        st.subheader("Click Below To Start Front End Journey:")
        but=st.button('Start Onboarding Journey', on_click=change_state)
            #st.session_state["status"]=2
    elif st.session_state["status"]==2:
        st.title("Farmer Registration Screen")
        st.subheader("Farmer Personal Details")
        st.text_input("Aadhar Number:", value="Enter Details")
        st.text_input("First Name:", value="Enter Details")
        st.text_input("Last Name:", value="Enter Details")
        st.radio(label="Gender:", options=("Male", "Female"))
        st.date_input(label="Date of Birth:")
        st.text_input("Father Name:", value="Enter Details")
        st.subheader("Farmer Address Details")
        st.text_input("Door No:", value="Enter Details")
        st.text_input("Area:", value="Enter Details")
        st.text_input("City:", value="Enter Details")
        st.text_input("PIN:", value="Enter Details")
        st.text_input("District:", value="Enter Details")
        st.text_input("State:", value="Enter Details")
        st.text_input("Mobile:", value="Enter Details")
        but2=st.button('Submit', on_click=change_state2)
    elif st.session_state["status"]==3:
        st.write("Please select Annual House Hold Income of Farmer:")
        but3=st.button('More than 3 Lakhs', on_click=change_state3)
        but4=st.button('Upto 3 Lakhs', on_click=change_state4)

    elif st.session_state["status"]==4:
        st.subheader("Farmer Registration Completed, Kindly Proceed to Complete Your KYC")
        st.write("We can proceed with existing customer journey")

    elif st.session_state["status"]==5:
        st.radio(label="Type of Accomodation:", options=("Owned", "Rented"))
        st.multiselect(label="Select Available Basic Ammenities:", options=("Electricity", "Water", "Toilet", "Sewage", "LPG Connection"))
        st.multiselect(label="Select Available Assets:", options=("Land", "Livestocks", "vehicle", "Smartphone", "Other Electronic Items"))
        st.subheader("Member Income Details:")
        slide_val = st.slider("Select Count of House Hold Members", 0, 10,)
        if slide_val==0:
            st.write("None Selected")
        elif slide_val==1:
            st.text_input("Name of Applicant:", value="Enter Name")
            st.text_input("Income By Applicant:", value="Enter in INR")
        elif slide_val>1:
            st.text_input("Name of Applicant:", value="Enter Name")
            st.text_input("Income By Applicant:", value="Enter in INR")
            st.text_input("Liability On Applicant:", value="Enter in INR")

            temp_val=1
            while temp_val<slide_val+1:
                mem_label="Name of Member" + str(temp_val)
                income_label="Income By Member" + str(temp_val)
                liab_label="Liability on Member" + str(temp_val)
                rel_label="Member Relationship" + str(temp_val)
                st.text_input(label=mem_label, value="Enter Name")
                st.text_input(label=rel_label, value="Enter Relationship")
                st.text_input(label=income_label, value="Enter in INR")
                st.text_input(label=liab_label, value="Enter in INR")
                temp_val=temp_val+1
            st.text_input("Total House Hold Expenses:", value="Enter in INR")
            but5=st.button('Submit Details', on_click=change_state5)
    elif st.session_state["status"]==6:
        st.subheader("Farmer Registration Completed, Kindly Proceed to Complete Your KYC")

elif select=="Credit Assessment":
    st.subheader("Credit Assessment for farmer")
    st.write("Total HH Income (Sum of self declared income by all members) = A")
    st.write("Total HH Liability (Sum of self declared liability by all members) = B")
    st.write("50% of HH Income = A/2")
    st.write("Repayment Capacity (As per RBI Norms) = (A/2)-B")
    st.write("Maximum Allowed Limit = Principal Equivalent to Repayment Capacity (C)")
    st.write("Limit based on Highmark and existing credit assessment norms = D")
    st.write("Final Limit = Minimum of C and D")

elif select=="Fact Sheet":
    st.subheader("Factsheet Format: ")
    image = Image.open('RBI_FACTSHEET.jpg')
    st.image(image, caption='Factsheet as per RBI Norms')
    st.subheader("Repayment Schedule Format: ")
    image = Image.open('repayment_schedule.jpg')
    st.image(image, caption='Repayment Schedule as per RBI Norms')
