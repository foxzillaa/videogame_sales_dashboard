
FROM python:3.9-slim


WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto usado por Streamlit
EXPOSE 8501


CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
