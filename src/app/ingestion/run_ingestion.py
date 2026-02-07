from pathlib import Path

from .download import download_file
from .unzip_file import unzip_file

def main() -> None:
    url = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta%2ezip"

    raw_dir = Path("data/landing")
    extracted_base_dir = Path("data/extracted")

    zip_path = download_file(
        url = url,
        output_dir = raw_dir,
        filename = "BaseCompleta.zip",
        verify_ssl = False,
        timeout = 60,
    )

    print(f"Arquivo baixado em: {zip_path}")

    extracted_dir = extracted_base_dir / zip_path.stem
    out_dir = unzip_file(
        zip_path = zip_path,
        output_dir = extracted_dir,
        overwrite = False,
    )
    print(f"Arquivo extraído em: {out_dir}")

if __name__ == "__main__":
    main()