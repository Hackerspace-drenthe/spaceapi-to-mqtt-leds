import http.client
import json
import paho.mqtt.client as mqtt

def fetch_json(host, path):
    try:
        connection = http.client.HTTPSConnection(host)
        connection.request("GET", path)
        
        response = connection.getresponse()
        if response.status != 200:
            print(f"HTTP error: {response.status} {response.reason}")
            return None

        data = response.read().decode('utf-8')
        return json.loads(data)  # Parse JSON response
    except (http.client.HTTPException, json.JSONDecodeError) as e:
        print(f"Error fetching JSON: {e}")
    finally:
        connection.close()

def publish_to_mqtt(broker, topic, payload):
    client = mqtt.Client()
    try:
        client.connect(broker)
        client.loop_start()  # Starts networking loop in background

        # Convert JSON object to a JSON string
        payload_str = json.dumps(payload)
        client.publish(topic, payload_str, 0, True)

        print(f"Published to {topic} on {broker}")
    except Exception as e:
        print(f"Failed to publish to MQTT: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

# Main code
host = "api.spaceapi.io"    # Host for SpaceAPI
path = "/"                  # Path for the JSON data
api_data = fetch_json(host, path)

sample = {
    "led_index": 3, 
    "led_data": [255,0,0, 0,255,0, 0,0,255]
}

# leds = {
#     x_leeuwarden, x, groningen, x
#     coevorden, x,
#     tkkrlab, x,
#     hack42, nijmegen, wageningen,
#     amersfoort, utrecht,
#     amsterdam, leiden, denhaag, rotterdam
#     x, x, eindhoven,
#     x, venlo
#     x, heerlen,
#     7x, emmen
# }

# this is the mapping to the LEDs on the physical map. 
# First LED = 1, this used to be the hackerspace in Leeuwarden
spaces = {
    "Maakplek": 3,
    "Hackerspace Drenthe": 5,
    "TkkrLab": 7,
    "Hack42": 9,
    "Hackerspace Nijmegen": 10,
    "NURDspace": 11,
    "Bitlair": 12,
    "RandomData": 13,
    "LAG": 14,
    "The Space Leiden": 15,
    "RevSpace": 16,
    "PixelBar": 17,
    "Hackalot": 20,
    "TDvenlo": 22,
    "ACKspace": 24,
    "Hackerspace Drenthe (Emmmen)": 32
}

leds = [0 for _ in range(32*3)]


for space in api_data:
    #print("  ")
    #print(space)
    if not space["valid"]:
        continue
    if space["data"]["space"] in spaces:
        key = space["data"]["space"]
        led = spaces[key]
        color = [0, 0, 0]
        if "open" in space["data"]["state"]:
            if space["data"]["state"]["open"]:
                color = [0, 255, 0]
                leds[(led-1)*3] = 255
            else:
                color = [255, 0, 0]
                leds[(led-1)*3+1] = 255

        print(space["data"]["space"], " ", led, color)

json_data = {
    "led_data": leds
}



print("Publishing LED colours:", json_data)

if json_data:
    mqtt_broker = "mqtt.hackerspace-drenthe.nl"
    mqtt_topic = "emmen/kaart"
    publish_to_mqtt(mqtt_broker, mqtt_topic, json_data)
