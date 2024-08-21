import json, time

from log import *
from openai import OpenAI 

import prompt


messages = []
client = None

used_tokens = 0

PRICE_PER_M_TOK = 0.15
PRICE_PER_TOK = PRICE_PER_M_TOK / 1000000.0

MODELNAME="gpt-4o-mini"
TEMP=0.7
MAX_TOKENS=512

def call_ai(msgs, perf=True):
    api_time = Profiler("API Call")
    resp = client.chat.completions.create(
        model=MODELNAME,
        messages=msgs,
        temperature=TEMP,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        tools=prompt.tools,
        response_format=prompt.response_format
    )
    global used_tokens
    used_tokens += resp.usage.total_tokens

    if perf:
        api_time.end()

    return resp




def remove_old_images(debug = True):
    print(f"{Back.RED} REMOVE OLD IMAGES {Style.RESET_ALL}")
    global messages
    removed = 0
    chars = 0
    for message in messages:
        #print(repr(chat_message))
       # message = chat_message.content
        if message['role'] != 'user': continue
        if message == messages[-1]: continue

        for content in message['content']:
            if content['type'] == 'text' and debug:
                print("     >looking at message: ", content['text'])
            if content['type'] != 'image_url': continue
            chars += len(content["image_url"]['url'])
            message['content'].remove(content)
            removed += 1
            if debug:
                print(Fore.RED + "     >removed image for message" + Style.RESET_ALL)

    print(f"{Back.RED} Removed {removed} images from history to save {chars} chars / ~{chars // 4} tok {Style.RESET_ALL}")

def create_function_result(result, call_id):
    global messages
    messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                        "tool_call_id" : call_id
                    })
    return result