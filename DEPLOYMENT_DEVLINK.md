# DevLink review deployment

URL: https://devlink.com.ar/campingacalujan/

The independent Docker Compose project lives at `/opt/camping_aca_devlink`.
It uses the existing `traefik_proxy` network and PostgreSQL container, with its
own `camping_aca_devlink` database, copied media, static directory and logs.
The older `/opt/camping_aca_web` installation remains separate.

`docker-compose.devlink.yml` strips the URL prefix at Traefik, and configures
Django's `FORCE_SCRIPT_NAME`, HTTPS proxy trust and scoped session/CSRF cookies.
It does not publish a host port or run the legacy initialization entrypoint.
Database restoration is an explicit first-deployment operation. Startup only
collects static files and runs Gunicorn.

Credentials are read from a server-only `.env` with mode 0600. Never commit it.
Set `CAMPING_RELEASE` to the deployed Git revision when building or updating:

```sh
docker compose -p camping-devlink -f docker-compose.devlink.yml build
docker compose -p camping-devlink -f docker-compose.devlink.yml up -d
docker compose -p camping-devlink -f docker-compose.devlink.yml ps
```

After the initial restore, run `python scripts/prepare_devlink.py` inside the
new image with the new database selected. It polishes copied public text,
hides historical rates without deleting their values, selects the forest
photograph and disables the copied administrator only if its password is the
old predictable default. Administrators are created explicitly; startup never
creates an account or prints a password.

Verification includes the landing, prefixed static/media files, login redirects,
CSRF cookie path, browser console, expanded mobile navigation and text contrast.
Run automated checks with the isolated local settings:

```powershell
.\.venv\Scripts\python.exe manage.py test scripts.test_subpath scripts.test_landing_front scripts.test_dev_preview --settings=config.settings_local
```

Rollback: stop only `camping_aca_devlink` to remove this dedicated route, or
recreate it using its previously deployed image tag. Keep the review database,
media and backup intact. Do not run `docker compose down -v`, delete a database,
or modify the shared Traefik service as part of rollback.
