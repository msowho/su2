from typing import IO
from datetime import datetime

class BinaryFile:
    def __init__(self, io: IO) -> None:
        self._io = io
    
    def move_to_position(self, 
                        offset: int, 
                        from_start: bool = True, 
                        from_current: bool = False, 
                        from_end: bool = False) -> int:
        if from_start: return self._io.seek(offset, 0)
        if from_current: return self._io.seek(offset, 1)
        if from_end: return self._io.seek(offset, 2)

        return 0
    
    def read_bytes(self, size: int):
        return self._io.read(size)

    def read_int(self, size: int = 4, signed: bool = True):
        return int.from_bytes(self.read_bytes(size), 'little', signed=signed)
    
    def read_char(self, size: int):
        return self.read_bytes(size).replace(b"\x00", b"").decode('ascii')
    
    def read_datetime(self):
        year = self.read_int(2)
        month = self.read_int(2)
        day = self.read_int(2)
        hour = self.read_int(2)
        minute = self.read_int(2)
        second = self.read_int(2)

        return datetime(year, month, day, hour, minute, second)

    def write_bytes(self, source: bytes) -> int:
        return self._io.write(source)
    
    def write_int(self, number: int, size: int = 4) -> int:
        serialized_number = number.to_bytes(size, 'little')
        return self.write_bytes(serialized_number)
    
    def write_char(self, string: str, size: int) -> int:
        assert len(string) > size
        char = string.ljust(size, "\0").encode("ascii")
        return self.write_bytes(char)
    
    def write_datetime(self, source: datetime) -> int:
        result = 0

        self.write_int(source.year, 2)
        self.write_int(source.month, 2)
        self.write_int(source.day, 2)
        self.write_int(source.hour, 2)
        self.write_int(source.minute, 2)
        self.write_int(source.second, 2)

        return result
