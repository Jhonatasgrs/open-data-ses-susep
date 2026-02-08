from pathlib import Path
from zipfile import ZipFile, BadZipFile

def unzip_file(
        zip_path: str | Path,
        output_dir: str | Path | None = None,
        overwrite: bool = False,
) -> Path:
    """
    Extrai um arquivo ZIP para uma pasta.

    Args:
        zip_path: Caminho do arquivo .zip
        output_dir: Pasta de destino. Se None, cria uma pasta com o nome do zip
        overwrite: Se True, sobrescreve arquivos existentes

    Returns:
        Path da pasta onde os arquivos foram extraídos
    """
    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(f"Arquivo ZIP não encontrado: {zip_path}")
    
    if zip_path.suffix.lower() != ".zip":
        raise ValueError(f"Arquivo não é um ZIP válido: {zip_path}")
    
    if output_dir is None:
        output_dir = zip_path.with_suffix("")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        with ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                target_path = output_dir / member

                if target_path.exists() and not overwrite:
                    continue  # Pula arquivos existentes se overwrite=False

                zip_ref.extract(member, output_dir)

    except BadZipFile as e:
        raise ValueError(f"Erro ao ler o arquivo ZIP: {zip_path}") from e

    return output_dir    