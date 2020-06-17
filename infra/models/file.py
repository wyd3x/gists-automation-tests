from typing import List


class File:
    def __init__(self,
                 size: int = None,
                 filename: str = None,
                 type: str = None,
                 raw_url: str = None,
                 content: str = None,
                 language: str = None,
                 truncated: bool = None, ):
        self.size = size
        self.filename = filename
        self.type = type
        self.raw_url = raw_url
        self.content = content
        self.language = language
        self.truncated = truncated

    @staticmethod
    def from_github(data: dict) -> List['File']:
        files = []

        for file in data:
            files.append(File.from_github_single_file(data[file]))

        return files

    @staticmethod
    def from_github_single_file(data: dict) -> 'File':
        return File(filename=data.get('filename'),
                    type=data.get('type'),
                    language=data.get('language'),
                    raw_url=data.get('raw_url'),
                    size=data.get('size'),
                    truncated=data.get('truncated'),
                    content=data.get('content'), )

    def to_json(self) -> dict:
        object_dict = {
            'size': self.size,
            'type': self.type,
            'content': self.content,
            'raw_url': self.raw_url,
            'language': self.language,
            'filename': self.filename,
            'truncated': self.truncated,
        }

        # remove `None` values from the dict
        object_dict = {k: v for k, v in object_dict.items() if v is not None}

        return object_dict

    def __eq__(self, other: 'File') -> bool:
        return self.filename == other.filename \
            and self.truncated == other.truncated \
            and self.language == other.language \
            and self.raw_url == other.raw_url \
            and self.content == other.content \
            and self.type == other.type
