# Configuration

The application can be configured via Environment variables. The `ENVIRONMENT` variable sets sensible defaults based on its value. The following environments available:

  * `default` - Default settings suitable for production.
  * `develop` - Settings for local development with debugging enabled.

## Environment Variables

| Variable Name                      | Description                                         | Default Value                          |
|------------------------------------|-----------------------------------------------------|----------------------------------------|
| `ENVIRONMENT`                      | Sets the environment for the application.           | `default`                              |
| `RELEASE`                          | The release version of the application.             | `None`                                 |
| `SENTRY_DSN`                       | The DSN for Sentry error tracking.                  | `None`                                 |
| `DEBUG`                            | Enables or disables debug mode.                     | `True` if `ENVIRONMENT` is `develop`   |
| `SECRET_KEY`                       | The secret key for the application.                 | `not-a-secret-key` if `DEBUG` is `True`|
| `ALLOWED_HOST`                     | The allowed host for the application.               | `None`                                 |
| `STATIC_ROOT`                      | The directory where static files are collected.     | `BASE_DIR/public/static`               |
| `DATA_DIR`                         | The directory for storing data.                     | `BASE_DIR/data`                        |
| `EMBEDDING_MODEL_NAME`             | The name of the embedding model to use.             | `intfloat/multilingual-e5-small`       |
| `EMBEDDING_MODEL_CACHE_DIR`        | The directory for caching the embedding model.      | `DATA_DIR/embedding`                   |
