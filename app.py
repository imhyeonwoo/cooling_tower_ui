# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# MQTT Settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [
    ("tower/ct/status", 0),
    ("tower/pump/status", 0),
    ("tower/system/status", 0),
    ("tower/log", 0)
]

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"MQTT Connected with result code {rc}")
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = json.loads(msg.payload.decode())
    except:
        payload = msg.payload.decode()
    
    print(f"Received: {topic} -> {payload}")
    
    # Send to web clients via Socket.IO
    socketio.emit('mqtt_message', {
        'topic': topic,
        'data': payload
    })

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Web client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Web client disconnected')

if __name__ == '__main__':
    # Connect to MQTT Broker
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print(f"MQTT connecting to {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"MQTT connection failed: {e}")
    
    # Run Flask with Socket.IO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
