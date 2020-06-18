from datetime import datetime
from typing import List

from infra.models.file import File


class Gist:
    def __init__(self,
                 public: bool,
                 description: str,
                 files: List[File],
                 id: str = None,
                 url: str = None,
                 created_at: datetime = None,
                 updated_at: datetime = None,):
        self.id = id
        self.url = url
        self.public = public
        self.created_at = created_at
        self.description = description
        self.files = files
        self.updated_at = updated_at

    def to_github(self):
        files_list = {}
        for file in self.files:
            files_list[file.filename] = file.to_json()

        object_dict = {
            'id': self.id,
            'url': self.url,
            'files': files_list,
            'public': self.public,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'description': self.description,
        }

        # remove `None` values from the dict
        object_dict = {k: v for k, v in object_dict.items() if v is not None}

        return object_dict

    @staticmethod
    def from_github(data: dict) -> 'Gist':
        list_files = File.from_github(data.get('files'))
        files = []

        for file in list_files:
            files.append(file)

        return Gist(id=data.get('id'),
                    url=data.get('url'),
                    files=files,
                    public=data.get('public'),
                    created_at=data.get('created_at'),
                    description=data.get('description'),
                    updated_at=data.get('updated_at',))

    def __eq__(self, other: 'Gist') -> bool:
        # comparision updated_at removed because github sometimes change it after creating for some reason
        return self.id == other.id \
            and self.files == other.files \
            and self.description == other.description \
            and self.public == other.public \
            and self.url == other.url \
            and self.created_at == other.created_at
