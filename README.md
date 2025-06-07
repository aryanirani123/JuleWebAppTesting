# JuleWebAppTesting

This is a simple Flask web application that allows users to submit feedback and view all submitted feedback. It was originally designed to use a local JSON file for storage and has been updated to use Google Cloud Firestore as its backend database.

## Features

- Submit feedback with a name and message.
- View a list of all feedback submitted, ordered by timestamp.
- Uses Google Cloud Firestore for persistent data storage.
- Includes unit tests for the Firestore service module.

## Project Structure

```
/
|-- app.py                  # Main Flask application
|-- firestore_service.py    # Module for Firestore interactions (add/get feedback)
|-- requirements.txt        # Python dependencies
|-- setup.txt               # Instructions for setting up Firestore
|-- templates/
|   |-- index.html          # Homepage with feedback submission form
|   |-- feedback.html       # Page to display feedback
|-- tests/
|   |-- test_firestore_service.py # Unit tests for Firestore service
|-- .gitignore
|-- LICENSE
|-- README.md
```

## Backend Setup: Firestore

This application uses Google Cloud Firestore to store and manage feedback data.
To set up Firestore for this project, please follow the detailed instructions in the [`setup.txt`](./setup.txt) file.

**Dependencies:**
The application requires the `google-cloud-firestore` Python package. It is listed in `requirements.txt` and can be installed by running:
```bash
pip install -r requirements.txt
```
Make sure you have set up your Google Cloud project and authentication as described in `setup.txt` before running the application.

## Running the Application

To run the application locally:

1.  **Clone the repository** (if you haven't already).
2.  **Set up Python Environment**: It's recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up Firestore**: Follow the instructions in [`setup.txt`](./setup.txt) to configure your Google Cloud project and authentication. Crucially, ensure the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is correctly set to the path of your service account JSON key file.
5.  **Run the Application**:
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

## Testing

Unit tests for the Firestore service module can be run using:
```bash
python -m unittest tests.test_firestore_service.TestFirestoreService
```
Ensure dependencies are installed before running tests.