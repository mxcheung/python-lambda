from confluent_kafka import Consumer, KafkaException, KafkaError

def message_handler(message):
    if message.error():
        print(f"Error: {message.error()}")
    else:
        print(f"Received message: {message.value().decode('utf-8')}")

conf = {
    'bootstrap.servers': '<bootstrap.servers>',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '<username>',
    'sasl.password': '<password>',
    'group.id': '<group.id>',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
topic = '<topic>'
consumer.subscribe([topic])

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



Error: KafkaError{code=GROUP_AUTHORIZATION_FAILED,val=30,str="FindCoordinator response error: Group authorization failed."}
