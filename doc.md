# **Software Design Document: LingoJourn**

Version: 1.0  
Date: September 9, 2025  
Status: Final Draft

### **Table of Contents**

1. **Introduction**  
   * 1.1. Project Overview  
   * 1.2. Goals and Objectives  
   * 1.3. Target Audience  
2. **System Architecture**  
   * 2.1. Architectural Diagram  
   * 2.2. Component Breakdown  
3. **User Stories**  
4. **Detailed Feature Specification**  
   * 4.1. User Authentication  
   * 4.2. Dashboard View  
   * 4.3. Journal Creation & Editor View  
   * 4.4. Learning & Progress Analysis  
5. **Database Design**  
   * 5.1. Schema Diagram  
   * 5.2. Detailed Schema (SQL)  
6. **API Specification**  
   * 6.1. Authentication Endpoints  
   * 6.2. Journal Endpoints  
   * 6.3. AI Interaction Endpoints  
7. **AI & Prompt Engineering Strategy**  
   * 7.1. Core Principles  
   * 7.2. Prompt Categories  
8. **Deployment & Hosting**

### **1\. Introduction**

#### **1.1. Project Overview**

LingoJourn is a web-based journaling application enhanced with a sophisticated AI tutor. It aims to transform the daily practice of journaling into an engaging and effective method for learning English as a foreign language. The application provides two distinct modes of writing—a fully AI-guided conversational mode and a manual mode with on-demand AI feedback—to cater to various user preferences and learning styles.

#### **1.2. Goals and Objectives**

* To create an intuitive and encouraging environment for daily English writing practice.  
* To leverage a powerful Large Language Model (LLM) to provide personalized, real-time feedback on grammar, cohesion, and vocabulary.  
* To systematically track a user's learning journey, identify recurring errors, and provide tailored explanations to address specific weaknesses.  
* To deliver a seamless, responsive user experience across desktop and mobile devices.

#### **1.3. Target Audience**

The primary audience is non-native English speakers, from intermediate to advanced levels, who are looking for a practical and consistent way to improve their written and conversational English skills.

### **2\. System Architecture**

The application will be built on a modern, decoupled architecture, designed for self-hosting on a dedicated Linux server.

#### **2.1. Architectural Diagram**

#### **2.2. Component Breakdown**

* **Frontend (Client):** A single-page application (SPA) built with **Vue.js**. It is responsible for all user interface rendering and state management using **Pinia**. It interacts with the backend via a RESTful API.  
* **Backend (Server):** A **FastAPI (Python)** application that serves the API. Its responsibilities include:  
  * Handling business logic (user management, journal operations).  
  * Securely authenticating users via **JWT**.  
  * Interfacing with the database via **SQLAlchemy**.  
  * Managing all interactions with the external **Gemini LLM API**.  
  * Handling file uploads and interfacing with the MinIO server.  
* **Database:** A **PostgreSQL** relational database for persistent data storage.  
* **Image Storage:** A self-hosted **MinIO** instance, providing an S3-compatible API for storing user-uploaded images.

### **3\. User Stories**

* **As a new user, I want to** create an account with a username, email, and password **so that I can** save my journal entries securely.  
* **As a user, I want to** log in to my account **so that I can** access my dashboard and previous journals.  
* **As a user, I want to** see my streak of consecutive journaling days **so that I feel** motivated to write every day.  
* **As a user, I want to** start a new journal entry by chatting with an AI **so that I can** get ideas and write easily even when I don't know what to say.  
* **As a user, I want to** type my journal entry manually **and** ask the AI for feedback when I'm done **so that I can** learn from my mistakes.  
* **As a user, I want to** upload a photo from my device and place it within my journal text **so that I can** add visual context to my memories.  
* **As a user, I want to** see my common mistakes and the AI's explanations in one place **so that I can** review what I've learned and track my progress.

### **4\. Detailed Feature Specification**

#### **4.1. User Authentication**

Standard token-based authentication. The bcrypt library will be used for password hashing. JWT tokens will have a defined expiration time for security.

#### **4.2. Dashboard View**

* **Journal Streak Logic:** The backend will calculate the streak by checking for journal entries on consecutive dates (journal\_date) for the logged-in user. A gap of one day resets the counter.  
* **Journal List:** The API will provide a paginated list of past journals, including the AI-generated title, a content snippet, date, and URLs to any associated images for thumbnail display.

#### **4.3. Journal Creation & Editor View**

* **Mode Switching:** A clear toggle/button in the UI will allow the user to switch between "Chat Mode" and "Editor Mode".  
  * Switching from Chat to Editor will unlock the text area for manual editing.  
  * Switching from Editor to Chat will lock the text area and present the chat interface, sending the current text to the AI for context.  
* **Inline Image Rendering:** When a user uploads an image, it is sent to the backend, stored in MinIO, and a unique markdown-like tag (e.g., \!\[image:unique-image-id.jpg\]) is inserted into the text. The Vue.js frontend will parse this text and replace the tag with an \<img\> element pointing to the corresponding MinIO URL.

#### **4.4. Learning & Progress Analysis**

This data can be presented to the user in a dedicated "My Progress" or "Learning Hub" section of the application.

* **Errors Data:** This view will show a list of learning\_topics the user has made mistakes in (e.g., "Prepositions of Time"). Clicking on a topic will reveal the specific incorrect\_phrases, their repetition\_count, and their status ('active' or 'overcome').  
* **New Learning Points:** This will act as a personalized knowledge base, showing all the unique learning\_points (explanations and suggestions) the AI has provided to the user, grouped by learning\_topic. This allows for easy review.

### **5\. Database Design**

#### **5.1. Schema Diagram**

#### **5.2. Detailed Schema (SQL)**

The schema is designed to track user progress in a structured way.

\-- users table: Stores user credentials and profile information.  
CREATE TABLE users (  
    id SERIAL PRIMARY KEY,  
    username VARCHAR(50) UNIQUE NOT NULL,  
    email VARCHAR(255) UNIQUE NOT NULL,  
    hashed\_password VARCHAR(255) NOT NULL,  
    created\_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())  
);

\-- journals table: The core table for each journal entry.  
CREATE TABLE journals (  
    id SERIAL PRIMARY KEY,  
    user\_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,  
    journal\_date DATE NOT NULL,  
    title VARCHAR(255), \-- AI-generated title  
    content TEXT, \-- The main journal text, may include image placeholders  
    created\_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),  
    updated\_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),  
    UNIQUE(user\_id, journal\_date) \-- Ensures only one journal per user per day  
);

\-- learning\_topics: The master list of learning categories, populated by the system.  
CREATE TABLE learning\_topics (  
    id SERIAL PRIMARY KEY,  
    topic\_name VARCHAR(100) UNIQUE NOT NULL, \-- e.g., 'Prepositions of Time', 'Past Perfect Tense'  
    description TEXT  
);

\-- user\_errors: Tracks every specific error a user makes to identify patterns and progress.  
CREATE TABLE user\_errors (  
    id SERIAL PRIMARY KEY,  
    user\_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,  
    journal\_id INTEGER NOT NULL REFERENCES journals(id) ON DELETE CASCADE,  
    topic\_id INTEGER NOT NULL REFERENCES learning\_topics(id),  
    incorrect\_phrase TEXT NOT NULL,  
    repetition\_count INTEGER DEFAULT 1,  
    status VARCHAR(50) DEFAULT 'active', \-- 'active' or 'overcome'  
    first\_occurred\_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),  
    last\_occurred\_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())  
);

\-- learning\_points: Stores unique AI explanations to avoid redundancy and track teaching methods.  
CREATE TABLE learning\_points (  
    id SERIAL PRIMARY KEY,  
    topic\_id INTEGER NOT NULL REFERENCES learning\_topics(id),  
    explanation\_text TEXT NOT NULL,  
    suggestion\_text TEXT NOT NULL,  
    UNIQUE(topic\_id, explanation\_text) \-- No duplicate explanations for the same topic.  
);

\-- user\_learning\_history: Links which explanation was given for which error instance.  
CREATE TABLE user\_learning\_history (  
    id SERIAL PRIMARY KEY,  
    error\_id INTEGER NOT NULL REFERENCES user\_errors(id) ON DELETE CASCADE,  
    learning\_point\_id INTEGER NOT NULL REFERENCES learning\_points(id),  
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())  
);

### **6\. API Specification**

#### **6.1. Authentication Endpoints**

* POST /api/auth/signup  
  * **Request Body:** { "username": "string", "email": "string", "password": "string" }  
  * **Response (201 Created):** { "id": 1, "username": "string", "email": "string" }  
* POST /api/auth/token  
  * **Request Body (form data):** username=string\&password=string  
  * **Response (200 OK):** { "access\_token": "string", "token\_type": "bearer" }

#### **6.2. Journal Endpoints**

* POST /api/journals  
  * **Request Body:** { "content": "string" }  
  * **Response (201 Created):** { "id": 1, "journal\_date": "YYYY-MM-DD", "content": "string" }  
* GET /api/journals/{journal\_date}  
  * **Response (200 OK):** Full journal object including content and title.  
* PUT /api/journals/{journal\_date}  
  * **Request Body:** { "content": "string" }  
  * **Response (200 OK):** Updated journal object.

#### **6.3. AI Interaction Endpoints**

* POST /api/ai/chat  
  * **Request Body:** { "journal\_id": 1, "message": "string" }  
  * **Response (200 OK):** { "ai\_response": "string", "updated\_journal\_content": "string" }  
* POST /api/ai/feedback  
  * **Request Body:** { "journal\_id": 1, "content": "string" }  
  * **Response (200 OK):** \[ { "error\_type": "Grammar:Tense", "incorrect\_phrase": "I have go", "suggestion": "I have gone", "explanation": "..." }, ... \]

### **7\. AI & Prompt Engineering Strategy**

#### **7.1. Core Principles**

The AI's persona will be encouraging, patient, and clear. All prompts will be engineered to produce concise, helpful, and non-judgmental responses. The system will use a multi-prompt approach for complex tasks.

#### **7.2. Prompt Categories**

1. **Conversational Prompt:** Instructs the AI to act as a friendly conversation partner, asking open-ended questions to elicit details about the user's day.  
2. **Journal Generation Prompt:** Takes a full conversation transcript as input and instructs the AI to synthesize it into a coherent, first-person journal entry.  
3. **Feedback & Analysis Prompt:** A complex, multi-step prompt. It will instruct the AI to:  
   * First, identify grammatical errors, awkward phrasing, and cohesion issues in a given text.  
   * Second, for each error, classify it into a predefined learning\_topic.  
   * Third, generate a concise explanation and a corrected suggestion.  
   * Fourth, format the output as a JSON array for easy parsing by the FastAPI backend.  
4. **Entity Extraction & Title Generation Prompt:** Instructs the AI to read the final journal entry, identify key entities (people, places, weather), and generate a short, fitting title.

### **8\. Deployment & Hosting**

The entire stack will be deployed on a single Linux server, likely using **Docker and Docker Compose** for containerization.

* **Vue.js App:** Will be built into static HTML/CSS/JS files and served by a lightweight web server like **Nginx**.  
* **FastAPI App:** Will be run using an ASGI server like **Uvicorn** behind the Nginx reverse proxy.  
* **PostgreSQL & MinIO:** Will run as separate Docker containers, with persistent data stored in Docker volumes on the host server.