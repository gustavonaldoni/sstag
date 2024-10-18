import shutil
from handlers.file_handler import FileHandler


class FileCopier:
    @staticmethod
    def copy_file(file_path: str) -> str:
        copy_path = FilePathHelper.get_copy_file_path(file_path)
        try:
            shutil.copyfile(file_path, copy_path)
        except IOError as e:
            raise RuntimeError(f"Erro de IO ao copiar o arquivo: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro inesperado ao copiar o arquivo: {e}")
        return copy_path


class FileAppender:
    @staticmethod
    def append_file(src_path: str, dst_path: str) -> None:
        try:
            with open(src_path, "rb") as src_file, open(dst_path, "ab") as dst_file:
                chunk_size = 4096
                for chunk in iter(lambda: src_file.read(chunk_size), b""):
                    dst_file.write(chunk)
        except IOError as e:
            raise RuntimeError(f"Erro de IO ao manipular algum arquivo: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro inesperado durante a esteganografia: {e}")


class FilePathHelper:
    @staticmethod
    def get_copy_file_path(file_path: str) -> str:
        extension = FileHandler.get_extension(file_path)
        return f"{file_path} Copy.{extension}"


class SimpleStagInserter:
    def insert_file_at_the_end(self, src_path: str, dst_path: str) -> None:
        FileHandler.validate_file_path(src_path)
        FileHandler.validate_file_path(dst_path)

        copy_path = FileCopier.copy_file(dst_path)
        FileAppender.append_file(src_path, copy_path)
