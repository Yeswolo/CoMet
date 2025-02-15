# utils.py

from openai import OpenAI
import random
import itertools
import time
import json
import http.client
from datetime import datetime
import csv
from typing import List, Dict, Optional
import os
import config
import requests






LOG_FILE_PATH = config.API_logfir
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)



def call_api(
        input_messages: Optional[List[Dict]] = None,
        temperature: float = 0.6,
        max_tokens: int = 1024,
        n: int = 1,
        stop: Optional[List[str]] = None,
        seed: Optional[int] = None,
        model = 'gpt-3.5'
):
    if model == "gpt-3.5" or model == "gpt-3.5-turbo" or model == "gpt-4" or model == "gpt-4o" or model == "o1-preview":
        return call_gpt_api(input_messages = input_messages, temperature = temperature, max_tokens=max_tokens, model = model)
    else:
        # write by yourself
        return



def call_gpt_api(input_messages, temperature, max_tokens, model):

    client = OpenAI(
        base_url=config.URL,
        api_key=config.OPENAI_API_KEY
    )
    completion = client.chat.completions.create(
    model=model,
    messages=input_messages,
    temperature=temperature,
    max_tokens=max_tokens,
    )
    return completion.choices[0].message.content


def get_word_config(num):
    WORD_LIST = config.WIU_word_list
    return WORD_LIST[num]


