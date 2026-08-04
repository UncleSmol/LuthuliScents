What this workflow does

- Sets the `BOBGO_API_KEY` environment variable on your Railway project and triggers a deploy.
- Runs on push to `main` and can be manually dispatched from the Actions tab.

Secrets you must add to the GitHub repository (Settings → Secrets → Actions):

- `RAILWAY_API_KEY` — Your Railway service token (create in Railway account settings).
- `RAILWAY_PROJECT_ID` — The Railway project ID to deploy (visible in Railway project settings or in the URL).
- `BOBGO_API_KEY` — Your BobGo API key (this will be written into the Railway project env during the workflow).

How to trigger

- Add the three secrets above.
- Push to `main` or open the Actions tab and run the "Deploy to Railway" workflow manually.

Notes & security

- Keep `RAILWAY_API_KEY` and `BOBGO_API_KEY` private — they are stored encrypted in GitHub Secrets.
- If you prefer not to store `BOBGO_API_KEY` in GitHub, you can manually add it in Railway UI instead and skip adding it as a secret.
