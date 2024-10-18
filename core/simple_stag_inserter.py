import os
import shutil


class SimpleStagInserter:
    def insert_file_at_the_end(self, src_path: str, dst_path: str) -> None:
        self._validate_file_path(src_path)
        self._validate_file_path(dst_path)

        self._copy_file(dst_path)
        copy_path = self._get_copy_file_path(dst_path)

        try:
            with open(src_path, "rb") as src_file, open(copy_path, "ab") as copy_file:
                chunk_bytes = 4096
                chunk_data = src_file.read(chunk_bytes)

                while chunk_data:
                    copy_file.write(chunk_data)
                    chunk_data = src_file.read(chunk_bytes)

        except IOError as e:
            raise RuntimeError(f"Erro de IO ao manipular alguma arquivo: {e}")

        except Exception as e:
            raise RuntimeError(f"Erro inesperado durante a esteganografia: {e}")

    def _validate_file_path(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não existe: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError(
                f"Caminho informado não se refere a um arquivo: {file_path}"
            )

    def _copy_file(self, file_path: str) -> None:
        copy_path = self._get_copy_file_path(file_path)

        try:
            shutil.copyfile(file_path, copy_path)

        except IOError as e:
            raise RuntimeError(f"Erro de IO ao copiar o arquivo: {e}")

        except Exception as e:
            raise RuntimeError(f"Erro inesperado ao copiar o arquivo: {e}")

    def _get_copy_file_path(self, file_path: str) -> str:
        extension = self._get_extension(file_path)

        return f"{file_path} Copy.{extension}"

    def _get_extension(self, file_path: str) -> str:
        if "." not in file_path:
            raise ValueError(f"Arquivo sem extensão: {file_path}")

        return file_path.split(".")[-1]
