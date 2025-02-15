
import os

OPENAI_API_KEY = ""
URL = ""
# LLM parameters
temperature = 0.6
max_tokens=2048

# game

run_turns = 1
API_logfir = os.path.join(os.getcwd(), 'logs', 'api_logs.csv')


WIU_self_depend_word = 1       # 0:random  1: depend 1 pair   2: depend list pair
WIU_c_word = "goose"
WIU_u_word = "duck"
restart = 1

WIU_word_list = []


WIU_c_num = 3
WIU_u_num = 2


WIU_c_mode = 1
WIU_u_mode = 1
"""
player mode:
0:CoT
1:ComMet
"""


WIU_c_model = "gpt-3.5-turbo"
WIU_u_model = "gpt-3.5-turbo"



WIU_logdir = os.path.join(os.getcwd(), 'logs')
