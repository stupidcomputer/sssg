import os
from jinja2 import Environment, FileSystemLoader
from typing import Self
from pathlib import Path

from sssg.document import Document, DocumentType
from sssg.converters import SensibleConverterConfiguration

def dir_walk(dirpath: str) -> list[str]:
    filepaths: list[str] = []
    for root, dirs, files in os.walk(dirpath):
        for filename in files:
            complete = os.path.join(root, filename)
            print(complete)
            filepaths.append(complete)
        for dirname in dirs:
            complete = os.path.join(root, dirname)
            print(complete)
            filepaths += dir_walk(complete)

    filepaths = [path for path in filepaths if '~' not in path]
    print(filepaths)
    return filepaths

class Site:
    dir_path: str
    documents: list[Document]
    jinja_environment: Environment

    def __init__(
        self: Self,
        dir_path: str,
        documents: list[Document],
    ):
        self.dir_path = dir_path
        self.documents = documents
        self.jinja_environment = Environment(
            loader=FileSystemLoader(
                os.path.join(self.dir_path, "templates")
            )
        )

    def _ensure_output_directories(self: Self):
        output_dirs = [os.path.dirname(doc.result_path) for doc in self.documents]
        # remove duplicates
        output_dirs = list(set(output_dirs))

        for path in output_dirs:
            Path(path).mkdir(parents=True, exist_ok=True)

    def rebuild(
        self: Self,
    ):
        self._ensure_output_directories()
        config = SensibleConverterConfiguration(self.jinja_environment)
        for document in self.documents:
            config.convert(document)

    @classmethod
    def from_directory(cls: Self, dir_path: str):
        src_dir = os.path.join(dir_path, "src")
        paths = dir_walk(src_dir)
        paths = list(set(paths))
        documents = [
            Document.from_filepath(path)
            for path in paths
        ]

        return cls(
            dir_path=dir_path,
            documents=documents
        )
