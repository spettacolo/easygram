import os
import time
from stem.control import Controller
from stem.process import launch_tor_with_config

class TorClient:
    def __init__(self, socks_port=9050, control_port=9051):
        self.socks_port = socks_port
        self.control_port = control_port
        self.tor_process = None
        self.controller = None

    async def start(self):
        """Start the Tor process and initialize the controller"""
        if self.tor_process is None:
            config = {
                'SocksPort': str(self.socks_port),
                'ControlPort': str(self.control_port),
                'DataDirectory': os.path.join(os.getcwd(), 'tor_data')
            }
            
            self.tor_process = launch_tor_with_config(
                config=config,
                take_ownership=True
            )
            
            # Initialize the controller
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()

    async def stop(self):
        """Stop the Tor process and close the controller"""
        if self.controller:
            self.controller.close()
            self.controller = None
        
        if self.tor_process:
            self.tor_process.terminate()
            self.tor_process = None

    async def renew_connection(self):
        """Request a new Tor circuit"""
        if self.controller:
            self.controller.signal("NEWNYM")
            # Wait for the new circuit to be established
            time.sleep(5)

    async def get_socks_proxy(self):
        """Return the SOCKS proxy configuration"""
        return f'socks5h://127.0.0.1:{self.socks_port}'

    async def __enter__(self):
        await self.start()
        return self

    async def __exit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
