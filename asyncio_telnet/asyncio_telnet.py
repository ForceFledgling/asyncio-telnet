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


class Telnet:

    def __init__(self, host=None, port=0,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.debuglevel = 0
        self.host = host
        self.port = port
        self.timeout = timeout
        self.fast_read_timeout = 0.1
        self.reader = None
        self.writer = None
        if host is not None:
            asyncio.run(self.open(host, port, timeout))

    async def open(self, host, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.eof = 0
        if not port:
            port = TELNET_PORT
        self.host = host
        self.port = port
        self.timeout = timeout

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
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.writer:
            await self.writer.drain()
            self.writer.close()
            await self.writer.wait_closed()
            print("Connection closed")

    async def filter_telnet_data(self, data):
        """
        Удаляет управляющие символы TELNET из данных.
        """
        filtered_data = b''
        i = 0
        while i < len(data):
            if data[i:i+1] == IAC:
                # Если встречаем IAC, обрабатываем TELNET команду
                command = data[i:i+3]
                i += 3
                if command[1:2] in (WILL, WONT, DO, DONT, IAC):
                    # Это команда WONT, WILL, DO, DONT или IAC, удаляем ее
                    continue
                elif command[1:2] == b'\xfa':
                    # Это начало поддержки опции, пропускаем все до IAC SE
                    iac_se_pos = data.find(b'\xff\xf0', i)
                    if iac_se_pos != -1:
                        i = iac_se_pos + 2
                    else:
                        # Если IAC SE не найдено, прекращаем обработку данных
                        break
            else:
                # В противном случае добавляем текущий байт к отфильтрованным данным
                filtered_data += data[i:i+1]
                i += 1
        return filtered_data
