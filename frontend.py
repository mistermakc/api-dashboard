# Import modules
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import requests
import yaml
from yaml.loader import SafeLoader
import webbrowser

import streamlit_authenticator as stauth
import authenticator

# Setting theme for streamlit
image = Image.open('data/HM-Logo.png')
st.set_page_config(
    page_title="H&M Dashboard", 
    page_icon=image, 
    layout="centered", 
    initial_sidebar_state="expanded",
)

# Defining credentials 
with open('frontend/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating authenticator variable
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Establishing login
name, authentication_status, username = authenticator.login('Login', 'main')

# Defining function to load data
@st.cache
def load_data(url):
    try:
        headers = {'x-api-key': config['api_key']['key']}
        request = requests.get(f"https://api.maxharrison.de/api/v1/{url}", headers=headers).json()
        data = pd.DataFrame(request)
        data["kpi_date"] = pd.to_datetime(data["kpi_date"])
        if "sales_channel_id" in data.columns:
            data['sales_channel'] = data['sales_channel_id'].map({1: "Offline", 2: "Online"})
        if "fashion_news" in data.columns:
            data['fashion_news'] = data['fashion_news'].map({0: "No", 1: "Yes"})
    except Exception as e:
        print(e)
    return data

# Defining function to filter data
@st.cache(allow_output_mutation=True)
def filter_data(df, filters, filter_date):
    filtered_data = df.copy()
    for column, filter_values in filters.items():
        if filter_values:
            filtered_data = filtered_data[filtered_data[column].isin(filter_values)]
    filtered_data = filtered_data[
        filtered_data["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both')
    ]
    return filtered_data

# Defining function to create charts
@st.cache(allow_output_mutation=True)
def create_chart(data, x, y, color, title, height=368, legend_orient='bottom'):
    chart = alt.Chart(data).mark_bar().encode(
        x=x,
        y=y,
        color=color
    ).properties(
        title=title,
        height=height
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient=legend_orient,
        padding=10
    )
    return chart

# Establishing routes to login
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    # Loading data for KPIs
    df_sg = load_data("sales_growth",)
    df_aov = load_data("average_order_value")
    df_fne = load_data("fashion_news_effectiveness")
    df_fnf = load_data("fashion_news_frequency")
    df_it = load_data("inventory_turnover")
    df_crr = load_data("customer_retentation_rate")
    df_ps = load_data("product_sales")
    
    # Defining Streamlit widgets for filters
    st.sidebar.image("data/HM-Logo.png", output_format='PNG', use_column_width=True)

    st.sidebar.header("Filters:")
    sales_channel_unique = df_sg["sales_channel"].drop_duplicates().to_list()
    filter_sales_channel = st.sidebar.multiselect("SALES CHANNEL", sales_channel_unique, default=sales_channel_unique, key="multiselect_sales_channel")

    year_month_min = df_sg["kpi_date"].min().to_pydatetime()
    year_month_max = df_sg["kpi_date"].max().to_pydatetime()
    filter_date = st.sidebar.slider("TIME RANGE", min_value=year_month_min, max_value=year_month_max, value=(year_month_min, year_month_max), format="MM-YYYY")

    fashion_news_unique = df_fne["fashion_news"].drop_duplicates().to_list()
    filter_fashion_news = st.sidebar.multiselect("FASHION NEWS", fashion_news_unique, default=fashion_news_unique, key="multiselect_fashion_news")

    fashion_news_frequency_unique = df_fnf["fashion_news_frequency"].drop_duplicates().to_list()
    filter_fashion_news_frequency = st.sidebar.multiselect("FASHION NEWS FREQUENCY", fashion_news_frequency_unique, default=fashion_news_frequency_unique, key="multiselect_fashion_news_frequency")

    product_unique = df_ps["product_type_name"].drop_duplicates().to_list()
    filter_product = st.sidebar.multiselect("PRODUCTS", product_unique, default="Bag", key="multiselect_product")

    # Filtering the data for the different KPIs and metrics
    filters = {"sales_channel": filter_sales_channel}
    filtered_data_sg = filter_data(df_sg, filters, filter_date)
    filtered_data_aov = filter_data(df_aov, filters, filter_date)
    filtered_data_it = filter_data(df_it, filters, filter_date)

    filters = {"fashion_news": filter_fashion_news}
    filtered_data_fne = filter_data(df_fne, filters, filter_date)

    filters = {"fashion_news_frequency": filter_fashion_news_frequency}
    filtered_data_fnf = filter_data(df_fnf, filters, filter_date)

    filters = {"product_type_name": filter_product}
    filtered_data_ps = filter_data(df_ps, filters, filter_date)
    filtered_data_ps["kpi_date"] = pd.to_datetime(filtered_data_ps["kpi_date"]).dt.strftime('%m-%Y')
    filtered_data_ps = filtered_data_ps.rename(columns={"kpi_date": "Date", "product_type_name": "Product Name", "price": "Numbers Sold"})

    filters = {}
    filtered_data_crr = filter_data(df_crr, filters, filter_date)

    metrics_sg = f"€{filtered_data_sg['revenue'].sum():,.0f}"
    metrics_aov = f"€{filtered_data_aov['price'].sum():,.2f}"

    # Creating charts for KPIs
    chart_sg = create_chart(filtered_data_sg, alt.X('yearmonth(kpi_date):T', title='Date'), alt.Y('revenue:Q', title='Revenue', axis=alt.Axis(format=',.2s')), alt.Color('sales_channel:N', title='Sales Channel', scale=alt.Scale(domain=["Offline", "Online"], range=['#26272F', '#CC071E'])), 'Revenue by Sales Channel')
    chart_aov = create_chart(filtered_data_aov, alt.X('yearmonth(kpi_date):T', title='Date'), alt.Y('price:Q', title='Price'), alt.Color('sales_channel:N', title='Sales Channel', scale=alt.Scale(domain=["Offline", "Online"], range=['#26272F', '#CC071E'])), 'Price by Sales Channel')

    # Adding more charts using the create_chart function
    chart_fne = create_chart(filtered_data_fne, alt.X('yearmonth(kpi_date):T', title='Date'), alt.Y('revenue_normalized:Q', title='Revenue (%)'), alt.Color('fashion_news:N', title='Fashion News', scale=alt.Scale(domain=["No", "Yes"], range=['#26272F', '#CC071E'])), 'Fashion News Effectiveness')
    chart_fnf = create_chart(filtered_data_fnf, alt.X('yearmonth(kpi_date):T', title='Date'), alt.Y('fashion_news_frequency_percentage:Q', title='Fashion News Frequency (%)'), alt.Color('fashion_news_frequency:N', title='Frequency', scale=alt.Scale(domain=["NONE", "Regularly", "Monthly"], range=['#26272F', '#CC071E', '#F0F2F6'])), 'Fashion News Frequency')
    chart_it = create_chart(filtered_data_it, alt.X('yearmonth(kpi_date):T', title='Date'), alt.Y('inventory_turnover:Q', title='Inventory Turnover'), alt.Color('sales_channel:N', title='Sales Channel', scale=alt.Scale(domain=["Offline", "Online"], range=['#26272F', '#CC071E'])), 'Inventory Turnover')
    chart_crr = create_chart(filtered_data_crr, alt.X('yearmonth(kpi_date):T', title='Date'), alt.Y('customer_retention_rate:Q', title='Customer Retention Rate'), alt.Color(value='#CC071E'), 'Customer Retention',height=300)

    # Displaying the title 
    st.title("H&M KPI Dashboard")

    # Displaying the two metrics
    with st.container():
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            label = "Total Revenue",
            value = metrics_sg,
            delta = "{:,.2f}%".format(((filtered_data_sg['revenue'].mean() - df_sg['revenue'].mean()) / df_sg['revenue'].mean()) * 100),
        )
        kpi2.metric(
            label = "Average Order Value",
            value = metrics_aov,
            delta = "{:,.2f}%".format(((filtered_data_aov['price'].mean() - df_aov['price'].mean()) / df_aov['price'].mean()) * 100),
        )

    # Creating tabs to display different KPIs
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue", "Marketing", "Resources", "Catalogue"])

    with tab1:
        # Displaying the two charts side by side
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.altair_chart(chart_sg, use_container_width=True)
        with col2:
            st.altair_chart(chart_aov, use_container_width=True)

    with tab2:
        # Displaying the two charts side by side
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.altair_chart(chart_fne, use_container_width=True)
        with col2:
            st.altair_chart(chart_fnf, use_container_width=True)

    with tab3:
        # Displaying the two charts side by side
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.altair_chart(chart_it, use_container_width=True)
        with col2:
            st.altair_chart(chart_crr, use_container_width=True)

    with tab4:
        url = "https://mistermakc-capstone.streamlit.app"
        st.markdown(f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; text-align: center; background-color: #CC071E; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none;">Open Catalogue</a>', unsafe_allow_html=True)

    # Creating a dataframe
    with st.expander("Explore product sales per month and year"):
        st.dataframe(filtered_data_ps, use_container_width=True)
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')