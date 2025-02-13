# Stract Challenge

## Description

This project is a local server implemented in Python using Flask. It consumes data from an API and delivers reports in real-time, presented in CSV format with appropriate headers. The reports are accessible through the following endpoints:

- `/`
- `/{{plataforma}}`
- `/{{plataforma}}/resumo`
- `/geral`
- `/geral/resumo`

## Endpoints

### `/`
Returns the developer's name, email, and LinkedIn link.

### `/{{plataforma}}`
Returns a table where each row represents an ad served on the specified platform. The columns include all insight fields of that ad, as well as the name of the account serving the ad. IDs are not returned.

### `/{{plataforma}}/resumo`
Returns a table where each row represents an account that served ads on the specified platform. The columns include the account name, the number of ads served, the total amount spent, and the total number of clicks.

### `/geral`
Returns a table where each row represents an ad served on any platform. The columns include all insight fields of that ad, as well as the name of the account serving the ad. IDs are not returned.

### `/geral/resumo`
Returns a table where each row represents an account that served ads on any platform. The columns include the account name, the number of ads served, the total amount spent, and the total number of clicks.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/caio-rds/StractChallengce.git
   cd <repository_directory>
   

## Running

1. Create and Activate virtual environment:
   ```sh   
    python -m venv venv
    source venv/bin/activate       
   ```

2. Install the dependencies:
   ```sh
    pip install -r requirements.txt
    ```

3. Run the server:
    ```sh
     python app.py
     ```

4. Use Docker:
    ```sh
    docker build -t stract_challenge .
    docker run -p 5000:5000 stract_challenge
    ```

## Usage

Access the endpoints through the browser or a tool like Postman.