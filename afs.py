from binary_file import BinaryFile
from typing import IO

class AFS(BinaryFile):
    def __init__(self, io: IO) -> None:
        super().__init__(io)
        self._load()
    
    def _load(self) -> None:
        assert self.read_bytes(4) == b"AFS\x00"

        self.file_count = self.read_int()
        self.chunks = []

        print("Parsing chunks...")
        for index in range(self.file_count):
            offset = self.read_int()
            length = self.read_int()

            chunk = {
                "offset": offset,
                "length": length
            }

            self.chunks.append(chunk)
        
        self.fd_offset = self.read_int()
        self.fd_length = self.read_int()

        self.fd = []
        self.files = []

        self.move_to_position(self.fd_offset)

        print("Parsing filename directory...")
        for index in range(self.file_count):
            filename = self.read_char(32)
            datetime = self.read_datetime()
            length = self.read_int()

            element = {
                "filename": filename,
                "datetime": datetime,
                "length": length
            }

            assert filename == "pro"

            self.fd.append(filename)
        
        print("Parsing ONE archives...")
        for chunk in self.chunks:
            self.files += self._load_one_archive(chunk["offset"])
    
    def _load_one_archive(self, offset: int):
        self.move_to_position(offset)
        
        files = []

        assert self.read_char(4) == "one."
        file_count = self.read_int()

        for index in range(file_count):
            file = {
                "filename": self.read_char(56),
                "offset": offset + self.read_int(),
                "length": self.read_int()
            }

            files.append(file)
        
        return files
