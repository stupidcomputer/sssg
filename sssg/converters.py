from sssg.document import DocumentType, Document
from markdown import Markdown
from jinja2 import Environment
from typing import Self
import os

class Converter:
    document: Document
    jinja_environment: Environment
    def __init__(self: Self, document: Document, environment: Environment):
        self.document = document
        self.jinja_environment = environment

    def realize_to_output(self: Self):
        # should be subclassed
        pass

class ConverterConfiguration:
    converters = dict[DocumentType, Converter]
    jinja_environment: Environment

    def __init__(self: Self, converters: dict[DocumentType, Converter], environment: Environment):
        self.converters = converters
        self.jinja_environment = environment

    def convert(self: Self, document: Document):
        self.converters[document.doc_type](document, self.jinja_environment).realize_to_output()

class BasicConverter(Converter):
    def realize_to_output(self: Self):
        with open(self.document.file_path, "r") as file:
            contents = file.read()
            md = Markdown(extensions=["meta", "fenced_code", "tables"])
            html = md.convert(contents)

        template = self.jinja_environment.get_template("article.html")

        with open(self.document.result_path, "w") as file:
            file.write(template.render(md_html=html))

BlogConverter = BasicConverter

class BinaryConverter(Converter):
    def realize_to_output(self: Self):
        with open(self.document.file_path, "rb") as origin:
            with open(self.document.result_path, "wb") as target:
                target.write(origin.read())

class SensibleConverterConfiguration(ConverterConfiguration):
    def __init__(self: Self, environment: Environment):
        self.jinja_environment = environment
        self.converters = {
            DocumentType.generic_markdown: BasicConverter,
            DocumentType.blog: BlogConverter,
            DocumentType.binary: BinaryConverter,
        }
