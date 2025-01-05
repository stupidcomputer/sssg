import markdown

from dataclasses import dataclass
from typing import Self
from enum import auto, Enum

class DocumentType(Enum):
    generic_markdown = auto()
    blog = auto()
    binary = auto()

@dataclass
class Document:
    doc_type: DocumentType
    file_path: str

    @property
    def result_path(self: Self) -> str:
        # change the 'src' to 'output' -- loop backwards and replace
        splitted = self.file_path.split('/')
        found_src = False
        # can't use reversed(enumerate(...)) -- so use a workaround
        for index, value in sorted(enumerate(splitted), reverse=True):
            if value == "src":
                splitted[index] = "output"
                found_src = True
                break

        if not found_src:
            raise ValueError("Your source directory must be named 'src/'")

        file_path = '/'.join(splitted)

        if self.doc_type == DocumentType.binary:
            return file_path
        elif (
            self.doc_type == DocumentType.generic_markdown or
            self.doc_type == DocumentType.blog
        ):
            splitted = file_path.split('.')
            return '.'.join(splitted[:-1] + ["html"])

    @classmethod
    def from_filepath(cls: Self, file_path: str) -> Self:
        # this is stupid, but try to detect DocumentType from the file
        # extension, and then disambiguate into the DocumentType.blog and
        # DocumentType.generic_markdown cases as needed

        is_markdown = file_path.endswith(".md")
        if is_markdown:
            with open(file_path, "r") as file:
                contents = file.read()
                md = markdown.Markdown(extensions=["meta"])
                md.convert(contents)

                try:
                    is_blog = md.Meta["blog"] == "yes"
                except KeyError:
                    is_blog = False

            if is_blog:
                doc_type = DocumentType.blog
            else:
                doc_type = DocumentType.generic_markdown
        else:
            doc_type = DocumentType.binary

        return cls(
                    doc_type=doc_type,
                    file_path=file_path
        )
