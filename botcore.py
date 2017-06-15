import os
import zmq
import sys
import json
import pymisp
import warnings
from pyaml import yaml
from cabby import create_client
import logging
from pathlib import Path

# Set up logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

here = Path(os.path.dirname(__file__))
configFile = here / "config.yaml"

# Load config
with configFile.open("r") as f:
    config = yaml.load(f.read())

# Set up our ZMQ socket to recieve MISP JSON on publish
context = zmq.Context()
socket = context.socket(zmq.SUB)

log.info("Subscribing to tcp://{}:{}".format(
                                    config["zmq"]["host"],
                                    config["zmq"]["port"]
                                    ))

# Connect to the socket
socket.connect("tcp://{}:{}".format(
                                    config["zmq"]["host"],
                                    config["zmq"]["port"]
                                    ))
# Set the option to subscribe
socket.setsockopt_string(zmq.SUBSCRIBE, '')


while True:
    # Wait for something to come in on the ZMQ socket
    message = socket.recv().decode("utf-8")
    log.info("Recieved a message!")
    topic = message.split(' ', 1)[0]

    if topic != 'misp_json_conversation':
      log.info("Ignoring " + topic + "...")
      continue

    # Process the JSON payload
    log.debug("Processing...")
    payload = message[len(topic)+1:]

    # Load the message JSON
    msg = json.loads(payload)

    log.debug(msg)

