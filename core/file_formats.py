from dataclasses import dataclass


from dataclasses import dataclass


@dataclass
class FileFormat:
    full_name: str
    extension_name: str
    SOF: bytes
    EOF: bytes


from dataclasses import dataclass


@dataclass
class FileFormat:
    full_name: str
    extension_name: str
    SOF: bytes
    EOF: bytes


FILE_FORMATS = {
    # Imagens
    "png": FileFormat(
        full_name="Portable Network Graphics",
        extension_name="png",
        SOF=b"\x89PNG\r\n\x1a\n",
        EOF=b"IEND\xae\x42\x60\x82",
    ),
    "jpg": FileFormat(
        full_name="JPEG Image",
        extension_name="jpg",
        SOF=b"\xff\xd8\xff",
        EOF=b"\xff\xd9",
    ),
    "gif": FileFormat(
        full_name="Graphics Interchange Format",
        extension_name="gif",
        SOF=b"GIF87a",
        EOF=b"\x00\x3b",
    ),
    "bmp": FileFormat(
        full_name="Bitmap Image File",
        extension_name="bmp",
        SOF=b"BM",
        EOF=None,  # Não há EOF fixo
    ),
    # Áudio
    "mp3": FileFormat(
        full_name="MPEG Audio Layer III",
        extension_name="mp3",
        SOF=b"\xff\xfb",
        EOF=None,  # MP3 não possui EOF fixo
    ),
    "wav": FileFormat(
        full_name="Waveform Audio File",
        extension_name="wav",
        SOF=b"RIFF",
        EOF=None,  # Não há EOF definido para WAV
    ),
    "flac": FileFormat(
        full_name="Free Lossless Audio Codec",
        extension_name="flac",
        SOF=b"fLaC",
        EOF=None,  # EOF pode variar
    ),
    # Vídeo
    "mp4": FileFormat(
        full_name="MPEG-4 Video",
        extension_name="mp4",
        SOF=b"\x00\x00\x00\x18ftypmp42",
        EOF=None,  # EOF pode variar
    ),
    "avi": FileFormat(
        full_name="Audio Video Interleave",
        extension_name="avi",
        SOF=b"RIFF",
        EOF=None,  # Não há EOF fixo
    ),
    "mkv": FileFormat(
        full_name="Matroska Video",
        extension_name="mkv",
        SOF=b"\x1A\x45\xDF\xA3",  # EBML Header
        EOF=None,  # EOF pode variar
    ),
    "mov": FileFormat(
        full_name="QuickTime Movie",
        extension_name="mov",
        SOF=b"\x00\x00\x00\x14ftypqt",
        EOF=None,  # EOF pode variar
    ),
    # Documentos
    "pdf": FileFormat(
        full_name="Portable Document Format",
        extension_name="pdf",
        SOF=b"%PDF",
        EOF=b"%%EOF",
    ),
    "docx": FileFormat(
        full_name="Microsoft Word Document",
        extension_name="docx",
        SOF=b"PK\x03\x04",  # Arquivo ZIP (docx é baseado em ZIP)
        EOF=b"PK\x05\x06",  # Fim de arquivo ZIP
    ),
    "xlsx": FileFormat(
        full_name="Microsoft Excel Spreadsheet",
        extension_name="xlsx",
        SOF=b"PK\x03\x04",  # Arquivo ZIP (xlsx é baseado em ZIP)
        EOF=b"PK\x05\x06",  # Fim de arquivo ZIP
    ),
    "pptx": FileFormat(
        full_name="Microsoft PowerPoint Presentation",
        extension_name="pptx",
        SOF=b"PK\x03\x04",  # Arquivo ZIP (pptx é baseado em ZIP)
        EOF=b"PK\x05\x06",  # Fim de arquivo ZIP
    ),
    # Arquivos Compactados
    "zip": FileFormat(
        full_name="ZIP Archive",
        extension_name="zip",
        SOF=b"PK\x03\x04",
        EOF=b"PK\x05\x06",
    ),
    "rar": FileFormat(
        full_name="RAR Archive",
        extension_name="rar",
        SOF=b"\x52\x61\x72\x21\x1A\x07\x00",
        EOF=None,  # EOF pode variar
    ),
    # Outros formatos úteis
    "tar": FileFormat(
        full_name="Tape Archive",
        extension_name="tar",
        SOF=b"ustar",
        EOF=None,  # EOF pode variar
    ),
    "7z": FileFormat(
        full_name="7-Zip Archive",
        extension_name="7z",
        SOF=b"\x37\x7A\xBC\xAF\x27\x1C",
        EOF=None,  # EOF pode variar
    ),
}


SUPPORTED_FORMATS = list(FILE_FORMATS.keys())
SUPPORTED_FORMATS_WITH_SOF_AND_EOF = [
    name for name, file_format in FILE_FORMATS.items() if file_format.EOF
]
SUPPORTED_FORMATS_WITHOUT_EOF = [
    name for name, file_format in FILE_FORMATS.items() if not file_format.EOF
]
