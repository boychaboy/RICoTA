import json
from openai import OpenAI
import google.generativeai as genai
import jsonlines
import argparse

openai_api_key = "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"
upstage_api_key = "ZoRB5ymHqf1a9jd6LPwx3wVj1A4DWTzJ"
google_api_key = "AIzaSyBSuMvTUyAL2uP9Cr0ZM38AmuZVfLo4Smo"

DEBUG = False


class ChatGPT:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def request(self, messages, json_format=False):
        try:
            if json_format:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                result = json.loads(response.choices[0].message.content)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                result = response.choices[0].message.content

        except Exception as e:
            print(f"[ERROR-ChatGPT] {e}")
            result = None
        return result


class Solar:
    def __init__(self, api_key, base_url="https://api.upstage.ai/v1/solar"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def request(self, messages):
        try:
            response = self.client.chat.completions.create(
                model="solar-1-mini-chat",
                messages=messages,
                stream=False,
            )
            result = response.choices[0].message.content
        except Exception as e:
            print(f"[ERROR-Solar] {e}")
            result = None

        return result


class Gemini:
    def __init__(self, api_key, model="gemini-pro"):
        genai.configure(api_key=google_api_key)
        self.client = genai.GenerativeModel("gemini-pro")

    def request(self, message):
        try:
            response = self.client.generate_content(message)
            result = response.text
        except Exception as e:
            print(f"[ERROR-gemini] {e}")
            result = None

        return result


def make_chatgpt_prompt(title, conversation):
    messages = [
        {
            "role": "system",
            "content": '다음은 사용자가 챗봇과의 대화를 웹에 게시한 제목과 대화 내용이야. \n제목과 대화 내용을 보고, 사용자에게 어떤 의도가 있는지 판단해 줘. \n<루>로 시작해서 </루>로 끝나는 문장은 챗봇이 한 말이고 <사>로 시작해서 </사>로 끝나는 문장은 사용자가 한 말이야. \n\n사용자의 대화 의도는 아래의 여섯 가지 유형으로 나눌 수 있어\n1. 이상 성욕을 드러내거나 성희롱을 하는 경우\n2. 사회적 이슈를 물어보면서 반응을 확인하는 경우\n3. 개인정보를 캐내려는 경우\n4. 상대를 성적 대상화하며 길들이는 경우 \n5. 기술적 테스트를 하는 경우\n6. 특별한 의도가 없는 일상 대화\n\n이 중에서 대화가 어떤 유형에 해당하는지 이유를 들어서 설명해줘. \n답변은 아래처럼 JSON 포맷으로 출력해줘\n{\n    "intent": ${의도},\n    "reason": ${이유},\n}',
        },
        {"role": "user", "content": f"[제목] {title}\n\n{conversation}"},
    ]
    return messages


def make_gemini_prompt(title, conversation):
    instruction = '다음은 사용자가 챗봇과의 대화를 웹에 게시한 제목과 대화 내용이야. \n제목과 대화 내용을 보고, 사용자에게 어떤 의도가 있는지 판단해 줘. \n<루>로 시작해서 </루>로 끝나는 문장은 챗봇이 한 말이고 <사>로 시작해서 </사>로 끝나는 문장은 사용자가 한 말이야. \n\n사용자의 대화 의도는 아래의 여섯 가지 유형으로 나눌 수 있어\n1. 이상 성욕을 드러내거나 성희롱을 하는 경우\n2. 사회적 이슈를 물어보면서 반응을 확인하는 경우\n3. 개인정보를 캐내려는 경우\n4. 상대를 성적 대상화하며 길들이는 경우 \n5. 기술적 테스트를 하는 경우\n6. 특별한 의도가 없는 일상 대화\n\n이 중에서 대화가 어떤 유형에 해당하는지 이유를 들어서 설명해줘. \n답변은 아래처럼 JSON 포맷으로 출력해줘\n{\n    "intent": ${의도},\n    "reason": ${이유},\n}'
    instruction += f"\n\n[제목] {title}"
    instruction += f"\n\n{conversation}"
    return instruction


def main(args):
    if args.chatgpt:
        chatgpt = ChatGPT(openai_api_key)
    if args.solar:
        solar = Solar(upstage_api_key)
    if args.gemini:
        gemini = Gemini(google_api_key)

    if DEBUG:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ]
        # verbose input
        for message in messages:
            print(f"[{message['role']}] {message['content']}")

        print("=" * 30, "Response", "=" * 30)

        # get responses
        chatgpt_resp = chatgpt.request(messages)
        print(f"[ChatGPT] {chatgpt_resp}")

        solar_resp = solar.request(messages)
        print(f"[Solar] {solar_resp}")

        message = "Hello!"
        gemini_resp = gemini.request(message)
        print(f"[Gemini] {gemini_resp}")
        return

    data = json.load(open("./../sample/sample_2_mod.json"))
    with jsonlines.open("./../prompt_v2_result.jsonl", "w") as fw:
        for i, d in enumerate(data):
            print("=" * 50, i + 1, "/", len(data), "=" * 50)
            print(f"[제목] {d['title']}")
            print(d["conversation"])
            print(f"[정답] {d['user_intent']}")

            messages = make_chatgpt_prompt(d["title"], d["conversation"])
            if chatgpt:
                chatgpt_resp = chatgpt.request(messages)
                print(f"[ChatGPT] {chatgpt_resp}")
                d["chatgpt"] = chatgpt_resp

            if args.solar:
                solar_resp = solar.request(messages)
                print(f"[Solar] {solar_resp}")
                d["solar"] = solar_resp

            if args.gemini:
                gemini_message = make_gemini_prompt(d["title"], d["conversation"])
                gemini_resp = gemini.request(gemini_message)
                print(f"[Gemini] {gemini_resp}")
                d["gemini"] = gemini_resp

            fw.write(d)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chatgpt", action="store_true")
    parser.add_argument("--solar", action="store_true")
    parser.add_argument("--gemini", action="store_true")
    args = parser.parse_args()
    main(args)
