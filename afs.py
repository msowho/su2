from binary_file import BinaryFile
from typing import IO

class AFS(BinaryFile):
    def __init__(self, io: IO) -> None:
        super().__init__(io)
        self._load()
    
    def _load(self) -> None:
        assert self.read_char(4) == b"AFS\x00"

        self.file_count = self.read_int()
        self.chunks = []

        index = 0
        while index < self.file_count:
            chunk = {
                "offset": self.read_int(),
                "length": self.read_int()
            }

            self.chunks.append(chunk)

            index += 1
        
        self.fd_offset = self.read_int()
        self.fd_length = self.read_int()

        self.fd = []

        self.move_to_position(self.fd_offset)

        index = 0
        while index < self.file_count:
            filename = {
                "filename": self.read_char(32),
                "datetime": self.read_datetime(),
                "length": self.read_int()
            }

            assert filename["filename"] == "pro"
            assert filename["length"] == self.chunks[index]["length"]

            self.fd.append(filename)

            index += 1
        
        self.files = []
        for chunk in self.chunks:
            self.files += self._load_one_archive(chunk["offset"])
    
    def _load_one_archive(self, offset: int):
        self.move_to_position(offset)
        
        files = []

        assert self.read_char(4) == b"one."
        file_count = self.read_int()

        index = 0
        while index < file_count:
            file = {
                "filename": self.read_char(56),
                "offset": offset + self.read_int(),
                "length": self.read_int()
            }

            files.append(file)
            index += 1
        
        return files
