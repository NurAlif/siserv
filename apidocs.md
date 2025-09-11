# **LingoJourn Backend API Documentation**

**Version: 1.0**

This document provides a comprehensive overview of the LingoJourn backend, its structure, and its API endpoints. It is intended for frontend developers who will be building the client-side application.

## **1\. Backend Application Structure**

The backend is built with FastAPI and follows a modular structure to keep the code organized and maintainable.

lingojourn/  
│  
├── .env                    \# Stores environment variables like database URLs and API keys.  
├── .gitignore              \# Specifies files for Git to ignore.  
│  
└── app/                    \# The main Python package for the application.  
    │  
    ├── routers/            \# Contains modules that group related API endpoints.  
    │   ├── auth.py         \# Handles user signup, login, and profile endpoints.  
    │   ├── journals.py     \# Handles CRUD operations for journal entries.  
    │   └── ai.py           \# Handles interactions with the AI (feedback and chat).  
    │  
    ├── services/           \# Contains modules for business logic, especially external services.  
    │   └── ai\_service.py   \# Manages all communication with the Google Gemini API.  
    │  
    ├── config.py           \# Manages loading settings from the .env file.  
    ├── database.py         \# Configures the database connection (SQLAlchemy).  
    ├── main.py             \# The main entry point of the application. Initializes FastAPI and includes the routers.  
    ├── models.py           \# Defines the database table structures using SQLAlchemy ORM.  
    ├── schemas.py          \# Defines the data shapes (request/response bodies) using Pydantic.  
    └── security.py         \# Contains all security-related functions (password hashing, JWT creation/verification).

## **2\. Authentication Flow**

All endpoints, except for signup and login, are protected. The client must include a JWT access token in the Authorization header for all protected requests.

**Flow:**

1. **Sign Up:** The user registers via the POST /api/auth/signup endpoint.  
2. **Log In:** The user logs in using the POST /api/auth/token endpoint. The server responds with an access\_token.  
3. **Store Token:** The frontend client must securely store this token (e.g., in memory or localStorage).  
4. Authorized Requests: For every subsequent request to a protected endpoint, the client must add the following header:  
   Authorization: Bearer \<your\_access\_token\>  
5. **Get User Profile:** It is good practice to call GET /api/auth/me after login to fetch the user's profile data.

## **3\. API Endpoint Reference**

The base URL for the API is http://127.0.0.1:8000.

### **Authentication (/api/auth)**

#### **Sign Up User**

* **Endpoint:** POST /api/auth/signup  
* **Description:** Registers a new user in the system.  
* **Request Body:**  
  {  
    "email": "user@example.com",  
    "username": "newuser",  
    "password": "strongpassword"  
  }

* **Success Response (201 Created):**  
  {  
    "email": "user@example.com",  
    "username": "newuser",  
    "id": 1,  
    "created\_at": "2025-09-10T12:00:00.000Z"  
  }

* **Error Responses:**  
  * 409 Conflict: If the email or username already exists.

#### **Log In for Access Token**

* **Endpoint:** POST /api/auth/token  
* **Description:** Authenticates a user and returns a JWT. The request body must be sent as form data (application/x-www-form-urlencoded).  
* **Request Body (Form Data):**  
  * username: The user's email or username.  
  * password: The user's password.  
* **Success Response (200 OK):**  
  {  
    "access\_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  
    "token\_type": "bearer"  
  }

* **Error Responses:**  
  * 401 Unauthorized: If credentials are incorrect.

#### **Get Current User Profile**

* **Endpoint:** GET /api/auth/me  
* **Protection:** **Required**  
* **Description:** Fetches the profile of the currently authenticated user.  
* **Success Response (200 OK):**  
  {  
    "email": "user@example.com",  
    "username": "newuser",  
    "id": 1,  
    "created\_at": "2025-09-10T12:00:00.000Z"  
  }

### **Journals (/api/journals)**

#### **Create Journal Entry**

* **Endpoint:** POST /api/journals/  
* **Protection:** **Required**  
* **Description:** Creates a new journal entry for the current day. If an entry for today already exists, it will return an error.  
* **Request Body:**  
  {  
    "content": "This is my first journal entry."  
  }

* **Success Response (201 Created):**  
  * The full journal object is returned (see JournalOut schema).  
* **Error Responses:**  
  * 409 Conflict: If a journal for the current date already exists.

#### **Get All Journal Entries**

* **Endpoint:** GET /api/journals/  
* **Protection:** **Required**  
* **Description:** Retrieves a list of all journal entries for the logged-in user.  
* **Success Response (200 OK):**  
  \[  
    { "id": 1, "journal\_date": "2025-09-10", ... },  
    { "id": 2, "journal\_date": "2025-09-09", ... }  
  \]

#### **Get Journal Entry by Date**

* **Endpoint:** GET /api/journals/{journal\_date}  
* **Protection:** **Required**  
* **Description:** Retrieves a single journal entry by its date (format: YYYY-MM-DD).  
* **Success Response (200 OK):**  
  * The full journal object is returned.  
* **Error Responses:**  
  * 404 Not Found: If no entry exists for that date.

#### **Update Journal Entry**

* **Endpoint:** PUT /api/journals/{journal\_date}  
* **Protection:** **Required**  
* **Description:** Updates the content of an existing journal entry.  
* **Request Body:**  
  {  
    "content": "This is the updated content."  
  }

* **Success Response (200 OK):**  
  * The updated journal object is returned.

### **AI (/api/ai)**

#### **Get AI Feedback**

* **Endpoint:** POST /api/ai/feedback/{journal\_date}  
* **Protection:** **Required**  
* **Description:** Analyzes journal text, returns structured feedback, and saves the learning points to the database.  
* **Request Body:**  
  {  
    "text": "I have go to the park yesterday. The weather was very nice."  
  }

* **Success Response (200 OK):**  
  {  
    "feedback": \[  
      {  
        "error\_type": "Grammar: Tense",  
        "incorrect\_phrase": "I have go",  
        "suggestion": "I went",  
        "explanation": "..."  
      }  
    \]  
  }

* **Error Responses:**  
  * 404 Not Found: If the journal entry for the date doesn't exist.  
  * 503 Service Unavailable: If the AI service fails.

#### **Chat with AI**

* **Endpoint:** POST /api/ai/chat/{journal\_date}  
* **Protection:** **Required**  
* **Description:** Sends a message to the AI in the context of a journal entry. The journal's content is updated with the conversation transcript.  
* **Request Body:**  
  {  
    "message": "I had a great day today\!"  
  }

* **Success Response (200 OK):**  
  {  
    "ai\_response": "That's wonderful to hear\! What made it so great?",  
    "updated\_journal\_content": "User: I had a great day today\!\\n\\nLingo: That's wonderful to hear\! What made it so great?"  
  }

* **Error Responses:**  
  * 404 Not Found: If the journal entry for the date doesn't exist.