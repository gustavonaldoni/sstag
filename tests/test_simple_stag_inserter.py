import pytest
from unittest.mock import patch, mock_open
from core.simple_stag_inserter import (
    FileAppender,
    FileCopier,
    FilePathHelper,
    SimpleStagInserter,
)


# Testes para FileCopier
@patch("shutil.copyfile")
@patch("FilePathHelper.get_copy_file_path", return_value="test_file Copy.txt")
def test_file_copier_success(mock_get_copy_file_path, mock_copyfile):
    file_path = "test_file.txt"
    result = FileCopier.copy_file(file_path)

    mock_copyfile.assert_called_once_with(file_path, "test_file Copy.txt")
    assert result == "test_file Copy.txt"


@patch("shutil.copyfile", side_effect=IOError("Erro de IO"))
@patch("FilePathHelper.get_copy_file_path", return_value="test_file Copy.txt")
def test_file_copier_io_error(mock_get_copy_file_path, mock_copyfile):
    file_path = "test_file.txt"

    with pytest.raises(
        RuntimeError, match="Erro de IO ao copiar o arquivo: Erro de IO"
    ):
        FileCopier.copy_file(file_path)


@patch("shutil.copyfile", side_effect=Exception("Erro inesperado"))
@patch("FilePathHelper.get_copy_file_path", return_value="test_file Copy.txt")
def test_file_copier_unexpected_error(mock_get_copy_file_path, mock_copyfile):
    file_path = "test_file.txt"

    with pytest.raises(
        RuntimeError, match="Erro inesperado ao copiar o arquivo: Erro inesperado"
    ):
        FileCopier.copy_file(file_path)


# Testes para FileAppender
@patch("builtins.open", new_callable=mock_open)
def test_file_appender_success(mock_open):
    src_path = "source.txt"
    dst_path = "destination.txt"

    FileAppender.append_file(src_path, dst_path)

    mock_open.assert_any_call(src_path, "rb")
    mock_open.assert_any_call(dst_path, "ab")
    assert mock_open().write.called


@patch("builtins.open", side_effect=IOError("Erro de IO"))
def test_file_appender_io_error(mock_open):
    src_path = "source.txt"
    dst_path = "destination.txt"

    with pytest.raises(
        RuntimeError, match="Erro de IO ao manipular algum arquivo: Erro de IO"
    ):
        FileAppender.append_file(src_path, dst_path)


@patch("builtins.open", side_effect=Exception("Erro inesperado"))
def test_file_appender_unexpected_error(mock_open):
    src_path = "source.txt"
    dst_path = "destination.txt"

    with pytest.raises(
        RuntimeError, match="Erro inesperado durante a esteganografia: Erro inesperado"
    ):
        FileAppender.append_file(src_path, dst_path)


# Testes para FilePathHelper
@patch("handlers.file_handler.FileHandler.get_extension", return_value="txt")
def test_file_path_helper_success(mock_get_extension):
    file_path = "test_file.txt"
    result = FilePathHelper.get_copy_file_path(file_path)

    assert result == "test_file.txt Copy.txt"
    mock_get_extension.assert_called_once_with(file_path)


# Testes para SimpleStagInserter
@patch("FileHandler.validate_file_path")
@patch("FileCopier.copy_file", return_value="test_file Copy.txt")
@patch("FileAppender.append_file")
def test_simple_stag_inserter_success(
    mock_append_file, mock_copy_file, mock_validate_file_path
):
    inserter = SimpleStagInserter()
    src_path = "source.txt"
    dst_path = "destination.txt"

    inserter.insert_file_at_the_end(src_path, dst_path)

    mock_validate_file_path.assert_any_call(src_path)
    mock_validate_file_path.assert_any_call(dst_path)
    mock_copy_file.assert_called_once_with(dst_path)
    mock_append_file.assert_called_once_with(src_path, "test_file Copy.txt")


@patch("FileHandler.validate_file_path")
@patch(
    "FileCopier.copy_file", side_effect=RuntimeError("Erro de IO ao copiar o arquivo")
)
def test_simple_stag_inserter_copy_file_error(mock_copy_file, mock_validate_file_path):
    inserter = SimpleStagInserter()
    src_path = "source.txt"
    dst_path = "destination.txt"

    with pytest.raises(RuntimeError, match="Erro de IO ao copiar o arquivo"):
        inserter.insert_file_at_the_end(src_path, dst_path)


@patch("FileHandler.validate_file_path", side_effect=ValueError("Caminho inválido"))
def test_simple_stag_inserter_invalid_file_path(mock_validate_file_path):
    inserter = SimpleStagInserter()
    src_path = "source.txt"
    dst_path = "destination.txt"

    with pytest.raises(ValueError, match="Caminho inválido"):
        inserter.insert_file_at_the_end(src_path, dst_path)
