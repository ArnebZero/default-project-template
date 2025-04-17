import shutil
from pathlib import Path


def remove_file_or_folder(path: str | Path) -> None:
    """Remove a file or folder at the specified path.
    If the path is a directory, it will be removed recursively.
    
    Args:
        path (str | Path): The path to the file or folder to remove.
    """
    path = Path(path)
    if not path.exists():
        return
    if path.is_file() or path.is_symlink():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        raise ValueError(f"Path {path} is neither a file nor a directory.")
