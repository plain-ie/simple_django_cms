from typing import List, Optional, Union

from django.shortcuts import reverse

from pydantic import BaseModel

from ..serializers import ItemSerializer


class ImageTranslatableContentSerializer(BaseModel):

    language: str
    title: str
    description: Union[str, None]
    file_url: Union[str, None]


class ImageDataSerializer(BaseModel):

    translatable_contents: Optional[List[ImageTranslatableContentSerializer]]


class ImageSerializer(ItemSerializer):

    data: ImageDataSerializer
