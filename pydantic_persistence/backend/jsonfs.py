import json
from pathlib import Path
from typing import List, Optional, Union

from pydantic_persistence.base import BaseBackendConfig, ListDictBackend


class JsonFsConfig(BaseBackendConfig):
    """Json file system base backend"""

    base_folder: Path

    def __init__(self, base_folder: Union[Path, str, None] = None):
        if not base_folder:
            base_folder = "."
        if isinstance(base_folder, str):
            base_folder = Path(base_folder)
        self.base_folder = base_folder


class JsonFs(ListDictBackend):
    """Json file system backend"""

    backend_config: JsonFsConfig

    def __init__(self, table_name: str, backend_config: Optional[JsonFsConfig] = None):
        if not backend_config:
            backend_config = JsonFsConfig()
        super().__init__(table_name, backend_config)

    def get_file_path(self) -> Path:
        return self.backend_config.base_folder / f"{self.table_name}.json"

    def get_data(self) -> List[dict]:
        if self.get_file_path().exists():
            return json.loads(self.get_file_path().read_text())
        else:
            return []

    def save_data(self, data: List[dict]) -> None:
        if not self.get_file_path().exists():
            self.get_file_path().touch()
        self.get_file_path().write_text(json.dumps(data))
