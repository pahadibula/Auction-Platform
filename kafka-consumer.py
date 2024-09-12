from kafka import KafkaConsumer
import json

# Setup Kafka consumer
consumer = KafkaConsumer(
    'auction_bids',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    bid_data = message.value
    try:
        auction_id = bid_data['auction_id']
        bid_amount = bid_data['bid']  # Change 'bid_amount' to 'bid'
        user = bid_data['user']
        # Process the bid data
        print(f"Auction ID: {auction_id}, Bid Amount: {bid_amount}, User: {user}")
    except KeyError as e:
        print(f"Missing key: {e}")
