# Streamlit Frontend

The Streamlit app is in `streamlit_app.py` and talks to the FastAPI backend.

Run the full stack with Docker:

```bash
docker compose up --build
```

Open the Streamlit UI:

```text
http://localhost:8501
```

Open the FastAPI docs:

```text
http://localhost:8000/docs
```

For local development without Docker, start the API first:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then start Streamlit in another terminal:

```bash
streamlit run streamlit_app.py
```
