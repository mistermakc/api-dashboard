# REST API Documentation - Flask-RestX

This document highlights the REST API built using Flask-RestX for a web application that visualizes KPIs for H&M aggregated through article, transaction, and customer data.

Try the API: [H&M API](api.maxharrison.de)

## Overview

To improve the request time for the API, dedicated KPI tables have been created by using the underyling three main datafiles. This REST API is designed to provide access to the following resources:

- **Revenue**
  - Sales Growth
  - Average Order Value
- **Marketing**
  - Fashion News Effectiveness
  - Fashion News Frequency
- **Resources**
  - Inventory Turnover
  - Customer Retention Rate
- **Products**
  - Product Sales

This includes operations for fetching the given resources, including error handling. The API uses as a predefined API key for authentication and authorization: `"IEMCSBT23"`.

## Required Modules

Before using the REST API, the following Python modules must be installed:

1. Flask: `pip install Flask`
2. Flask-RESTx: `pip install flask-restx`
3. SQLAlchemy: `pip install sqlalchemy`
4. Retry: `pip install retry`

## Endpoints

### Revenue

#### GET /api/v1/average_order_value

- Description: Fetches the average order value.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of the average order value per year and month.

#### GET /api/v1/sales_growth

- Description: Fetches the revenue.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of the revenue per year and month.

### Marketing

#### GET /api/v1/fashion_news_effectiveness

- Description: Fetches the fashion news effectiveness.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of the fashion news effectiveness per year and month.
  
#### GET /api/v1/fashion_news_frequency

- Description: Fetches the fashion news frequency.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of the fashion news frequency per year and month.

### Resources

#### GET /api/v1/customer_retention_rate

- Description: Fetches the customer retention rate.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of the customer retention rate per year and month.

#### GET /api/v1/inventory_turnover

- Description: Fetches the inventory turnover.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of the inventory turnover per year and month and channel.
  
### Products

#### GET /api/v1/product_sales

- Description: Fetches all product sales.
- Authorization: Requires the valid API key.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of all product sales per year and month.

## Error Handling

In case of any errors, the API will return a JSON object containing an error message and an appropriate HTTP status code.
  200: 'Success'
  401: 'Not authenticated'
  404: 'Not found'
  500: 'Database offline'
