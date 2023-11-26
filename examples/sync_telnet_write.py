"""
Example: Synchronous Telnet Connection with Write Operation

This example demonstrates a synchronous Telnet connection to 'example.com' using the asyncio_telnet library.
By specifying sync_mode=True, a wrapper for calling asynchronous methods synchronously is activated internally.

Usage:
- Install the asyncio_telnet library: pip install asyncio-telnet
- Run the script.

Note: Make sure to replace 'example.com' with the actual IP address.
"""

from asyncio_telnet import Telnet

def main():
    tn = Telnet(sync_mode=True)
    tn.open('example.com')
    tn.write(b'Vladimir\r\n')
    response = tn.read_until_eof()
    tn.close()
    return response

if __name__ == '__main__':
    result = main()
    print(result)

# Example of successful execution:
# b'\n***************** User Access Login ********************\r\n\r\nUser:Vladimir\r\nPassword:'
