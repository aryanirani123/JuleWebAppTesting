from google.cloud import firestore

# Initialize Firestore client
# It's good practice to initialize it once and reuse it.
# Ensure your Google Cloud credentials are set up in the environment
# where this code will run (e.g., GOOGLE_APPLICATION_CREDENTIALS).
db = firestore.Client()

def add_feedback(name: str, message: str):
    """Adds a new feedback document to the 'feedback' collection in Firestore.

    Args:
        name (str): The name of the person submitting feedback.
        message (str): The feedback message.
    """
    if not name or not message:
        raise ValueError("Name and message cannot be empty.")

    feedback_collection = db.collection('feedback')
    feedback_collection.add({
        'name': name,
        'message': message,
        'timestamp': firestore.SERVER_TIMESTAMP  # Optional: add a server timestamp
    })

def get_feedback() -> list:
    """Retrieves all documents from the 'feedback' collection, ordered by timestamp.

    Returns:
        list: A list of feedback documents (dictionaries).
    """
    feedback_collection = db.collection('feedback').order_by(
        'timestamp', direction=firestore.Query.DESCENDING  # Optional: order by timestamp
    )
    feedback_items = []
    for doc in feedback_collection.stream():
        item = doc.to_dict()
        item['id'] = doc.id  # Optionally include the document ID
        feedback_items.append(item)
    return feedback_items

if __name__ == '__main__':
    # Example usage (optional, for testing purposes)
    # Make sure Firestore is set up and credentials are available
    print("Attempting to add feedback...")
    try:
        add_feedback("Test User", "This is a test feedback message from firestore_service.py.")
        print("Feedback added successfully.")
    except Exception as e:
        print(f"Error adding feedback: {e}")

    print("\nFetching feedback...")
    try:
        all_feedback = get_feedback()
        if all_feedback:
            print("Retrieved feedback:")
            for item in all_feedback:
                print(f"- {item.get('name')}: {item.get('message')} (ID: {item.get('id')}, Timestamp: {item.get('timestamp')})")
        else:
            print("No feedback found.")
    except Exception as e:
        print(f"Error fetching feedback: {e}")
