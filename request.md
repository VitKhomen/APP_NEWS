API Testing Guide for Postman
Base URL: http://localhost:8000/api/v1

Authentication Endpoints
1. Register User
POST /auth/register/
Headers:
Content-Type: application/json
Body (JSON):
json{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
}
Success Response (201):
json{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "full_name": "Test User",
        "avatar": null,
        "bio": "",
        "created_at": "2025-10-03T10:00:00Z",
        "updated_at": "2025-10-03T10:00:00Z",
        "posts_count": 0,
        "comments_count": 0
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "User register successfully"
}

2. Login User
POST /auth/login/
Headers:
Content-Type: application/json
Body (JSON):
json{
    "email": "testuser@example.com",
    "password": "SecurePass123!"
}
Success Response (200):
json{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "full_name": "Test User",
        "avatar": null,
        "bio": "",
        "created_at": "2025-10-03T10:00:00Z",
        "updated_at": "2025-10-03T10:00:00Z",
        "posts_count": 0,
        "comments_count": 0
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "User login successfully"
}

3. Get User Profile
GET /auth/profile/
Headers:
Authorization: Bearer {access_token}
Success Response (200):
json{
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "full_name": "Test User",
    "avatar": null,
    "bio": "",
    "created_at": "2025-10-03T10:00:00Z",
    "updated_at": "2025-10-03T10:00:00Z",
    "posts_count": 5,
    "comments_count": 12
}

4. Update User Profile
PUT/PATCH /auth/profile/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "This is my updated bio"
}
Body (Form-data) - For avatar upload:
first_name: Updated
last_name: Name
bio: This is my updated bio
avatar: [file]
Success Response (200):
json{
    "first_name": "Updated",
    "last_name": "Name",
    "avatar": "/media/avatars/avatar.jpg",
    "bio": "This is my updated bio"
}

5. Change Password
PUT /auth/change-password/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
}
Success Response (200):
json{
    "message": "Password change successfully"
}

6. Refresh Token
POST /auth/token/refresh/
Headers:
Content-Type: application/json
Body (JSON):
json{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
Success Response (200):
json{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

7. Logout User
POST /auth/logout/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
Success Response (200):
json{
    "message": "Logout successful"
}

Category Endpoints
8. Get All Categories
GET /posts/category/
Headers:
Authorization: Bearer {access_token} (optional)
Query Parameters:
?search=tech
&ordering=name
&ordering=-created_at
Success Response (200):
json{
    "count": 10,
    "next": "http://localhost:8000/api/v1/posts/category/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Technology",
            "slug": "technology",
            "description": "Tech related posts",
            "posts_count": 15,
            "created_at": "2025-10-01T10:00:00Z"
        }
    ]
}

9. Create Category
POST /posts/category/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "name": "Technology",
    "description": "All about technology and innovation"
}
Success Response (201):
json{
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "All about technology and innovation",
    "posts_count": 0,
    "created_at": "2025-10-03T10:00:00Z"
}

10. Get Category Detail
GET /posts/category/{slug}/
Example: /posts/category/technology/
Headers:
Authorization: Bearer {access_token} (optional)
Success Response (200):
json{
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "All about technology and innovation",
    "posts_count": 15,
    "created_at": "2025-10-01T10:00:00Z"
}

11. Update Category
PUT/PATCH /posts/category/{slug}/
Example: /posts/category/technology/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "name": "Tech & Innovation",
    "description": "Updated description"
}
Success Response (200):
json{
    "id": 1,
    "name": "Tech & Innovation",
    "slug": "tech-innovation",
    "description": "Updated description",
    "posts_count": 15,
    "created_at": "2025-10-01T10:00:00Z"
}

12. Delete Category
DELETE /posts/category/{slug}/
Example: /posts/category/technology/
Headers:
Authorization: Bearer {access_token}
Success Response (204):
No Content

13. Get Posts by Category
GET /posts/category/{category_slug}/posts/
Example: /posts/category/technology/posts/
Headers:
Authorization: Bearer {access_token} (optional)
Success Response (200):
json{
    "category": {
        "id": 1,
        "name": "Technology",
        "slug": "technology",
        "description": "Tech related posts",
        "posts_count": 15,
        "created_at": "2025-10-01T10:00:00Z"
    },
    "posts": [
        {
            "id": 1,
            "title": "Introduction to AI",
            "slug": "introduction-to-ai",
            "content": "Artificial Intelligence is...",
            "image": "/media/posts/ai.jpg",
            "category": "Technology",
            "author": "testuser",
            "status": "published",
            "created_at": "2025-10-02T10:00:00Z",
            "updated_at": "2025-10-02T10:00:00Z",
            "views_count": 150,
            "comments_count": 12
        }
    ]
}

Post Endpoints
14. Get All Posts (List)
GET /posts/
Headers:
Authorization: Bearer {access_token} (optional)
Query Parameters:
?search=technology
&category=1
&author=1
&status=published
&ordering=-created_at
&ordering=-views_count
&page=1
Success Response (200):
json{
    "count": 50,
    "next": "http://localhost:8000/api/v1/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Introduction to AI",
            "slug": "introduction-to-ai",
            "content": "Artificial Intelligence is transforming...",
            "image": "/media/posts/ai.jpg",
            "category": "Technology",
            "author": "testuser",
            "status": "published",
            "created_at": "2025-10-02T10:00:00Z",
            "updated_at": "2025-10-02T10:00:00Z",
            "views_count": 150,
            "comments_count": 12
        }
    ]
}

15. Create Post
POST /posts/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "title": "My First Post",
    "content": "This is the content of my first post. It contains detailed information...",
    "category": 1,
    "status": "published"
}
Body (Form-data) - With image:
title: My First Post
content: This is the content of my first post...
category: 1
status: published
image: [file]
Success Response (201):
json{
    "id": 1,
    "title": "My First Post",
    "slug": "my-first-post",
    "content": "This is the content of my first post...",
    "image": "/media/posts/image.jpg",
    "category": "Technology",
    "author": "testuser",
    "status": "published",
    "created_at": "2025-10-03T10:00:00Z",
    "updated_at": "2025-10-03T10:00:00Z",
    "views_count": 0,
    "comments_count": 0
}

16. Get Post Detail
GET /posts/{slug}/
Example: /posts/introduction-to-ai/
Headers:
Authorization: Bearer {access_token} (optional)
Success Response (200):
json{
    "id": 1,
    "title": "Introduction to AI",
    "slug": "introduction-to-ai",
    "content": "Full content of the post...",
    "image": "/media/posts/ai.jpg",
    "category": 1,
    "category_info": {
        "id": 1,
        "name": "Technology",
        "slug": "technology"
    },
    "author": 1,
    "author_info": {
        "id": 1,
        "username": "testuser",
        "fullname": "Test User",
        "avatar": "/media/avatars/avatar.jpg"
    },
    "status": "published",
    "created_at": "2025-10-02T10:00:00Z",
    "updated_at": "2025-10-02T10:00:00Z",
    "views_count": 151,
    "comments_count": 12
}

17. Update Post
PUT/PATCH /posts/{slug}/
Example: /posts/introduction-to-ai/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
Body (JSON):
json{
    "title": "Updated Post Title",
    "content": "Updated content...",
    "category": 2,
    "status": "draft"
}
Success Response (200):
json{
    "title": "Updated Post Title",
    "content": "Updated content...",
    "image": "/media/posts/ai.jpg",
    "category": 2,
    "status": "draft"
}

18. Delete Post
DELETE /posts/{slug}/
Example: /posts/introduction-to-ai/
Headers:
Authorization: Bearer {access_token}
Success Response (204):
No Content

19. Get My Posts
GET /posts/my-posts/
Headers:
Authorization: Bearer {access_token}
Query Parameters:
?search=title
&category=1
&status=draft
&ordering=-created_at
Success Response (200):
json{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "My Post",
            "slug": "my-post",
            "content": "Content...",
            "image": "/media/posts/image.jpg",
            "category": "Technology",
            "author": "testuser",
            "status": "published",
            "created_at": "2025-10-02T10:00:00Z",
            "updated_at": "2025-10-02T10:00:00Z",
            "views_count": 100,
            "comments_count": 5
        }
    ]
}

20. Get Popular Posts
GET /posts/popular/
Headers:
Authorization: Bearer {access_token} (optional)
Success Response (200):
json[
    {
        "id": 1,
        "title": "Most Popular Post",
        "slug": "most-popular-post",
        "content": "This post has the most views...",
        "image": "/media/posts/popular.jpg",
        "category": "Technology",
        "author": "testuser",
        "status": "published",
        "created_at": "2025-09-01T10:00:00Z",
        "updated_at": "2025-09-01T10:00:00Z",
        "views_count": 5000,
        "comments_count": 250
    }
]

21. Get Recent Posts
GET /posts/recent/
Headers:
Authorization: Bearer {access_token} (optional)
Success Response (200):
json[
    {
        "id": 10,
        "title": "Latest Post",
        "slug": "latest-post",
        "content": "This is the most recent post...",
        "image": "/media/posts/recent.jpg",
        "category": "News",
        "author": "newuser",
        "status": "published",
        "created_at": "2025-10-03T09:00:00Z",
        "updated_at": "2025-10-03T09:00:00Z",
        "views_count": 10,
        "comments_count": 0
    }
]

Common Error Responses
400 Bad Request
json{
    "field_name": [
        "Error message"
    ]
}
401 Unauthorized
json{
    "detail": "Authentication credentials were not provided."
}
403 Forbidden
json{
    "detail": "You do not have permission to perform this action."
}
404 Not Found
json{
    "detail": "Not found."
}
500 Internal Server Error
json{
    "detail": "Internal server error."
}

Postman Environment Variables
Create an environment with these variables:
base_url: http://localhost:8000/api/v1
access_token: (will be set after login)
refresh_token: (will be set after login)
user_id: (will be set after login)
Postman Pre-request Script (for authenticated requests)
javascriptpm.environment.set("access_token", pm.environment.get("access_token"));
Postman Tests Script (for login/register)
javascriptif (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
    if (jsonData.user) {
        pm.environment.set("user_id", jsonData.user.id);
    }
}