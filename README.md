# Capstone project

This repository contains the code for the capstone project. The project's objective is to establish a data visualization dashboard, 
which includes understanding and cleaning the dataset, deploying a database solution (e.g. MySQL), integrating a back-end service for the API and 
developing a front-end.

The structure of this repository is as follows:
- *API*
  - Developed with Flask Rest-X
  - To deliver data, an API-key in the header is required
  - The API connects to a MySQL database in the Google Cloud
- App/ Client
  - Developed with Pandas, Streamlit, and Streamlit Authenticator
  - To view the visualized data, a username and password is required
  - Allows for data analysis and insight generation
- Architecture (visualization of system architecture)
  - Overview about the solution's architecture
- Data (csv files)
  - Individual and untouchd data fils
- Data Cleaning + Upload
  - Developed with Pandas 
  - Cleaned to avoid duplicates, missing values, or various variable-content definitions (e.g. NONE, None, none)
- KPIs
  - Developed with Pandas
  - Uploaded as individual tables to the database to increase the request time 
  
## Solution Architecture

![alt text](https://github.com/mistermakc/capstone/blob/main/architecture/Capstone%20Architecture.png)

> **More detailed documentation (README) about the api and app can be found in their respective folders**
