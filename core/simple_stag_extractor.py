from core.file_formats import FILE_FORMATS
from handlers.file_handler import FileHandler


class ByteExtractor:
    def __init__(self, file_bytes: bytes, extension: str):
        self.file_bytes = file_bytes
        self.eof = FILE_FORMATS[extension].EOF

    def extract(self) -> bytes:
        start_eof_index = self.file_bytes.find(self.eof)
        if start_eof_index == -1:
            raise ValueError("EOF não encontrado no arquivo.")

        end_eof_index = start_eof_index + len(self.eof)
        return self.file_bytes[end_eof_index:]


class FileSignatureDetector:
    @staticmethod
    def detect_extension(new_file_bytes: bytes) -> str:
        for name, file_format in FILE_FORMATS.items():
            if new_file_bytes.startswith(file_format.SOF):
                return name
        raise ValueError("Assinatura SOF não reconhecida no arquivo.")


class SimpleStagExtractor:
    def extract_file(self, file_path: str) -> None:
        FileHandler.validate_extension(file_path)

        file_bytes = FileHandler.read_file_bytes(file_path)
        extension = FileHandler.get_extension(file_path)

        byte_extractor = ByteExtractor(file_bytes, extension)
        new_file_bytes = byte_extractor.extract()

        new_file_extension = FileSignatureDetector.detect_extension(new_file_bytes)

        self._save_new_file(new_file_bytes, new_file_extension)

    def _save_new_file(self, new_file_bytes: bytes, new_file_extension: str) -> None:
        with open(f"extracted.{new_file_extension}", "wb") as new_file:
            new_file.write(new_file_bytes)
