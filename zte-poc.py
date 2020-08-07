import paho.mqtt.client as mqtt
import sys,os,logging
import ssl

CAFILE = "ca.crt"
CERTFILE = "cloudserver.crt"
PRIVATEKEY = "cloudserver.key"
LOGFILE = "zte8820.log"
KEYPASSWORD = "12qwaszx"
TARGET = "" ###### device SN
TOPIC = TARGET
PAYLOAD = ""   ###### Publish empty payload
#HOST = "hn5-auth.ztehome.com.cn"
#PORT = 8883
HOST = "rot-01.ztehome.com.cn"
PORT = 8883

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        #ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=CAFILE)
        ssl_context.load_cert_chain(certfile=CERTFILE, keyfile=PRIVATEKEY)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

def onConnect(client, userdata, flags, rc):
    if(rc!=0):
        print("connect error, rc: {}".format(rc))
    else:
        client.publish(TOPIC, PAYLOAD)

def onMessage(client, userdata, message):
    topic = message.topic
    payload = message.payload
    print("topic: {}, payload: {}".format(topic, payload))
    fp.write("topic: {}\n".format(topic))
    fp.write(payload + '\n\n')
    fp.flush()


mqttClient = mqtt.Client()
fp = open(LOGFILE,'a+')
mqttClient.on_connect = onConnect
mqttClient.on_message = onMessage
ssl_context = ssl_alpn()
mqttClient.tls_set_context(context=ssl_context)
mqttClient.tls_insecure_set(True)
mqttClient.connect(HOST, PORT, 60)
mqttClient.loop_forever()
