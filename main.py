from modules.easygram import Easygram
from modules.tor import TorClient as Tor
from dotenv import load_dotenv
import os, asyncio

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

async def main():
    # Initialize components
    tor = Tor(socks_port=9050, control_port=9051)
    proxy = dict(scheme="socks5", hostname="127.0.0.1", port=9050)
    
    if api_id is None:
        raise ValueError("API_ID environment variable is not set")
    if api_hash is None:
        raise ValueError("API_HASH environment variable is not set")
        
    client = Easygram(api_id=int(api_id), api_hash=api_hash, proxy=proxy, workdir="sessions")
    
    try:
        # Start services
        await tor.start()
        print("Tor started")

        await client.set_handlers()
        await client.start()
        print("Client started")
        
        # Send a test message
        await client.send_message("me", None, "Hello, World!")
        
        # Use pyrogram's idle function directly
        from pyrogram import idle
        await idle()
    except KeyboardInterrupt:
        pass
    finally:
        # Ensure proper cleanup
        if hasattr(client, 'client') and client.client.is_connected:
            await client.stop()
        await tor.stop()

if __name__ == "__main__":
    print("Starting...")
    asyncio.run(main())
