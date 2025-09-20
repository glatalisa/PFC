# teste_ouvinte.py
import paho.mqtt.client as mqtt
import time

BROKER_ENDERECO = "localhost"
PORTA_BROKER = 1883
TOPICO_STATUS = "projeto/atuador/1/status"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[Ouvinte] CONECTADO ao broker com sucesso!")
        client.subscribe(TOPICO_STATUS)
    else:
        print(f"[Ouvinte] FALHA na conexão, código: {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[Ouvinte] INSCRITO no tópico: {TOPICO_STATUS}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print("--------------------------------------------------")
    print(f"[Ouvinte] MENSAGEM RECEBIDA: {payload}")
    print("--------------------------------------------------")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "ouvinte_teste_01")
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

print("[Ouvinte] Tentando conectar...")
client.connect(BROKER_ENDERECO, PORTA_BROKER, 60)

# Usa o loop bloqueante aqui, já que este script não faz mais nada.
client.loop_forever()