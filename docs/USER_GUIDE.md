# User Guide - Book Exchange System

This guide will help you navigate and use all features of the Book Exchange System.

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [User Registration & Login](#user-registration--login)
3. [Browsing Books](#browsing-books)
4. [Managing Your Books](#managing-your-books)
5. [AI Recommendations](#ai-recommendations)
6. [Exchange Requests](#exchange-requests)
7. [Dashboard Overview](#dashboard-overview)
8. [Search & Filters](#search--filters)

## 🚀 Getting Started

### First Time Setup

1. **Access the Application**
   - Open your web browser
   - Navigate to `http://localhost:3000`
   - You'll see the homepage with login/register options

2. **Create Your Account**
   - Click "Sign Up" in the top right
   - Fill in your details (first name, last name, email, password)
   - Click "Register" to create your account

3. **Login**
   - Use your email and password to login
   - You'll be redirected to the dashboard

## 👤 User Registration & Login

### Registration Process
1. **Navigate to Registration**
   - Click "Sign Up" from the homepage
   - Or go directly to `/register`

2. **Fill Required Information**
   - **First Name**: Your first name
   - **Last Name**: Your last name  
   - **Email**: Valid email address (used for login)
   - **Password**: Minimum 8 characters
   - **Confirm Password**: Must match your password

3. **Account Verification**
   - After successful registration, you'll be automatically logged in
   - Your account will have "User" role by default

### Login Process
1. **Access Login Page**
   - Click "Login" from the homepage
   - Or go directly to `/login`

2. **Enter Credentials**
   - **Email**: Your registered email
   - **Password**: Your account password

3. **Stay Logged In**
   - Your session will remain active
   - JWT token is stored securely in browser

## 📖 Browsing Books

### Viewing All Books
1. **Navigate to Books**
   - Click "Browse Books" in the navigation
   - Or go to `/books`

2. **Book Information Displayed**
   - **Book cover image** (if available)
   - **Title and Author**
   - **Category** (Fiction, Science, etc.)
   - **Condition** (New, Like New, Good, Fair, Poor)
   - **Description**
   - **Availability status**
   - **Owner information**

3. **Book Interactions**
   - **❤️ Like Button**: Click to like a book (helps with recommendations)
   - **Request Exchange**: Send exchange request to book owner
   - **View Details**: Click on book to see more information

### Book Conditions Explained
- **New**: Brand new, never used
- **Like New**: Excellent condition, minimal wear
- **Good**: Normal wear, all pages intact
- **Fair**: Noticeable wear, but readable
- **Poor**: Heavy wear, may have damage

## 📚 Managing Your Books

### Adding a New Book
1. **Access Book Form**
   - Go to Dashboard → "Add New Book"
   - Or navigate to `/books/new`

2. **Fill Book Details**
   - **Title**: Full book title
   - **Author**: Author's name
   - **ISBN**: (Optional) Book's ISBN number
   - **Category**: Select from dropdown
   - **Condition**: Select book's condition
   - **Description**: (Optional) Additional details

3. **Upload Book Image**
   - Click "Upload Image" or drag & drop
   - Supported formats: PNG, JPG, JPEG, GIF
   - Maximum size: 5MB

4. **Save Book**
   - Click "Add Book" to save
   - Book will appear in your listings

### Editing Your Books
1. **Find Your Book**
   - Go to Dashboard → "My Books"
   - Click "Edit" on the book you want to modify

2. **Update Information**
   - Modify any field as needed
   - Upload new image if desired

3. **Save Changes**
   - Click "Update Book"
   - Changes will be reflected immediately

### Deleting Books
1. **Access Your Books**
   - Go to Dashboard → "My Books"

2. **Delete Book**
   - Click "Delete" on the book
   - Confirm deletion in the popup
   - **Note**: This will also cancel any pending exchange requests

## 🤖 AI Recommendations

### How Recommendations Work
The system uses advanced AI algorithms to suggest books based on:
- **Your interaction history** (books you've viewed, liked, requested)
- **Content similarity** (TF-IDF analysis of book descriptions)
- **Category preferences** (genres you interact with most)
- **Author preferences** (authors you've shown interest in)

### Viewing Recommendations
1. **Dashboard Recommendations**
   - Personalized recommendations appear on your dashboard
   - Shows top 6 recommendations with relevance scores

2. **Full Recommendations Page**
   - Click "View All Recommendations" or navigate to `/recommendations`
   - See up to 12 personalized recommendations
   - View your interaction statistics
   - Understand how the AI works

3. **Recommendation Information**
   - **Relevance Score**: Percentage match to your interests
   - **Explanation**: Why this book was recommended
   - **Similarity Badge**: Content similarity percentage

### Improving Recommendations
To get better recommendations:
1. **Browse and View Books**: Each view is tracked
2. **Like Books**: Heart books you're interested in
3. **Request Exchanges**: Shows strong interest
4. **Search for Books**: Indicates your interests
5. **Complete Exchanges**: Provides feedback on preferences

### Similar Books Feature
- When viewing a book, see "Similar Books" section
- Shows books with similar content using AI analysis
- Similarity percentages help you find related content

## 🔄 Exchange Requests

### Sending Exchange Requests
1. **Find a Book**
   - Browse books or use search
   - Click on a book you want

2. **Request Exchange**
   - Click "Request Exchange" button
   - **Note**: You cannot request your own books

3. **Add Message** (Optional)
   - Include a personal message to the owner
   - Explain why you want the book
   - Suggest your books for exchange

4. **Submit Request**
   - Click "Send Request"
   - Owner will be notified

### Managing Received Requests
1. **View Requests**
   - Go to Dashboard → "Exchange Requests"
   - See all incoming requests

2. **Review Request Details**
   - **Requester Information**: Who wants your book
   - **Message**: Any message from requester
   - **Book Details**: Which book they want
   - **Request Date**: When request was made

3. **Respond to Requests**
   - **Approve**: Accept the exchange request
   - **Reject**: Decline the request
   - **Message**: Send response message

### Exchange Status Tracking
- **Pending**: Waiting for owner response
- **Approved**: Owner accepted request
- **Rejected**: Owner declined request
- **Completed**: Exchange finished
- **Cancelled**: Request was cancelled

### Exchange History
- View all your past exchanges
- Track successful exchanges
- See exchange patterns and statistics

## 📊 Dashboard Overview

### Dashboard Sections

1. **AI Recommendations**
   - Personalized book suggestions
   - Relevance scores and explanations
   - Quick access to full recommendations page

2. **Exchange Management**
   - **Sent Requests**: Requests you've made
   - **Received Requests**: Requests for your books
   - **Active Exchanges**: Ongoing exchanges
   - **Exchange History**: Past exchanges

3. **Quick Stats**
   - **My Books**: Total books you've listed
   - **Active Exchanges**: Current ongoing exchanges
   - **Pending Requests**: Requests awaiting response
   - **Completed**: Successfully finished exchanges

4. **Recent Activity**
   - Latest exchange requests
   - Recent book additions
   - System notifications

### Dashboard Actions
- **Add New Book**: Quick access to book creation
- **View All Books**: See your complete book collection
- **Manage Requests**: Handle incoming exchange requests
- **View Recommendations**: Access AI-powered suggestions

## 🔍 Search & Filters

### Basic Search
1. **Search Bar**
   - Located at top of Books page
   - Type book title, author, or keywords
   - Real-time suggestions appear as you type

2. **Search History**
   - Recent searches are saved
   - Click on previous searches to repeat them
   - Clear history if needed

### Advanced Filters
1. **Category Filter**
   - Filter by book genres (Fiction, Science, History, etc.)
   - Multiple categories can be selected

2. **Condition Filter**
   - Filter by book condition
   - Choose from New, Like New, Good, Fair, Poor

3. **Author Filter**
   - Search for books by specific authors
   - Partial name matching supported

4. **Availability Filter**
   - Show only available books
   - Hide books that are not available for exchange

### Search Tips
- **Use partial words**: "harr" will find "Harry Potter"
- **Combine filters**: Use multiple filters for precise results
- **Save searches**: Bookmark URLs for repeated searches
- **Clear filters**: Reset all filters to see all books

### Search Interaction Tracking
- All searches are tracked for AI recommendations
- Search patterns help improve future suggestions
- Popular search terms influence recommendation algorithms

## 💡 Tips for Best Experience

### Getting Better Recommendations
1. **Be Active**: View, like, and request books regularly
2. **Diversify**: Explore different categories and authors
3. **Complete Exchanges**: Finish exchanges to improve algorithm
4. **Use Search**: Search for books you're interested in

### Successful Exchanges
1. **Good Photos**: Upload clear, well-lit book images
2. **Accurate Descriptions**: Be honest about book condition
3. **Respond Quickly**: Reply to exchange requests promptly
4. **Communicate**: Use messages to coordinate exchanges

### Account Security
1. **Strong Password**: Use a secure, unique password
2. **Logout**: Always logout on shared computers
3. **Update Info**: Keep your profile information current
4. **Report Issues**: Contact support for any problems

## ❓ Frequently Asked Questions

### General Questions

**Q: How do I change my password?**
A: Currently, password changes are not implemented in the UI. Contact an administrator.

**Q: Can I delete my account?**
A: Account deletion is not currently available through the UI. Contact support.

**Q: How many books can I list?**
A: There's no limit on the number of books you can list.

### Exchange Questions

**Q: What happens if someone doesn't respond to my request?**
A: Requests remain pending until the owner responds. You can cancel if needed.

**Q: Can I request multiple books from the same person?**
A: Yes, you can send multiple exchange requests to the same user.

**Q: How do I coordinate the physical exchange?**
A: Use the messaging system to arrange meeting details privately.

### Recommendation Questions

**Q: Why am I not getting recommendations?**
A: You need to interact with books first. View, like, or request books to build your profile.

**Q: How often do recommendations update?**
A: Recommendations update in real-time based on your interactions.

**Q: Can I see why a book was recommended?**
A: Yes, each recommendation includes an explanation of why it was suggested.

## 📞 Support

If you encounter any issues or have questions:

1. **Check this guide** for common solutions
2. **Review error messages** for specific guidance
3. **Contact system administrator** for technical issues
4. **Report bugs** through the appropriate channels

---

*This guide covers the main features of the Book Exchange System. For technical details or development information, see the Developer Guide.*