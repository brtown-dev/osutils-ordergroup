import base as b
import streamlit as st
import random
import pandas as pd
import os

c = b.read_config("config.json")
datadir = c["datadir_ordergroup"]

def main():
    st.header('ordergroup register', divider='grey')

    if 'key' not in st.session_state:
        st.session_state["key"] = str(random.randint(1000, 100000000))

    if "success" in st.session_state:
        st.success(f"successfully registered")
        st.button("back")
        del st.session_state["success"]
    
    else:
        infile = st.file_uploader(
            "Choose a xlsx file",
            type="xlsx", 
            key=st.session_state["key"]
        )

        with open("pages/sample_ordergroup.xlsx", 'rb') as f:
            st.download_button('Download Sample', f, file_name='sample_ordergroup.xlsx')

        if infile and validate_data(infile):
            st.button("register",  type="primary", on_click=register_data, args=[infile])
            st.dataframe(pd.read_excel(infile), hide_index=True)

def register_data(infile):
    os.makedirs(datadir, exist_ok=True)
    outfile = infile.name.replace(".xlsx", "")
    df = pd.read_excel(infile)
    df.to_pickle(f'{datadir}/{outfile}.pkl')

    st.session_state["success"] = True

def validate_data(infile):
    df = pd.read_excel(infile)
    df = df.fillna("")  # "nan"を空文字に変換
    df = df.astype(str)  # 全データを文字列に変換
    state = True

    # ファイルが空ではないかチェック
    if df.empty:
        st.error(f'empty file')
        state = False
    
    else:
        state = True

    return state

if __name__ == "__main__":
    main()