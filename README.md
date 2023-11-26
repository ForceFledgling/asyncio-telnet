# **Python Telnet Utility: asyncio-powered**

The **asyncio-telnet** library designed for convenient interaction with Telnet devices in both synchronous and asynchronous modes, making the process straightforward and flexible in various usage scenarios.

[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg)](docs) [![License: Apache License 2.0](https://img.shields.io/badge/License-Apache2-brightgreen.svg)](https://choosealicense.com/licenses/apache-2.0/) [![PyPi Version](https://img.shields.io/pypi/v/asyncio-telnet.svg?style=flat-square&logo=asyncio-telnet&logoColor=white)](https://pypi.org/project/asyncio-telnet/) [![PyPi downloads](https://static.pepy.tech/personalized-badge/asyncio-telnet?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/asyncio-telnet/)

- **Support for Asynchrony and Synchrony**: Harness the power of asyncio for efficient and non-blocking communication with Telnet servers. With this library, you have the option to choose between asynchronous and synchronous modes, depending on the requirements of your project.
- **Ease of Use**: The library provides a user-friendly interface for both synchronous and asynchronous cases, making it adaptable to different project needs.
- **Telnet Protocol Handling**: Transparently handles the intricacies of the Telnet protocol, allowing you to focus on the logic of your application.
- **Flexible Integration**: Easily integrate Telnet functionality into your Python applications with a simple API.

# Installation

You can install the library using pip. Make sure you have Python 3.6 or later installed.

`pip install asyncio-telnet`

# Usage

Example: Asynchronous Telnet Connection with Default Timeout

```python
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
# b'\n***************** User Access Login ********************\r\n\r\nUser:'
```

Example: Synchronous Telnet Connection

```python
from asyncio_telnet import Telnet

def main():
    tn = Telnet(sync_mode=True)
    tn.open('example.com')
    response = tn.read_until_eof()
    tn.close()
    return response

if __name__ == '__main__':
    result = main()
    print(result)


# Example of successful execution:
# b'\n***************** User Access Login ********************\r\n\r\nUser:'
```

Example: Asynchronous Telnet Connection with Custom Timeout.

By default, the timeout is set to 30 seconds.

```python
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
```

Example: Asynchronous Telnet Connection with Write Operation

```python
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
```

Feel free to check the [documentation](docs) and [examples](examples) for more detailed information.
