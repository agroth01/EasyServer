"""
Easyserver.

An easy high level way to create a client/server application.
"""

__version__ = "0.1.0"
__author__ = 'Alexander Groth'
__credits__ = 'Alexander Groth'


from easyserver.server.easyserver import EasyServer
from easyserver.client.easyclient import EasyClient
from easyserver.networking.network_message import NetworkMessage