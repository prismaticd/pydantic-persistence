import json
from pathlib import Path
from typing import List, Optional, Union

from pydantic_persistence.base import BaseBackendConfig, ListDictBackend


class JsonLocalStorageConfig(BaseBackendConfig):
    """Json file system base backend"""

    base_folder: Path

    def __init__(self, base_folder: Union[Path, str, None] = None):
        if not base_folder:
            base_folder = "."
        if isinstance(base_folder, str):
            base_folder = Path(base_folder)
        self.base_folder = base_folder


class JsonLocalStorage(ListDictBackend):
    """Json file system backend"""

    backend_config: JsonLocalStorageConfig

    def __init__(self, table_name: str, backend_config: Optional[JsonLocalStorageConfig] = None):
        if not backend_config:
            backend_config = JsonLocalStorageConfig()
        super().__init__(table_name, backend_config)

    def get_file_path(self) -> Path:
        """Return the path of the table on disk"""
        return self.backend_config.base_folder / f"{self.table_name}.json"

    def get_data(self) -> List[dict]:
        """Return the data as list of dict from disk"""
        if self.get_file_path().exists():
            return json.loads(self.get_file_path().read_text())
        else:
            return []

    def save_data(self, data: List[dict]) -> None:
        """Save the data back to disk"""
        if not self.get_file_path().exists():
            self.get_file_path().touch()
        self.get_file_path().write_text(json.dumps(data))
