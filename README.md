# Linguabot Backend

This is the backend for the Linguabot conversational AI application. It provides APIs for managing conversations, messages, and user authentication. The backend is built using FastAPI and integrates with MongoDB for storing conversations and messages.

---

## Table of Contents
- [Features](#features)
- [API Endpoints](#api-endpoints)
  - [Conversations](#conversations)
  - [Messages](#messages)
  - [Authentication](#authentication)
- [Request and Response Examples](#request-and-response-examples)
- [Setup and Installation](#setup-and-installation)

---

## Features
- Create, retrieve, and delete conversations.
- Add and retrieve messages in a conversation.
- JWT-based authentication for secure access.
- Integration with Gemini AI for generating bot replies.

---

## API Endpoints

### Conversations
#### 1. Create a Conversation
- **Endpoint:** `POST /conversation/`
- **Description:** Creates a new conversation.
- **Input:**
  ```json
  {
    "title": "Chat with AI",
    "description": "A conversation with the AI bot",
    "image": "https://example.com/image.png"
  }
  ```
- **Output:**
  ```json
  {
    "id": "680458b3324cd9ea63434145",
    "title": "Chat with AI",
    "description": "A conversation with the AI bot",
    "image": "https://example.com/image.png",
    "user_id": "12345",
    "created_at": "2025-04-25T12:00:00Z",
    "last_message_at": null
  }
  ```

#### 2. Get All Conversations for a User
- **Endpoint:** `GET /conversation/`
- **Description:** Retrieves all conversations for the authenticated user.
- **Input:** JWT token in the `Authorization` header.
- **Output:**
  ```json
  [
    {
      "id": "680458b3324cd9ea63434145",
      "title": "Chat with AI",
      "description": "A conversation with the AI bot",
      "image": "https://example.com/image.png",
      "user_id": "12345",
      "created_at": "2025-04-25T12:00:00Z",
      "last_message_at": "2025-04-25T12:30:00Z"
    }
  ]
  ```

#### 3. Delete a Conversation
- **Endpoint:** `DELETE /conversation/{conversation_id}`
- **Description:** Deletes a conversation by its ID.
- **Input:**
  - Path parameter: `conversation_id` (string)
  - JWT token in the `Authorization` header.
- **Output:**
  ```json
  {
    "detail": "Conversation deleted successfully"
  }
  ```

---

### Messages
#### 1. Add a Message
- **Endpoint:** `POST /message/{conversation_id}/message`
- **Description:** Adds a message to a conversation and generates a bot reply.
- **Input:**
  - Path parameter: `conversation_id` (string)
  - Request body:
    ```json
    {
      "content": "Hello, AI!",
      "sender_id": "user",
      "message_type": "text",           // optional, defaults to "text"
      "embedding": [0.1, 0.2],          // optional, can be omitted
      "reply_to": "message_id"          // optional, can be omitted
    }
    ```
- **Output:**
  ```json
  {
    "_id": "string",
    "content": "string",
    "sender_id": "string",
    "message_type": "text",
    "embedding": [0.1, 0.2],
    "reply_to": "message_id",
    "conversation_id": "string",
    "timestamp": "2025-06-28T12:00:00",
    "corrections": "string",
    "grammar_score": 0.0
  }
  ```

#### 2. Get Conversation History
- **Endpoint:** `GET /message/{conversation_id}/history`
- **Description:** Retrieves the message history for a conversation.
- **Input:**
  - Path parameter: `conversation_id` (string)
  - Query parameters:
    - `limit` (integer, optional): Number of messages to retrieve (default: 20).
    - `offset` (integer, optional): Number of messages to skip (default: 0).
- **Output:**
  ```json
  [
    {
      "_id": "string",
      "content": "string",
      "sender_id": "string",
      "message_type": "text",
      "embedding": [0.1, 0.2],
      "reply_to": "message_id",
      "conversation_id": "string",
      "timestamp": "2025-06-28T12:00:00",
      "corrections": "string",
      "grammar_score": 0.0
    }
  ]
  ```

---

### Authentication
#### 1. Login
- **Endpoint:** `POST /auth/login`
- **Description:** Authenticates a user and returns a JWT token.
- **Input:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Output:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

#### 2. Get Current User
- **Endpoint:** `GET /auth/user`
- **Description:** Retrieves the details of the authenticated user.
- **Input:** JWT token in the `Authorization` header.
- **Output:**
  ```json
  {
    "id": "12345",
    "email": "user@example.com",
    "username": "JohnDoe"
  }
  ```

---

## Request and Response Examples

### Authorization Header
All protected routes require the `Authorization` header with the JWT token:
```
Authorization: Bearer <your_token>
```

---

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/linguabot-backend.git
   cd linguabot-backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key
     ALGORITHM=HS256
     GEMINI_API_KEY=your_gemini_api_key
     ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the API documentation:
   - Open your browser and go to `http://127.0.0.1:8000/docs`.

---

## Contributing
Feel free to submit issues or pull requests to improve this project.

---

## License
This project is licensed under the MIT License.