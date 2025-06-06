# 📝 Notes API

A Django REST API for managing personal notes. Supports user authentication, note creation, tagging, and automatic log tracking. Built with Django REST Framework.

## Features

- User registration & login (token-based)
- CRUD operations on notes
- Tag support for notes
- Search notes by title/content
- Automatic log creation per note
- Modular and extensible architecture

## Installation

1. **Clone the repository**
    ```
   git clone https://github.com/yourusername/notes-api.git
   cd notes-api
    ```
    
2. **Create and activate a virtual environment**
    ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations**
    ```
   python manage.py migrate
    ```

5. **Create a superuser (optional)**
    ```
   python manage.py createsuperuser
    ```
6. **Run the development server**
    ```
   python manage.py runserver
    ```

## API Endpoints

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| POST   | `/api/register/`  | Register new users       |
| POST   | `/api/login/`     | Obtain auth token        |
| GET    | `/api/notes/`     | List all user notes      |
| POST   | `/api/notes/`     | Create a new note        |
| GET    | `/api/note/<id>/` | Retrieve a specific note |
| PUT    | `/api/note/<id>/` | Update a note            |
| DELETE | `/api/note/<id>/` | Delete a note            |

## Authentication

Token-based authentication is required for all note endpoints. Use the token returned from `/api/login/` in the `Authorization` header:

```
Authorization: Token your_token_here
```

## License

This project is licensed under the MIT License.
