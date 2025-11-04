from pydantic import BaseModel


class ArticlesModel(BaseModel):
    """Model for representing article information."""
    title: str
    url: str
    date: str
    description: str
    image_url: str


class ArticlesItems(BaseModel):
    """..."""
    items: list[ArticlesModel]


class PodcastModel(BaseModel):
    """Model for representing podcast episode information."""
    title: str
    url: str
    date: str
    description: str
    image_url: str


class PodcastItems(BaseModel):
    """Model for a list of podcast episodes."""
    items: list[PodcastModel]

