### Install and Run Server

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

3. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Automated Testing
```bash
python manage.py test
```

## Access the Website
Once the server is running, visit:
- Home page: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`
To create a superuser for admin:
```bash
python manage.py createsuperuser
```


