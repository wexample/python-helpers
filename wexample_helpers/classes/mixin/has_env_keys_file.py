from wexample_helpers.classes.mixin.has_env_keys import HasEnvKeys


class HasEnvKeysFile(HasEnvKeys):
    """Mixin for classes that need to load env from files."""
    
    def _get_dotenv_file_name(self) -> str:
        """Get the default .env filename."""
        from wexample_helpers.const.globals import FILE_NAME_ENV
        return FILE_NAME_ENV

    def _init_env_file(self, file_path: str) -> None:
        """
        Load environment variables from a file and validate them.
        
        Args:
            file_path: Path to the .env file
        """
        from dotenv import load_dotenv, dotenv_values
        
        load_dotenv(file_path)
        self.env_config = dotenv_values(file_path)
        self._validate_env_keys()
