import base as b
import streamlit as st
import os
import re
import pandas as pd
import requests
import json

c = b.read_config("config.json")
datadir = c["datadir_ordergroup"]


def main():
    st.header('ordergroup post', divider='grey')

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
            st.button("Post", type="primary", on_click=post_data, args=[selected])

            df = pd.read_pickle(f'{datadir}/{selected}.pkl')
            st.dataframe(df, hide_index=True)

        else:
            st.error("no data is registered.")


def post_data(selected):
    df = pd.read_pickle(f'{datadir}/{selected}.pkl')
    data = generate_json_payload(df)

    st.session_state["data"] =  data

    try:
        response = requests.post(
            f'{c["uri"]}/wms/black/order/receive',
            data,
            headers={'Content-Type': 'application/json'},
            timeout=3.5
        )
        st.session_state["success"] =  response

    except requests.exceptions.RequestException as e:
        st.session_state["error"] = e


def generate_json_payload(df):
    sorted = dict()
    for x in df.values.tolist():
        if f'{x[0]}-{x[1]}' not in sorted.keys():
            sorted[f'{x[0]}-{x[1]}'] = list()
        sorted[f'{x[0]}-{x[1]}'].append(x)
    
    if "ordergroup_id" in st.session_state:
        ordergroup_id = st.session_state["ordergroup_id"]
    else:
        ordergroup_id = b.generate_ordergroup_id()
        st.session_state["ordergroup_id"] = ordergroup_id

    data = list()
    order_count = 1
    for y in sorted:
        wall, grid = y.split('-')
        order_id = f'{ordergroup_id}-{order_count}'
        data.append({
            "orderGroupId": ordergroup_id,
            "orderId": order_id,
            "systemId": c["systemid"],
            "type": "Normal",
            "wallId": f'{c["systemid"]}-WALL-{wall[0]}-{wall[1]}',
            "indexInWall": int(grid),
            "details": order_details(sorted[y], order_id)
        })
        order_count += 1

    return json.dumps({"data": data})


def order_details(indata, order_id):
    data = list()
    order_detail_count = 1
    for i in indata:
        order_detail = {
            "orderDetailId": f'{order_id}-{order_detail_count}',
            "productId": i[2],
            "productBarcode": i[2],
            "qty": int(i[3]),
        }

        data.append(order_detail)
        order_detail_count += 1

    return data


if __name__ == "__main__":
    main()