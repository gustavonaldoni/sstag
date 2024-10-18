import os


from core.file_formats import SUPPORTED_FORMATS_WITH_SOF_AND_EOF


class FileHandler:
    @staticmethod
    def get_extension(file_path: str) -> str:
        if "." not in file_path:
            raise ValueError(f"Arquivo sem extensão: {file_path}")

        return file_path.split(".")[-1]

    @staticmethod
    def read_file_bytes(file_path: str) -> bytes:
        with open(file_path, "rb") as file:
            return file.read()

    @staticmethod
    def validate_extension(file_path: str) -> None:
        extension = FileHandler.get_extension(file_path)
        if extension not in SUPPORTED_FORMATS_WITH_SOF_AND_EOF:
            raise ValueError(f"Formato de arquivo não suportado: {extension}")

    @staticmethod
    def validate_file_path(file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não existe: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError(
                f"Caminho informado não se refere a um arquivo: {file_path}"
            )
