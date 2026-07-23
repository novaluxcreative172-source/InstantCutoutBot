# InstantCutoutBot

A Telegram bot that removes image backgrounds, powered by the open-source
rembg (u2net) model — no paid API, no API key required.

Send it a photo → get back a transparent PNG.

## How it works

- bot.py runs a long-polling Telegram bot (python-telegram-bot).
- Incoming photos/images are passed to rembg.remove(), which runs a
  pre-trained segmentation model locally to strip the background.
- The result is sent back as a PNG with an alpha channel.

## 1. Create the bot on Telegram

1. Open Telegram, message @BotFather.
2. /newbot → give it a name and a username ending in `bot`
   (e.g. InstantCutoutBot).
3. BotFather gives you a token — save it, you'll need it below.

## 2. Push this code to GitHub

    cd InstantCutoutBot
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/<your-username>/InstantCutoutBot.git
    git push -u origin main

## 3. Deploy on Railway

1. Go to railway.app → New Project → Deploy from GitHub repo →
   select InstantCutoutBot.
2. Railway auto-detects Python via Nixpacks and reads railway.json.
3. Go to your service's Variables tab and add:
   - BOT_TOKEN = the token from BotFather
4. Railway will build and deploy automatically. Check the Deploy Logs —
   you should see "InstantCutoutBot starting (polling mode)...".

No exposed port needed, since the bot uses polling rather than webhooks.
Railway will keep it running as a background worker.

## Resource notes

- The first run downloads the u2net.onnx model (~176 MB) — cached for
  subsequent runs, though Railway's ephemeral filesystem may re-download
  it after redeploys.
- Recommended: at least 1 GB RAM on your Railway plan.
- Consider a Railway volume mounted at /root/.u2net to persist the model
  between deploys.

## Local testing

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export BOT_TOKEN=your_token_here
    python bot.py
