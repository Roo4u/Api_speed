FROM ubuntu:latest

# Installieren von Python und anderen Abhängigkeiten
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Kopieren Sie Ihre Python-Dateien in das Image
COPY app.py /app/app.py
COPY wsgi.py /app/wsgi.py
COPY requirements.txt /app/requirements.txt

# Installieren Sie die erforderlichen Pakete
RUN pip3 install -r /app/requirements.txt

# Setzen Sie das Arbeitsverzeichnis
WORKDIR /app

# Starten Sie die API mit Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]