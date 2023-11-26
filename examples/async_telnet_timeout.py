"""
Example: Asynchronous Telnet Connection with Custom Timeout

This example demonstrates an asynchronous Telnet connection to 'example.com' using the asyncio_telnet library.
The connection has a custom timeout of 5 seconds.

Usage:
- Install the asyncio_telnet library: pip install asyncio-telnet
- Run the script.

Note: Make sure to replace 'example.com' with the actual hostname or IP address.
"""

import asyncio
from asyncio_telnet import Telnet

async def main():
    tn = Telnet(timeout=5)
    try:
        await tn.open('example.com')
        response = await tn.read_until_eof()
        await tn.close()
        return response
    except ValueError as e:
        print(f"Example of a timeout occurrence: {e}")

if __name__ == '__main__':
    asyncio.run(main())


# Example response:
# Example of a timeout occurrence: Timeout connecting to example.com:23
