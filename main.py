import os, errno, argparse
from pathlib import Path
from typing import Literal, Optional, List, Dict, Tuple
from pandas import read_excel
from PIL import Image
from PyPDF2 import PdfReader


file_types = Literal["image", "pdf", "excel"]
TYPES: List[Dict[file_types, (str | Tuple[str, ...])]] = [
    {"exts": (".png", ".jpg", "jpeg"), "file_type": "image"},
    {"exts": (".pdf"), "file_type": "pdf"},
    {
        "exts": (".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"),
        "file_type": "excel",
    },
]


def delete_file(path: str | Path) -> None:
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
    except Exception as err:
        print("Erro ao remover arquivo", path, ". Erro abaixo")
        print(err)


def check_file(
    filename: str, *, base_path: str = "./", file_type: Optional[file_types] = None
) -> bool | None:
    check = None
    full_path = base_path + "/" + filename

    if file_type == "image":
        try:
            img = Image.open(full_path)
            img.load()
            img.verify()

            check = True
        except (IOError, SyntaxError):
            check = False
    elif file_type == "pdf":
        with open(full_path, "rb") as f:
            try:
                pdf = PdfReader(f)
                info = pdf.metadata
                if info:
                    check = True
                else:
                    check = False
            except:
                check = False
    elif file_type == "excel":
        try:
            df = read_excel(full_path, engine="openpyxl")

            check = not df.empty
        except:
            check = False

    return check


def search_files(base_path: str = "./", remove_corrupted: bool = False) -> None:
    print("Checando arquivos no diretório:", base_path)
    if remove_corrupted is True:
        print("Arquivos corrompidos serão removidos!")
    for filename in os.listdir(base_path):
        print("-" * 30)
        print("Checando arquivo:", filename)

        check = None

        for option in TYPES:
            if filename.endswith(option.get("exts", ())):
                check = check_file(
                    filename, base_path=base_path, file_type=option.get("file_type", "")
                )

        if check is None:
            check = check_file(filename, base_path=base_path, file_type=None)

        if check is False:
            print("Arquivo corrompido!")
            if remove_corrupted is True:
                print("Removendo arquivo...")
                os.remove(base_path + "/" + filename)
        elif check is True:
            print("Arquivo seguro!")
        else:
            print("Não foi possível verificar o arquivo.")


def main(args: argparse.Namespace):
    search_files(args.dirpath, args.removecorrupted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Encontrar arquivos corrompidos em um diretório."
    )

    where_the_script_is = str(Path(__file__).parent.resolve())
    where_the_script_is_running = str(Path().resolve())

    parser.add_argument(
        "-d",
        "--dirpath",
        type=str,
        required=False,
        default=where_the_script_is or where_the_script_is_running,
        help="Caminho para a pasta contendo os arquivos.",
    )
    parser.add_argument(
        "--removecorrupted",
        type=bool,
        required=False,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Se os arquivos corrompidos devem ser removidos.",
    )

    args = parser.parse_args()
    main(args)
