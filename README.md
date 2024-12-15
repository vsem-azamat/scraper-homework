# Project Title

This project is designed to track prices of WebShops and notify users via email when prices change.
- *Homework of Azamat Almazbek uulu*

## Features

- Environment variable management with python-decouple
- Configurable tracking period and email settings
- Modular project structure for better readability and maintainability
- Utility functions for common tasks
- Logging for debugging and monitoring

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/vsem-azamat/scraper-homework
    cd scraper-homework
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory or you can use the `.env.dev` file as a template. Then, add the following environment variables:
    ```plaintext
    FILE_LINKS_PATH=./links_example.csv
    PERIOD_TRACKING=3600

    # EMAIL
    SMTP_SERVER=<smtp.gmail.com>
    SMTP_PORT=<smtp_port>
    SMTP_PASSWORD=<smtp_password>
    SENDER_EMAIL=<sender_email>
    RECEIVER_EMAIL=<receiver_email>
    ```

## Usage

1. Run the main script:
    ```sh
    python3 -m main
    ```

2. The script will read the links from the CSV file specified in the `.env` file, track the prices periodically, and send email notifications if there are any changes.
