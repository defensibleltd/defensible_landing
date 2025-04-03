FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health

RUN apt-get update && apt-get install -y gcc weasyprint 

RUN python3 -m pip install poetry

RUN poetry install --all-extras

ENTRYPOINT ["poetry", "run", "streamlit", "run", "ipfabric_reports/frontend/frontend.py", "--server.port=80", "--theme.primaryColor=#8C989B", "--theme.backgroundColor=#222D32", "--theme.secondaryBackgroundColor=#264183", "--theme.textColor=#F6F6F6", "--theme.font=monospace", "--server.enableCORS=false"]
