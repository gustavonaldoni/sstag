import os
import pytest
import shutil
from unittest.mock import patch, mock_open
from core.simple_stag_inserter import SimpleStagInserter


# Configuração antes de cada teste
@pytest.fixture
def setup_files(tmpdir):
    src_file = tmpdir.join("source.txt")
    dst_file = tmpdir.join("destination.txt")
    
    src_file.write("Conteudo de teste para arquivo de origem.")
    dst_file.write("Conteudo de teste para arquivo de destino.")
    
    return str(src_file), str(dst_file)


# Teste: inserção de arquivo bem-sucedida
def test_insert_file_at_the_end_success(setup_files):
    src_file, dst_file = setup_files
    inserter = SimpleStagInserter()

    inserter.insert_file_at_the_end(src_file, dst_file)

    copy_file_path = f"{dst_file} Copy.txt"
    assert os.path.exists(copy_file_path)
    
    with open(copy_file_path, "rb") as f:
        data = f.read()
        assert b"Conteudo de teste para arquivo de origem." in data
        assert b"Conteudo de teste para arquivo de destino." in data


# Teste: falha ao inserir quando arquivo de origem não existe
def test_insert_file_at_the_end_src_file_not_found(tmpdir):
    inserter = SimpleStagInserter()
    non_existent_file = tmpdir.join("missing.txt")
    dst_file = tmpdir.join("destination.txt")
    dst_file.write("Conteúdo de teste")

    with pytest.raises(FileNotFoundError):
        inserter.insert_file_at_the_end(str(non_existent_file), str(dst_file))


# Teste: falha ao inserir quando arquivo de destino não existe
def test_insert_file_at_the_end_dst_file_not_found(tmpdir):
    inserter = SimpleStagInserter()
    src_file = tmpdir.join("source.txt")
    src_file.write("Conteúdo de teste para arquivo de origem.")
    non_existent_file = tmpdir.join("missing.txt")

    with pytest.raises(FileNotFoundError):
        inserter.insert_file_at_the_end(str(src_file), str(non_existent_file))


# Teste: falha quando caminho de arquivo não é um arquivo
def test_validate_file_path_not_a_file(tmpdir):
    inserter = SimpleStagInserter()
    directory_path = tmpdir.mkdir("not_a_file")

    with pytest.raises(ValueError, match="Caminho informado não se refere a um arquivo"):
        inserter._validate_file_path(str(directory_path))


# Teste: erro de IO durante a cópia do arquivo
def test_copy_file_io_error(setup_files):
    src_file, dst_file = setup_files
    inserter = SimpleStagInserter()

    with patch("shutil.copyfile", side_effect=IOError("Erro de IO")):
        with pytest.raises(RuntimeError, match="Erro de IO ao copiar o arquivo"):
            inserter._copy_file(dst_file)


# Teste: arquivo sem extensão
def test_get_extension_no_extension(tmpdir):
    inserter = SimpleStagInserter()
    file_no_extension = tmpdir.join("no_extension_file")
    file_no_extension.write("Sem extensão")

    with pytest.raises(ValueError, match="Arquivo sem extensão"):
        inserter._get_extension(str(file_no_extension))


# Teste: obtenção do caminho de cópia correto
def test_get_copy_file_path(setup_files):
    src_file, dst_file = setup_files
    inserter = SimpleStagInserter()

    expected_copy_path = f"{dst_file} Copy.txt"
    assert inserter._get_copy_file_path(dst_file) == expected_copy_path


# Teste: inserção de arquivo com exceção inesperada
def test_insert_file_unexpected_error(setup_files):
    src_file, dst_file = setup_files
    inserter = SimpleStagInserter()

    with patch("builtins.open", side_effect=Exception("Erro inesperado")):
        with pytest.raises(RuntimeError, match="Erro inesperado"):
            inserter.insert_file_at_the_end(src_file, dst_file)


# Teste: falha ao validar arquivo inexistente
def test_validate_file_path_file_not_found():
    inserter = SimpleStagInserter()

    with pytest.raises(FileNotFoundError, match="Arquivo não existe: arquivo_inexistente.txt"):
        inserter._validate_file_path("arquivo_inexistente.txt")

