FROM python:3.12.1

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV OPENAI_API_KEY="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"

CMD ["python", "app.py"]