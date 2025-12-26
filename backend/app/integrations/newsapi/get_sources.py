# shiny-memeimport requests
from typing import Any, Dict

from app.integrations.base import BaseIntegration
from app.integrations.models import IntegrationMetadata
from app.credentials.resolver import CredentialsResolver
from app.logger import logger


class NewsApiGetSourcesIntegration(BaseIntegration):
    """
    Integration: NewsAPI Get Sources
    Description: Get available news sources from NewsAPI
    """

    metadata = IntegrationMetadata(
        id="newsapi_get_sources",
        name="NewsAPI Get Sources",
        description="Get list of available news sources from NewsAPI",
        category="news",
        version="1.0.0",
        provider="newsapi",
        icon_s3_key=None,
        config_schema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "description": "Filter sources by language (e.g. en, ru)"
                },
                "country": {
                    "type": "string",
                    "description": "Filter sources by country (e.g. us, gb)"
                },
                "category": {
                    "type": "string",
                    "description": "Filter sources by category (e.g. business, technology)"
                }
            },
            "required": []
        }
    )

    async def execute(self, config: Dict[str, Any], credentials_resolver: CredentialsResolver) -> Dict[str, Any]:
        try:
            credentials = credentials_resolver.get_default_for(
                provider="newsapi",
                strategy="api_key"
            )

            api_key = credentials.payload.get("api_key")
            if not api_key:
                raise ValueError("NewsAPI api_key not provided")

            url = "https://newsapi.org/v2/sources"

            params = {
                "apiKey": api_key
            }

            if config.get("language"):
                params["language"] = config["language"]
            if config.get("country"):
                params["country"] = config["country"]
            if config.get("category"):
                params["category"] = config["category"]

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                "status": "success",
                "sources": data.get("sources", [])
            }

        except Exception as e:
            logger.exception("Failed to get NewsAPI sources")
            return {
                "status": "error",
                "message": str(e)
            }
