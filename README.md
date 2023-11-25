# **Python Telnet Utility: asyncio-powered**

The \`\*\*asyncio-telnet\*\*\` library designed for convenient interaction with Telnet devices in both synchronous and asynchronous modes, making the process straightforward and flexible in various usage scenarios.

- **Support for Asynchrony and Synchrony**: Harness the power of asyncio for efficient and non-blocking communication with Telnet servers. With this library, you have the option to choose between asynchronous and synchronous modes, depending on the requirements of your project.
- **Ease of Use**: The library provides a user-friendly interface for both synchronous and asynchronous cases, making it adaptable to different project needs.
- **Telnet Protocol Handling**: Transparently handles the intricacies of the Telnet protocol, allowing you to focus on the logic of your application.
- **Flexible Integration**: Easily integrate Telnet functionality into your Python applications with a simple API.

# Installation

You can install the library using pip. Make sure you have Python 3.6 or later installed.

`pip install asyncio-telnet`

# Usage

Here is a simple example of using in an asynchronous context:

```python
import asyncio
from asyncio_telnet import Telnet

async def main():
    tn = Telnet()
    await tn.open('example.com')
    response = await tn.read_until_eof()
    return response

if __name__ == '__main__':
    result = asyncio.run(main())
    print(result)
```

For synchronous usage, you can use the library in a similar way by simply specifying sync_mode=True:

```python
from asyncio_telnet import Telnet

def main():
    # by specifying sync_mode=True, a wrapper for calling asynchronous methods synchronously is activated internally.
    tn = Telnet(sync_mode=True)
    # now it is possible to directly invoke asynchronous methods through the wrapper
    tn.open('example.com')
    response = tn.read_until_eof()
    return response

if __name__ == '__main__':
    result = main()
    print(result)
```

Feel free to check the documentation for more detailed information and examples.
