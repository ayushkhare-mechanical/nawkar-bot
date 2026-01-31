from fyers_apiv3.FyersWebsocket import data_ws
from app.core.config import settings
import json

class DataStreamer:
    def __init__(self, access_token):
        self.access_token = access_token
        self.fyers_socket = data_ws.FyersDataSocket(
            access_token=self.access_token,
            log_path="logs",
            lmode=data_ws.HeaderMessage.LITE_MODE,
            write_to_file=False,
            on_connect=self.on_connect,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message
        )
        self.subscribed_symbols = []

    def on_connect(self):
        print("Connected to Fyers WebSocket")
        if self.subscribed_symbols:
            self.subscribe(self.subscribed_symbols)

    def on_message(self, message):
        print(f"Tick: {message}")
        # TODO: Send to Strategy Engine

    def on_error(self, message):
        print(f"Error: {message}")

    def on_close(self, message):
        print("Connection Closed")

    def connect(self):
        self.fyers_socket.connect()

    def subscribe(self, symbols: list):
        self.subscribed_symbols = symbols
        # Symbol format: "NSE:SBIN-EQ"
        self.fyers_socket.subscribe(symbols=symbols, data_type=data_ws.SymbolUpdateType.SYMBOL_UPDATE)

    def unsubscribe(self, symbols: list):
        self.fyers_socket.unsubscribe(symbols=symbols)

