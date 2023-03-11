# Import modules
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml
import authenticator

with open('app/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    # Defining querying function
    @st.experimental_memo #st.cache
    def load_data(url):
        try:
            data = pd.read_json(f"api.maxharrison.de/api/v1/{url}")
        except Exception as e:
            print(e)
        return data 

    # Loading data for KPIs
    df_sg = load_data("sales_growth")             
    df_aov = load_data("average_order_value")
    df_fne = load_data("fashion_news_effectiveness")
    df_fnf = load_data("fashion_news_frequency")
    df_it = load_data("inventory_turnover")
    df_crr = load_data("customer_retentation_rate")
    df_ps = load_data("product_sales")
    
    # Encode kpi_date
    def encode_date(df):
        df["kpi_date"] = pd.to_datetime(df["kpi_date"])
        return df
    
    df_sg = encode_date(df_sg)        
    df_aov = encode_date(df_aov) 
    df_fne = encode_date(df_fne) 
    df_fnf = encode_date(df_fnf) 
    df_it = encode_date(df_it) 
    df_crr = encode_date(df_crr) 
    df_ps = encode_date(df_ps) 

    # Encoding "Sales Channel" variable
    def encode_id(x):
        if x == 1:
            return "Offline"
        if x == 2:
            return "Online"
    df_sg['sales_channel'] = df_sg['sales_channel_id'].transform(encode_id)
    df_aov['sales_channel'] = df_aov['sales_channel_id'].transform(encode_id)
    df_it['sales_channel'] = df_it['sales_channel_id'].transform(encode_id)

    # Encoding "Fashion News" variable
    def encode_fn(x):
        if x == 0:
            return "No"
        if x == 1:
            return "Yes"
    df_fne['fashion_news'] = df_fne['fashion_news'].transform(encode_fn)

    # Defining multiselection in Streamlit for sales channel
    sales_channel_unique = df_sg["sales_channel"].drop_duplicates().to_list()
    filter_sales_channel = st.sidebar.multiselect(
        label="SALES CHANNEL",
        options=sales_channel_unique,
        default=sales_channel_unique,
        key="multiselect_sales_channel"
    )

    # Defining slider in Streamlit for date
    year_month_min = df_sg["kpi_date"].min().to_pydatetime()
    year_month_max = df_sg["kpi_date"].max().to_pydatetime()
    filter_date = st.sidebar.slider(
        "TIME RANGE",
        min_value=year_month_min,
        max_value=year_month_max,
        value=(year_month_min, year_month_max),
        format="MM-YYYY",
    )

    # Defining multiselection in Streamlit for fashion news
    fashion_news_unique = df_fne["fashion_news"].drop_duplicates().to_list()
    filter_fashion_news = st.sidebar.multiselect(
        label="FASHION NEWS",
        options=fashion_news_unique,
        default=fashion_news_unique,
        key="multiselect_fashion_news"
    )

    # Defining multiselection in Streamlit for fashion news frequency
    fashion_news_frequency_unique = df_fnf["fashion_news_frequency"].drop_duplicates().to_list()
    filter_fashion_news_frequency = st.sidebar.multiselect(
        label="FASHION NEWS FREQUENCY",
        options=fashion_news_frequency_unique,
        default=fashion_news_frequency_unique,
        key="multiselect_fashion_news_frequency"
    )

    # Defining multiselection in Streamlit for product sales
    product_unique = df_ps["product_type_name"].drop_duplicates().to_list()
    filter_product = st.sidebar.multiselect(
        label="PRODUCTS",
        options=product_unique,
        default=product_unique,
        key="multiselect_product"
    )

    # Defining data to be shown based on filters
    filtered_data_sg = df_sg[
        (df_sg["sales_channel"].isin(filter_sales_channel)) & 
        (df_sg["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]

    filtered_data_aov = df_aov[
        (df_aov["sales_channel"].isin(filter_sales_channel)) & 
        (df_aov["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]

    filtered_data_fne = df_fne[
        (df_fne["fashion_news"].isin(filter_fashion_news)) & 
        (df_fne["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]

    filtered_data_fnf = df_fnf[
        (df_fnf["fashion_news_frequency"].isin(filter_fashion_news_frequency)) & 
        (df_fnf["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]

    filtered_data_it = df_it[
        (df_it["sales_channel"].isin(filter_sales_channel)) & 
        (df_it["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]

    filtered_data_crr = df_crr[
        (df_crr["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]

    filtered_data_ps = df_ps[
        (df_ps["product_type_name"].isin(filter_product)) & 
        (df_ps["kpi_date"].between(filter_date[0], filter_date[1], inclusive='both'))]
    filtered_data_ps["kpi_date"] = pd.to_datetime(filtered_data_ps["kpi_date"]).dt.strftime('%m-%Y')
    filtered_data_ps = filtered_data_ps.rename(columns={"kpi_date": "Date",
                            "product_type_name": "Product Name",
                            "price": "Numbers Sold"
                            })

    # Creating the chart for sales growth
    chart_sg = alt.Chart(filtered_data_sg).mark_bar().encode(
        x=alt.X('yearmonth(kpi_date):T', title='Date'),
        y=alt.Y('revenue:Q', title='Revenue',axis=alt.Axis(format=',.2s')),
        color=alt.Color('sales_channel:N', title='Sales Channel', 
                        scale=alt.Scale(domain=["Offline","Online"], range=['#26272F', '#CC071E'])),
    ).properties(
        title='Revenue by Sales Channel',
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    )

    # Creating the chart for average order value
    chart_aov = alt.Chart(filtered_data_aov).mark_bar().encode(
        x=alt.X('yearmonth(kpi_date):T', title='Date'),
        y=alt.Y('price:Q', title='Price'),
        color=alt.Color('sales_channel:N', title='Sales Channel', 
                        scale=alt.Scale(domain=["Offline","Online"], range=['#26272F', '#CC071E'])),
    ).properties(
        title='Price by Sales Channel',
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    )

    # Creating the chart for fashion news effectiveness
    chart_fne = alt.Chart(filtered_data_fne).mark_bar().encode(
        x=alt.X('yearmonth(kpi_date):T', title='Date'),
        y=alt.Y('revenue_normalized:Q', title='Revenue (%)'),
        color=alt.Color('fashion_news:N', title='Fashion News', 
                        scale=alt.Scale(domain=["No","Yes"], range=['#26272F', '#CC071E'])),
    ).properties(
        title="Fashion News Effectiveness",
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    )

    # Creating the chart for fashion news frequency
    chart_fnf = alt.Chart(filtered_data_fnf).mark_bar().encode(
        x=alt.X('yearmonth(kpi_date):T', title='Date'),
        y=alt.Y('fashion_news_frequency_percentage:Q', title='Fashion News Frequency (%)'),
        color=alt.Color('fashion_news_frequency:N', title='Frequency', 
                        scale=alt.Scale(domain=["NONE","Regularly", "Monthly"], range=['#26272F', '#CC071E','#F0F2F6'])),
    ).properties(
        title='Fashion News Frequency',
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    )

    # Creating the chart for inventory turnover
    chart_it = alt.Chart(filtered_data_it).mark_bar().encode(
        x=alt.X('yearmonth(kpi_date):T', title='Date'),
        y=alt.Y('inventory_turnover:Q', title='Inventory Turnover'),
        color=alt.Color('sales_channel:N', title='Sales Channel', 
                        scale=alt.Scale(domain=["Offline","Online"], range=['#26272F', '#CC071E'])),
    ).properties(
        title='Inventory Turnover',
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    )

    # Creating the chart for customer retention rate
    chart_crr = alt.Chart(filtered_data_crr).mark_bar(color='#CC071E').encode(
        x=alt.X('yearmonth(kpi_date):T', title='Date'),
        y=alt.Y('customer_retention_rate:Q', title='Customer Retention Rate'),
    ).properties(
        title='Customer Retention',
        height=300
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    )

    # Displaying the two charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.title("H&M Dashboard")
    with col2:
        image = Image.open('data/H&M-Logo-S.png')
        st.image(image, width=100, output_format='PNG')

    # Creating tabs to display different KPIs
    tab1, tab2, tab3 = st.tabs(["Revenue", "Marketing", "Resources"])

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

    # Creating a dataframe
    with st.expander("Explore product sales per month and year"):
        st.dataframe(filtered_data_ps, use_container_width=True)
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')