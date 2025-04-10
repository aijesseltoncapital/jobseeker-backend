# JobSeeker API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Project Setup](#project-setup)
3. [Authentication](#authentication)
4. [API Documentation](#api-documentation)
   - [Authentication APIs](#authentication-apis)
   - [Job APIs](#job-apis)
   - [Messaging APIs](#messaging-apis)
   - [Notification APIs](#notification-apis)
   - [Profile APIs](#profile-apis)
   - [Settings APIs](#settings-apis)
   - [Payment and Rewards APIs](#payment-and-rewards-apis)
5. [WebSocket Integration](#websocket-integration)
6. [Troubleshooting](#troubleshooting)

## Introduction

The JobSeeker API provides a comprehensive backen d for a job search and application platform. This document provides detailed information on how to set up the project and work with all available API endpoints.

## Project Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (recommended) or SQLite
- Redis (for WebSocket functionality)

### Installation

1. Clone the repository

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables (.env file):

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://username:password@localhost/jobseeker
GOOGLE_CLIENT_ID=your-google-client-id
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

5. Initialize the database:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:

```bash
flask run
```

For production deployment:

```bash
gunicorn --worker-class eventlet -w 1 "app:create_app()"
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header for protected endpoints:

```
Authorization: Bearer <your_jwt_token>
```

## API Documentation

### Authentication APIs

#### 1. Job Seeker Login

- **Endpoint**: `/api/jobseeker/login`
- **Method**: POST
- **Description**: Authenticates a job seeker using phone number and password
- **Request Parameters**:
  - `phone_number` (string): User's phone number
  - `password` (string): User's password
- **Response Format**:
  ```json
  {
    "status": "success",
    "token": "JWT_TOKEN",
    "user": {
      "id": 123,
      "name": "John Doe",
      "phone_number": "+1234567890"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Invalid credentials"
  }
  ```

#### 2. Social Login (Google)

- **Endpoint**: `/api/jobseeker/login/google`
- **Method**: POST
- **Description**: Logs in a job seeker using Google authentication
- **Request Parameters**:
  - `google_token` (string): Token from Google OAuth
- **Response Format**:
  ```json
  {
    "status": "success",
    "token": "JWT_TOKEN",
    "user": {
      "id": 123,
      "name": "John Doe",
      "email": "johndoe@gmail.com"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Invalid Google token"
  }
  ```

#### 3. Social Login (LinkedIn)

- **Endpoint**: `/api/jobseeker/login/linkedin`
- **Method**: POST
- **Description**: Logs in a job seeker using LinkedIn authentication
- **Request Parameters**:
  - `linkedin_token` (string): Token from LinkedIn OAuth
- **Response Format**:
  ```json
  {
    "status": "success",
    "token": "JWT_TOKEN",
    "user": {
      "id": 123,
      "name": "John Doe",
      "linkedin_id": "john123"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Invalid LinkedIn token"
  }
  ```

#### 4. Forgot Password

- **Endpoint**: `/api/jobseeker/forgot-password`
- **Method**: POST
- **Description**: Sends a password reset OTP to the job seeker
- **Request Parameters**:
  - `phone_number` (string): User's phone number
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "OTP sent to phone number"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "User not found"
  }
  ```

#### 5. OTP Verification

- **Endpoint**: `/api/jobseeker/check-otp`
- **Method**: POST
- **Description**: OTP verification
- **Request Parameters**:
  - `otp` (string): One-time password sent to user
  - `phone_number` (string): User's phone number
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "OTP confirmed"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Invalid OTP"
  }
  ```

#### 6. Reset Password

- **Endpoint**: `/api/jobseeker/reset-password`
- **Method**: POST
- **Description**: Resets job seeker's password
- **Request Parameters**:
  - `phone_number` (string): User's phone number
  - `new_password` (string): New password
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Password reset successful"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "User not found"
  }
  ```

#### 7. Sign Up

- **Endpoint**: `/api/jobseeker/signup`
- **Method**: POST
- **Description**: Registers a new job seeker account
- **Request Parameters**:
  - `phone_number` (string): User's phone number
  - `password` (string): User's password
  - Other optional fields (name, email, etc.)
- **Response Format**:
  ```json
  {
    "status": "success",
    "token": "JWT_TOKEN",
    "user": {
      "id": 123,
      "phone_number": "+1234567890"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Phone number already registered"
  }
  ```

#### 8. Logout

- **Endpoint**: `/api/jobseeker/logout`
- **Method**: POST
- **Description**: Logs out the current job seeker
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Logged out successfully"
  }
  ```

### Job APIs

#### 9. Get Recommended Jobs

- **Endpoint**: `/api/jobs/recommended`
- **Method**: GET
- **Description**: Fetches recommended jobs based on user skills and preferences
- **Request Parameters**:
  - JWT token in Authorization header
  - Optional filter parameters (query string)
- **Response Format**:
  ```json
  {
    "status": "success",
    "jobs": [
      {
        "id": 1,
        "title": "Software Engineer",
        "company": "Tech Co",
        "location": "San Francisco, CA",
        "job_type": "full-time",
        "salary": "$100,000-$120,000",
        "posted_at": "2023-04-01T10:30:00"
      }
      // More job listings...
    ]
  }
  ```

#### 10. Get All Jobs

- **Endpoint**: `/api/jobs`
- **Method**: GET
- **Description**: Returns a list of available jobs
- **Request Parameters**:
  - `search` (string, optional): Search keyword
  - `location` (string, optional): Job location
  - `type` (string, optional): Job type
  - `page` (integer, optional): Page number (default: 1)
  - `limit` (integer, optional): Results per page (default: 20)
- **Response Format**:
  ```json
  {
    "status": "success",
    "total": 100,
    "page": 1,
    "limit": 20,
    "jobs": [
      {
        "id": 1,
        "title": "Software Engineer",
        "company": "Tech Co",
        "location": "San Francisco, CA",
        "job_type": "full-time",
        "salary": "$100,000-$120,000",
        "posted_at": "2023-04-01T10:30:00"
      }
      // More job listings...
    ]
  }
  ```

#### 11. Quick Apply Job

- **Endpoint**: `/api/jobs/{jobId}/apply`
- **Method**: POST
- **Description**: Allows the user to quickly apply to a job
- **Request Parameters**:
  - JWT token in Authorization header
  - `jobId` (integer): ID of the job to apply for
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Successfully applied to job"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Already applied for this job"
  }
  ```

#### 12. View Job Detail

- **Endpoint**: `/api/job/{id}`
- **Method**: GET
- **Description**: Returns detailed info of a single job
- **Request Parameters**:
  - `id` (integer): Job ID
- **Response Format**:
  ```json
  {
    "status": "success",
    "job": {
      "id": 1,
      "title": "Software Engineer",
      "company": "Tech Co",
      "location": "San Francisco, CA",
      "job_type": "full-time",
      "salary": "$100,000-$120,000",
      "posted_at": "2023-04-01T10:30:00",
      "description": "Detailed job description...",
      "requirements": "Job requirements...",
      "benefits": "Job benefits...",
      "expires_at": "2023-05-01T10:30:00",
      "application_count": 45
    }
  }
  ```

#### 13. Save Job

- **Endpoint**: `/api/job/{id}/save`
- **Method**: POST
- **Description**: Saves a job to user's saved list
- **Request Parameters**:
  - JWT token in Authorization header
  - `id` (integer): Job ID
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Job saved successfully"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Job already saved"
  }
  ```

#### 14. Saved Job List

- **Endpoint**: `/api/job/saved`
- **Method**: GET
- **Description**: Retrieves list of saved jobs
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "jobs": [
      {
        "id": 1,
        "title": "Software Engineer",
        "company": "Tech Co",
        "location": "San Francisco, CA",
        "job_type": "full-time",
        "salary": "$100,000-$120,000",
        "posted_at": "2023-04-01T10:30:00"
      }
      // More job listings...
    ]
  }
  ```

#### 15. Map View Job List

- **Endpoint**: `/api/jobs/map`
- **Method**: GET
- **Description**: Job listings shown on map
- **Response Format**:
  ```json
  {
    "status": "success",
    "jobs": [
      {
        "id": 1,
        "title": "Software Engineer",
        "company": "Tech Co",
        "lat": 37.7749,
        "lng": -122.4194,
        "salary": "$100,000-$120,000"
      }
      // More job listings...
    ]
  }
  ```

### Messaging APIs

#### 16. Messages List

- **Endpoint**: `/api/messages`
- **Method**: GET
- **Description**: Returns chat list with search
- **Request Parameters**:
  - JWT token in Authorization header
  - `keyword` (string, optional): Search keyword
  - `page` (integer, optional): Page number (default: 1)
  - `limit` (integer, optional): Results per page (default: 20)
- **Response Format**:
  ```json
  {
    "status": "success",
    "total": 10,
    "page": 1,
    "limit": 20,
    "conversations": [
      {
        "id": 1,
        "title": "Job Application - Software Engineer",
        "created_at": "2023-04-01T10:30:00",
        "updated_at": "2023-04-02T11:45:00",
        "last_message": {
          "text": "Thank you for your interest!",
          "created_at": "2023-04-02T11:45:00",
          "sender_id": 456
        }
      }
      // More conversations...
    ]
  }
  ```

#### 17. Message Detail

- **Endpoint**: `/api/messages/{id}`
- **Method**: GET
- **Description**: Returns detailed messages in a thread
- **Request Parameters**:
  - JWT token in Authorization header
  - `id` (integer): Conversation ID
- **Response Format**:
  ```json
  {
    "status": "success",
    "conversation": {
      "id": 1,
      "title": "Job Application - Software Engineer",
      "created_at": "2023-04-01T10:30:00",
      "updated_at": "2023-04-02T11:45:00",
      "last_message": {
        "text": "Thank you for your interest!",
        "created_at": "2023-04-02T11:45:00",
        "sender_id": 456
      }
    },
    "messages": [
      {
        "id": 101,
        "conversation_id": 1,
        "sender_id": 123,
        "receiver_id": 456,
        "text": "I'm interested in this position.",
        "created_at": "2023-04-01T10:30:00",
        "read_at": "2023-04-01T10:35:00",
        "is_read": true
      },
      {
        "id": 102,
        "conversation_id": 1,
        "sender_id": 456,
        "receiver_id": 123,
        "text": "Thank you for your interest!",
        "created_at": "2023-04-02T11:45:00",
        "read_at": null,
        "is_read": false
      }
      // More messages...
    ]
  }
  ```

#### 18. Send Message (WebSocket)

- **Connection**: WebSocket
- **Event**: `message`
- **Description**: Sends a message via WebSocket
- **Request Data**:
  - `token` (string): JWT token for authentication
  - `receiver_id` (integer): Recipient user ID
  - `text` (string): Message content
  - `conversation_id` (integer, optional): Existing conversation ID
- **Response Event**: `new_message`
- **Response Format**:
  ```json
  {
    "id": 103,
    "conversation_id": 1,
    "sender_id": 123,
    "receiver_id": 456,
    "text": "When would be a good time to schedule an interview?",
    "created_at": "2023-04-03T14:20:00",
    "read_at": null,
    "is_read": false
  }
  ```

### Notification APIs

#### 19. Notification List

- **Endpoint**: `/api/notifications`
- **Method**: GET
- **Description**: List of user notifications
- **Request Parameters**:
  - JWT token in Authorization header
  - `page` (integer, optional): Page number (default: 1)
  - `limit` (integer, optional): Results per page (default: 20)
- **Response Format**:
  ```json
  {
    "status": "success",
    "total": 15,
    "page": 1,
    "limit": 20,
    "read_count": 3,
    "notifications": [
      {
        "id": 1,
        "title": "New Message",
        "message": "You have received a new message from Recruiter",
        "notification_type": "message",
        "related_id": 1,
        "created_at": "2023-04-03T14:25:00",
        "read_at": null,
        "is_read": false
      }
      // More notifications...
    ]
  }
  ```

#### 20. Mark All as Read

- **Endpoint**: `/api/notifications/mark-read-all`
- **Method**: POST
- **Description**: Marks all notifications as read
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "All notifications marked as read",
    "count": 12
  }
  ```

### Profile APIs

#### 21. Get Profile

- **Endpoint**: `/api/profile`
- **Method**: GET
- **Description**: Returns profile info
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "user": {
      "id": 123,
      "name": "John Doe",
      "phone_number": "+1234567890",
      "email": "johndoe@example.com",
      "bio": "Experienced software engineer...",
      "skills": "JavaScript, Python, React",
      "profile_image": "https://example.com/profile/image123.jpg",
      "resume_url": "https://example.com/resume/johndoe.pdf",
      "created_at": "2023-01-15T08:30:00"
    }
  }
  ```

#### 22. Edit Profile

- **Endpoint**: `/api/profile/edit`
- **Method**: PUT
- **Description**: Edits profile fields
- **Request Parameters**:
  - JWT token in Authorization header
  - `name` (string, optional): User's name
  - `bio` (string, optional): User's bio
  - `skills` (string, optional): User's skills
  - `email` (string, optional): User's email
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Profile updated successfully",
    "user": {
      "id": 123,
      "name": "John Doe",
      "phone_number": "+1234567890",
      "email": "johndoe@example.com"
    }
  }
  ```

#### 23. Download Resume

- **Endpoint**: `/api/profile/resume`
- **Method**: GET
- **Description**: Downloads job seeker's resume
- **Request Parameters**:
  - JWT token in Authorization header
- **Response**: File download (PDF/DOC)

#### 24. Upload Credential

- **Endpoint**: `/api/profile/credentials`
- **Method**: POST
- **Description**: Uploads certificates/credentials
- **Request Parameters**:
  - JWT token in Authorization header
  - `credential` (file): File to upload
  - `title` (string): Credential title
  - `description` (string, optional): Description
  - `credential_type` (string, optional): Type of credential
  - `issuer` (string, optional): Issuing organization
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Credential uploaded successfully",
    "credential": {
      "id": 1,
      "title": "AWS Certified Developer",
      "description": "Associate level certification",
      "credential_type": "certificate",
      "issuer": "Amazon Web Services",
      "issue_date": "2023-01-10T00:00:00",
      "expiry_date": null,
      "file_url": "https://example.com/credentials/aws_cert.pdf",
      "created_at": "2023-04-05T15:30:00"
    }
  }
  ```

#### 28. Working Schedule

- **Endpoint**: `/api/profile/schedule`
- **Method**: GET
- **Description**: Returns job seeker's schedule
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "schedules": [
      {
        "id": 1,
        "day_of_week": 1,
        "start_time": "09:00",
        "end_time": "17:00",
        "availability": true
      },
      {
        "id": 2,
        "day_of_week": 2,
        "start_time": "09:00",
        "end_time": "17:00",
        "availability": true
      }
      // Other days...
    ]
  }
  ```

#### 29. Change Password

- **Endpoint**: `/api/profile/change-password`
- **Method**: POST
- **Description**: Changes password
- **Request Parameters**:
  - JWT token in Authorization header
  - `current_password` (string): Current password
  - `new_password` (string): New password
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Password changed successfully"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Current password is incorrect"
  }
  ```

### Settings APIs

#### 25. Delete Account

- **Endpoint**: `/api/settings/account/delete`
- **Method**: DELETE
- **Description**: Deletes user account
- **Request Parameters**:
  - JWT token in Authorization header
  - `password` (string): User's password for confirmation
  - `confirmation` (string): Must be "DELETE" to confirm
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Account deleted successfully"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "message": "Incorrect password"
  }
  ```

#### 30. Get Notification Preferences

- **Endpoint**: `/api/settings/notifications`
- **Method**: GET
- **Description**: Retrieves user's notification settings
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "preferences": {
      "email_notifications": true,
      "push_notifications": true,
      "sms_notifications": true,
      "job_alerts": true,
      "message_notifications": true,
      "application_updates": true
    }
  }
  ```

#### 31. Update Notification Preferences

- **Endpoint**: `/api/settings/notifications`
- **Method**: PUT
- **Description**: Updates notification preferences
- **Request Parameters**:
  - JWT token in Authorization header
  - JSON object with preference settings
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Notification preferences updated",
    "preferences": {
      "email_notifications": false,
      "push_notifications": true,
      "sms_notifications": false,
      "job_alerts": true,
      "message_notifications": true,
      "application_updates": false
    }
  }
  ```

#### 32. Get Privacy Settings

- **Endpoint**: `/api/settings/privacy`
- **Method**: GET
- **Description**: Returns privacy settings
- **Request Parameters**:
  - JWT token in Authorization header
- **Response Format**:
  ```json
  {
    "status": "success",
    "settings": {
      "profile_visibility": "public",
      "resume_visibility": "connections",
      "contact_info_visibility": "connections",
      "job_application_visibility": "private"
    }
  }
  ```

#### 33. Update Privacy Settings

- **Endpoint**: `/api/settings/privacy`
- **Method**: PUT
- **Description**: Updates privacy settings
- **Request Parameters**:
  - JWT token in Authorization header
  - JSON object with privacy settings
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Privacy settings updated",
    "settings": {
      "profile_visibility": "connections",
      "resume_visibility": "private",
      "contact_info_visibility": "private",
      "job_application_visibility": "private"
    }
  }
  ```

### Payment and Rewards APIs

#### 26. Get Payment History

- **Endpoint**: `/api/payments/history`
- **Method**: GET
- **Description**: Lists job seeker's payment history
- **Request Parameters**:
  - JWT token in Authorization header
  - `page` (integer, optional): Page number (default: 1)
  - `limit` (integer, optional): Results per page (default: 20)
- **Response Format**:
  ```json
  {
    "status": "success",
    "total": 5,
    "page": 1,
    "limit": 20,
    "payments": [
      {
        "id": 1,
        "amount": 29.99,
        "currency": "USD",
        "payment_type": "subscription",
        "status": "completed",
        "transaction_id": "tx_12345",
        "provider": "Stripe",
        "description": "Premium subscription - Monthly",
        "created_at": "2023-04-01T00:00:00",
        "updated_at": "2023-04-01T00:00:00"
      }
      // More payments...
    ]
  }
  ```

#### 27. Points & Rewards List

- **Endpoint**: `/api/rewards`
- **Method**: GET
- **Description**: Displays user points and rewards
- **Request Parameters**:
  - JWT token in Authorization header
  - `page` (integer, optional): Page number (default: 1)
  - `limit` (integer, optional): Results per page (default: 20)
- **Response Format**:
  ```json
  {
    "status": "success",
    "total_points": 1250,
    "total_entries": 15,
    "page": 1,
    "limit": 20,
    "rewards": [
      {
        "id": 1,
        "points": 50,
        "action": "profile_complete",
        "description": "Completed profile information",
        "created_at": "2023-03-15T12:30:00"
      },
      {
        "id": 2,
        "points": 100,
        "action": "apply",
        "description": "Applied to Software Engineer position",
        "created_at": "2023-03-20T14:45:00"
      }
      // More rewards...
    ]
  }
  ```

## WebSocket Integration

For real-time messaging, the application uses Socket.IO. To connect:

```javascript
// Client-side JavaScript example
const socket = io("http://your-server-url", {
  auth: {
    token: "your-jwt-token",
  },
});

// Listen for new messages
socket.on("new_message", (message) => {
  console.log("New message received:", message);
});

// Send a message
socket.emit("message", {
  receiver_id: 456,
  text: "Hello, I am interested in this position.",
  conversation_id: 1, // Optional if starting a new conversation
});
```

## Troubleshooting

### Common Issues

1. **Authentication Issues**

   - Ensure your JWT token is valid and not expired
   - Check that you're including the token in the Authorization header

2. **File Upload Issues**

   - Check that file size is under 16MB
   - Ensure file format is supported (PDF, DOC, DOCX for resumes, JPG/PNG for images)

3. **Socket Connection Issues**
   - Verify that your token is valid
   - Check that you're connecting to the correct server URL
   - Ensure CORS is properly configured on both client and server