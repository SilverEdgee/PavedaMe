# PavedaMe

Requirements:

- Python 3.12 or newer
- uv
- just
- Docker and Docker Compose

Setup:

1. Prepare the project:

```bash
just bootstrap
```

2. Edit `.env`. A local PostgreSQL configuration can look like this:

```env
POSTGRES_USER=postgres
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
POSTGRES_DRIVER=asyncpg
POSTGRES_DB=pavedame
```

3. Configure Gmail SMTP in `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_google_app_password
SMTP_FROM_NAME=PavedaMe
SMTP_START_TLS=True
SMTP_TIMEOUT=30
```

Enable two-step verification in your Google account and create an App Password. Write the App Password without spaces. Do not use your regular Google password and do not commit `.env`.

4. Start PostgreSQL:

```bash
just up
```

5. Apply database migrations:

```bash
just migrate
```

6. Start the API:

```bash
just uvicorn
```

Open Swagger UI at:

```text
http://localhost:8000/docs
```

To test email verification, register with `POST /auth/signup`, open the email sent by PavedaMe, and follow the verification link.

Development checks:

```bash
just lint
just static
```
