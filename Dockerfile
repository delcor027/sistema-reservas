# Use a imagem oficial do Python
FROM python:3.12-slim

# Variáveis de ambiente para desativar buffer e configurar o Poetry
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    curl build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências do Poetry
COPY pyproject.toml poetry.lock ./

# Instala as dependências sem criar um virtualenv
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copia o restante do código do projeto
COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando para rodar o servidor FastAPI
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
