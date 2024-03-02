import json
from openai import OpenAI

openai_api_key = "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"
upstage_api_key = "ZoRB5ymHqf1a9jd6LPwx3wVj1A4DWTzJ"


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


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ]
    # verbose input
    for message in messages:
        print(f"[{message['role']}] {message['content']}")

    chatgpt = ChatGPT(openai_api_key)
    chatgpt_resp = chatgpt.request(messages)

    solar = Solar(upstage_api_key)
    solar_resp = solar.request(messages)

    # verbose output
    print("=" * 30, "Response", "=" * 30)
    print(f"[ChatGPT] {chatgpt_resp}")
    print(f"[Solar] {solar_resp}")
