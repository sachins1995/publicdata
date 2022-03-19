import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
#from PIL import Image as img

#Putting Image
#image=img.open(r"C:\Users\SachinSingh\Desktop\Python projects\Streamlit\Samunnati Logo-01.png")#opening image
#st.image(image)#displaying image

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

#filtering columns to Showing
df_raw_filter=df_raw[['FPONAME', "MEMBERID", "MEMBERNAME",'FARMERPRIMARYMOBILENUMBER',
                            "FARMERGENDER", 'DISTRICT', 'STATE', 'PINCODE', 'FARMERSAMID']]

#removing test FPOs
remove=["Mamali Gayen", "SHRI AMARANARAYANA HFPCL", "KAMTANATHJI KRISHAK PCL", "Test_FPO_02",
                    "BUDHASAMBAR DAL & VEGETABLE P C L", "JAN NAYAK F P C L"]
df_raw_filter=df_raw_filter[~df_raw_filter.FPONAME.isin(remove)].reset_index(drop=1)

#Showing text on page
data_load=st.text("Kisan Pay Data is Loading.........")

#Showing download option
st.download_button(label="DOWNLOAD ALL FARMER DATA", data=df_raw.to_csv(),
                        file_name="All_farmer_data.csv", help="Click to download complete farmer data")

#Showing table to page
st.write(df_raw_filter)

#Showing reapeated text
data_load.text("Kisan Pay Data Loaded Successfully")

#making data for pie chart
df_pivot=pd.pivot_table(df_raw_filter, values="MEMBERNAME",
                    index=['FPONAME'], aggfunc="count")
df_pivot=df_pivot.reindex(df_pivot.sort_values(by='MEMBERNAME', ascending=0).index)#sorting values
df_pivot_5=df_pivot.head(5)#getting top 5 values
list_fpo=(list(df_pivot_5.index))
list_fpocount=(list(df_pivot_5.MEMBERNAME))
list_exp=[0.1, 0, 0, 0, 0]

#making pie chart in matplotlib
fig_pie, ax1=plt.subplots()
ax1.pie(list_fpocount, labels=list_fpo, shadow=1, startangle=90, autopct='%1.1f%%', explode=list_exp)
plt.title("Percentage of Registered Farmer by Top 5 FPOs")

#showing the pie chart
st.subheader(":camping:Registered Farmer Count by FPOs")
st.download_button(label="DOWNLOAD FPO WISE FARMER COUNT", data=df_pivot.to_csv(),
                        file_name="FPO_WISE_FARMER_COUNT.csv",
                        help="Click to download complete data of FPO wise farmer count")
df_pivot["FPO NAME"]=df_pivot.index #making a new column similar to index
df_pivot["Farmer Count"]=df_pivot["MEMBERNAME"] #making a new column similar to MEMBERNAME
df_pivot=df_pivot.reset_index(drop=True) #reseting index to default
df_pivot = df_pivot.drop('MEMBERNAME', 1) #deleting MEMBERNAME column
st.write(df_pivot)
st.pyplot(fig_pie)

#making data for date wise card issuance and registration
