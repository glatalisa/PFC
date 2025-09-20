# Importa a biblioteca Flask e a blibioteca MQTT
from flask import Flask
import paho.mqtt.client as mqtt
import json

# Configurações
BROKER_ENDERECO = "localhost" # O mesmo broker usado pelo simulador
PORTA_BROKER = 1883
TOPICO_COMANDO = "projeto/atuador/1/comando"
TOPICO_STATUS = "projeto/atuador/1/status"

# --- Funções de Callback de LOG ---

# NOVO: Esta função roda quando o cliente se CONECTA ao broker
def on_connect_servidor(client, userdata, flags, rc):
    if rc == 0:
        print("LOG DE DEBUG: Conexão com o Broker MQTT bem-sucedida!")
        # A inscrição (subscribe) é movida para cá. É mais garantido.
        print("LOG DE DEBUG: Tentando se inscrever no tópico de status...")
        client.subscribe(TOPICO_STATUS)
    else:
        print(f"LOG DE DEBUG: Falha ao conectar, código de erro: {rc}")

# NOVO: Esta função roda quando a INSCRIÇÃO (subscribe) é bem-sucedida
def on_subscribe_servidor(client, userdata, mid, granted_qos):
    print("LOG DE DEBUG: Inscrição no tópico de status bem-sucedida!")

# Função de Callback para o Servidor
# Esta função será chamada quando uma mensagem de STATUS chegar
def on_message_servidor(client, userdata, msg):
    status_recebido = msg.payload.decode("utf-8")
    print(f"<<< Mensagem de STATUS recebida no tópico '{msg.topic}':{status_recebido}")

# Configuração do Cliente MQTT
# Criamos o cliente MQTT fora das rotas da web.
# Isso é importante para que ele não seja criado toda vez que uma página é acessada.
print("Configurando o cliente MQTT...")
client_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "servidor_pi_01")
client_mqtt.on_message = on_message_servidor
client_mqtt.connect(BROKER_ENDERECO, PORTA_BROKER, 60)
client_mqtt.subscribe(TOPICO_STATUS)
print(f"   - Assinando o tópico: {TOPICO_STATUS}")
client_mqtt.loop_start() # Inicia uma thread para manter a conexão MQTT em segundo plano

# Configuração do Servidor Web Flask
app = Flask(__name__)

# Esta função será executada quando alguém acessar http://127.0.0.1:5000/ no navegador.
@app.route("/")
def index():
    return "<h1>Servidor de Controle de Atuadores</h1><p>Use os endpoints para controlar os atuadores.</p>"

# Esta função será executada quando acessarmos http://127.0.0.1:5000/atuador/1/avancar
@app.route("/atuador/1/avancar")
def avancar_atuador1():
    print(">>> Endpoint /atuador/1/avancar foi chamado!")

    # Prepara o payload (a mensagem) em formato JSON
    payload = json.dumps({"acao": "avancar"})

    # Publica a mensagem no tópico de comando
    client_mqtt.publish(TOPICO_COMANDO, payload)

    print(f"  - Publicado no tópico '{TOPICO_COMANDO}': {payload}")
    return "Comando 'avançar' enviado para o atuador 1!"

# Esta função será executada quando acessarmos http: //127.0.0.1:5000/atuador/1/recuar
@app.route("/atuador/1/recuar")
def recuar_atuador1():
    print(">>> Endpoint /atuador/1/recuar foi chamado!")

    payload = json.dumps({"acao": "recuar"})

    client_mqtt.publish(TOPICO_COMANDO, payload)

    print(f"  - Publicado no tópico '{TOPICO_COMANDO}': {payload}")
    return "Comando 'recuar' enviado para o atuador 1!"

# Roda o servidor
if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    # O host='0.0.0.0' permite que o servidor seja acessado de outros dispositivos na mesma rede.
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)