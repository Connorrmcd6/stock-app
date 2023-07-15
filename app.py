import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from functions import write_to_google 
from configs import *

st.set_page_config(page_title='Sinani Inventory',
                   layout='wide', initial_sidebar_state='collapsed')


stock_in, stock_out = st.tabs(['Stock In', 'Stock Out'])


with stock_in:

    form_container = st.container()
    preview_container = st.container()

    with form_container:
        delivery_details, spacer, stock_details = st.columns([1, 0.5, 2])
        with delivery_details:
            st.header("Delivery Details")
            selected_name = st.selectbox(
                'Name:', ("", "Jesse", "Nhlanhla", "Derenzo", "Able"))
            selected_supplier = st.selectbox(
                'Supplier:', ("", "ALLBRO Industrial", "Builders Warehouse", "Chavda International"))
            selected_invoice = st.text_input('Invoice/Deleivery Note Number:')
            selected_invoice_image = st.text_input(
                'Invoice/Delivery Note Image:')  # change to file uploader

        with stock_details:
            st.header("Stock Details")
            selected_unit = st.selectbox(
                "Stock Unit:", ("", "Cable Management", "Cabling", "Consumables", "Modules", "Mounting Structure"))
            selected_item = st.text_input("Item:")
            selected_quantity = st.number_input("Quantity:", min_value=1)
            selected_notes = st.text_input("Notes:")
            delivery_time = datetime.now().strftime("%d/%m/%y %H:%M:%S")


            if st.button('Add Item'):
                if 'data' not in st.session_state:
                    data_obj = {
                        'Timestamp': [delivery_time],
                        'Name': [selected_name],
                        'Stock Unit': [selected_unit],
                        'Supplier': [selected_supplier],
                        'Invoice/Deleivery Note Number': [selected_invoice],
                        'Invoice/Deleivery Note Image': [selected_invoice_image],
                        'Item': [selected_item],
                        'Quantity': [selected_quantity],
                        'Notes': [selected_notes]
                    }

                    data = pd.DataFrame(data_obj)
                    st.session_state.data = data


                else:
                    data_obj = {
                        'Timestamp': [delivery_time],
                        'Name': [selected_name],
                        'Stock Unit': [selected_unit],
                        'Supplier': [selected_supplier],
                        'Invoice/Deleivery Note Number': [selected_invoice],
                        'Invoice/Deleivery Note Image': [selected_invoice_image],
                        'Item': [selected_item],
                        'Quantity': [selected_quantity],
                        'Notes': [selected_notes]
                    }

                    data = pd.DataFrame(data_obj)
                    st.session_state.data = pd.concat(
                        [st.session_state.data, data])

            if st.button('Submit'):
                data = st.session_state.data
                write_to_google(data, path_to_json, sheet_key, sheet_name)

    with preview_container:
        st.header('Preview')

        if st.button('Delete Entry'):
            st.session_state.data = None

        else:
            if 'data' not in st.session_state:
                st.write('Add a line item to see preview')

            else:
                st.table(st.session_state.data)


with stock_out:
    st.header('stock out')
        