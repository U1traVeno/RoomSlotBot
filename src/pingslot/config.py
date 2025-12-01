import os
from pathlib import Path
from typing import Any, Annotated

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
    YamlConfigSettingsSource,
)


class EnvVarFileConfigSettingsSource(InitSettingsSource):
    """
    一个从环境变量中指定的文件加载配置的源。
    它会根据文件扩展名自动选择 TOML 解析器。
    """

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        env_var: str = "ROOMSLOT_CONFIG_FILE",
    ):
        """
        Args:
            settings_cls: The settings class.
            env_var: The name of the environment variable to read the file path from.
        """
        self.env_var = env_var
        self.file_path_str = os.getenv(env_var)

        file_data: dict[str, Any] = {}

        if not self.file_path_str:
            super().__init__(settings_cls, file_data)
            return

        file_path = Path(self.file_path_str)
        if not file_path.exists():
            print(f"警告: 环境变量 '{self.env_var}' 指向的文件 '{file_path}' 不存在。")
            super().__init__(settings_cls, file_data)
            return

        # 根据文件扩展名，复用现有的源逻辑
        suffix = file_path.suffix.lower()
        if suffix == ".toml":
            # 内部创建一个 TomlConfigSettingsSource 实例来加载文件
            file_data = TomlConfigSettingsSource(
                settings_cls, toml_file=file_path
            ).toml_data
        else:
            print(f"警告: 不支持的文件类型 '{suffix}'。已忽略。")

        # 调用 InitSettingsSource 的 __init__，传入从文件中加载的数据
        super().__init__(settings_cls, file_data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(env_var={self.env_var}, file_path={self.file_path_str!r})"


class ServerConfig(BaseModel):
    """服务器配置"""

    host: str = "0.0.0.0"
    port: Annotated[int, Field(ge=1024, le=65535)] = 8105
    api_prefix: str = "/api/v1"
    debug: bool = False


class DatabaseConfig(BaseModel):
    """数据库配置"""

    url: str = "sqlite:///./roomslotbot.db"
    echo: bool = False


class Settings(BaseSettings):
    """应用程序主配置"""

    model_config = SettingsConfigDict(
        # 从项目根目录读取配置文件
        toml_file="config.toml",
        # 环境变量配置
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="ROOMSLOT_",
        env_nested_delimiter="__",
        # 大小写敏感
        case_sensitive=False,
        # 允许额外字段
        extra="ignore",
    )

    # 项目信息
    project_name: str = "RoomSlotBot"
    version: str = "0.1.0"

    # 各模块配置
    server: ServerConfig = ServerConfig()
    database: DatabaseConfig = DatabaseConfig()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        定义不同配置源的优先级（从高到低）：
        1. init_settings: 初始化时传入的参数
        2. env_var_file_settings: 通过环境变量指定的配置文件 (ROOMSLOT_CONFIG_FILE)
        3. env_settings: 环境变量
        4. dotenv_settings: .env 文件
        5. toml_settings: config.toml 文件
        6. file_secret_settings: secrets 文件
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            EnvVarFileConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


# 全局配置实例
settings = Settings()
