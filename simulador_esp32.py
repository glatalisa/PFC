# Importa a biblioteca MQTT
import paho.mqtt.client as mqtt
import json #Biblioteca para trabalhar com o formato JSON
import time #Bliblioteca para usar pausas (time.sleep)

# Configurações do broker MQTT
BROKER_ENDERECO = "localhost" # Use "localhost" se o broker Mosquitto estiver no mesmo PC
                              # ou o IP do Raspberry Pi, quando ele estiver na rede
PORTA_BROKER = 1883
TOPICO_COMANDO = "projeto/atuador/1/comando"
TOPICO_STATUS = "projeto/atuador/1/status"

# Funções de Callback

# Esta função é chamada AUTOMATICAMENTE quando o nosso simulador consegue se conectar ao broker.
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker MQTT com código de resultado: {rc}")
    # Após conectar, imediatamente assina o tópico de comando para ouvir as instruções
    client.subscribe(TOPICO_COMANDO)
    print(f"Assinando o tópico: {TOPICO_COMANDO}")

# Esta função é chamada AUTOMATICAMENTE toda vez que uma NOVA MENSAGEM chega no tópico que assinamos.
def on_message(client, userdata, msg):
    print("---------------------")
    print(f"Mensagem recebida no tópico: {msg.topic}")

    # O payload (a mensagem em si) vem em bytes, então decodificamos para texto.
    payload_texto = msg.payload.decode("utf-8")
    print(f"Payload (mensagem): {payload_texto}")

    try:
        # Tentamos interpretar o texto como JSON
        dados = json.loads(payload_texto)
        acao = dados.get("acao") # Usamos .get() para evitar erros se a chave "acao" não existir

        if acao == "avancar":
            print("SIMULADOR: Recebi comando 'avancar'. Acionando solenoide para AVANÇAR o atuador 1...")
            time.sleep(1) #Simula o tempo que a ação leva
            print("SIMULADOR: Atuador 1 avançado.")

            # Prepara a mensagem de status para enviar de volta
            status_payload = json.dumps({"status": "avancado"})
            client.publish(TOPICO_STATUS, status_payload)
            print(f"Publicado no tópico '{TOPICO_STATUS}': {status_payload}")

        elif acao == "recuar":
            print("SIMULADOR: Recebi comando 'recuar'. Acionando solenoide para RECUAR o atuador 1...")
            time.sleep(1) #Simula o tempo que a ação leva
            print("SIMULADOR: Atuador 1 recuado.")

            # Prepara a mensagem de status para enviar de volta
            status_payload = json.dumps({"status": "recuado"})
            client.publish(TOPICO_STATUS, status_payload)
            print(f"Publicado no tópico '{TOPICO_STATUS}': {status_payload}")
        
        else:
            print(f"Ação desconhecida: {acao}")
    
    except json.JSONDecodeError:
        print("Erro: A mensagem recebida não é um JSON válido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    print ("---------------------")


# Programa Principal

# 1. Cria um "cliente" MQTT. É ele quem vai fazer a comunicação.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "simulador_esp32_01")

# 2. Associa nossas funções de callback ao cliente.
client.on_connect = on_connect
client.on_message = on_message

# 3. Conecta ao broker.
print(f"Tentando conectar ao broker em {BROKER_ENDERECO}...")
client.connect(BROKER_ENDERECO, PORTA_BROKER, 60)

# 4. Inicia um loop infinito.
# Isso mantém nosso script rodando e "ouvindo" por novas mensagens.
# É um loop "não-bloqueante", ou seja, ele roda em segundo plano.
client.loop_forever()