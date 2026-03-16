# INFOBOT - College Notice Board with Chatbot

A full-stack Django web application for college notices with a rule-based chatbot, using MongoDB.

## Prerequisites
- Python 3.8+
- MongoDB (running locally or a connection string)
- VS Code (recommended)

## Setup Instructions

1.  **Clone/Open the project**
    Open the `infobot_project` folder in VS Code.

2.  **Create a Virtual Environment**
    Open the terminal in VS Code (Ctrl+`) and run:
    ```bash
    python -m venv venv
    ```

3.  **Activate Virtual Environment**
    - Windows:
      ```bash
      venv\Scripts\activate
      ```
    - Mac/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```

5.  **MongoDB Setup**
    - Ensure MongoDB is running locally on `localhost:27017`.
    - Create a database named `noticeboard_db` (optional, Djongo will create it).

6.  **Run Migrations**
    ```bash
    cd infobot
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Create Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run Server**
    ```bash
    python manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000/`.

## Features
- **Admin**: Login, Add/Edit/Delete notices.
- **Student**: View notices, filter by category, use Chatbot.
- **Chatbot**: Ask "exam notices", "events", etc.

## Project Structure
- `infobot/`: Django project settings.
- `notices/`: Main app containing models, views, and chatbot logic.
- `templates/`: HTML files.
- `static/`: CSS and JS files.
