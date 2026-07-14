from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables
    and the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    #
    # Application
    #

    app_name: str = Field(
        default="Enterprise AI Assistant",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="1.0.0",
        alias="APP_VERSION",
    )

    environment: str = Field(
        default="development",
        alias="ENVIRONMENT",
    )

    #
    # OpenAI
    #

    openai_api_key: str = Field(
        alias="OPENAI_API_KEY",
    )

    openai_chat_model: str = Field(
        default="gpt-4.1",
        alias="OPENAI_CHAT_MODEL",
    )

    #
    # Anthropic
    #

    anthropic_api_key: str | None = Field(
        default=None,
        alias="ANTHROPIC_API_KEY",
    )

    anthropic_chat_model: str = Field(
        default="claude-sonnet-5",
        alias="ANTHROPIC_CHAT_MODEL",
    )

    embedding_model: str = Field(
        default="text-embedding-3-small",
        alias="OPENAI_EMBEDDING_MODEL",
    )

    # Chroma

    chroma_persist_directory: str = "./storage/chroma"

    #
    # Server
    #

    host: str = Field(
        default="127.0.0.1",
        alias="HOST",
    )

    port: int = Field(
        default=8000,
        alias="PORT",
    )

    #
    # Logging
    #

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    #
    # MCP
    #

    mcp_server_host: str = Field(
        default="127.0.0.1",
        alias="MCP_SERVER_HOST",
    )

    mcp_server_port: int = Field(
        default=8765,
        alias="MCP_SERVER_PORT",
    )

    @property
    def mcp_server_url(self) -> str:
        return f"http://{self.mcp_server_host}:{self.mcp_server_port}/mcp"

    #
    # Frontend
    #

    frontend_url: str = Field(
        default="http://127.0.0.1:5500",
        alias="FRONTEND_URL",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Create a cached Settings instance.

    Using lru_cache ensures the configuration
    is loaded only once during the application's
    lifetime.
    """

    return Settings()


settings = get_settings()