FROM alpine:latest
WORKDIR /app
COPY . .
RUN apk update && apk add --no-cache gcc python3 py3-pip
RUN pip install --break-system-packages --upgrade pip
RUN pip install --break-system-packages -r requirements.txt
EXPOSE 9001
CMD ["python3", "main.py"]
