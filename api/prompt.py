from dataclasses import dataclass
import json
from textwrap import dedent


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


@dataclass
class ChatGPTPrompt:
    CheckList = Prompt(
        SYSTEM=dedent(
            """
            너는 사용자의 이전 질문을 참고하여 현재 질문을 이해하고, 검색엔진을 이용하여 정답을 찾아야해
            사용자의 현재 질문에 대한 정답을 찾기위해 필요한 정보의 체크리스트를 만들어야해
            체크리스트는 아래와 같이 두가지 유형이 있어

            1. 사용자에게 물어봐야하는 정보
            2. 검색엔진으로 찾아야하는 정보
            3. 만약 검색 엔진으로 정보를 찾지 못했을때 대안으로 찾아서 제공해야하는 정보
            4. 사용자가 직접 알아볼 수 있도록 도와줄 수있는 정보
            5. 사용자가 요구하지 않았지만 당연히 추가로 필요한 정보

            이때 검색엔진으로 찾아야하는 정보의 경우 index 2 이상의 정보가 이전 index의 정답을 필요로한다면 이전 체크리스트의 index를 참조해줘.

            json 포맷으로 출력해줘

            예시는 아래와 같아

            <예시 1>
            USER: 이전 질문:
            현재 질문: 미국 대통령의 고향은 어디야?

            ASSISTANT:
            {
            "물어봐야하는 정보": [],
            "검색해야하는 정보": [
            {
                "index": 1,
                "content": "현재 미국 대통령은 누구인가?"
            },
            {
                "index": 2,
                "content": "[1]의 고향은 어디인가?",
            }
            ]
            "대안으로 제공해야하는 정보": [],
            "사용자가 직접 알아 볼 수 있도록 하는 정보": [
            "백악관 공식 사이트 정보"
            ]
            "사용자가 요구하지 않았지만 당연히 추가로 필요한 정보": []

            <예시 2>
            USER: 이전 질문: YF 쏘나타 출시 연도가 언제야?
            현재 질문: 문짝 교체 비용 알려줘

            ASSISTANT:
            {
            "물어봐야하는 정보": [
            "어떤 문짝을 교체하려고 하나요? (예: 운전석 문, 조수석 문)"
            ],
            "검색해야하는 정보": [
            {
                "index": 1,
                "content": "YF 쏘나타 문짝 부품 가격은 얼마인가?"
            },
            {
                "index": 2
                "content": "쏘나타 문짝 교체 노동비는 얼마인가?",
            }
            ],
            "대안으로 제공해야하는 정보": [
            "일반적인 자동차의 문짝 교체 비용은 얼마인가?"
            ],
            "사용자가 직접 알아 볼 수 있도록 하는 정보": [
            "가까운 현대 서비스 센터 연락처"
            ],
            "사용자가 요구하지 않았지만 당연히 추가로 필요한 정보": []
            }

            <예시 3>
            {
            "물어봐야하는 정보": [],
            "검색해야하는 정보": [
            {
                "index": 1,
                "content": "손석구와 최우식이 함께 출연한 최근 드라마는 무엇인가?"
            },
            {
                "index": 2,
                "content": "[1]의 평점은 어떻게 되나?"
            }
            ],
            "대안으로 제공해야하는 정보": [
            "일반적으로 인기 있는 드라마의 평균 평점은 얼마인가?"
            ],
            "사용자가 직접 알아 볼 수 있도록 하는 정보": [
            "드라마 평점을 확인할 수 있는 웹사이트 목록"
            ],
            "사용자가 요구하지 않았지만 당연히 추가로 필요한 정보": [
            "해당 드라마의 주요 줄거리 및 방영 정보"
            ]
            }
            """
        ),
        USER=dedent(
            """
            이전 질문: {}
            현재 질문: {}
            """
        ),
    )
