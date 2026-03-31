# Desafio MBA Engenharia de Software com IA - Full Cycle

## Configuração das variáveis de ambiente

1. Copie o arquivo de exemplo para criar o seu `.env` local:

   ```bash
   cp .env.example .env
   ```

1. Preencha os valores no arquivo `.env` com suas credenciais:

   - `OPENAI_API_KEY`: sua chave de API da OpenAI
   - `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL (ex: `postgresql://user:password@localhost:5432/dbname`)
   - `PG_VECTOR_COLLECTION_NAME`: nome da coleção a ser criada no pgvector (ex: `documents`)
   - `PDF_PATH`: caminho para o arquivo PDF a ser ingerido (padrão: `document.pdf`)

---

## Inicialização do ambiente virtual (venv)

No diretório do projeto, crie/ative o ambiente virtual do Python:

<pre>python -m venv venv</pre>
<pre>.\venv\Scripts\activate</pre>

Instale as dependências do projeto com o comando abaixo:

<pre>pip install -r requirements.txt</pre>

## Ordem de execução

1. Subir o banco de dados com Docker:
<pre>docker compose up -d</pre>

2. Executar ingestão do PDF:
<pre>python src/ingest.py</pre>

3. Rodar o chat:
<pre>python src/chat.py</pre>
