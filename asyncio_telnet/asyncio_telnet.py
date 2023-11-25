import asyncio
import re
import socket


# Tunable parameters
DEBUGLEVEL = 0

# Telnet protocol defaults
TELNET_PORT = 23

# Telnet protocol characters (don't change)
IAC  = bytes([255]) # "Interpret As Command"
DONT = bytes([254])
DO   = bytes([253])
WONT = bytes([252])
WILL = bytes([251])
theNULL = bytes([0])
ECHO = bytes([1])


class AsyncTelnet:
    def __init__(self, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.debuglevel = 0
        self.timeout = timeout
        self.fast_read_timeout = 0.1
        self.reader = None
        self.writer = None

    async def open(self, host, port=0):
        self.eof = 0
        if not port:
            port = TELNET_PORT
        self.port = port
        self.host = host

        try:
            self.reader, self.writer = await asyncio.open_connection(host, port)

        except asyncio.CancelledError:
            raise

        except Exception as e:
            print(f"Error connecting to {host}:{port}: {e}")
            raise
    
    async def write(self, buffer):
        buffer = buffer.replace(b'\xff', b'\xff\xff')
        self.writer.write(buffer)
        await self.writer.drain()

    async def read(self, num_bytes=1):
        data = await self.reader.read(num_bytes)
        return data
    
    async def read_until_eof(self, fast_mode=True):
        """
        Performs reading data until the end of the file (EOF).
        Typically used in the context of file
        or stream handling to read and extract data from a 
        source until the end of the file is reached.
        """
        timeout = self.fast_read_timeout if fast_mode else self.timeout
        response = b''
        while True:
            try:
                data = await asyncio.wait_for(self.read(100), timeout=timeout)
                if not data:
                    break
                if data.startswith(IAC):
                    data = await self.filter_telnet_data(data)
                response += data
            except asyncio.TimeoutError:
                break
        print('response', response)
        return response

    async def __aenter__(self):
        """
        Is part of an asynchronous context manager.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Is part of an asynchronous context manager.
        """
        if self.writer:
            await self.writer.drain()
            self.writer.close()
            await self.writer.wait_closed()
            print("Connection closed")

    async def filter_telnet_data(self, data):
        """
        Removes TELNET control characters from the data.
        """
        filtered_data = b''
        i = 0
        while i < len(data):
            if data[i:i+1] == IAC:
                # If IAC is encountered, process the TELNET command
                command = data[i:i+3]
                i += 3
                if command[1:2] in (WILL, WONT, DO, DONT, IAC):
                    # It's a command WONT, WILL, DO, DONT, or IAC, remove it
                    continue
                elif command[1:2] == b'\xfa':
                    # It's the beginning of option support, skip everything until IAC SE
                    iac_se_pos = data.find(b'\xff\xf0', i)
                    if iac_se_pos != -1:
                        i = iac_se_pos + 2
                    else:
                        # If IAC SE is not found, stop processing data
                        break
            else:
                # Otherwise, add the current byte to the filtered data
                filtered_data += data[i:i+1]
                i += 1
        return filtered_data


class AsyncToSyncWrapper:
    def __init__(self, async_class_instance):
        self.async_class_instance = async_class_instance

    def __getattr__(self, name):
        if hasattr(self.async_class_instance, name):
            attr = getattr(self.async_class_instance, name)
            if asyncio.iscoroutinefunction(attr):
                return lambda *args, **kwargs: self._sync_method(attr, *args, **kwargs)
            else:
                return attr
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _sync_method(self, async_method, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(async_method(*args, **kwargs))


class Telnet:
    def __init__(self, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, sync_mode=False):
        if sync_mode:
            self._instance = AsyncToSyncWrapper(AsyncTelnet(timeout))
        else:
            self._instance = AsyncTelnet(timeout)

    def __getattr__(self, name):
        return getattr(self._instance, name)
