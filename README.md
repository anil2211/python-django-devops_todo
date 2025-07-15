# 📝 Django ToDo App

A simple and elegant web-based ToDo List application built using the Django framework. It allows users to create, mark as complete, and delete tasks.

---

## 🚀 Features

- Add new tasks
- Mark tasks as complete/incomplete
- Delete tasks
- Responsive layout using Bootstrap
- Modern UI with centered layout

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, FontAwesome
- **Database:** SQLite (default)

---

## ⚙️ Setup Instructions

Follow the steps below to run this project locally.

### 🔧 Prerequisites

- Python 3.7+ installed
- pip (Python package installer)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) *(optional but recommended)*

---

### 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/django-todo-app.git
cd django-todo-app

# 2. Create virtual environment
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver
