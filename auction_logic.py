from datetime import datetime
from bson.objectid import ObjectId

def create_auction(item_name, start_price, image_path, mongo):
    auction = {
        "item_name": item_name,
        "start_price": float(start_price),
        "highest_bid": float(start_price),
        "highest_bidder": None,
        "status": "ongoing",
        "image_url": image_path,
        "bid_history": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = mongo.db.auctions.insert_one(auction)
    return str(result.inserted_id)

def place_bid(auction_id, bid_amount, user, mongo, redis_client, producer):
    auction = mongo.db.auctions.find_one({"_id": ObjectId(auction_id)})
    if auction and float(bid_amount) > auction['highest_bid']:
        mongo.db.auctions.update_one(
            {"_id": ObjectId(auction_id)},
            {"$set": {
                "highest_bid": float(bid_amount),
                "highest_bidder": user,
                "updated_at": datetime.utcnow()},
            "$push": {
                "bid_history": {
                    "user": user,
                    "amount": float(bid_amount),
                    "time": datetime.utcnow()}
            }}
        )
        # Publish bid to Kafka
        producer.send('auction_bids', {'auction_id': auction_id, 'bid': bid_amount, 'user': user})
        return True
    return False

def end_auction(auction_id, mongo, producer):
    auction = mongo.db.auctions.find_one({"_id": ObjectId(auction_id)})
    if auction and auction['status'] == 'ongoing':
        mongo.db.auctions.update_one(
            {"_id": ObjectId(auction_id)},
            {"$set": {"status": "completed", "updated_at": datetime.utcnow()}}
        )
        # Notify completion via Kafka
        producer.send('auction_completed', {'auction_id': auction_id})
        return True
    return False

def get_auction(auction_id, mongo):
    return mongo.db.auctions.find_one({"_id": ObjectId(auction_id)})
