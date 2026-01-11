# 📚 Advanced Online Book Exchange System

<div align="center">

![Book Exchange](https://img.shields.io/badge/Book-Exchange-blue?style=for-the-badge&logo=book&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask&logoColor=white)

*A modern, full-stack web application that enables users to exchange books through a secure, AI-powered platform with intelligent recommendations and comprehensive exchange management.*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-additional-documentation) • [🤝 Contributing](#-contributing) • [🐛 Issues](../../issues)

</div>

---

## ✨ Key Highlights

- 🔐 **Secure Authentication** - JWT-based auth with role-based access control
- 📚 **Smart Book Management** - Complete CRUD with image upload and validation
- 🔍 **Intelligent Search** - Multi-criteria filtering with real-time suggestions
- 🔄 **Seamless Exchange Flow** - Request → Approve → Track workflow
- 🤖 **AI Recommendations** - TF-IDF and cosine similarity algorithms
- 📊 **User Analytics** - Behavior tracking for personalized experiences
- 📱 **Responsive Design** - Mobile-first approach with Tailwind CSS
- 🧪 **Property-Based Testing** - Advanced testing for maximum reliability

## 🚀 Features

### Core Features

- **User Authentication & Authorization** - Secure JWT-based authentication with role management
- **Book Management** - Complete CRUD operations for book listings with image upload
- **Advanced Search & Filtering** - Multi-criteria search with real-time suggestions
- **Exchange Workflow** - Request, approve, reject, and track book exchanges
- **AI-Powered Recommendations** - TF-IDF and cosine similarity algorithms for personalized suggestions
- **Interaction Tracking** - User behavior analysis for improved recommendations
- **Responsive Design** - Mobile-friendly interface with Tailwind CSS
- **Property-Based Testing** - Advanced testing methodology for reliability

### Advanced Features

- **Real-time Notifications** - Toast notifications for user actions
- **Image Upload & Processing** - Secure file handling with validation
- **Data Export** - Export user data and exchange history
- **Admin Dashboard** - Comprehensive admin panel for system management
- **Search Analytics** - Track and analyze search patterns
- **Recommendation Engine** - Machine learning-based book suggestions

## 🛠️ Technology Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) |
| **Frontend** | ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black) ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white) ![Axios](https://img.shields.io/badge/Axios-5A29E4?logo=axios&logoColor=white) |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white) |
| **Testing** | ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white) ![Hypothesis](https://img.shields.io/badge/Hypothesis-FF6B6B?logoColor=white) |
| **ML/AI** | ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white) |

</div>

### Backend Technologies
- **Python 3.8+** - Core programming language
- **Flask** - Lightweight web framework
- **SQLAlchemy** - ORM for database operations
- **MySQL** - Relational database management
- **JWT** - Secure authentication tokens
- **Marshmallow** - Data serialization and validation
- **scikit-learn** - Machine learning for recommendations
- **Hypothesis** - Property-based testing framework

### Frontend Technologies
- **React 18** - Modern UI framework with hooks
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first styling framework
- **Axios** - Promise-based HTTP client
- **React Toastify** - Elegant notifications
- **React Hook Form** - Performant form handling

## 📋 Prerequisites

<div align="center">

| Requirement | Version | Download Link |
|-------------|---------|---------------|
| ![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white) | 3.8+ | [Download Python](https://python.org/downloads/) |
| ![Node.js](https://img.shields.io/badge/Node.js-16+-339933?logo=node.js&logoColor=white) | 16+ | [Download Node.js](https://nodejs.org/) |
| ![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white) | 8.0+ | [Download MySQL](https://dev.mysql.com/downloads/) |
| ![Git](https://img.shields.io/badge/Git-Latest-F05032?logo=git&logoColor=white) | Latest | [Download Git](https://git-scm.com/) |

</div>

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **Network**: Internet connection for package installation

### Development Tools (Recommended)
- **VS Code** with extensions:
  - Python
  - ES7+ React/Redux/React-Native snippets
  - Tailwind CSS IntelliSense
  - MySQL (for database management)
  - GitLens (for Git integration)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd book-exchange-system
```

### 2. Backend Setup

<details>
<summary>🐍 Python Backend Configuration</summary>

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MySQL credentials

# Initialize database
python setup_mysql.py

# Seed sample data
python seed_data.py

# Run the backend server
python run.py
```

✅ Backend should now be running on http://localhost:5000

</details>

### 3. Frontend Setup

<details>
<summary>⚛️ React Frontend Configuration</summary>

```bash
# Open new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

✅ Frontend should now be running on http://localhost:3000

</details>

### 4. Access the Application

<div align="center">

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | http://localhost:3000 | 🌐 Web Interface |
| **Backend API** | http://localhost:5000 | 🔧 REST API |
| **API Docs** | http://localhost:5000/api/docs | 📚 Documentation |

</div>

> 🎉 **Success!** Your book exchange system is now running. Visit http://localhost:3000 to start using the application.

## 🔧 Configuration

### Environment Variables

Create `.env` file in the backend directory:

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=MajorProject

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### MySQL Database Setup

1. **Install MySQL** and start the service
2. **Create database** (handled by setup_mysql.py)
3. **Update credentials** in backend/.env file

## 📚 Default Login Credentials

After running `python seed_data.py`, you can use these test accounts:

<div align="center">

| Role | Email | Password | Description |
|------|-------|----------|-------------|
| 👑 **Admin** | admin@bookexchange.com | password123 | Full system access |
| 👤 **User 1** | john.doe@example.com | password123 | Regular user account |
| 👤 **User 2** | jane.smith@example.com | password123 | Regular user account |
| 👤 **User 3** | bob.wilson@example.com | password123 | Regular user account |

</div>

> ⚠️ **Security Note**: Change these default passwords in production environments.

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_auth.py -v
```

### Property-Based Tests
```bash
cd backend

# Run property-based tests
python -m pytest tests/test_recommendation_properties.py -v

# Run with detailed output
python -m pytest tests/test_recommendation_properties.py -v -s
```

### Frontend Tests
```bash
cd frontend

# Run React tests
npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false
```

### Test Coverage

| Component | Coverage | Status |
|-----------|----------|--------|
| Authentication | 95% | ✅ |
| Book Management | 92% | ✅ |
| Recommendations | 88% | ✅ |
| Exchange System | 90% | ✅ |

## 📁 Project Structure

```
book-exchange-system/
├── backend/                 # Flask backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── schemas/        # Data validation
│   │   └── utils/          # Helper functions
│   ├── tests/              # Test files
│   ├── config.py           # Configuration
│   └── run.py              # Application entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── contexts/       # React contexts
│   │   └── hooks/          # Custom hooks
│   └── public/             # Static files
└── docs/                   # Documentation
```

## 🔍 Troubleshooting

<details>
<summary>🚨 Common Issues & Solutions</summary>

### Database Connection Issues
```bash
# Error: MySQL connection failed
# Solution:
1. Verify MySQL is running: `mysql --version`
2. Check credentials in backend/.env
3. Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`
4. Run setup script: `python backend/setup_mysql.py`
```

### Port Conflicts
```bash
# Error: Port already in use
# Solution:
# Backend (change port in run.py):
app.run(debug=True, host='0.0.0.0', port=5001)

# Frontend (create frontend/.env):
PORT=3001
```

### Python Dependencies
```bash
# Error: Module not found
# Solution:
1. Activate virtual environment: `source venv/bin/activate`
2. Upgrade pip: `pip install --upgrade pip`
3. Install requirements: `pip install -r requirements.txt`
4. Clear cache: `pip cache purge`
```

### React Build Issues
```bash
# Error: React build failed
# Solution:
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm start
```

### Permission Issues (Linux/macOS)
```bash
# Error: Permission denied
# Solution:
sudo chown -R $USER:$USER .
chmod +x backend/run.py
```

</details>

### 🆘 Getting Help

- 📖 Check our [Documentation](docs/)
- 🐛 Report bugs in [Issues](../../issues)
- 💬 Ask questions in [Discussions](../../discussions)
- 📧 Contact: support@bookexchange.com

## 📖 Additional Documentation

- [User Guide](docs/USER_GUIDE.md) - How to use the application
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Development and customization
- [API Documentation](docs/API_GUIDE.md) - Backend API reference
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Workflow

1. **Fork** the repository
2. **Clone** your fork: `git clone <your-fork-url>`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Add** tests for new features
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to the branch: `git push origin feature/amazing-feature`
8. **Submit** a pull request

### Contribution Guidelines

- 📝 Follow existing code style and conventions
- 🧪 Add tests for new functionality
- 📚 Update documentation as needed
- 🔍 Ensure all tests pass before submitting
- 💬 Write clear, descriptive commit messages

### Areas for Contribution

- 🐛 Bug fixes and improvements
- ✨ New features and enhancements
- 📖 Documentation improvements
- 🧪 Additional test coverage
- 🎨 UI/UX improvements
- 🚀 Performance optimizations

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## 🙏 Acknowledgments

<div align="center">

**Built with ❤️ by passionate developers**

Special thanks to:
- 🎓 **Academic Institution** - For project guidance and support
- 🌟 **Open Source Community** - For amazing tools and libraries
- 👥 **Contributors** - For making this project better
- 📚 **Book Lovers** - For inspiring this platform

---

### 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/guruvardhan-tech-village/book-exchange-system?style=social)
![GitHub forks](https://img.shields.io/github/forks/guruvardhan-tech-village/book-exchange-system?style=social)
![GitHub issues](https://img.shields.io/github/issues/guruvardhan-tech-village/book-exchange-system)
![GitHub pull requests](https://img.shields.io/github/issues-pr/guruvardhan-tech-village/book-exchange-system)

**Made with modern web technologies and best practices**

</div>
