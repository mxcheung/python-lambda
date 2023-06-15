from confluent_kafka import SerializingProducer, DeserializingConsumer, Message, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from typing import Dict, List, Callable
import os
from urllib.parse import quote_plus
from uuid import uuid4

print(os.environ['KAFKA_BOOTSTRAP_SERVERS'])

KAFKA_INSTRUCTION_TOPIC = 'KAFKA_INSTRUCTION_TOPIC'
KAFKA_STATUS_TOPIC = 'KAFKA_STATUS_TOPIC'
KAFKA_SWIFT_TOPIC = 'KAFKA_SWIFT_TOPIC'
KAFKA_PAYMENT_CONFIRMATION_TOPIC = 'KAFKA_PAYMENT_CONFIRMATION_TOPIC'
KAFKA_FEEDBACK_TOPIC = 'KAFKA_FEEDBACK_TOPIC'
KAFKA_REGISTRY_USER = 'KAFKA_REGISTRY_USER'
KAFKA_REGISTRY_PASSWORD = 'KAFKA_REGISTRY_PASSWORD'
KAFKA_SERVER_USER = 'KAFKA_SERVER_USER'
KAFKA_SERVER_PASSWORD = 'KAFKA_SERVER_PASSWORD'
KAFKA_DEADLETTER_TOPIC = 'KAFKA_DEADLETTER_TOPIC'

def _get_default_schema(topic: str) -> str:
    return {
        os.getenv(KAFKA_INSTRUCTION_TOPIC): """
            {
              "type": "record",
              "name": "instruction",
              "namespace": "cii.dt",
              "fields": [
                {
                  "name": "instruction",
                  "type": "string"
                },
                {
                  "name": "client_id",
                  "type": "int"
                },
                {
                  "name": "bcc_entity",
                  "type": "string"
                },
                {
                  "name": "user_id",
                  "type": "string"
                },
                {
                  "name": "source_file",
                  "type": "string"
                },
                {
                  "name": "client_reference",
                  "type": "string"
                }
              ]
            }
        """,
        os.getenv(KAFKA_STATUS_TOPIC): """
            {
              "type": "record",
              "name": "status",
              "namespace": "cii.dt",
              "fields": [
                {
                  "name": "instruction",
                  "type": "string"
                },
                {
                  "name": "client_id",
                  "type": "int"
                },
                {
                  "name": "bcc_entity",
                  "type": [
                    "null",
                    {
                      "type": "enum",
                      "name": "region",
                      "symbols": [
                        "FCA",
                        "FCO",
                        "FCL",
                        "FCG",
                        "FCH",
                        "FCJ",
                        "FCS"
                      ]
                    }
                  ]
                }
              ]
            }
        """,
        os.getenv(KAFKA_SWIFT_TOPIC): """
            {
              "type": "record",
              "name": "instruction",
              "namespace": "cii.dt",
              "fields": [
                {
                  "name": "iso_message",
                  "type": "string"
                },
                {
                  "name": "client_id",
                  "type": "int"
                },
                {
                  "name": "bcc_entity",
                  "type": "string"
                }
              ]
            }
        """,
        os.getenv(KAFKA_PAYMENT_CONFIRMATION_TOPIC): """
            {
              "type": "record",
              "name": "payment_confirmation",
              "namespace": "cii.dt",
              "fields": [
                {
                  "name": "iso_message",
                  "type": "string"
                }
              ]
            }
        """,
        os.getenv(KAFKA_FEEDBACK_TOPIC): """
            {
              "type": "record",
              "name": "feedback",
              "namespace": "cii.dt",
              "fields": [
                {
                  "name": "instruction",
                  "type": "string"
                },
                {
                  "name": "client_id",
                  "type": "int"
                },
                {
                  "name": "bcc_entity",
                  "type": "string"
                }
              ]
            }
        """,
        os.getenv(KAFKA_DEADLETTER_TOPIC): """
            {
              "type": "record",
              "name": "deadletter",
              "namespace": "cii.dt",
              "fields": [
                {
                  "name": "uuid",
                  "type": "string"
                },
                {
                  "name": "datetime",
                  "type": "string"
                },
                {
                  "name": "message",
                  "type": "string"
                },
                {
                  "name": "topic",
                  "type": "string"
                },
                {
                  "name": "error",
                  "type": "string"
                },
                {
                  "name": "stacktrace",
                  "type": "string"
                }
              ]
            }
        """,
    }[topic]


def _get_default_schema_registry_client(
        registry_username: str,
        registry_password: str
) -> SchemaRegistryClient:
    registry_host = os.environ('KAFKA_REGISTRY_HOST')
    registry_proxy = os.environ('KAFKA_REGISTRY_PROXY')
    client = SchemaRegistryClient(
        {
            "url": f"https://{registry_username}:{quote_plus(registry_password)}@{registry_host}"
        }
    )
    client._rest_client.session.proxies.update({'https': registry_proxy})
    return client


def get_consumer(
        topics: List[str],
        registry_username: str,
        registry_password: str,
        server_username: str,
        server_password: str,
        consumer_group: str = "default_consumer_group",
) -> DeserializingConsumer:
    """
    Return a Kafka consumer which can poll topics `topics`.
    If the consumer group `consumer_group` is not set, then multiple subscribed consumers will not get the same
    messages. All subscribers that belong to the same consumer group will not get the same messages.
    """
    schema_registry = _get_default_schema_registry_client(
        registry_username=registry_username,
        registry_password=registry_password
    )
    bootstrap_servers = os.environ('KAFKA_BOOTSTRAP_SERVERS')
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'ssl.endpoint.identification.algorithm': 'https',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': server_username,
        'sasl.password': server_password,
        "value.deserializer": AvroDeserializer(
            schema_str=None,
            schema_registry_client=schema_registry
        ),
        'group.id': consumer_group,
        "auto.offset.reset": 'latest',
        # Explicit consumer config to guarantee we don't consume duplicate messages
        # and re-consume the same message and create duplicate during processing.
        # the Kafka broker. See:
        # https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#isolation-level
        # https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#enable-auto-commit
        'enable.auto.commit': False,
        'isolation.level': 'read_committed'
    }
    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe(topics)
    return consumer


registry_username = os.environ['KAFKA_REGISTRY_USER']
registry_password = os.environ['KAFKA_REGISTRY_PASSWORD']
server_username = os.environ['KAFKA_SERVER_USER']
server_password = os.environ['KAFKA_SERVER_PASSWORD']
instruction_topic = os.environ['KAFKA_INSTRUCTION_TOPIC']
read_topics = [instruction_topic]

consumer = get_consumer(
    topics=read_topics,
    registry_username=registry_username,
    registry_password=registry_password,
    server_username=server_username,
    server_password=server_password,
    consumer_group="cii-kafka-service-2",
)

topic = f'{KAFKA_INSTRUCTION_TOPIC}'

def message_handler(message):
    message_contents = message.value()
    print('Message: %s', message_contents)
    if message.error():
        print(f"Error: {message.error()}")
    else:
        print(f"Received message: {message.value().decode('utf-8')}")
        # print(f"Received message: {message.value().decode('utf-8')}")


try:
    while True:
        message = consumer.poll(timeout=1.0)
        if message is None:
            continue
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {message.error()}")
                break
        else:
            message_handler(message)

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
