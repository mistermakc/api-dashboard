# REST API Documentation - Flask-RestX

This document highlights the REST API built using Flask-RestX for a web application that visualizes KPIs for H&M aggregated through article, transaction, and customer data.

## Overview

To improve the request time for the API, dedicated KPI tables have been created which use the underyling three data files. This REST API is designed to provide access to the following resources:

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

This includes operations for fetching the given resources, including error handling. The API uses as a predefined API key for authentication and authorization. 

## Required Modules

Before using the REST API, the following Python modules must be installed:

1. Flask: `pip install Flask`
2. Flask-RESTx: `pip install flask-restx`
3. SQLAlchemy: `pip install sqlalchemy`
4. Retry: `pip install retry`

## Endpoints

### Revenue

#### GET /api/v1/articles

- Description: Fetches all articles.
- Authorization: Requires a valid JWT access token.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of articles.

### Transactions

#### GET /api/v1/transactions

- Description: Fetches all transactions.
- Authorization: Requires a valid JWT access token.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of transactions.

### Customers

#### GET /api/v1/customers

- Description: Fetches all customers.
- Authorization: Requires a valid JWT access token.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of customers.

### Users

#### GET /api/v1/users/login

- Description: Logs in a user and generates access and refresh tokens.
- Request:
  - Query parameters:
    - username (string): The username of the user.
    - password (string): The password of the user.
- Response:
  - Status code: 200 on success.
  - Body: JSON object containing the user details, access token, refresh token, and their respective expiration times.

#### POST /api/v1/users/register

- Description: Registers a new user and generates access and refresh tokens.
- Request:
  - Query parameters:
    - username (string): The desired username of the new user.
    - password (string): The desired password of the new user.
- Response:
  - Status code: 200 on success.
  - Body: JSON object containing the user details, access token, refresh token, and their respective expiration times.

#### POST /api/v1/users/refresh

- Description: Refreshes an access token using a valid refresh token.
- Authorization: Requires a valid JWT refresh token.
- Response:
  - Status code: 200 on success.
  - Body: JSON object containing the new access token and its expiration time.

## Error Handling

In case of errors, the API will return a JSON object containing an error message and an appropriate HTTP status code.

## Authentication and Authorization

The API uses JWT for authentication and authorization. Users must log in or register to obtain a valid access token, which must be included in the Authorization header of requests to protected endpoints. Access tokens have a limited lifetime, and users can refresh them using their refresh token at the /api/v1/users/refresh endpoint.
