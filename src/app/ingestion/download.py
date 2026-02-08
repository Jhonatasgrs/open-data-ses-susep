from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests

def download_file(
        url: str,
        output_dir: str | Path,
        filename: Optional[str] = None,
        chunk_size: int = 8192,
        timeout: int | float = 60,
        verify_ssl: bool = True,
) -> Path:
    """
    Baixa um arquivo via HTTP/HTTPS para uma pasta específica.

    Args:
        url: URL do arquivo.
        output_dir: Pasta de destino (relativa ou absoluta).
        filename: Nome do arquivo. Se None, tenta inferir pela URL, senão usa 'download.bin'.
        chunk_size: Tamanho do chunk no streaming.
        timeout: Timeout (segundos).
        verify_ssl: Verifica SSL (True recomendado). Use False se o servidor der problema.

    Returns:
        Path do arquivo salvo.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not filename:
        inferred = url.split("/")[-1].split("?")[0] or "download.bin"
        filename = inferred
    
    file_path = output_dir / filename

    with requests.get(url, stream=True, timeout=timeout, verify=verify_ssl) as response:
        response.raise_for_status()
        tmp_path = file_path.with_suffix(file_path.suffix + ".part")
        with open(tmp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        os.replace(tmp_path, file_path)
    return file_path