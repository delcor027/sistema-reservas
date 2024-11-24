# Testando Métodos Individualmente com Pytest

Para testar métodos individuais em seus arquivos de teste, utilize o comando `pytest` com o parâmetro `--cache-clear` seguido do caminho do arquivo e o método específico, escolhi essa alternativa pois os testes estavam tendo bug de loop e assíncronos em testar vários de uma vez, por isso testei somente de forma única com este comando no terminal.

### Exemplo de Uso

Se quiser testar apenas o método `test_get_rooms_with_filters`, execute o seguinte comando no terminal:

```bash
pytest --cache-clear app/tests/test_rooms.py::test_get_rooms_with_filters
```

## Estrutura do Comando

- **`pytest`**: Comando base para executar os testes.
- **`--cache-clear`**: Garante que o cache do pytest seja limpo antes de rodar o teste, prevenindo resultados inconsistentes.
- **`<caminho do arquivo>`**: Caminho completo para o arquivo de teste onde o método está localizado.
- **`::<nome do método>`**: Nome exato do método de teste a ser executado.

## Benefícios

- Permite testar métodos específicos de forma isolada.
- Evita a execução desnecessária de outros testes, otimizando o tempo.
- Facilita a depuração de testes com falhas.

## Recomendações

- Certifique-se de que o nome do método está correto.
- Utilize o parâmetro `--cache-clear` sempre que alterar o código para evitar inconsistências.

Com este guia, você pode testar métodos individuais com clareza e eficiência! 🚀

# Sistema de Reservas

## Visão Geral

Este projeto é uma aplicação FastAPI para gerenciar reservas de salas, incluindo funcionalidades como criar, listar, atualizar e deletar reservas e salas. A aplicação utiliza MongoDB como banco de dados e Docker/Docker Compose para provisionamento e execução.

---

## Estrutura do Projeto

### Diretórios e Arquivos

- `app/`:
  - `builders/`: Lógica para construção de filtros de consulta.
  - `factories/`: Implementação de Factory Patterns para criar objetos de domínio.
  - `models/`: Definições de modelos de dados com Pydantic.
  - `routers/`: Serviços REST para reservas e salas.
  - `services/`: Contém validações e lógica adicional para a aplicação.
  - `tests/`: Testes automatizados utilizando pytest.
  - `database.py`: Configuração do banco de dados MongoDB.
  - `main.py`: Ponto de entrada para a aplicação.

- Arquivos de configuração:
  - `Dockerfile`: Configuração para construção do container Docker.
  - `docker-compose.yml`: Orquestração de serviços Docker.
  - `pyproject.toml` e `poetry.lock`: Gerenciamento de dependências com Poetry.

---

## Requisitos

- **Python 3.12+**
- **Poetry 1.6.1+**
- **Docker e Docker Compose**

---

## Configuração e Execução

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd sistema_reservas
```

### 2. Instalar Dependências

Usando o **Poetry**:

```bash
poetry install
```

### 3. Configurar o MongoDB

Certifique-se de que o MongoDB está configurado localmente ou utilize o contêiner definido no **`docker-compose.yml`**.

### 4. Executar com Docker Compose

```bash
docker-compose up --build
```

A aplicação estará disponível em **`http://localhost:8000/docs#/`**.

## Endpoints

### Reservas (`/reservations`)

- **GET** `/reservations?user=<user>`: Lista todas as reservas de um usuário.
- **POST** `/reservations`: Cria uma nova reserva.
  - **Body**:
    ```json
    {
      "user": "usuario1",
      "room_id": "id_da_sala",
      "start_time": "2024-11-25T14:00:00",
      "end_time": "2024-11-25T15:00:00"
    }
    ```
- **DELETE** `/reservations/{reservation_id}`: Exclui uma reserva.

### Salas (`/rooms`)

- **POST** `/rooms`: Cria uma nova sala.
  - **Body**:
    ```json
    {
      "name": "Sala A",
      "capacity": 10,
      "resources": ["Wi-Fi", "Projetor"],
      "status": "A"
    }
    ```
- **GET** `/rooms`: Lista salas com filtros opcionais:
  - **Query Params**: `capacity`, `resources`.
- **GET** `/rooms/{room_id}`: Retorna os detalhes de uma sala.
- **PUT** `/rooms/{room_id}`: Atualiza uma sala existente.
- **DELETE** `/rooms/{room_id}`: Exclui uma sala.

