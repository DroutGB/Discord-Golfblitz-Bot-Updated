#!/usr/bin/env python3
import asyncio
import websockets
import json
import hmac
import hashlib
import base64
import requests

game_entryURL = "wss://live-f351468gBSWz.ws.gamesparks.net/ws/device/f351468gBSWz"

async def test():
    try:
        ws1 = await websockets.connect(game_entryURL, compression=None)
        print("Connected to ws1")
    except Exception as e:
        print(f"Failed to connect to ws1: {e}")
        return

    try:
        info = await ws1.recv()
        print("Received info from ws1")
        connect_url = json.loads(info)["connectUrl"]
        print(f"Connect URL: {connect_url}")
    except Exception as e:
        print(f"Failed to receive or parse info from ws1: {e}")
        return

    try:
        ws2 = await websockets.connect(connect_url, compression=None)
        print("Connected to ws2")
    except Exception as e:
        print(f"Failed to connect to ws2: {e}")
        return

    try:
        info2 = await ws2.recv()
        print("Received info from ws2")
        nonce = json.loads(info2)["nonce"]
        print(f"Nonce: {nonce}")
    except Exception as e:
        print(f"Failed to receive or parse info from ws2: {e}")
        return

    try:
        hmac_key = b'a3insvuyMEertN6BV14ys1K05qcfaaoN'
        hmac_digest = base64.b64encode(hmac.new(hmac_key, nonce.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        outobj = {
            "@class": ".AuthenticatedConnectRequest",
            "hmac": hmac_digest,
            "os": "uh"
        }
        await ws2.send(json.dumps(outobj))
        print(f"Sent AuthenticatedConnectRequest: {outobj}")
    except Exception as e:
        print(f"Failed to send AuthenticatedConnectRequest: {e}")
        return

    try:
        await ws2.recv()
        print("Received response to AuthenticatedConnectRequest")
    except Exception as e:
        print(f"Failed to receive response to AuthenticatedConnectRequest: {e}")
        return

    try:
        auth_request = {
            "@class": ".AuthenticationRequest",
            "userName": "put in your username",
            "password": "put in your password",
            "scriptData": {"game_version": 9999, "client_version": 99999},
            "requestId": "ok"
        }
        await ws2.send(json.dumps(auth_request))
        print("Sent AuthenticationRequest")
    except Exception as e:
        print(f"Failed to send AuthenticationRequest: {e}")
        return

    try:
        print("Logged in")
        for i in range(4):
            await ws2.recv()
            print(f"Received message {i+1}")
    except Exception as e:
        print(f"Failed to receive messages: {e}")
        return

    try:
        log_event_request = {
            "@class": ".LogEventRequest",
            "eventKey": "REFRESH_CHALLENGE_MODE",
            "requestId": ""
        }
        await ws2.send(json.dumps(log_event_request))
        print("Sent LogEventRequest")
    except Exception as e:
        print(f"Failed to send LogEventRequest: {e}")
        return

    try:
        async for message in ws2:
            print(message)
    except Exception as e:
        print(f"Failed during message reception: {e}")

asyncio.run(test())
