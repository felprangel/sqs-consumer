#!/usr/bin/env python3
import json
import time
import signal
import sys
import os
import boto3
from botocore.exceptions import ClientError
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)

SQS_ENDPOINT = os.environ.get('SQS_ENDPOINT')
QUEUE_URL = os.environ.get('SQS_QUEUE_URL')
REGION = os.environ.get('AWS_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

sqs = boto3.resource(
    'sqs',
    endpoint_url=SQS_ENDPOINT,
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

queue = sqs.Queue(QUEUE_URL)

running = True

def process_message(message_body):
    try:
        data = json.loads(message_body)

        print(f"Processando mensagem: {json.dumps(data, indent=2)}")

        print(f"Mensagem processada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")
        return False

def signal_handler(sig, frame):
    global running
    print("Encerrando o consumidor...")
    running = False

def main():
    print(f"Iniciando consumidor para a fila: {QUEUE_URL}")
    print(f"Usando endpoint SQS: {SQS_ENDPOINT}")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while running:
        try:
            messages = queue.receive_messages(
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5,
                AttributeNames=['All'],
                MessageAttributeNames=['All']
            )

            for message in messages:
                print(f"Mensagem recebida: ID {message.message_id}")

                success = process_message(message.body)

                if success:
                    message.delete()
                    print(f"Mensagem {message.message_id} excluída da fila")
                else:
                    print(f"Mensagem {message.message_id} não foi processada e permanecerá na fila")

        except ClientError as e:
            print(f"Erro ao acessar a fila SQS: {e}")
            time.sleep(5)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
    print("Consumidor encerrado.")
