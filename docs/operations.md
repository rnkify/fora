# Fora operations runbook

This runbook is for Fora V1.1. Production consists of the `fora-web` Django
service and its separate Railway PostgreSQL service.

## Setup and required configuration

For local development, copy `.env.example` to `.env`, use a local PostgreSQL
`DATABASE_URL`, then follow the README commands. Production requires a unique
`SECRET_KEY`, PostgreSQL `DATABASE_URL`, absolute HTTPS `APP_URL`, explicit
`ALLOWED_HOSTS`, explicit HTTPS `CSRF_TRUSTED_ORIGINS`, and `DEBUG=False`.
Never put credentials in Git or command output.

## Deploy and verify

Link the CLI to the production project and confirm the target before deploying:

```shell
railway status
railway service status --service fora-web
railway up --service fora-web
railway logs --service fora-web
```

**Always deploy only `fora-web`. Never run `railway up` against `Postgres`.**
The container startup script applies pending migrations transactionally before
Gunicorn starts. The Railway deployment health check uses `/health/`; `/ready/`
also verifies PostgreSQL connectivity. After a deploy, require HTTP 200 from both,
confirm static CSS returns HTTP 200, and run:

```shell
railway ssh --service fora-web -- env DJANGO_SETTINGS_MODULE=config.settings.production python manage.py showmigrations
```

## Staff operations

Create a staff operator without putting a password on the command line:

```shell
railway ssh --service fora-web -- env DJANGO_SETTINGS_MODULE=config.settings.production python manage.py createsuperuser
```

Reset a lost password interactively with `railway ssh --service fora-web -- env
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py changepassword
USERNAME`.
Operators sign in at `/ops/login/`; unauthenticated `/ops/` requests return there
with a validated `next` destination.

An inquiry creates a lead. Staff review and qualify the lead, set service, plan,
value and follow-up, then mark it Won. Starting delivery creates exactly one
project and opens its workspace. Project status, due date, activity and tasks form
the lightweight delivery record.

## SMTP

Inquiry notification email is optional and provider-neutral. Configure these on
`fora-web`: `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USERNAME`,
`EMAIL_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_TIMEOUT`, `DEFAULT_FROM_EMAIL`, and
`INQUIRY_NOTIFICATION_EMAIL`. Use
`django.core.mail.backends.smtp.EmailBackend`; normally use port 587, TLS, and the
existing 10-second timeout. Submit one clearly labelled demo inquiry to a recipient
controlled by the operator, confirm receipt and confirm the inquiry persisted.
Then remove the demo record only through an intentional staff/admin operation.
Delivery errors are logged by inquiry ID and do not roll back the inquiry.

## Database backups and restore testing

In Railway, open **Postgres → Backups** and enable Daily, Weekly and Monthly volume
backups. Railway retains daily backups for 6 days, weekly backups for 1 month and
monthly backups for 3 months. Create and lock a manual backup before a risky schema
or infrastructure change. For stronger recovery-point coverage, enable PostgreSQL
PITR from the same tab if the account permits it; PITR restoration creates a new
sibling database instead of changing the source.

At least quarterly, test recovery without touching production:

1. Select a backup in **Postgres → Backups** and restore it to a separate volume or
   use PITR to create a new sibling PostgreSQL service.
2. Do not change `fora-web`'s `DATABASE_URL`. Connect a temporary verification
   environment to the restored database.
3. Run `python manage.py showmigrations --plan`, `python manage.py check`, and
   read-only counts for inquiries, leads, projects, activities and tasks.
4. Open `/ready/` on that temporary environment and inspect representative records.
5. Record the backup timestamp and result, then remove the temporary recovery
   service only after verification. Never rehearse a restore against live storage.

An additional portable backup can be made from a trusted machine with the matching
PostgreSQL client: `pg_dump --format=custom --no-owner --no-acl --file=fora.dump
"$DATABASE_URL"`. Store the dump encrypted outside the primary database lifecycle.
Restore it only into an empty separate database with `pg_restore --no-owner
--no-acl --dbname "$RESTORE_DATABASE_URL" fora.dump`, then perform the same checks.

## Recovery and rollback

- Deployment fails: leave the prior deployment serving, inspect `railway logs
  --service fora-web`, fix only the failure, run the release gate, and redeploy.
- PostgreSQL/readiness fails: verify the Postgres service and volume are healthy,
  then verify the `DATABASE_URL` reference on `fora-web`; do not replace it with a
  copied credential unless recovery requires a deliberate cutover.
- Static assets fail: confirm the Docker build completed `collectstatic` and that
  the CSS URL returns 200; rebuild the same release rather than editing production.
- Migration fails: stop the release, preserve the logs and take a backup. Determine
  whether the migration is unapplied or partially applied before retrying. Do not
  fake migration state or reverse data migrations without a reviewed recovery plan.
- Operator password is lost: use the interactive `changepassword` command above.

To roll back code, identify the previous known-good annotated tag with
`git tag --sort=-creatordate` and inspect it before deployment. Check it out in a
separate worktree, link that worktree to the same Railway project, explicitly select
`fora-web`, and deploy it. A code rollback does not automatically reverse database
migrations; keep forward-compatible schema changes in place unless a reviewed,
backup-backed migration rollback is required.
