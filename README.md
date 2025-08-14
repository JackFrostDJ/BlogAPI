# Blog API

A RESTful API for managing blog posts and comments using Django REST Framework.

## Endpoints
- `/api/posts/` – CRUD for posts
- `/api/comments/` – CRUD for comments
- `/api/generate_post/` – AI-generated blog post from a prompt (bonus)

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver