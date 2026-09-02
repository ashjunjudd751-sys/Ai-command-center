# AI Command Center — iPhone Web App

This package is designed for iPhone testing without a Mac. The FastAPI server serves the mobile web app from the same origin, so the browser does not need a separate API URL.

## Deploy from a phone

The simplest route is to put this folder in a GitHub repository and deploy it as a Docker web service on a host such as Render. Set `OPENAI_API_KEY` in the host's environment variables. The included `render.yaml` is a starting blueprint.

After deployment, open the HTTPS URL in Safari. On iOS 26, Safari can add websites to the Home Screen as web apps; Apple documents: Share → Add to Home Screen → Open as Web App → Add.

## Important

- Never put `OPENAI_API_KEY` in frontend JavaScript.
- Use the deployed HTTPS URL on the phone.
- SQLite is suitable for testing, but production should move to PostgreSQL and durable file storage.
