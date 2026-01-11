# Installation Guide - Book Exchange System

This guide provides step-by-step instructions for setting up the Book Exchange System on a new laptop or development environment.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Software Installation](#software-installation)
3. [Development Tools Setup](#development-tools-setup)
4. [Project Setup](#project-setup)
5. [Database Configuration](#database-configuration)
6. [Running the Application](#running-the-application)
7. [Verification Steps](#verification-steps)
8. [Troubleshooting](#troubleshooting)

## 💻 System Requirements

### Minimum Hardware Requirements
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space
- **CPU**: Dual-core processor (Quad-core recommended)
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+

### Network Requirements
- Internet connection for downloading dependencies
- Port 3000 (Frontend) and 5000 (Backend) available
- Port 3306 (MySQL) available

## 🛠️ Software Installation

### 1. Python Installation

#### Windows
1. **Download Python**
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.8 or higher (3.9+ recommended)
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

#### macOS
1. **Using Homebrew** (Recommended)
   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python@3.9
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### 2. Node.js Installation

#### All Platforms
1. **Download Node.js**
   - Go to [nodejs.org](https://nodejs.org/)
   - Download LTS version (16.x or higher)
   - Run the installer with default settings

2. **Verify Installation**
   ```bash
   node --version
   npm --version
   ```

#### Alternative: Using Node Version Manager (NVM)
```bash
# Install NVM (Linux/macOS)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal, then install Node.js
nvm install --lts
nvm use --lts
```

### 3. MySQL Installation

#### Windows
1. **Download MySQL Installer**
   - Go to [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
   - Download MySQL Installer for Windows
   - Choose "Custom" installation

2. **Installation Steps**
   - Select "MySQL Server" and "MySQL Workbench"
   - Set root password (remember this!)
   - Configure as Windows Service
   - Complete installation

3. **Verify Installation**
   ```cmd
   mysql --version
   ```

#### macOS
```bash
# Using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation (set root password)
mysql_secure_installation
```

#### Linux (Ubuntu/Debian)
```bash
# Install MySQL Server
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 4. Git Installation

#### Windows
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings
3. Verify: `git --version`

#### macOS
```bash
# Using Homebrew
brew install git

# Or use Xcode Command Line Tools
xcode-select --install
```

#### Linux
```bash
sudo apt install git
```

## 🔧 Development Tools Setup

### 1. Visual Studio Code (Recommended)

#### Installation
1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install with default settings

#### Essential Extensions
Install these extensions for better development experience:

1. **Python Extensions**
   - Python (Microsoft)
   - Python Docstring Generator
   - autoDocstring

2. **JavaScript/React Extensions**
   - ES7+ React/Redux/React-Native snippets
   - Bracket Pair Colorizer
   - Auto Rename Tag
   - JavaScript (ES6) code snippets

3. **General Development**
   - GitLens
   - Live Server
   - Prettier - Code formatter
   - Material Icon Theme

4. **Database Extensions**
   - MySQL (Jun Han)
   - SQLTools

5. **Tailwind CSS**
   - Tailwind CSS IntelliSense

#### VS Code Configuration
Create `.vscode/settings.json` in project root:
```json
{
  "python.defaultInterpreterPath": "./backend/venv/Scripts/python",
  "python.terminal.activateEnvironment": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  },
  "tailwindCSS.includeLanguages": {
    "javascript": "javascript",
    "html": "html"
  }
}
```

### 2. Alternative IDEs

#### PyCharm (Python-focused)
- Download from [jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)
- Community edition is free
- Excellent for Python development

#### WebStorm (JavaScript-focused)
- Download from [jetbrains.com/webstorm/](https://www.jetbrains.com/webstorm/)
- 30-day free trial, then paid
- Excellent for React development

### 3. Database Management Tools

#### MySQL Workbench (Free)
- Usually installed with MySQL
- Good for database design and queries

#### phpMyAdmin (Web-based)
```bash
# Install via XAMPP/WAMP (Windows)
# Or install separately on Linux/macOS
```

#### DBeaver (Free, Cross-platform)
- Download from [dbeaver.io](https://dbeaver.io/)
- Supports multiple database types

## 📁 Project Setup

### 1. Clone or Download Project

#### Option A: Clone from Repository
```bash
git clone <repository-url>
cd book-exchange-system
```

#### Option B: Download ZIP
1. Download project ZIP file
2. Extract to desired location
3. Open terminal in project directory

### 2. Backend Setup

#### Create Virtual Environment
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
# Windows:
python -m venv venv

# macOS/Linux:
python3 -m venv venv
```

#### Activate Virtual Environment
```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

#### Install Python Dependencies
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

#### Create Environment File
```bash
# Copy example environment file
# Windows:
copy .env.example .env

# macOS/Linux:
cp .env.example .env
```

#### Edit Environment Variables
Open `.env` file and configure:
```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=MajorProject

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-make-it-long-and-random
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
# Open new terminal window/tab
cd frontend
```

#### Install Node.js Dependencies
```bash
npm install
```

#### Create Frontend Environment File (Optional)
```bash
# Create .env file in frontend directory
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

## 🗄️ Database Configuration

### 1. Start MySQL Service

#### Windows
- MySQL should start automatically as a service
- Or use MySQL Workbench to start

#### macOS
```bash
brew services start mysql
```

#### Linux
```bash
sudo systemctl start mysql
```

### 2. Create Database User (Optional)

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create dedicated user for the application
CREATE USER 'bookexchange'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON MajorProject.* TO 'bookexchange'@'localhost';
GRANT ALL PRIVILEGES ON MajorProject_test.* TO 'bookexchange'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Initialize Database

```bash
# Ensure you're in backend directory with activated virtual environment
cd backend
# Activate venv if not already activated

# Run database setup script
python setup_mysql.py
```

### 4. Seed Sample Data

```bash
# Add sample data for testing
python seed_data.py
```

## 🚀 Running the Application

### 1. Start Backend Server

```bash
# In backend directory with activated virtual environment
python run.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 2. Start Frontend Server

```bash
# In new terminal, navigate to frontend directory
cd frontend

# Start React development server
npm start
```

You should see:
```
Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

### 3. Access Application

1. **Open Browser**
   - Navigate to `http://localhost:3000`
   - You should see the Book Exchange homepage

2. **Test Login**
   - Use sample credentials: `john.doe@example.com` / `password123`
   - Or register a new account

## ✅ Verification Steps

### 1. Backend Verification

#### Test API Endpoints
```bash
# Test health endpoint
curl http://localhost:5000/api/auth/register

# Should return method not allowed (405) - this is correct
```

#### Check Database Connection
```bash
# In backend directory
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    print('Database connection successful!')
    from app.models.user import User
    print(f'Users in database: {User.query.count()}')
"
```

### 2. Frontend Verification

#### Check React App
1. Navigate to `http://localhost:3000`
2. Verify homepage loads
3. Check navigation links work
4. Test registration/login forms

#### Check API Integration
1. Register a new account
2. Login with credentials
3. Navigate to Books page
4. Verify data loads from backend

### 3. AI Recommendations Verification

1. **Login** with sample account
2. **Browse books** and click like buttons
3. **Navigate to Recommendations** page
4. **Verify** personalized recommendations appear

### 4. Full Workflow Test

1. **Register** new account
2. **Add** a book listing with image
3. **Search** for books
4. **Request** book exchange
5. **Check** dashboard for requests
6. **View** AI recommendations

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Python/Pip Issues

**Issue**: `python` command not found
```bash
# Windows: Use py instead
py --version
py -m pip install -r requirements.txt

# macOS/Linux: Use python3
python3 --version
python3 -m pip install -r requirements.txt
```

**Issue**: Permission denied installing packages
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or ensure virtual environment is activated
```

#### 2. MySQL Connection Issues

**Issue**: Access denied for user 'root'
```bash
# Reset MySQL root password
# Windows: Use MySQL Installer to reconfigure
# macOS: 
brew services stop mysql
mysqld_safe --skip-grant-tables &
mysql -u root
# Then reset password

# Linux:
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';
```

**Issue**: Can't connect to MySQL server
```bash
# Check if MySQL is running
# Windows: Check Services
# macOS: brew services list | grep mysql
# Linux: sudo systemctl status mysql

# Start MySQL if not running
```

#### 3. Node.js/NPM Issues

**Issue**: `npm install` fails
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**Issue**: Port 3000 already in use
```bash
# Kill process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm start
```

#### 4. Virtual Environment Issues

**Issue**: Virtual environment not activating
```bash
# Windows: Try different activation script
venv\Scripts\activate.bat
# Or
venv\Scripts\Activate.ps1

# macOS/Linux: Check shell
echo $SHELL
# Use appropriate activation script
```

**Issue**: Wrong Python version in virtual environment
```bash
# Delete and recreate virtual environment
rm -rf venv
python3.9 -m venv venv  # Use specific Python version
```

#### 5. Database Migration Issues

**Issue**: Migration fails
```bash
# Reset migrations
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Issue**: Table already exists
```bash
# Drop and recreate database
mysql -u root -p
DROP DATABASE MajorProject;
CREATE DATABASE MajorProject;
EXIT;

# Run setup again
python setup_mysql.py
```

#### 6. Frontend Build Issues

**Issue**: React app won't start
```bash
# Check Node.js version
node --version  # Should be 16+

# Clear React cache
rm -rf node_modules/.cache
```

**Issue**: Tailwind CSS not working
```bash
# Ensure Tailwind is properly installed
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Getting Help

#### Log Files to Check
1. **Backend logs**: Terminal output from `python run.py`
2. **Frontend logs**: Browser console (F12 → Console)
3. **MySQL logs**: Check MySQL error log location
4. **System logs**: Check system event logs for service issues

#### Useful Commands for Debugging
```bash
# Check running processes
# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :3000
lsof -i :5000

# Check Python packages
pip list

# Check Node.js packages
npm list

# Test database connection
mysql -u root -p -e "SHOW DATABASES;"
```

#### Environment Information
When seeking help, provide:
1. **Operating System** and version
2. **Python version**: `python --version`
3. **Node.js version**: `node --version`
4. **MySQL version**: `mysql --version`
5. **Error messages** (full text)
6. **Steps to reproduce** the issue

---

*This installation guide should help you set up the Book Exchange System on any new development environment. If you encounter issues not covered here, refer to the troubleshooting section or seek additional help.*