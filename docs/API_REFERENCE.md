# API Reference - Book Exchange System

This document provides comprehensive documentation for all API endpoints in the Book Exchange System.

## 📋 Table of Contents

1. [Base URL & Authentication](#base-url--authentication)
2. [Authentication Endpoints](#authentication-endpoints)
3. [Book Management Endpoints](#book-management-endpoints)
4. [Exchange Request Endpoints](#exchange-request-endpoints)
5. [AI Recommendation Endpoints](#ai-recommendation-endpoints)
6. [Error Handling](#error-handling)
7. [Response Formats](#response-formats)

## 🌐 Base URL & Authentication

### Base URL
```
http://localhost:5000/api
```

### Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <jwt_token>
```

### Content Type
All requests should use JSON content type:

```http
Content-Type: application/json
```

## 🔐 Authentication Endpoints

### Register User
Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Validation Rules:**
- `email`: Valid email format, unique
- `password`: Minimum 8 characters
- `first_name`: Required, max 50 characters
- `last_name`: Required, max 50 characters

### Login User
Authenticate user and get JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get Current User
Get information about the currently authenticated user.

**Endpoint:** `GET /auth/me`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

## 📚 Book Management Endpoints

### Get All Books
Retrieve all books with optional filtering and pagination.

**Endpoint:** `GET /books`

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 10, max: 100)
- `category` (string): Filter by category
- `condition` (string): Filter by condition
- `author` (string): Filter by author
- `title` (string): Filter by title
- `search` (string): General search across multiple fields
- `available` (boolean): Filter by availability (default: true)

**Example Request:**
```http
GET /books?page=1&per_page=10&category=Fiction&available=true
```

**Response (200 OK):**
```json
{
  "books": [
    {
      "id": 1,
      "user_id": 2,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "9780743273565",
      "category": "Fiction",
      "condition": "good",
      "description": "A classic American novel",
      "image_url": "/uploads/book1.jpg",
      "available": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "owner": {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### Advanced Search
Search books with enhanced filtering capabilities.

**Endpoint:** `GET /books/search`

**Query Parameters:**
- `q` (string): Search query
- `category` (string): Filter by category
- `condition` (string): Filter by condition
- `author` (string): Filter by author
- `title` (string): Filter by title
- `min_year` (integer): Minimum publication year
- `max_year` (integer): Maximum publication year
- `available` (boolean): Filter by availability
- `page` (integer): Page number
- `per_page` (integer): Items per page

**Example Request:**
```http
GET /books/search?q=gatsby&category=Fiction&condition=good
```

**Response:** Same format as Get All Books

### Get Single Book
Retrieve details of a specific book.

**Endpoint:** `GET /books/{book_id}`

**Response (200 OK):**
```json
{
  "book": {
    "id": 1,
    "user_id": 2,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "category": "Fiction",
    "condition": "good",
    "description": "A classic American novel",
    "image_url": "/uploads/book1.jpg",
    "available": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "owner": {
      "id": 2,
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane@example.com"
    }
  }
}
```

### Create Book
Add a new book listing.

**Endpoint:** `POST /books`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "To Kill a Mockingbird",
  "author": "Harper Lee",
  "isbn": "9780061120084",
  "category": "Fiction",
  "condition": "like_new",
  "description": "A gripping tale of racial injustice",
  "image_url": "/uploads/mockingbird.jpg"
}
```

**Response (201 Created):**
```json
{
  "message": "Book listing created successfully",
  "book": {
    "id": 3,
    "user_id": 1,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "isbn": "9780061120084",
    "category": "Fiction",
    "condition": "like_new",
    "description": "A gripping tale of racial injustice",
    "image_url": "/uploads/mockingbird.jpg",
    "available": true,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
}
```

**Validation Rules:**
- `title`: Required, max 200 characters
- `author`: Required, max 100 characters
- `isbn`: Optional, max 20 characters
- `category`: Required, max 50 characters
- `condition`: Required, one of: new, like_new, good, fair, poor
- `description`: Optional, text
- `image_url`: Optional, max 255 characters

### Update Book
Update an existing book listing (owner only).

**Endpoint:** `PUT /books/{book_id}`

**Headers:** `Authorization: Bearer <token>`

**Request Body:** Same as Create Book (all fields optional)

**Response (200 OK):**
```json
{
  "message": "Book listing updated successfully",
  "book": {
    // Updated book object
  }
}
```

### Delete Book
Delete a book listing (owner only).

**Endpoint:** `DELETE /books/{book_id}`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "message": "Book listing deleted successfully"
}
```

### Upload Book Image
Upload an image for a book listing.

**Endpoint:** `POST /books/upload-image`

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body:**
```
Form data with 'image' field containing the image file
```

**Response (200 OK):**
```json
{
  "message": "Image uploaded successfully",
  "image_url": "/uploads/unique-filename.jpg"
}
```

**File Requirements:**
- **Formats**: PNG, JPG, JPEG, GIF
- **Size**: Maximum 5MB
- **Processing**: Automatic unique filename generation

## 🔄 Exchange Request Endpoints

### Get Exchange Requests
Retrieve exchange requests for the authenticated user.

**Endpoint:** `GET /exchanges`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `type` (string): 'sent' or 'received' (default: both)
- `status` (string): Filter by status
- `page` (integer): Page number
- `per_page` (integer): Items per page

**Response (200 OK):**
```json
{
  "sent_requests": [
    {
      "id": 1,
      "requester_id": 1,
      "owner_id": 2,
      "book_id": 3,
      "message": "I'd love to read this book!",
      "status": "pending",
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00",
      "book": {
        "id": 3,
        "title": "1984",
        "author": "George Orwell"
      },
      "owner": {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith"
      }
    }
  ],
  "received_requests": [
    {
      "id": 2,
      "requester_id": 3,
      "owner_id": 1,
      "book_id": 1,
      "message": "Can I borrow this book?",
      "status": "pending",
      "created_at": "2024-01-01T11:00:00",
      "book": {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald"
      },
      "requester": {
        "id": 3,
        "first_name": "Bob",
        "last_name": "Wilson"
      }
    }
  ]
}
```

### Create Exchange Request
Send an exchange request for a book.

**Endpoint:** `POST /exchanges`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "book_id": 3,
  "message": "I'm very interested in this book. Would love to exchange!"
}
```

**Response (201 Created):**
```json
{
  "message": "Exchange request sent successfully",
  "exchange_request": {
    "id": 4,
    "requester_id": 1,
    "owner_id": 2,
    "book_id": 3,
    "message": "I'm very interested in this book. Would love to exchange!",
    "status": "pending",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

### Update Exchange Request Status
Approve, reject, or complete an exchange request (owner only).

**Endpoint:** `PUT /exchanges/{request_id}`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "status": "approved",
  "response_message": "Sure! Let's arrange the exchange."
}
```

**Response (200 OK):**
```json
{
  "message": "Exchange request updated successfully",
  "exchange_request": {
    "id": 4,
    "status": "approved",
    "response_message": "Sure! Let's arrange the exchange.",
    "updated_at": "2024-01-01T13:00:00"
  }
}
```

**Valid Status Values:**
- `pending`: Initial status
- `approved`: Owner accepted the request
- `rejected`: Owner declined the request
- `completed`: Exchange was completed
- `cancelled`: Request was cancelled

### Get Exchange Request Details
Get detailed information about a specific exchange request.

**Endpoint:** `GET /exchanges/{request_id}`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "exchange_request": {
    "id": 4,
    "requester_id": 1,
    "owner_id": 2,
    "book_id": 3,
    "message": "I'm very interested in this book.",
    "response_message": "Sure! Let's arrange the exchange.",
    "status": "approved",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T13:00:00",
    "book": {
      "id": 3,
      "title": "1984",
      "author": "George Orwell",
      "condition": "good",
      "image_url": "/uploads/1984.jpg"
    },
    "requester": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    },
    "owner": {
      "id": 2,
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane@example.com"
    }
  }
}
```

## 🤖 AI Recommendation Endpoints

### Get Personalized Recommendations
Get AI-powered book recommendations for the authenticated user.

**Endpoint:** `GET /recommendations`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `limit` (integer): Number of recommendations (1-50, default: 10)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "book": {
          "id": 5,
          "title": "Brave New World",
          "author": "Aldous Huxley",
          "category": "Science Fiction",
          "condition": "good",
          "description": "A dystopian social science fiction novel",
          "image_url": "/uploads/brave-new-world.jpg",
          "available": true,
          "owner": {
            "id": 3,
            "first_name": "Alice",
            "last_name": "Johnson"
          }
        },
        "relevance_score": 0.87,
        "recommendation_reason": "Recommended because you've shown interest in Science Fiction books and you've liked books by similar authors"
      }
    ],
    "count": 5,
    "user_id": 1
  }
}
```

### Get Similar Books
Get books similar to a specific book based on content analysis.

**Endpoint:** `GET /recommendations/similar/{book_id}`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `limit` (integer): Number of similar books (1-50, default: 10)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "similar_books": [
      {
        "book": {
          "id": 6,
          "title": "Animal Farm",
          "author": "George Orwell",
          "category": "Fiction",
          "condition": "like_new"
        },
        "similarity_score": 0.92
      }
    ],
    "count": 3,
    "reference_book": {
      "id": 3,
      "title": "1984",
      "author": "George Orwell"
    }
  }
}
```

### Record User Interaction
Track user interactions with books for AI learning.

**Endpoint:** `POST /interactions`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "book_id": 5,
  "interaction_type": "like"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "interaction": {
      "id": 10,
      "user_id": 1,
      "book_id": 5,
      "interaction_type": "like",
      "created_at": "2024-01-01T14:00:00"
    },
    "message": "Interaction recorded successfully"
  }
}
```

**Valid Interaction Types:**
- `view`: User viewed the book
- `like`: User liked the book
- `request`: User requested the book for exchange
- `search`: User searched for the book

### Get Recommendation Statistics
Get user's interaction statistics and recommendation insights.

**Endpoint:** `GET /recommendations/stats`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total_interactions": 25,
    "interaction_breakdown": {
      "view": 15,
      "like": 7,
      "request": 3,
      "search": 0
    },
    "top_categories": [
      {
        "category": "Science Fiction",
        "interaction_count": 12
      },
      {
        "category": "Fiction",
        "interaction_count": 8
      }
    ],
    "has_sufficient_data": true
  }
}
```

### Refresh Recommendation Model
Update the AI recommendation model with latest data.

**Endpoint:** `POST /recommendations/refresh`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Recommendation model refreshed successfully"
}
```

## ❌ Error Handling

### Error Response Format
All errors follow a consistent format:

```json
{
  "success": false,
  "error": "Error Type",
  "message": "Human-readable error message",
  "details": "Additional error details (optional)"
}
```

### HTTP Status Codes

#### Success Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content returned

#### Client Error Codes
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate email)
- `422 Unprocessable Entity`: Validation errors

#### Server Error Codes
- `500 Internal Server Error`: Server-side error

### Common Error Examples

#### Validation Error (400)
```json
{
  "success": false,
  "error": "Validation Error",
  "message": {
    "email": ["Not a valid email address."],
    "password": ["Shorter than minimum length 8."]
  }
}
```

#### Authentication Error (401)
```json
{
  "success": false,
  "error": "Authentication Required",
  "message": "Missing Authorization Header"
}
```

#### Permission Error (403)
```json
{
  "success": false,
  "error": "Forbidden",
  "message": "You can only edit your own book listings"
}
```

#### Not Found Error (404)
```json
{
  "success": false,
  "error": "Not Found",
  "message": "Book not found"
}
```

#### Server Error (500)
```json
{
  "success": false,
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## 📝 Response Formats

### Pagination Format
Endpoints that return lists include pagination information:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### Date Format
All dates are returned in ISO 8601 format:
```
"2024-01-01T12:00:00"
```

### Boolean Values
Boolean values are returned as JSON booleans:
```json
{
  "available": true,
  "has_next": false
}
```

### Null Values
Missing or null values are explicitly returned as `null`:
```json
{
  "description": null,
  "image_url": null
}
```

## 🔧 Rate Limiting

Currently, no rate limiting is implemented, but it's recommended for production:

- **Authentication endpoints**: 5 requests per minute
- **General endpoints**: 100 requests per minute
- **File upload endpoints**: 10 requests per minute

## 📚 SDK Examples

### JavaScript/Axios Example
```javascript
// Configure axios instance
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login
const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  localStorage.setItem('token', response.data.access_token);
  return response.data;
};

// Get books
const getBooks = async (params = {}) => {
  const response = await api.get('/books', { params });
  return response.data;
};

// Create book
const createBook = async (bookData) => {
  const response = await api.post('/books', bookData);
  return response.data;
};
```

### Python/Requests Example
```python
import requests

class BookExchangeAPI:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url
        self.token = None
    
    def login(self, email, password):
        response = requests.post(f'{self.base_url}/auth/login', json={
            'email': email,
            'password': password
        })
        data = response.json()
        self.token = data['access_token']
        return data
    
    def _headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def get_books(self, **params):
        response = requests.get(
            f'{self.base_url}/books',
            headers=self._headers(),
            params=params
        )
        return response.json()
    
    def create_book(self, book_data):
        response = requests.post(
            f'{self.base_url}/books',
            headers=self._headers(),
            json=book_data
        )
        return response.json()
```

---

*This API reference provides comprehensive documentation for all endpoints in the Book Exchange System. For implementation examples and integration guides, see the Developer Guide.*