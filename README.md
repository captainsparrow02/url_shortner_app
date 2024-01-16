# FastAPI URL Shortener Backend

This FastAPI-based backend application serves as a URL shortener, allowing users to create short URLs for easier sharing. The project utilizes Pydantic for data modeling, SQLAlchemy as the ORM for defining schemas, and SQLite 3 as the lightweight database.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [API Endpoints](#api-endpoints)
    -   [Root](#root)
    -   [Create URL](#create-url)
    -   [Forward to Target URL](#forward-to-target-url)
    -   [Administrative Info](#administrative-info)
    -   [Delete URL](#delete-url)
-   [Data Models](#data-models)
    -   [URLBase](#urlbase)
    -   [URLInfo](#urlinfo)
    -   [HTTPValidationError](#httpvalidationerror)
    -   [ValidationError](#validationerror)

## Installation

1.  Clone the repository:
    
```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```
    
2.  Install dependencies:
    
```bash 
pip install -r requirements.txt
```
    
3.  Run the FastAPI application:
    
```bash 
uvicorn app:app --reload
```
The application should now be running at `http://localhost:8000`.

## Usage

Once the application is running, you can interact with it through the provided API endpoints. Refer to the API documentation for details on each endpoint.

## API Endpoints

### Root

-   **Description**: Root endpoint providing basic information.
-   **Method**: GET
-   **URL**: `/`

### Create URL

-   **Description**: Create a short URL.
-   **Method**: POST
-   **URL**: `/url`
-   **Request Body**: JSON, [URLBase](#urlbase)
-   **Response**: JSON, [URLInfo](#urlinfo)

### Forward to Target URL

-   **Description**: Redirect to the target URL associated with the provided short URL key.
-   **Method**: GET
-   **URL**: `/{url_key}`
-   **Path Parameter**: `url_key` (string)
-   **Response**: JSON

### Administrative Info

-   **Description**: Retrieve administrative information about a short URL using the secret key.    
-   **Method**: GET    
-   **URL**: `/admin/{secret_key}`    
-   **Path Parameter**: `secret_key` (string)    
-   **Response**: JSON, [URLInfo](#urlinfo)    
-   **Description**: Delete a short URL using the secret key.    
-   **Method**: DELETE    
-   **URL**: `/admin/{secret_key}`
-   **Path Parameter**: `secret_key` (string)
-   **Response**: JSON

### Delete URL

-   **Description**: Delete a short URL using the secret key.
-   **Method**: DELETE
-   **URL**: `/admin/{secret_key}`
-   **Path Parameter**: `secret_key` (string)
-   **Response**: JSON


## Data Models

### URLBase

-   **Properties**:
    -   `target_url` (string, required): The target URL to shorten.

### URLInfo

-   **Properties**:
    -   `target_url` (string): The original target URL.
    -   `clicks` (integer): Number of clicks on the short URL.
    -   `is_active` (boolean): Indicates whether the short URL is active.
    -   `url` (string): The short URL.
    -   `admin_url` (string): Administrative URL for further actions.

### HTTPValidationError

-   **Properties**:
    -   `detail` (array of [ValidationError](#validationerror), required): Details about validation errors.

### ValidationError

-   **Properties**:
    -   `loc` (array of any): Location of the validation error.
    -   `msg` (string): Error message.
    -   `type` (string): Type of error.

Feel free to explore and integrate these endpoints into your frontend or other applications. Happy URL shortening!