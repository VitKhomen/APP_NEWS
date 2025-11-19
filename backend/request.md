# API Testing Guide for Postman

Base URL: `http://localhost:8000/api/v1`

---

## Authentication Endpoints

### 1. Register User
**POST** `/auth/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
}
```

**Success Response (201):**
```json
{
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
```

---

### 2. Login User
**POST** `/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "testuser@example.com",
    "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
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
```

---

### 3. Get User Profile
**GET** `/auth/profile/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Success Response (200):**
```json
{
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
```

---

### 4. Update User Profile
**PUT/PATCH** `/auth/profile/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "This is my updated bio"
}
```

**Body (Form-data) - For avatar upload:**
```
first_name: Updated
last_name: Name
bio: This is my updated bio
avatar: [file]
```

**Success Response (200):**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "avatar": "/media/avatars/avatar.jpg",
    "bio": "This is my updated bio"
}
```

---

### 5. Change Password
**PUT** `/auth/change-password/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
}
```

**Success Response (200):**
```json
{
    "message": "Password change successfully"
}
```

---

### 6. Refresh Token
**POST** `/auth/token/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 7. Logout User
**POST** `/auth/logout/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200):**
```json
{
    "message": "Logout successful"
}
```

---

## Category Endpoints

### 8. Get All Categories
**GET** `/posts/category/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Query Parameters:**
```
?search=tech
&ordering=name
&ordering=-created_at
```

**Success Response (200):**
```json
{
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
```

---

### 9. Create Category
**POST** `/posts/category/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "name": "Technology",
    "description": "All about technology and innovation"
}
```

**Success Response (201):**
```json
{
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "All about technology and innovation",
    "posts_count": 0,
    "created_at": "2025-10-03T10:00:00Z"
}
```

---

### 10. Get Category Detail
**GET** `/posts/category/{slug}/`

**Example:** `/posts/category/technology/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
{
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "All about technology and innovation",
    "posts_count": 15,
    "created_at": "2025-10-01T10:00:00Z"
}
```

---

### 11. Update Category
**PUT/PATCH** `/posts/category/{slug}/`

**Example:** `/posts/category/technology/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "name": "Tech & Innovation",
    "description": "Updated description"
}
```

**Success Response (200):**
```json
{
    "id": 1,
    "name": "Tech & Innovation",
    "slug": "tech-innovation",
    "description": "Updated description",
    "posts_count": 15,
    "created_at": "2025-10-01T10:00:00Z"
}
```

---

### 12. Delete Category
**DELETE** `/posts/category/{slug}/`

**Example:** `/posts/category/technology/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Success Response (204):**
```
No Content
```

---

### 13. Get Posts by Category
**GET** `/posts/category/{category_slug}/posts/`

**Example:** `/posts/category/technology/posts/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
{
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
```

---

## Post Endpoints

### 14. Get All Posts (List)
**GET** `/posts/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Query Parameters:**
```
?search=technology
&category=1
&author=1
&status=published
&ordering=-created_at
&ordering=-views_count
&page=1
```

**Success Response (200):**
```json
{
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
```

---

### 15. Create Post
**POST** `/posts/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "title": "My First Post",
    "content": "This is the content of my first post. It contains detailed information...",
    "category": 1,
    "status": "published"
}
```

**Body (Form-data) - With image:**
```
title: My First Post
content: This is the content of my first post...
category: 1
status: published
image: [file]
```

**Success Response (201):**
```json
{
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
```

---

### 16. Get Post Detail
**GET** `/posts/{slug}/`

**Example:** `/posts/introduction-to-ai/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
{
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
```

---

### 17. Update Post
**PUT/PATCH** `/posts/{slug}/`

**Example:** `/posts/introduction-to-ai/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "title": "Updated Post Title",
    "content": "Updated content...",
    "category": 2,
    "status": "draft"
}
```

**Success Response (200):**
```json
{
    "title": "Updated Post Title",
    "content": "Updated content...",
    "image": "/media/posts/ai.jpg",
    "category": 2,
    "status": "draft"
}
```

---

### 18. Delete Post
**DELETE** `/posts/{slug}/`

**Example:** `/posts/introduction-to-ai/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Success Response (204):**
```
No Content
```

---

### 19. Get My Posts
**GET** `/posts/my-posts/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
?search=title
&category=1
&status=draft
&ordering=-created_at
```

**Success Response (200):**
```json
{
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
```

---

### 20. Get Popular Posts
**GET** `/posts/popular/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
[
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
```

---

### 21. Get Recent Posts
**GET** `/posts/recent/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
[
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
```

---

## Comment Endpoints

### 22. Get All Comments
**GET** `/comments/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Query Parameters:**
```
?search=great
&post=1
&author=1
&parent=5
&ordering=-created_at
&page=1
```

**Success Response (200):**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/v1/comments/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "content": "Great post! Very informative.",
            "author": 1,
            "author_info": {
                "id": 1,
                "username": "testuser",
                "fullname": "Test User",
                "avatar": "/media/avatars/avatar.jpg"
            },
            "parent": null,
            "is_active": true,
            "replies_count": 3,
            "is_reply": false,
            "created_at": "2025-10-03T10:00:00Z",
            "updated_at": "2025-10-03T10:00:00Z"
        }
    ]
}
```

---

### 23. Create Comment
**POST** `/comments/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON) - Main Comment:**
```json
{
    "post": 1,
    "content": "This is a great article! Thanks for sharing."
}
```

**Body (JSON) - Reply to Comment:**
```json
{
    "post": 1,
    "parent": 5,
    "content": "I totally agree with your point!"
}
```

**Success Response (201):**
```json
{
    "id": 15,
    "content": "This is a great article! Thanks for sharing.",
    "author": 1,
    "author_info": {
        "id": 1,
        "username": "testuser",
        "fullname": "Test User",
        "avatar": "/media/avatars/avatar.jpg"
    },
    "parent": null,
    "is_active": true,
    "replies_count": 0,
    "is_reply": false,
    "created_at": "2025-10-08T20:00:00Z",
    "updated_at": "2025-10-08T20:00:00Z"
}
```

---

### 24. Get Comment Detail
**GET** `/comments/{id}/`

**Example:** `/comments/5/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
{
    "id": 5,
    "content": "Great post! Very informative.",
    "author": 1,
    "author_info": {
        "id": 1,
        "username": "testuser",
        "fullname": "Test User",
        "avatar": "/media/avatars/avatar.jpg"
    },
    "parent": null,
    "is_active": true,
    "replies_count": 3,
    "is_reply": false,
    "created_at": "2025-10-03T10:00:00Z",
    "updated_at": "2025-10-03T10:00:00Z",
    "replies": [
        {
            "id": 6,
            "content": "I agree!",
            "author": 2,
            "author_info": {
                "id": 2,
                "username": "user2",
                "fullname": "User Two",
                "avatar": null
            },
            "parent": 5,
            "is_active": true,
            "replies_count": 0,
            "is_reply": true,
            "created_at": "2025-10-03T11:00:00Z",
            "updated_at": "2025-10-03T11:00:00Z"
        }
    ]
}
```

---

### 25. Update Comment
**PUT/PATCH** `/comments/{id}/`

**Example:** `/comments/5/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "content": "Updated comment text with new information."
}
```

**Success Response (200):**
```json
{
    "content": "Updated comment text with new information."
}
```

---

### 26. Delete Comment (Soft Delete)
**DELETE** `/comments/{id}/`

**Example:** `/comments/5/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Note:** This performs a soft delete (sets `is_active=False`)

**Success Response (204):**
```
No Content
```

---

### 27. Get My Comments
**GET** `/comments/my-comments/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
?search=great
&post=1
&parent=5
&is_active=true
&ordering=-created_at
```

**Success Response (200):**
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "content": "My comment on the post",
            "author": 1,
            "author_info": {
                "id": 1,
                "username": "testuser",
                "fullname": "Test User",
                "avatar": "/media/avatars/avatar.jpg"
            },
            "parent": null,
            "is_active": true,
            "replies_count": 2,
            "is_reply": false,
            "created_at": "2025-10-03T10:00:00Z",
            "updated_at": "2025-10-03T10:00:00Z"
        }
    ]
}
```

---

### 28. Get Comments by Post
**GET** `/comments/post/{post_id}/`

**Example:** `/comments/post/1/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
{
    "post": {
        "id": 1,
        "title": "Introduction to AI",
        "slug": "introduction-to-ai"
    },
    "comments": [
        {
            "id": 1,
            "content": "Great article!",
            "author": 1,
            "author_info": {
                "id": 1,
                "username": "testuser",
                "fullname": "Test User",
                "avatar": "/media/avatars/avatar.jpg"
            },
            "parent": null,
            "is_active": true,
            "replies_count": 2,
            "is_reply": false,
            "created_at": "2025-10-02T10:00:00Z",
            "updated_at": "2025-10-02T10:00:00Z",
            "replies": [
                {
                    "id": 2,
                    "content": "Thanks!",
                    "author": 3,
                    "author_info": {
                        "id": 3,
                        "username": "author",
                        "fullname": "Post Author",
                        "avatar": null
                    },
                    "parent": 1,
                    "is_active": true,
                    "replies_count": 0,
                    "is_reply": true,
                    "created_at": "2025-10-02T11:00:00Z",
                    "updated_at": "2025-10-02T11:00:00Z"
                }
            ]
        }
    ],
    "comments_count": 12
}
```

---

### 29. Get Comment Replies
**GET** `/comments/post/{comment_id}/replies/`

**Example:** `/comments/post/5/replies/`

**Headers:**
```
Authorization: Bearer {access_token} (optional)
```

**Success Response (200):**
```json
{
    "parent_comment": {
        "id": 5,
        "content": "Great post!",
        "author": 1,
        "author_info": {
            "id": 1,
            "username": "testuser",
            "fullname": "Test User",
            "avatar": "/media/avatars/avatar.jpg"
        },
        "parent": null,
        "is_active": true,
        "replies_count": 3,
        "is_reply": false,
        "created_at": "2025-10-03T10:00:00Z",
        "updated_at": "2025-10-03T10:00:00Z"
    },
    "replies": [
        {
            "id": 6,
            "content": "I agree!",
            "author": 2,
            "author_info": {
                "id": 2,
                "username": "user2",
                "fullname": "User Two",
                "avatar": null
            },
            "parent": 5,
            "is_active": true,
            "replies_count": 0,
            "is_reply": true,
            "created_at": "2025-10-03T11:00:00Z",
            "updated_at": "2025-10-03T11:00:00Z"
        },
        {
            "id": 7,
            "content": "Me too!",
            "author": 4,
            "author_info": {
                "id": 4,
                "username": "user3",
                "fullname": "User Three",
                "avatar": "/media/avatars/user3.jpg"
            },
            "parent": 5,
            "is_active": true,
            "replies_count": 0,
            "is_reply": true,
            "created_at": "2025-10-03T12:00:00Z",
            "updated_at": "2025-10-03T12:00:00Z"
        }
    ],
    "replies_count": 3
}
```

---

## Common Error Responses

### 400 Bad Request
```json
{
    "field_name": [
        "Error message"
    ]
}
```

**Examples:**
```json
{
    "post": ["Post not found"]
}
```

```json
{
    "parent": ["Parent comment must belong to the same post"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error."
}
```

---

## Postman Environment Variables

Create an environment with these variables:

```
base_url: http://localhost:8000/api/v1
access_token: (will be set after login)
refresh_token: (will be set after login)
user_id: (will be set after login)
post_id: (for testing comments)
comment_id: (for testing replies)
```

## Postman Pre-request Script (for authenticated requests)

```javascript
pm.environment.set("access_token", pm.environment.get("access_token"));
```

## Postman Tests Script (for login/register)

```javascript
if (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
    if (jsonData.user) {
        pm.environment.set("user_id", jsonData.user.id);
    }
}
```

## Postman Tests Script (for creating post/comment)

```javascript
if (pm.response.code === 201) {
    var jsonData = pm.response.json();
    if (jsonData.id) {
        // For posts
        pm.environment.set("post_id", jsonData.id);
        // For comments
        pm.environment.set("comment_id", jsonData.id);
    }
}
```

---

## Testing Order Recommendation

### Phase 1: Authentication
1. **Register User** → Save tokens
2. **Login User** → Update tokens
3. **Get Profile** → Verify authentication

### Phase 2: Setup Content
4. **Create Category** → Get category ID
5. **Create Post** → Get post ID (save to environment)

### Phase 3: Posts Testing
6. **Get All Posts** → Verify post appears
7. **Get Post Detail** → Verify slug works
8. **Update Post** → Test edit functionality
9. **Get My Posts** → Verify filter works
10. **Get Popular Posts** → Test sorting
11. **Get Recent Posts** → Test ordering

### Phase 4: Comments Testing
12. **Create Comment** → Create main comment on post
13. **Get All Comments** → Verify comment appears
14. **Get Comment Detail** → Test with replies
15. **Create Reply** → Reply to existing comment
16. **Get Comments by Post** → Test nested structure
17. **Get Comment Replies** → Test reply filtering
18. **Update Comment** → Test edit
19. **Get My Comments** → Verify ownership filter
20. **Delete Comment** → Test soft delete

### Phase 5: Profile Management
21. **Update Profile** → Test profile editing
22. **Change Password** → Test security
23. **Logout** → Clean session

---

## Notes

### General
- All timestamps are in ISO 8601 format (UTC)
- Image uploads require `multipart/form-data` content type
- Pagination is set to 20 items per page by default
- Search is case-insensitive
- Ordering supports multiple fields (comma-separated)
- Use `-` prefix for descending order (e.g., `-created_at`)

### Posts
- Draft posts are only visible to their authors
- Views count increments automatically on GET requests to post detail
- Published posts are visible to everyone

### Comments
- Comments have a nested structure (parent/child)
- Soft delete is used (comments are marked as inactive, not deleted)
- Only active comments (`is_active=True`) are shown by default
- Parent comment must belong to the same post as the reply
- Comments on draft posts are not accessible via public endpoints

### Permissions
- **AllowAny**: No authentication required (public access)
- **IsAuthenticated**: Must be logged in
- **IsAuthenticatedOrReadOnly**: Anyone can read, only authenticated can write
- **IsAuthorOrReadOnly**: Anyone can read, only author can edit/delete

---

## Quick Reference - All Endpoints

### Authentication (7)
- POST `/auth/register/`
- POST `/auth/login/`
- GET `/auth/profile/`
- PUT/PATCH `/auth/profile/`
- PUT `/auth/change-password/`
- POST `/auth/token/refresh/`
- POST `/auth/logout/`

### Categories (6)
- GET `/posts/category/`
- POST `/posts/category/`
- GET `/posts/category/{slug}/`
- PUT/PATCH `/posts/category/{slug}/`
- DELETE `/posts/category/{slug}/`
- GET `/posts/category/{category_slug}/posts/`

### Posts (8)
- GET `/posts/`
- POST `/posts/`
- GET `/posts/{slug}/`
- PUT/PATCH `/posts/{slug}/`
- DELETE `/posts/{slug}/`
- GET `/posts/my-posts/`
- GET `/posts/popular/`
- GET `/posts/recent/`

### Comments (8)
- GET `/comments/`
- POST `/comments/`
- GET `/comments/{id}/`
- PUT/PATCH `/comments/{id}/`
- DELETE `/comments/{id}/`
- GET `/comments/my-comments/`
- GET `/comments/post/{post_id}/`
- GET `/comments/post/{comment_id}/replies/`

**Total: 29 endpoints**