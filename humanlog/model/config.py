import xdg_base_dirs
import structlog
from typing import Optional
import json
from pathlib import Path

logger = structlog.get_logger()


class HumanLogConfig:
    default_db_location: Optional[str] = None
    default_db_filename: str = 'humanlog.db'

    _CONFIG_FILE_NAME: str = 'config.json'
    _APP_DIRECTORY: str = 'humanlog'
    _config_path: Optional[Path] = None

    def __init__(
        self,
        db_location: Optional[str] = None,
        db_filename: Optional[str] = None
        ):
        if db_filename is None:
            self.db_filename = self.default_db_filename
        else:
            self.db_filename = db_filename
        if db_location is None and self.default_db_location is None:
            self.db_location = str(xdg_base_dirs.xdg_data_home().joinpath(self._APP_DIRECTORY))
        elif db_location is None and isinstance(self.default_db_location, str):
            self.db_location = self.default_db_location
        elif isinstance(db_location, str):
            self.db_location = db_location
        else:
            raise ValueError('db_location must be None or a string')
        self.db_path = Path(self.db_location, self.db_filename)


    @classmethod
    def _load_config_dict_from_disk(cls, full_path: Path) -> Optional[dict]:
        if full_path.exists() is False:
            return None
        else:
            with full_path.open(mode='r') as f:
                config = json.load(f)
            return config

    @classmethod 
    def load_config(cls, overload_file_location: Optional[str] = None) -> "HumanLogConfig":
        if overload_file_location is None:
            config_path = xdg_base_dirs.xdg_config_home().joinpath(cls._APP_DIRECTORY, cls._CONFIG_FILE_NAME)
        else:
            config_path = Path(overload_file_location)

        config_dict = cls._load_config_dict_from_disk(full_path=config_path)
        cls._config_path = config_path
        if config_dict is None:
            logger.info('No configuration found, populating with defaults')
            config_dict = {}
        return cls(**config_dict)

    def save_config(self) -> None:
        config_dict = {
            'db_location': self.db_location,
            'db_filename': self.db_filename
        }
        if self._config_path is None:
            self._config_path = xdg_base_dirs.xdg_config_home().joinpath(self._APP_DIRECTORY, self._CONFIG_FILE_NAME)
        with self._config_path.open(mode='w+') as f:
            f.write(json.dumps(config_dict))
        logger.debug('Config Saved')
    
