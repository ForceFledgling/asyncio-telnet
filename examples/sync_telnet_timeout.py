"""
Example: Synchronous Telnet Connection with Timeout

This example demonstrates a synchronous Telnet connection to 'example.com' using the asyncio_telnet library.
By specifying sync_mode=True and timeout=5, a wrapper for calling asynchronous methods synchronously is activated.
The script opens a connection, reads the response, and closes the connection.

Usage:
- Install the asyncio_telnet library: pip install asyncio-telnet
- Run the script.

Note: Make sure to replace 'example.com' with the actual hostname or IP address.
"""

from asyncio_telnet import Telnet

def main():
    tn = Telnet(sync_mode=True, timeout=5)
    try:
        tn.open('example.com')
        response = tn.read_until_eof()
        tn.close()
        return response
    except ValueError as e:
        print(f"Example of a timeout occurrence: {e}")
        

if __name__ == '__main__':
    result = main()
    print(result)


# Example response:
# Example of a timeout occurrence: Timeout connecting to example.com:23
