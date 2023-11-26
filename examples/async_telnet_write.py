"""
Example: Asynchronous Telnet Connection with Write Operation

This example demonstrates an asynchronous Telnet connection to 'example.com' using the asyncio_telnet library.
The script opens a connection, writes 'Vladimir\r\n' to the Telnet server, and then reads the response.

Usage:
- Install the asyncio_telnet library: pip install asyncio-telnet
- Run the script.

Note: Make sure to replace 'example.com' with the actual hostname or IP address.
"""

import asyncio
from asyncio_telnet import Telnet

async def main():
    tn = Telnet()
    await tn.open('example.com')
    await tn.write(b'Vladimir\r\n')
    response = await tn.read_until_eof()
    await tn.close()
    return response

if __name__ == '__main__':
    result = asyncio.run(main())
    print(result)


# Example of successful execution:
# b'\n***************** User Access Login ********************\r\n\r\nUser:Vladimir\r\nPassword:'
