# -*- coding: utf-8 -*-
"""
MQTT Test Publisher
- MQTT 브로커에 테스트 데이터를 발행합니다.
- Flask 서버가 데이터를 잘 받는지 테스트용
"""
import paho.mqtt.client as mqtt
import json
import time
import random

MQTT_BROKER = "localhost"
MQTT_PORT = 1883

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("MQTT Test Publisher Started")
print("Press Ctrl+C to stop")

try:
    while True:
        # CT Status (random for testing)
        ct_status = {
            "ct": [random.choice([True, False]) for _ in range(10)],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        client.publish("tower/ct/status", json.dumps(ct_status))
        print(f"Published CT: {ct_status['ct']}")
        
        # Pump Status
        pump_status = {
            "pump_a": {"value": random.randint(30, 60), "status": "ok"},
            "pump_b": {"value": random.randint(30, 60), "status": "ok"},
            "pump_c": {"value": random.randint(30, 180), "status": "ok" if random.random() > 0.2 else "error"}
        }
        client.publish("tower/pump/status", json.dumps(pump_status))
        print(f"Published Pump: A={pump_status['pump_a']['value']}, B={pump_status['pump_b']['value']}, C={pump_status['pump_c']['value']}")
        
        # System Status
        system_status = {
            "mode": random.choice(["일간모드", "분할모드", "센서모드"]),
            "comm": "연결됨",
            "reset": random.randint(0, 10)
        }
        client.publish("tower/system/status", json.dumps(system_status))
        
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\nStopped")
    client.disconnect()
