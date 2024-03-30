# Importing the necessary packages
import streamlit as st
import openpyxl
import pandas as pd

# Setting up web app page
st.set_page_config(page_title='Exploratory Data Analysis App', page_icon=None, layout="wide")

# Section for file upload in the sidebar
st.sidebar.write("****A) File upload****")

# User prompt to select file type
ft = st.sidebar.selectbox("*What is the file type?*", ["Excel", "csv"])

# Creating dynamic file upload option in the sidebar
uploaded_file = st.sidebar.file_uploader("*Upload file here*")

if uploaded_file is not None:
    file_path = uploaded_file

    if ft == 'Excel':
        try:
            # User prompt to select sheet name in uploaded Excel
            sh = st.sidebar.selectbox("*Which sheet name in the file should be read?*", pd.ExcelFile(file_path).sheet_names)
            # User prompt to define row with column names if they aren't in the header row in the uploaded Excel
            h = st.sidebar.number_input("*Which row contains the column names?*", 0, 100)
        except:
            st.info("File is not recognised as an Excel file")
            sys.exit()
    elif ft == 'csv':
        try:
            # No need for sh and h for csv, set them to None
            sh = None
            h = None
        except:
            st.info("File is not recognised as a csv file.")
            sys.exit()

    # Caching function to load data
    @st.cache_data(experimental_allow_widgets=True)
    def load_data(file_path, ft, sh, h):
        if ft == 'Excel':
            try:
                # Reading the excel file
                data = pd.read_excel(file_path, header=h, sheet_name=sh, engine='openpyxl')
            except:
                st.info("File is not recognised as an Excel file.")
                sys.exit()
        elif ft == 'csv':
            try:
                # Reading the csv file
                data = pd.read_csv(file_path)
            except:
                st.info("File is not recognised as a csv file.")
                sys.exit()
        return data

    data = load_data(file_path, ft, sh, h)

    # Overview of the data
    st.write('### 1. Dataset Preview ')
    try:
        # View the dataframe in streamlit
        st.dataframe(data, use_container_width=True)
    except:
        st.info("The file wasn't read properly. Please ensure that the input parameters are correctly defined.")
        sys.exit()

    # Understanding the data
    st.write('### 2. High-Level Overview ')

    # Creating radio button and sidebar simultaneously
    selected = st.sidebar.radio("**B) What would you like to know about the data?**",
                                ["Field Descriptions", "Summary Statistics", "Value Counts of Fields", "Visualizations"])

    # Show selected information
    if selected == 'Field Descriptions':
        fd = data.dtypes.reset_index().rename(columns={'index': 'Field Name', 0: 'Field Type'}).sort_values(
            by='Field Type', ascending=False).reset_index(drop=True)
        st.dataframe(fd, use_container_width=True)

    elif selected == 'Summary Statistics':
        ss = pd.DataFrame(data.describe(include='all').round(2).fillna(''))
        st.dataframe(ss, use_container_width=True)

    elif selected == 'Value Counts of Fields':
        sub_selected = st.sidebar.radio("Which field should be investigated?", data.select_dtypes('object').columns)
        vc = data[sub_selected].value_counts().reset_index().rename(columns={'count': 'Count'}).reset_index(drop=True)
        st.dataframe(vc, use_container_width=True)

    elif selected == 'Visualizations':
        st.subheader("Data Visualizations")

        # Visualizations
        column_for_chart = st.selectbox("Select a column for visualization:", data.columns)
        chart_type = st.selectbox("Select a chart type:",
                                  ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])

        if chart_type == "Bar Chart":
            st.bar_chart(data[column_for_chart])

        elif chart_type == "Line Chart":
            st.line_chart(data[column_for_chart])

        elif chart_type == "Scatter Plot":
            st.write("Select x and y axes:")
            x_axis = st.selectbox("X Axis:", data.columns)
            y_axis = st.selectbox("Y Axis:", data.columns)
            st.write(f"Scatter plot between {x_axis} and {y_axis}")
            st.scatter_chart(data[[x_axis, y_axis]])

        elif chart_type == "Histogram":
            st.hist(data[column_for_chart], bins=20)

        # Showing the shape of the dataframe
        else:
            st.write('###### The data has the dimensions :', data.shape)
