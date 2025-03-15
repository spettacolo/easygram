from modules.easygram import Easygram
from modules.tor import TorClient as Tor
from dotenv import load_dotenv
import os, asyncio

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

async def setup(tor: Tor, client: Easygram):
    await tor.start()
    await client.start()

if __name__ == "__main__":
    tor = Tor(socks_port=9050, control_port=9051)
    proxy = dict(scheme="socks5", hostname="127.0.0.1", port=9050)
    client = None

    if api_id is not None:
        if api_hash is None:
            raise ValueError("API_HASH environment variable is not set")
        client = Easygram(api_id=int(api_id), api_hash=api_hash, proxy=proxy, workdir="sessions")
    else:
        raise ValueError("API_ID environment variable is not set")

    asyncio.run(setup(tor, client))
