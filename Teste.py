import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect("localhost", 1883, 60)  # conecta ao broker (mosquitto)

# mensagem JSON
payload = json.dumps({"command": "ON"})
client.publish("/bancada/atuador1/cmd", payload)

client.disconnect()
