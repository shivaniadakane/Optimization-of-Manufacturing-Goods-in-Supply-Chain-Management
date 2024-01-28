# Importing libraries

import pandas as pd
import streamlit as st 
from statsmodels.regression.linear_model import OLSResults
model = OLSResults.load("model.pickle")
from sqlalchemy import create_engine


def main():

    st.sidebar.title("Forecast")

    html_temp = """
    <div style="background-color:blue;padding:10px">
    <h2 style="color:white;text-align:center;">Pallets Quantity Forecasting App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    st.text("")
    
    uploadedFile = st.sidebar.file_uploader("Choose a file" ,type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    if uploadedFile is not None :
        try:
            df=pd.read_csv(uploadedFile,  index_col=0)
        except:
                try:
                    df = pd.read_excel(uploadedFile,  index_col=0)
                except:      
                    df = pd.DataFrame(uploadedFile)
                
    else:
        st.sidebar.warning("Upload a csv or excel file.")
    
    
    html_temp = """
    <div style="background-color:black;padding:10px">
    <p style="color:white;text-align:center;">Add DataBase Credientials </p>
    </div>
    """
    st.sidebar.markdown(html_temp, unsafe_allow_html = True)
            
    user = st.sidebar.text_input("user", "Type Here")
    pw = st.sidebar.text_input("password", "Type Here")
    db = st.sidebar.text_input("database", "Type Here")
    
    
    if st.button("Predict"):
        engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")
        
        
        st.subheader(":red[Forecasting data]", anchor=None)
         
        forecast_test = pd.DataFrame(model.predict(start=len(df.index), end=len(df.index) + 56))

        
        import seaborn as sns
        cm = sns.light_palette("blue", as_cmap=True)
        st.table(forecast_test.style.background_gradient(cmap=cm).format('{:.2f}'))


        df.to_sql('forecast_pred', con = engine, if_exists = 'replace', chunksize = 1000, index = False)

                           
if __name__=='__main__':
    main()