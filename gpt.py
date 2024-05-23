'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-08 19:05:49
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-09 03:18:50
FilePath: \毕设\code\gpt.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from openai import OpenAI
import httpx

# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  base_url="https://api.xiaoai.plus/v1", 
  api_key="sk-K7Nc6eaR37YZXGOyAd7b213d18A04f58A12006AfE0Db12D8",
  http_client=httpx.Client(
    base_url="https://api.xiaoai.plus/v1",
    follow_redirects=True,
  ),
)

def get_response(model_id, message):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.0
    )
    return response

if __name__ == "__main__":
    message = "鲁迅和周树人是什么关系"
    ans = get_response("gpt-4", messages=message)