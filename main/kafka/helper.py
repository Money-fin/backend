from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads

class KafkaHelper(object):
    @classmethod
    def _producer(cls):
        return KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

    @classmethod
    def _consumer(cls, topic):
        return KafkaConsumer(topic, bootstrap_servers=['localhost:9092'], value_deserializer=lambda x: loads(x.decode('utf8')))

    @classmethod
    def pub_ninput(cls, result):
        return cls._producer().send("ninput", result)

    @classmethod
    def pub_finput(cls, result):
        return cls._producer().send("finput", result)

    # consume functions are blockable til new record come
    @classmethod
    def consume_noutput(cls):
        record = next(iter(cls._consumer("noutput")))
        return record.value

    @classmethod
    def consume_foutput(cls):
        record = next(iter(cls._consumer("foutput")))
        return record.value