from helper import KafkaHelper

def receive_result():
    data = KafkaHelper.consume_noutput()
    return data

