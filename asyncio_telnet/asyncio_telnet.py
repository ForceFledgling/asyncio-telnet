import asyncio
import re
import socket


# Tunable parameters
DEBUGLEVEL = 0

# Telnet protocol defaults
TELNET_PORT = 23
GLOBAL_DEFAULT_TIMEOUT = 30

# Telnet protocol characters (don't change)
theNULL = bytes([0])    # Null (No operation)
ECHO = bytes([1])       # Echo
SB =  bytes([250])      # Subnegotiation Begin
WILL = bytes([251])     # Will
WONT = bytes([252])     # Will Not
DO   = bytes([253])     # Do
DONT = bytes([254])     # Do Not
IAC  = bytes([255])     # Interpret As Command
SE  = bytes([240])      # Subnegotiation End


class AsyncTelnet:

    def __init__(self, timeout=GLOBAL_DEFAULT_TIMEOUT):
        """
        Initializes the Telnet connection with optional timeout settings.

        Args:
            timeout: Timeout value for the Telnet connection.
        """
        self.debuglevel = 0
        self.timeout = timeout
        self.read_timeout = timeout
        self.fast_read_timeout = 2
        self.reader = None
        self.writer = None

    async def open(self, host, port=0):
        """
        Opens a connection to the specified host and port.

        Args:
            host: The host to connect to.
            port: The port to connect to (default is 0, which uses the default TELNET_PORT).
        """
        self.eof = 0
        if not port:
            port = TELNET_PORT
        self.port = port
        self.host = host

        try:
            connect_coroutine = asyncio.open_connection(host, port)
            self.reader, self.writer = await asyncio.wait_for(connect_coroutine, timeout=self.timeout)
        except asyncio.CancelledError:
            raise ValueError(f"Connection canceled for {host}:{port}")
        except Exception as e:
            raise ValueError(f"Timeout connecting to {host}:{port}")
    
    async def write(self, buffer):
        """
        Writes data to the Telnet connection.

        Args:
            buffer: The data to be written.
        """
        buffer = buffer.replace(IAC, IAC + IAC)
        self.writer.write(buffer)
        await self.writer.drain()

    async def read(self, num_bytes=1):
        """
        Reads data from the Telnet connection.

        Args:
            num_bytes: The number of bytes to read.

        Returns:
            The read data.
        """
        data = await self.reader.read(num_bytes)
        return data
    
    async def read_until_eof(self, fast_mode=True):
        """
        Reads data from the Telnet connection until the end of the stream.

        Args:
            fast_mode: If True, uses a fast read timeout; otherwise, uses the standard timeout.

        Returns:
            The read data until the end of the stream.
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
        return response

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
                elif command[1:2] == SB:
                    # It's the beginning of option support, skip everything until IAC SE
                    iac_se_pos = data.find(IAC + SE, i)
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
    
    async def close(self):
        """
        Closes the writer associated with the current instance.

        If a writer is present, this method first ensures any pending data is
        flushed using `await self.writer.drain()`. It then closes the writer
        using `self.writer.close()` and waits until the writer is fully closed
        with `await self.writer.wait_closed()`.

        Note: It is essential to call this method to gracefully close the writer
        and release associated resources.
        """
        if self.writer:
            await self.writer.drain()
            self.writer.close()
            await self.writer.wait_closed()


class AsyncToSyncWrapper:
    """
    Wraps an asynchronous class instance, allowing synchronous access to its methods.
    """
    def __init__(self, async_class_instance, loop=None):
        self.async_class_instance = async_class_instance
        self.loop = loop or asyncio.get_event_loop()

    def __getattr__(self, name):
        """
        Retrieves attributes from the asynchronous class instance and converts asynchronous methods to synchronous.

        Args:
            name: The name of the attribute.

        Returns:
            The attribute or a synchronous wrapper for an asynchronous method.
        """
        if hasattr(self.async_class_instance, name):
            attr = getattr(self.async_class_instance, name)
            if asyncio.iscoroutinefunction(attr):
                return lambda *args, **kwargs: self._sync_method(attr, *args, **kwargs)
            else:
                return attr
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _sync_method(self, async_method, *args, **kwargs):
        """
        Invokes an asynchronous method synchronously.

        Args:
            async_method: The asynchronous method to be invoked.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the asynchronous method.
        """
        try:
            return self.loop.run_until_complete(async_method(*args, **kwargs))
        finally:
            if self.loop.is_running():
                asyncio.run_coroutine_threadsafe(self.async_class_instance.close(), self.loop)
                self.loop.stop()


class Telnet:
    """
    Wrapper for synchronous or asynchronous Telnet communication.
    """
    def __init__(self, timeout=GLOBAL_DEFAULT_TIMEOUT, sync_mode=False):
        """
        Initializes the Telnet wrapper.

        Args:
            timeout: Timeout value for the Telnet connection.
            sync_mode: If True, operates in synchronous mode.
        """
        if sync_mode:
            self._instance = AsyncToSyncWrapper(AsyncTelnet(timeout))
        else:
            self._instance = AsyncTelnet(timeout)

    def __getattr__(self, name):
        """
        Retrieves attributes from the underlying Telnet instance.

        Args:
            name: The name of the attribute.

        Returns:
            The attribute from the underlying Telnet instance.
        """
        return getattr(self._instance, name)

    def __enter__(self):
        """
        Implements the context manager protocol for entering the 'with' statement.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Implements the context manager protocol for exiting the 'with' statement.
        """
        if self._instance.writer:
            loop = asyncio.get_event_loop()
            if not self._instance.writer.is_closing():
                loop.run_until_complete(self._instance.writer.drain())
                self._instance.writer.close()
                loop.run_until_complete(self._instance.writer.wait_closed())

    async def __aenter__(self):
        """
        Implements the asynchronous context manager protocol for entering the 'async with' statement.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Implements the asynchronous context manager protocol for exiting the 'async with' statement.
        """
        await self.close()
