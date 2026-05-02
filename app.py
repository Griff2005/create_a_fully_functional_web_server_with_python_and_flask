# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for storing user data (example)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Flask App</title>
</head>
<body>
    <h1>Welcome to the Flask App</h1>
    <form method="POST" action="{{ url_for('add_user') }}">
        <input type="text" name="username" placeholder="Enter username" required>
        <button type="submit">Add User</button>
    </form>
</body>
</html>
```

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>{% block title %}Flask App{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

```plaintext
# requirements.txt
Flask==2.0.3
Flask-SQLAlchemy==2.5.1
```

```python
# tests/test_app.py
import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Flask App' in response.data

def test_add_user(client):
    response = client.post('/add_user', data={'username': 'testuser'})
    assert response.status_code == 302  # Redirects after adding a user
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
```

```css
/* static/style.css */
body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
}

h1 {
    color: #007bff;
}

form {
    margin-top: 20px;
}