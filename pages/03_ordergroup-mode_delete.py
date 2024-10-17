import base as b
import streamlit as st
import os
import re
import pandas as pd

c = b.read_config("config.json")
datadir = c["datadir_ordergroup"]


def main():
    st.header('ordergroup-mode delete', divider='grey')

    if "success" in st.session_state:
        st.success(st.session_state["success"])
        st.json(st.session_state["success"].json())

        st.button("back")

        st.subheader("data")
        st.json(st.session_state["data"])

        del st.session_state["success"]
        del st.session_state["ordergroup_id"]
        del st.session_state["data"]
    
    elif "error" in st.session_state:
        st.subheader("error")
        st.error(st.session_state["error"])
        st.button("back")

        st.subheader("data")
        st.json(st.session_state["data"])

        del st.session_state["error"]
        del st.session_state["ordergroup_id"]
        del st.session_state["data"]

    else:
        os.makedirs(datadir, exist_ok=True)

        files = [ x.replace(".pkl", "") for x in os.listdir(datadir) if re.match(r'^.+.pkl$', x) ]

        if len(files) > 0:
            selected = st.radio("select and Post", files)
            st.button("Delete", type="primary", on_click=delete_data, args=[selected])

            df = pd.read_pickle(f'{datadir}/{selected}.pkl')
            st.dataframe(df, hide_index=True)

        else:
            st.error("no data is registered.")


def delete_data(selected):
    os.remove(f'{datadir}/{selected}.pkl')


if __name__ == "__main__":
    main()