"""
Easyserver.

An easy high level way to create a client/server application.
"""

__version__ = "0.1.0"
__author__ = 'Alexander Groth'
__credits__ = 'Alexander Groth'


from EasyServer.server.easyserver import EasyServer
from EasyServer.client.easyclient import EasyClient
from EasyServer.networking.network_message import NetworkMessage