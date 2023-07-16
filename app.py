import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from functions import write_to_google, check_inputs, alpha_list, upload_to_drive, save_uploadedfile, clear_image_cache
from configs import *

st.set_page_config(page_title='Sinani Inventory App',
                   layout='wide', initial_sidebar_state='collapsed')


stock_in, stock_out = st.tabs(['Stock In', 'Stock Out'])


with stock_in:

    form_container = st.container()
    preview_container = st.container()

    with form_container:
        delivery_details, spacer, stock_details = st.columns([1, 0.5, 1])
        with delivery_details:
            st.header("Delivery Details")
            selected_name = st.selectbox(
                '*Name:', alpha_list(path_to_names,','))
            selected_supplier = st.selectbox(
                '*Supplier:', alpha_list(path_to_suppliers,','))
            selected_invoice = st.text_input('*Invoice/Deleivery Note Number:')

            selected_invoice_image = st.file_uploader("Choose an image to upload", type=['png', 'jpeg', 'jpg', 'HEIC'])


        with stock_details:
            st.header("Stock Details")
            selected_unit = st.selectbox(
                "*Stock Unit:", alpha_list(path_to_stock_units,';'))
            selected_item = st.text_input("*Item:")
            selected_quantity = st.number_input("*Quantity:", min_value=1)
            selected_stock_type = st.selectbox('*Stock Type:', ["", "General Stock", "Site Specific Stock"])
            selected_notes = st.text_input("Notes:")
            delivery_time = (datetime.now() + timedelta(hours=2)).strftime("%d/%m/%y %H:%M:%S")

            if st.button('Add Item'):
                with st.spinner('Uploading image...'):
                    if "link" not in st.session_state:
                        if selected_invoice_image is not None:
                            save_uploadedfile(selected_invoice_image)
                            path = f'./image_cache/{selected_invoice_image.name}'
                            link = upload_to_drive(st.secrets["gcp_service_account"], parent_folder_key, selected_invoice_image.name, path)
                            st.session_state.link = link
                        else:
                            link = ""
                            st.session_state.link = link
                    
                    if check_inputs([selected_name, selected_supplier, selected_invoice, selected_unit, selected_item, selected_stock_type])== False:
                        st.error('Please fill out all the necessary fields', icon="🚨")

                    else:

                        if 'data' not in st.session_state:
                            data_obj = {
                                'Timestamp': [delivery_time],
                                'Name:': [selected_name],
                                'Stock Unit:': [selected_unit],
                                'Supplier:': [selected_supplier],
                                'Item:': [selected_item],
                                'Quantity:': [selected_quantity],
                                'Notes:': [selected_notes],
                                'Invoice/Delivery Note Number:': [selected_invoice],
                                'Invoice/Delivery Note:': [st.session_state.link],
                                'Stock Type:': [selected_stock_type]
                            }

                            data = pd.DataFrame(data_obj)
                            st.session_state.data = data


                        else:
                            data_obj = {
                                'Timestamp': [delivery_time],
                                'Name:': [selected_name],
                                'Stock Unit:': [selected_unit],
                                'Supplier:': [selected_supplier],
                                'Item:': [selected_item],
                                'Quantity:': [selected_quantity],
                                'Notes:': [selected_notes],
                                'Invoice/Delivery Note Number:': [selected_invoice],
                                'Invoice/Delivery Note:': [st.session_state.link],
                                'Stock Type:': [selected_stock_type]
                            }

                            data = pd.DataFrame(data_obj)
                            st.session_state.data = pd.concat(
                                [st.session_state.data, data])


    with preview_container:
        st.header('Preview')

        if st.button('Delete Last Entry'):

            data = pd.DataFrame(st.session_state.data)
            data = data.head(data.shape[0] - 1)
            st.session_state.data = data
            st.table(st.session_state.data)

            if st.button('Submit'):
                with st.spinner(text="Uploading to google sheets..."):
                    data = st.session_state.data
                    if write_to_google(data, st.secrets["gcp_service_account"], sheet_key, sheet_name):
                        st.success('Delivery Captured', icon="✅")
                        st.session_state.data = None
                        clear_image_cache('./image_cache')
                    else:
                        st.error('Something went wrong...',icon="🚨")

        else:
            if 'data' not in st.session_state:
                st.write('Add a line item to see preview')

            else:
                st.table(st.session_state.data)
                if st.button('Submit'):
                    with st.spinner(text="Uploading to google sheets..."):
                        data = st.session_state.data
                        if write_to_google(data, st.secrets["gcp_service_account"], sheet_key, sheet_name):
                            st.success('Delivery Captured', icon="✅")
                            st.session_state.data = None
                            clear_image_cache('./image_cache')
                        else:
                            st.error('Something went wrong...',icon="🚨")


with stock_out:
    st.header('stock out')
        