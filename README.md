## Utilização
Crie um `.env` seguindo o exemplo do `.env.example` (Vou dar um exemplo com uma fila local com [elasticmq](https://github.com/softwaremill/elasticmq)):

```env
SQS_ENDPOINT=http://localhost:9324
SQS_QUEUE_URL=http://localhost:9324/000000000000/fila-exemplo.fifo
AWS_REGION=sa-east-1
AWS_ACCESS_KEY_ID=dummy
AWS_SECRET_ACCESS_KEY=dummy
```

Depois disso é só rodar um `docker compose` e ser feliz:

```sh
docker compose up --build -d
```

As mensagens consumidas vão ser exibidas no log do container, então fique de olho com o comando:

```sh
docker logs -f sqs-consumer
```
