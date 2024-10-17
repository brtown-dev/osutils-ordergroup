import streamlit as st
import base
import random

c = base.read_config("config.json")

def main():
    if 'key' not in st.session_state: st.session_state.key = str(random.randint(1000, 100000000))
    
    st.header('Settings', divider='grey')
    
    # URI
    st.subheader("Destination URI")

    if not "uri" in c:
        c["uri"] = "http://10.0.64.108:4000"

    c["uri"] = st.text_input("Destination URI (e.g., \"http://10.0.64.108:4000\")", c["uri"])

    # System ID
    st.subheader("System ID")

    if not "systemid" in c:
        c["systemid"] = "JP001"

    c["systemid"] = st.text_input("SystemID (e.g., \"JP001\")", c["systemid"])

    # Data Directory
    st.subheader("Data Directory")

    ## orderGroup data
    if not "datadir_ordergroup" in c:
        c["datadir_ordergroup"] = "./data/ordergroup"

    c["datadir_ordergroup"] = st.text_input("orderGroup data directory path", c["datadir_ordergroup"])


    # ## preset data
    # if not "datadir_preset" in c:
    #     c["datadir_preset"] = "./data/preset"

    # c["datadir_preset"] = st.text_input("preset rules directory path", c["datadir_preset"])

    base.write_config(c)

if __name__ == "__main__":
    main()