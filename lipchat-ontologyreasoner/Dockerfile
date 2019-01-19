FROM python:3.6

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && \
  python -m spacy download en_core_web_sm && \
  python -m spacy link en_core_web_sm en && \
  python -c "import nltk; nltk.download('all');"

ENTRYPOINT ["python", "server.py"]

