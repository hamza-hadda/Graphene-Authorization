# -*- coding: utf-8 -*-
import decimal

import graphene
from django.core.files.images import ImageFile
from django.utils.translation import ugettext_lazy as _


class Error(graphene.ObjectType):
    field = graphene.String(
        description="""Name of a field that caused the error. A value of
        `null` indicates that the error isn't associated with a particular
        field.""",
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class Decimal(graphene.Float):
    """Custom Decimal implementation.
    Returns Decimal as a float in the API,
    parses float to the Decimal on the way back.
    """

    @staticmethod
    def parse_literal(node):
        try:
            return decimal.Decimal(node.value)
        except decimal.DecimalException:
            return None

    @staticmethod
    def parse_value(value):
        try:
            # Converting the float to str before parsing it to Decimal is
            # necessary to keep the decimal places as typed
            value = str(value)
            return decimal.Decimal(value)
        except decimal.DecimalException:
            return None


class Upload(graphene.types.Scalar):
    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value


class ImageUpload(Upload):
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "bmp"]
    IMAGE_MAX_SIZE = 29360128  # 28MB

    @classmethod
    def parse_value(cls, value):
        if value.name.split(".")[-1].lower() not in cls.ALLOWED_EXTENSIONS:
            raise Error(_("Wrong image extension"))

        if value.size > cls.IMAGE_MAX_SIZE:
            raise Error(_("Maximum file size exceeded"))

        return ImageFile(value)


class Image(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the image.")

    class Meta:
        description = "Represents an image."

    def resolve_url(self, info):
        return self.url


class File(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the file.")

    class Meta:
        description = "Represents an file."

    def resolve_url(self, info):
        return self.url
