# Backend for the Secret Santa app

To run the backend locally, simply run the following commands:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Before this project can be deployed to production, the following should be done:

1. Split the settings.py file into local and production settings
2. Configure an RDS for the production environment
3. Configure a mailing service for the production environment like SES
4. Update the settings to use environment variables
5. Update `ALLOWED_HOSTS`,`CSRF_TRUSTED_ORIGINS` and `CORS_ORIGIN_WHITELIST`