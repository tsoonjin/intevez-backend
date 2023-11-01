"""Minimal Litestar application."""
from asyncio import sleep
from typing import Any
from dotenv import load_dotenv
import weaviate
import os
from utils import weaviate_search
from dataclasses import dataclass
from typing import Optional, List


from litestar import Litestar, get, post, openapi

# Setup

load_dotenv()

client = weaviate.Client(
    url = os.getenv("WEAVIATE_CLUSTER_URL"),  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")  # Replace with your inference API key
    }
)

keys = [
 'name',
 'type',
 'color',
 'style',
 'features',
 'functionality',
 'price',
 'description',
 'length',
 'depth',
 'height',
 'shopifyId'
]

# Data contracts

@dataclass
class SearchRequest:
    query: str
    sessionId: Optional[str] = None

@dataclass
class Product:
    image_url: str
    score: float
    color: str
    depth: str
    height: str
    length: str
    description: str
    features: List[str]
    functionality: str
    style: List[str]
    name: str
    price: str
    type: str




@dataclass
class SearchResponse:
    message: str
    action: str
    products: List[Product]

# Routes

@get("/health", sync_to_thread=False)
def health() -> dict[str, Any]:
    """Route Handler that outputs hello world."""
    return {"hello": "world"}

@post("/search", sync_to_thread=False)
def search(data: SearchRequest) -> SearchResponse:
    print(client)
    print(data.query)
    products: List[Product] = weaviate_search(data.query, client, keys)
    message = "Here are the products that matches your query"
    action = "show_product"
    return SearchResponse(message, action, products)

app = Litestar(openapi_config=openapi.OpenAPIConfig(title="Rumahku", version="1.0.0", create_examples=True), route_handlers=[health, search])
