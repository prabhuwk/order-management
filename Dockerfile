FROM python:3.11.6-slim-bookworm

WORKDIR /app
RUN useradd -m trader && chown -R trader:trader /app/
USER trader

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src /app/src
CMD ["bash"]
