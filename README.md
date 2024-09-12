# Real-Time Auction Platform

## Overview
This project is a real-time auction platform built with Flask, allowing users to place bids and track auction progress seamlessly. It integrates modern technologies to deliver an efficient and responsive user experience.

## Key Features

- **Real-Time Bidding**: Users can place bids and follow auction progress live.
- **Real-Time Messaging**: Integrated with [Apache Kafka](https://kafka.apache.org) for instant notifications of bids and auction results.
- **Performance Optimization**: Utilizes [Redis](https://redis.io) caching to reduce load times and improve bid retrieval efficiency.
- **Responsive Design**: Implemented with [Bootstrap](https://getbootstrap.com) for a smooth user experience across various devices.

## Technologies Used

- **Backend**: 
  - [Flask](https://flask.palletsprojects.com) for the web framework
  - Apache Kafka for real-time messaging
  - Redis for caching
- **Frontend**: 
  - Bootstrap for responsive design

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/auction-platform.git
2. **Create a Virtual Environment**:
   ```cd auction-platform
   python -m venv venv
3. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
5. **Configure Kafka and Redis**: Ensure Kafka and Redis are running. Update the configuration files with your Kafka and Redis setup. You might need to set environment variables or update a configuration file for this purpose.
6. **Run the Application**:
   ```bash
   flask run
7. **Access the Platform**: Open your web browser and go to http://localhost:5000 to access the auction platform.

