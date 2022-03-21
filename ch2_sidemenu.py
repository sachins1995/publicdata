#pip install streamlit-option-menu
import streamlit as st
from streamlit_option_menu import option_menu as stmenu
import pandas as pd
from matplotlib import pyplot as plt
#from PIL import Image as img

#Title of the page
st.title('DASHBOARD FOR KISAN PAY')

#importing data from git hub, caching data,making column in upper case
@st.cache #this will cach data
def read_data(url):
    data=pd.read_csv(url)
    data_col=data.columns.str.upper() #making columns in upper case
    data.columns=data_col #renaming columns in upper case
    return data

df_raw=read_data("https://raw.githubusercontent.com/sachins1995/publicdata/main/kisan_dashboard_data.csv")

#removing test FPOs
remove=["Mamali Gayen", "SHRI AMARANARAYANA HFPCL", "KAMTANATHJI KRISHAK PCL", "Test_FPO_02",
                    "BUDHASAMBAR DAL & VEGETABLE P C L", "JAN NAYAK F P C L"]
df_raw=df_raw[~df_raw.FPONAME.isin(remove)].reset_index(drop=1)

#filtering columns to Showing
df_raw_filter=df_raw[['FPONAME', "MEMBERID", "MEMBERNAME",'FARMERPRIMARYMOBILENUMBER',
                            "FARMERGENDER", 'DISTRICT', 'STATE', 'PINCODE', 'FARMERSAMID']]


#inserting side bar
with st.sidebar:
    select=stmenu(menu_title="Kisan Pay Menu", #can aslo be set as none
        options=["Farmer Data", "Card Issuance", "Timeline", "Payments"],
        menu_icon="card-checklist", #icon names from https://icons.getbootstrap.com/
        icons=["fan", "exclude", "file-bar-graph-fill", "file-image-fill"], #icon names from https://icons.getbootstrap.com/
        default_index=0, #default selection 0 for 1st option, 1 for 2ns option and so on
        #orientation="horizontal" #use this for horizontal bar otherwise ignore
        )

#defining function of each options
if select=="Farmer Data":
    #Showing text on page
    data_load=st.text("Kisan Pay Data is Loading.........")

    #Showing download option
    st.download_button(label="DOWNLOAD ALL FARMER DATA", data=df_raw.to_csv(),
                            file_name="All_farmer_data.csv", help="Click to download complete farmer data")

    #Showing table to page
    st.write(df_raw_filter)

    #Showing reapeated text
    data_load.text("Kisan Pay Data Loaded Successfully")

if select=="Card Issuance":
    #making data for pie chart
    df_pivot=pd.pivot_table(df_raw_filter, values=("MEMBERNAME","FARMERSAMID"),
                        index=['FPONAME'], aggfunc="count")
    df_pivot=df_pivot.sort_values(by='MEMBERNAME', ascending=0)#sorting values
    df_pivot_5=df_pivot.head(5)#getting top 5 values
    list_fpo=(list(df_pivot_5.index))
    list_fpocount=(list(df_pivot_5.MEMBERNAME))
    list_exp=[0.1, 0, 0, 0, 0]

    #making pie chart in matplotlib
    fig_pie, ax1=plt.subplots()
    ax1.pie(list_fpocount, labels=list_fpo, shadow=1, startangle=90, autopct='%1.1f%%', explode=list_exp)
    plt.title("Percentage of Registered Farmer by Top 5 FPOs")

    #showing the pie chart
    df_pivot["FPO NAME"]=df_pivot.index #making a new column similar to index
    df_pivot["NO. OF REGISTERED FARMERS"]=df_pivot["MEMBERNAME"] #making a new column similar to MEMBERNAME
    df_pivot["NO. OF CARD ISSUED"]=df_pivot["FARMERSAMID"]
    df_pivot=df_pivot.reset_index(drop=1) #reseting index to default
    df_pivot = df_pivot.drop('MEMBERNAME', 1) #deleting MEMBERNAME column
    df_pivot = df_pivot.drop('FARMERSAMID', 1) #deleting FARMERSAMID column
    st.subheader(":camping:FPO Wise Registered Farmers VS Card Issuance")
    st.download_button(label="DOWNLOAD FPO WISE FARMER COUNT", data=df_pivot.to_csv(),
                            file_name="FPO_WISE_FARMER_COUNT.csv",
                            help="Click to download complete data of FPO wise farmer count")
    st.write(df_pivot)
    st.pyplot(fig_pie)

if select=="Timeline":
    #making data for date wise card issuance and registration
    df_pivot_time=pd.pivot_table(df_raw, index=["CARDISSUEDATE"], values="FARMERSAMID", aggfunc="count")
    df_pivot_time["DATE"]=df_pivot_time.index
    df_pivot_time["NO. OF CARD ISSUED"]=df_pivot_time["FARMERSAMID"]
    df_pivot_time=df_pivot_time.reset_index(drop=True)
    df_pivot_time=df_pivot_time.drop('FARMERSAMID', 1)
    df_pivot_time['DATE']=pd.to_datetime(df_pivot_time['DATE'], format="%d/%m/%y")
    df_pivot_time=df_pivot_time.sort_values(by='DATE', ascending=0)
    df_pivot_time=df_pivot_time.reset_index(drop=1)

    #making list for ploting line graph
    list_date=list(df_pivot_time.DATE)
    list_card=list(df_pivot_time["NO. OF CARD ISSUED"])

    #Ploting line graph
    fig_line, ax=plt.subplots()
    ax.plot(list_date, list_card)
    ax.set(ylabel="Count of Card Issued Per Day", xlabel="Date of Card Issuance",
                                                        title="Date Wise Card Issuance")
    st.subheader(":camping:DATE WISE CARD ISSUANCE COUNT")
    st.download_button(label="DOWNLOAD DATE WISE CARD ISSUANCE COUNT", data=df_pivot_time.to_csv(),
                            file_name="DATE_WISE_CARD_COUNT.csv",
                            help="Click to download complete data of date wise card issuance to farmers")
    st.pyplot(fig_line)
