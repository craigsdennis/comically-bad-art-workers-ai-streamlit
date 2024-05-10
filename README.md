# Comically Bad Art Generation

This app uses the wonderful Python UI Framework [Streamlit](https://streamlit.io) and [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/).

## Setup

[Sign up for Cloudflare](https://dash.cloudflare.com/sign-up) if you haven't yet already...its free and like c'mon. Head over to the Workers AI section in your dash. On the Overview page there is a button that says use the REST API, which this demo is doing. Get your values and copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Put your `CLOUDFLARE_ACCOUNT_ID` and the api token you generated into `CLOUDFLARE_API_TOKEN`

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
python -m streamlit run app.py
```
