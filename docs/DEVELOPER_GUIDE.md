# Developer Guide - Book Exchange System

This guide provides technical information for developers who want to understand, modify, or extend the Book Exchange System.

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [Database Schema](#database-schema)
5. [API Documentation](#api-documentation)
6. [AI Recommendation Engine](#ai-recommendation-engine)
7. [Testing Framework](#testing-framework)
8. [File Structure Guide](#file-structure-guide)
9. [Common Modifications](#common-modifications)
10. [Deployment](#deployment)

## 🏗️ System Architecture

### Overall Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   Flask Backend │    │   MySQL Database│
│   (Port 3000)   │◄──►│   (Port 5000)   │◄──►│   (Port 3306)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack Details

#### Backend (Flask)
- **Framework**: Flask with Blueprint architecture
- **ORM**: SQLAlchemy for database operations
- **Authentication**: JWT tokens with Flask-JWT-Extended
- **Validation**: Marshmallow schemas
- **AI/ML**: scikit-learn for TF-IDF and cosine similarity
- **Testing**: pytest with Hypothesis for property-based testing

#### Frontend (React)
- **Framework**: React 18 with functional components and hooks
- **Routing**: React Router v6
- **State Management**: React Context API
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Notifications**: React Toastify

#### Database (MySQL)
- **Primary Database**: MySQL 8.0+
- **ORM**: SQLAlchemy with declarative models
- **Migrations**: Flask-Migrate (Alembic)
- **Indexing**: Strategic indexes for performance

## 🔧 Backend Development

### Project Structure
```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   │   ├── user.py          # User model
│   │   ├── book.py          # Book model
│   │   ├── exchange_request.py # Exchange model
│   │   └── user_interaction.py # Interaction tracking
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   ├── books.py         # Book management routes
│   │   ├── exchanges.py     # Exchange routes
│   │   └── recommendations.py # AI recommendation routes
│   ├── services/            # Business logic
│   │   └── recommendation_engine.py # AI engine
│   ├── schemas/             # Data validation
│   │   ├── auth.py          # Auth schemas
│   │   └── book.py          # Book schemas
│   └── utils/               # Helper functions
│       └── auth.py          # Auth utilities
├── tests/                   # Test files
├── config.py               # Configuration settings
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

### Key Backend Files

#### `app/__init__.py` - Flask Application Factory
```python
# Creates and configures Flask app
# Registers blueprints
# Sets up extensions (JWT, CORS, etc.)
# Configures security headers
```

#### `config.py` - Configuration Management
```python
# Database connection strings
# JWT settings
# Environment-specific configurations
# Security settings
```

#### Models (`app/models/`)
- **`user.py`**: User authentication and profile data
- **`book.py`**: Book listings with metadata
- **`exchange_request.py`**: Exchange workflow management
- **`user_interaction.py`**: User behavior tracking for AI

#### Routes (`app/routes/`)
- **`auth.py`**: Registration, login, JWT management
- **`books.py`**: CRUD operations, search, image upload
- **`exchanges.py`**: Exchange request workflow
- **`recommendations.py`**: AI-powered recommendations

#### Services (`app/services/`)
- **`recommendation_engine.py`**: TF-IDF and cosine similarity algorithms

### Adding New API Endpoints

1. **Create Route Function**
```python
# In appropriate route file (e.g., app/routes/books.py)
@books_bp.route('/new-endpoint', methods=['POST'])
@jwt_required()
def new_endpoint():
    try:
        # Your logic here
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

2. **Add Validation Schema** (if needed)
```python
# In app/schemas/
class NewEndpointSchema(Schema):
    field1 = fields.String(required=True)
    field2 = fields.Integer(required=False)
```

3. **Register Blueprint** (if new file)
```python
# In app/__init__.py
from app.routes.new_routes import new_bp
app.register_blueprint(new_bp, url_prefix='/api/new')
```

### Database Migrations

1. **Create Migration**
```bash
cd backend
flask db migrate -m "Description of changes"
```

2. **Apply Migration**
```bash
flask db upgrade
```

3. **Rollback Migration**
```bash
flask db downgrade
```

## ⚛️ Frontend Development

### Project Structure
```
frontend/src/
├── components/              # Reusable components
│   ├── Layout/             # Layout components
│   │   ├── Header.js       # Navigation header
│   │   ├── Footer.js       # Page footer
│   │   └── Layout.js       # Main layout wrapper
│   ├── BookCard.js         # Book display component
│   ├── BookForm.js         # Book creation/editing
│   ├── BookList.js         # Book listing display
│   ├── SearchBar.js        # Search functionality
│   ├── FilterPanel.js      # Advanced filtering
│   ├── RecommendationList.js # AI recommendations
│   ├── ExchangeList.js     # Exchange management
│   └── ProtectedRoute.js   # Route protection
├── pages/                  # Page components
│   ├── Home.js            # Landing page
│   ├── Login.js           # Login page
│   ├── Register.js        # Registration page
│   ├── Books.js           # Book browsing page
│   ├── Dashboard.js       # User dashboard
│   └── Recommendations.js # AI recommendations page
├── services/              # API service layers
│   ├── api.js            # Axios configuration
│   ├── authService.js    # Authentication API
│   ├── bookService.js    # Book management API
│   ├── exchangeService.js # Exchange API
│   └── recommendationService.js # AI API
├── contexts/             # React contexts
│   └── AuthContext.js    # Authentication state
├── hooks/                # Custom hooks
│   └── useInteractionTracking.js # AI tracking
└── App.js               # Main app component
```

### Key Frontend Files

#### `src/App.js` - Main Application
```javascript
// Route configuration
// Context providers
// Global components (toasts, etc.)
```

#### `src/contexts/AuthContext.js` - Authentication State
```javascript
// User authentication state
// Login/logout functions
// JWT token management
// Protected route logic
```

#### Services (`src/services/`)
- **`api.js`**: Axios configuration with interceptors
- **`authService.js`**: Authentication API calls
- **`bookService.js`**: Book management API calls
- **`exchangeService.js`**: Exchange workflow API calls
- **`recommendationService.js`**: AI recommendation API calls

### Adding New Components

1. **Create Component File**
```javascript
// src/components/NewComponent.js
import React, { useState, useEffect } from 'react';

const NewComponent = ({ prop1, prop2 }) => {
  const [state, setState] = useState(null);

  useEffect(() => {
    // Component logic
  }, []);

  return (
    <div className="component-styles">
      {/* Component JSX */}
    </div>
  );
};

export default NewComponent;
```

2. **Add to Parent Component**
```javascript
import NewComponent from './components/NewComponent';

// Use in JSX
<NewComponent prop1="value" prop2={variable} />
```

3. **Add Route** (if it's a page)
```javascript
// In App.js
import NewPage from './pages/NewPage';

// Add to Routes
<Route path="/new-page" element={<NewPage />} />
```

### Styling with Tailwind CSS

The project uses Tailwind CSS for styling. Key classes used:

- **Layout**: `flex`, `grid`, `container`, `mx-auto`
- **Spacing**: `p-4`, `m-2`, `space-x-4`, `gap-6`
- **Colors**: `bg-blue-500`, `text-gray-900`, `border-gray-200`
- **Responsive**: `md:grid-cols-2`, `lg:flex-row`
- **States**: `hover:bg-blue-600`, `focus:ring-2`

## 🗄️ Database Schema

### Entity Relationship Diagram
```
Users (1) ──── (N) Books
  │                │
  │                │
  └── (N) ExchangeRequests (N) ──┘
  │
  └── (N) UserInteractions (N) ── Books
```

### Table Structures

#### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
);
```

#### Books Table
```sql
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20),
    category VARCHAR(50) NOT NULL,
    condition ENUM('new', 'like_new', 'good', 'fair', 'poor') NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    available BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_books_title (title),
    INDEX idx_books_author (author),
    INDEX idx_books_category (category),
    INDEX idx_books_available (available)
);
```

#### Exchange Requests Table
```sql
CREATE TABLE exchange_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    requester_id INT NOT NULL,
    owner_id INT NOT NULL,
    book_id INT NOT NULL,
    message TEXT,
    status ENUM('pending', 'approved', 'rejected', 'completed', 'cancelled') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES users(id),
    FOREIGN KEY (owner_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    INDEX idx_exchange_requests_requester (requester_id),
    INDEX idx_exchange_requests_owner (owner_id),
    INDEX idx_exchange_requests_status (status)
);
```

#### User Interactions Table
```sql
CREATE TABLE user_interactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    interaction_type ENUM('view', 'like', 'request', 'search') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    INDEX idx_user_interactions (user_id, created_at),
    INDEX idx_book_interactions (book_id, interaction_type)
);
```

## 🤖 AI Recommendation Engine

### Algorithm Overview

The recommendation system uses two main approaches:

1. **Content-Based Filtering**: TF-IDF + Cosine Similarity
2. **Collaborative Filtering**: User interaction patterns

### TF-IDF Implementation

Located in `backend/app/services/recommendation_engine.py`:

```python
class RecommendationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=1.0
        )
    
    def build_corpus(self):
        # Combines title, author, category, description
        # Preprocesses text (lowercase, remove special chars)
        # Returns list of processed documents
    
    def compute_similarity_matrix(self):
        # Uses cosine similarity on TF-IDF vectors
        # Returns similarity matrix between all books
    
    def generate_recommendations(self, user_id, num_recommendations=10):
        # Builds user profile from interactions
        # Calculates recommendation scores
        # Returns ranked recommendations with explanations
```

### User Profile Building

```python
def build_user_profile(self, user_id):
    # Analyzes user interactions with weighted scoring:
    # - view: 1.0 weight
    # - like: 2.0 weight  
    # - request: 3.0 weight
    # - search: 0.5 weight
    
    # Aggregates preferences by:
    # - Categories (Fiction, Science, etc.)
    # - Authors (preference patterns)
    # - Content similarity (TF-IDF analysis)
```

### Recommendation Scoring

Final recommendation score combines:
- **Category preference** (40% weight)
- **Author preference** (30% weight)
- **Content similarity** (30% weight)

### Modifying the AI Engine

1. **Adjust Weights**
```python
# In generate_recommendations method
score += category_pref * 0.4  # Change category weight
score += author_pref * 0.3    # Change author weight
score += content_score * 0.3  # Change content weight
```

2. **Add New Interaction Types**
```python
# In user_interaction.py model
interaction_type = db.Column(
    db.Enum('view', 'like', 'request', 'search', 'new_type'), 
    nullable=False
)

# In recommendation_engine.py
interaction_weights = {
    'view': 1.0,
    'like': 2.0,
    'request': 3.0,
    'search': 0.5,
    'new_type': 1.5  # Add new weight
}
```

3. **Modify TF-IDF Parameters**
```python
self.vectorizer = TfidfVectorizer(
    max_features=10000,      # Increase vocabulary size
    stop_words='english',
    ngram_range=(1, 3),      # Include trigrams
    min_df=2,                # Minimum document frequency
    max_df=0.8               # Maximum document frequency
)
```

## 🧪 Testing Framework

### Property-Based Testing

The system uses Hypothesis for property-based testing, which tests universal properties across many generated inputs.

#### Test Structure
```python
# tests/test_recommendation_properties.py
from hypothesis import given, strategies as st
from hypothesis.stateful import RuleBasedStateMachine

class RecommendationEngineStateMachine(RuleBasedStateMachine):
    @rule(target=users, email=st.emails())
    def create_user(self, email):
        # Generate random users
    
    @rule(target=books, user=users, title=st.text())
    def create_book(self, user, title):
        # Generate random books
    
    @rule(user=users)
    def test_recommendation_consistency(self, user):
        # Test that recommendations are consistent
```

#### Key Properties Tested
1. **Recommendation Consistency**: Same user state → same recommendations
2. **No Self-Recommendations**: Users never get their own books
3. **Score Ordering**: Recommendations ordered by relevance
4. **Valid Score Range**: All scores between 0 and 1
5. **Available Books Only**: Only available books recommended
6. **Similarity Symmetry**: Content similarity is symmetric

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_recommendation_properties.py -v

# Property-based tests only
python -m pytest tests/ -k "property" -v

# With coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### Adding New Tests

1. **Unit Tests**
```python
def test_new_feature():
    # Arrange
    setup_data()
    
    # Act
    result = function_to_test()
    
    # Assert
    assert result == expected_value
```

2. **Property Tests**
```python
@given(st.integers(min_value=1, max_value=100))
def test_property(value):
    result = function_to_test(value)
    assert property_holds(result)
```

## 📁 File Structure Guide

### When to Modify Which Files

#### Adding New Features

1. **New API Endpoint**
   - Add route in `backend/app/routes/`
   - Add schema in `backend/app/schemas/` (if needed)
   - Add service logic in `backend/app/services/` (if complex)

2. **New Database Model**
   - Create model in `backend/app/models/`
   - Create migration: `flask db migrate`
   - Update seed data in `backend/seed_data.py`

3. **New Frontend Page**
   - Create component in `frontend/src/pages/`
   - Add route in `frontend/src/App.js`
   - Add navigation link in `frontend/src/components/Layout/Header.js`

4. **New React Component**
   - Create in `frontend/src/components/`
   - Add to parent component imports
   - Style with Tailwind CSS classes

#### Modifying Existing Features

1. **Change API Response Format**
   - Modify route function in `backend/app/routes/`
   - Update schema in `backend/app/schemas/`
   - Update frontend service in `frontend/src/services/`

2. **Change UI Layout**
   - Modify component in `frontend/src/components/`
   - Update Tailwind classes
   - Test responsive design

3. **Change Database Schema**
   - Modify model in `backend/app/models/`
   - Create migration: `flask db migrate`
   - Update existing data if needed

4. **Change Business Logic**
   - Modify service in `backend/app/services/`
   - Update related routes
   - Add/update tests

#### Configuration Changes

1. **Environment Variables**
   - Update `backend/.env`
   - Modify `backend/config.py`
   - Update documentation

2. **Dependencies**
   - Backend: Update `backend/requirements.txt`
   - Frontend: Update `frontend/package.json`
   - Run install commands

3. **Database Connection**
   - Update `backend/config.py`
   - Modify `backend/setup_mysql.py` if needed

## 🚀 Common Modifications

### Adding New Book Categories

1. **Update Database Enum** (if using enum constraint)
```sql
ALTER TABLE books MODIFY COLUMN category VARCHAR(50);
-- Remove enum constraint, use varchar for flexibility
```

2. **Update Frontend Dropdown**
```javascript
// In BookForm.js or FilterPanel.js
const categories = [
  'Fiction', 'Non-Fiction', 'Science', 'History', 
  'Biography', 'Mystery', 'Romance', 'Fantasy',
  'New Category'  // Add here
];
```

### Changing Recommendation Algorithm

1. **Modify Weights**
```python
# In recommendation_engine.py
def generate_recommendations(self, user_id, num_recommendations=10):
    # Adjust these weights
    score += category_pref * 0.5  # Increase category importance
    score += author_pref * 0.2    # Decrease author importance
    score += content_score * 0.3  # Keep content same
```

2. **Add New Factors**
```python
# Add book popularity factor
popularity_score = self._calculate_popularity(book.id)
score += popularity_score * 0.1
```

### Adding New User Roles

1. **Update Database Model**
```python
# In app/models/user.py
role = db.Column(
    db.Enum('user', 'admin', 'moderator', 'premium'), 
    default='user', 
    nullable=False
)
```

2. **Update Authorization Logic**
```python
# In app/utils/auth.py
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in ['admin', required_role]:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### Customizing UI Theme

1. **Update Tailwind Config**
```javascript
// In frontend/tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          // Add custom colors
        }
      }
    }
  }
}
```

2. **Update Component Styles**
```javascript
// Replace bg-blue-500 with bg-primary-500 throughout components
className="bg-primary-500 hover:bg-primary-600 text-white"
```

## 🚀 Deployment

### Production Environment Setup

1. **Environment Variables**
```bash
# Production .env
FLASK_ENV=production
FLASK_DEBUG=False
JWT_SECRET_KEY=your-production-secret-key
MYSQL_HOST=production-db-host
MYSQL_DATABASE=production_db_name
```

2. **Database Setup**
```bash
# Create production database
mysql -u root -p
CREATE DATABASE production_book_exchange;

# Run migrations
flask db upgrade

# Don't run seed_data.py in production
```

3. **Frontend Build**
```bash
cd frontend
npm run build
# Serve build folder with nginx or apache
```

4. **Backend Deployment**
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker Deployment

1. **Create Dockerfile** (Backend)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

2. **Create Dockerfile** (Frontend)
```dockerfile
FROM node:16 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

3. **Docker Compose**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=db
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: book_exchange
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### Performance Optimization

1. **Database Indexing**
```sql
-- Add indexes for common queries
CREATE INDEX idx_books_search ON books(title, author, category);
CREATE INDEX idx_interactions_user_date ON user_interactions(user_id, created_at);
```

2. **Caching** (Redis)
```python
# Add Redis caching for recommendations
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_recommendations(user_id):
    cache_key = f"recommendations:{user_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    return None
```

3. **Frontend Optimization**
```javascript
// Add React.memo for expensive components
const BookCard = React.memo(({ book }) => {
  // Component logic
});

// Use lazy loading for routes
const Recommendations = lazy(() => import('./pages/Recommendations'));
```

---

*This developer guide provides comprehensive technical information for understanding and modifying the Book Exchange System. For user-facing information, see the User Guide.*