import streamlit as st
from docxtpl import DocxTemplate as dx
import pandas as pd

uploaded_file_template=st.file_uploader(
    label="Upload Any Word File Here",
    key="Key Name",
    help="This is just to help",
    type="docx")

if uploaded_file_template is not None:
    def create_doc(x, y):
        doc.render(x)
        final_doc_path=str(y) + str(list(x.values())[0]) + ".docx"
        doc.save(final_doc_path)


    doc=dx(uploaded_file_template)

    uploaded_file_excel=st.file_uploader(
        label="Upload Any Excel File Here",
        key="Key Name",
        help="This is just to help",
        type="csv")
    if uploaded_file_excel is not None:
        address= st.text_input(
                    label="Enter address of folder where you wish to save the files")
        df=pd.read_csv(uploaded_file_excel)
        df_dict=df.to_dict(orient="records")
        if address is not "":
            for element in df_dict:
                create_doc(element, address)
                st.write("Saved!!!!")
