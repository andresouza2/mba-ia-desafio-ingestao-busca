# Desafio MBA Engenharia de Software com IA - Full Cycle

## Inicialização do ambiente virtual (venv)

No diretório do projeto, crie/ative o ambiente virtual do Python:

<pre>python -m venv venv</pre>
<pre>.\venv\Scripts\activate</pre>

## Ordem de execução

1. Subir o banco de dados com Docker:
<pre>docker compose up -d</pre>

2. Executar ingestão do PDF:
<pre>python src/ingest.py</pre>

3. Rodar o chat:
<pre>python src/chat.py</pre>
