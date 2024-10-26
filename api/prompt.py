from dataclasses import dataclass
import json


@dataclass
class BaseObject:
    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            raise KeyError(item)

    def to_dict(self):
        return vars(self)

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_text(self):
        return ",".join(
            [
                f"{k}: {v}"
                for k, v in self.to_dict().items()
                if (isinstance(v, str) or isinstance(v, list) or isinstance(v, dict))
                and len(v) != 0
            ]
        )

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Prompt:
    SYSTEM: str = ""
    ASSISTANT: str = ""
    USER: str = ""
