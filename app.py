from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import redis
from kafka import KafkaProducer
import os
import json
from auction_logic import create_auction, place_bid, end_auction, get_auction

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/auctionDB"
mongo = PyMongo(app)

# Redis Setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Kafka Producer Setup
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# File upload configuration
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page displaying ongoing and completed auctions
@app.route('/')
def home():
    ongoing_auctions = list(mongo.db.auctions.find({"status": "ongoing"}))
    completed_auctions = list(mongo.db.auctions.find({"status": "completed"}))
    return render_template('home.html', auctions=ongoing_auctions, completed_auctions=completed_auctions)

# Start a new auction
@app.route('/start_auction', methods=['GET', 'POST'])
def start_auction():
    if request.method == 'POST':
        data = request.form
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        auction_id = create_auction(data['item_name'], data['start_price'], image_path, mongo)
        return redirect(url_for('auction_page', auction_id=auction_id))
    return render_template('new_auction.html')

# Auction page for bidding
@app.route('/auction/<auction_id>')
def auction_page(auction_id):
    auction = get_auction(auction_id, mongo)
    return render_template('auction.html', auction=auction)

# Place a bid
@app.route('/place_bid', methods=['POST'])
def place_bid_route():
    data = request.form
    bid_amount = data['bid_amount']
    user = data['user']
    auction_id = data['auction_id']

    # Place the bid using auction logic
    bid_success = place_bid(auction_id, bid_amount, user, mongo, redis_client, producer)
    if bid_success:
        auction = get_auction(auction_id,mongo)
        return render_template('auction.html', auction=auction)
        # return jsonify({"status": "success", "new_bid": bid_amount})
    else:
        return jsonify({"status": "failure"}), 400

# End the auction manually
@app.route('/end_auction/<auction_id>', methods=['POST'])
def end_auction_route(auction_id):
    end_auction(auction_id, mongo, producer)
    return redirect(url_for('auction_results', auction_id=auction_id))

# Show the auction results
@app.route('/auction_results/<auction_id>')
def auction_results(auction_id):
    auction = get_auction(auction_id, mongo)
    return render_template('results.html', auction=auction)

# End auction route
@app.route('/end_auction', methods=['GET'])
def end_auction_view():
    ongoing_auctions = list(mongo.db.auctions.find({"status": "ongoing"}))
    return render_template('end_auction.html', ongoing_auctions=ongoing_auctions)

if __name__ == '__main__':
    app.run(debug=True)
