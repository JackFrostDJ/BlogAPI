# Blog API with AI Post Generation

A RESTful API built with **Django** and **Django REST Framework** that allows users to:
- Create, view, update, and delete blog posts
- Add and manage comments for each post
- Generate AI-powered blog posts using the Featherless API (Bonus feature)
- Interact via a clean, responsive HTML/JS frontend

## Features
- **Posts**: CRUD operations via `/api/posts/`
- **Comments**: CRUD operations via `/api/comments/`
- **AI Post Generation**: `/api/generate_post/` accepts a prompt and returns a generated blog post
- **Frontend**: `frontend.html` provides a user-friendly interface for interacting with all API endpoints

## Project Structure

```
blog_api/                # Django project config
│
├── blog/                # Blog app
│   ├── models.py        # Post & Comment models
│   ├── serializers.py   # DRF serializers for Post & Comment
│   ├── views.py         # ViewSets + AI generation endpoint + frontend renderer
│   ├── urls.py          # API routing
│   └── templates/blog/frontend.html  # Simple HTML+JS UI
│
├── blog_api/settings.py # Project settings
├── blog_api/urls.py     # Root URL configuration
├── manage.py
└── requirements.txt
```

## Design Choices

### **1. Models**
Defined two main models in `models.py`:
- **Post**: Title, content, author, timestamp
- **Comment**: Linked to Post, with name, text, timestamp  
Relation: `Post` → `Comment` via ForeignKey (`related_name="comments"`).

### **2. Serialization**
- `PostSerializer` nests `CommentSerializer` so that GET requests for a post include its comments.
- All fields are exposed for flexibility.

### **3. Views**
- **ViewSets** for `Post` and `Comment` provide full CRUD via DRF routers.
- **AI generation endpoint** (`generate_post`) integrates with Featherless API for LLM-powered blog content.
- **frontend_view** serves the HTML UI.

### **4. API Documentation**
- Browsable API automatically available via Django REST Framework at `/api/posts/`, `/api/comments/`, `/api/generate_post/`.

### **5. Frontend**
- Single-page `frontend.html`:
  - Lists all posts and comments
  - Add/Edit/Delete posts and comments
  - Trigger AI post generation
  - Incremental “Show More” for comments
- Pure HTML/CSS/JS using Fetch API so no frameworks needed.

---

## Running Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Set environment variables
```bash
FEATHERLESS_API_KEY="your_api_key_here"
```

### 4. Start the server
```bash
python manage.py runserver
```

---

## API Endpoints

### **Posts**
| Method | Endpoint             | Description            |
|--------|----------------------|------------------------|
| GET    | `/api/posts/`        | List all posts         |
| POST   | `/api/posts/`        | Create a post          |
| GET    | `/api/posts/{id}/`   | Retrieve post details  |
| PUT    | `/api/posts/{id}/`   | Update a post          |
| DELETE | `/api/posts/{id}/`   | Delete a post          |

### **Comments**
| Method | Endpoint               | Description              |
|--------|------------------------|--------------------------|
| GET    | `/api/comments/`       | List all comments        |
| POST   | `/api/comments/`       | Create a comment         |
| GET    | `/api/comments/{id}/`  | Retrieve comment details |
| PUT    | `/api/comments/{id}/`  | Update a comment         |
| DELETE | `/api/comments/{id}/`  | Delete a comment         |

### **AI Post Generation**
| Method | Endpoint               | Description                               |
|--------|------------------------|-------------------------------------------|
| POST   | `/api/generate_post/`   | Generate a blog post from a given prompt |

Payload:
```json
{
  "prompt": "Benefits of AI in healthcare"
}
```

---

## Using the Frontend

1. Place `frontend.html` inside `blog/templates/blog/`.
2. In `views.py`, ensure `frontend_view` is defined and mapped in `urls.py`:
```python
from django.urls import path, include
from .views import frontend_view

urlpatterns = [
    path("", frontend_view),
    path("api/", include(router.urls)),
    path("api/generate_post/", generate_post),
]
```
3. Access via `http://127.0.0.1:8000/`
4. Use UI to:
   - Create posts
   - Add/view/delete comments
   - Generate AI posts
   - View all posts and comments

---

## Bonus Points
- Fully functional AI blog generation endpoint implemented.
- Frontend to interact with all endpoints without external tools like Postman.