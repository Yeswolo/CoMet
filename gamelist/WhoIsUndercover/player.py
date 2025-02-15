from gamelist.WhoIsUndercover.prompt import base_prompt
from gamelist.WhoIsUndercover.prompt import ComMet as FISA
from utils import call_api
import config
import re
import csv
import os
import json
import random


class Player:

    def __init__(
            self, 
            role: str, 
            word: str, 
            mode, 
            id,
            other_word,
            csv_name
    ):
        self.role = role
        self.word = word
        self.other_word = other_word
        self.mode = mode
        if self.role == 'civilian':
            self.model = config.WIU_c_model
        else:
            self.model = config.WIU_u_model
        self.id = id

        self.csv_name = csv_name

        self.categorization = ""
        self.feature = "Right now, the game has just started, you can only guess another word by the original clue:'The two words are similar or related, such as 'pencil' and 'pen', 'apple' and 'orange'.'."
        self.identity = "Right now, the game has just started, all players are still undetermined."
        self.strategy = "Right now, the game has just started, I don't have any strategy."
        self.reaction = ""
        self.metaphor = ""
        self.method = ""
        self.refer_experience_ids = []
        self.explaination = ""




    def log_player_action(self, content):

        with open(self.csv_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([content])


    def speak(self, *args, game_history=None, dialogue_history = None, round_dialogue = None, vote_history, **kwargs) -> str:
        if self.mode == 0:
            return self.player_speaking_cot(self.role, self.word, round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history)
        elif self.mode == 1:
            return self.player_speaking_ComMet(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history)

    def vote(self, *args, game_history=None, dialogue_history = None, round_dialogue = None,alive = None,vote_history , **kwargs):
        if self.mode == 0:
            return self.player_voting_cot(game_history=game_history, alive = alive)
        elif self.mode == 1:
            return self.player_voting_ComMet(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history, alive=alive)

    def player_speaking_cot(self, *args, dialogue_history, round_dialogue, game_history, **kwargs):
        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.analyse(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                game_history = game_history
            )}
        ])
        self.strategy = ret1
        self.log_player_action("\n\n\n=========================================   ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)

        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.speak(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue_history, analysis = self.strategy
            )}
        ])
        ret = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                            Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.
            
                                            sample to change the subject:
                                            text:"Pencil is a tool."
                                            output:It is a tool.
            
                                            text:"both two words can be used for writing."
                                            output:it can be used for writing.
            
                                            text:"a common feature is that slender."
                                            output:this thing is slender.
            """},
            {'role': 'user', 'content': ret2}
        ])
        self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
        self.log_player_action(ret2)
        return ret


    def player_voting_cot(self, *args, game_history, alive, **kwargs ):

        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.analyse(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                game_history = game_history
            )}
        ])
        self.strategy = ret1
        self.log_player_action("\n\n\n=========================================   ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)

        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                analysis = self.strategy, alive = alive
            )}
        ])
        self.log_player_action("\n\n\n=========================================   VOTING   =========================================\n\n\n")
        self.log_player_action(ret2)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret2}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int = vot
        return vot_int

    




    def player_speaking_naive(self, dialogue_history, vote_history):
        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.naive_speak(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id, dialogue, vote_history
            )}
        ])
        self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
        self.log_player_action(ret1)
        ret = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                            Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.
            
                                            sample to change the subject:
                                            text:"Pencil is a tool."
                                            output:It is a tool.
            
                                            text:"both two words can be used for writing."
                                            output:it can be used for writing.
            
                                            text:"a common feature is that slender."
                                            output:this thing is slender.
            """},
            {'role': 'user', 'content': ret1}
        ])
        return ret


    def player_voting_naive(self, dialogue_history, vote_history, alive):
        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.naive_vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,dialogue, vote_history, alive
            )}
        ])
        self.log_player_action("\n\n\n=========================================   ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret1}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int1 = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int1 = vot
        if vot_int1 not in alive:
            vot_int = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': f"{base_prompt.system(self.word, self.id)}\n\nNow you have already decided the final vote target: player {vot_int1}, but you made a mistake that you want to vote a player who was already eliminated. Now, please choose another player who is still alive."},
            {'role': 'user', 'content': ret1}
        ])
        else:
            vot_int = vot_int1
        return vot_int




    def player_speaking_ComMet(self, round_dialogue, game_history, dialogue_history, vote_history):

        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.feature(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, vote_history = vote_history,
                feature = self.feature
            )}
        ])
        ret1_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. the features of the other word mentioned in the input 
            2. all the guesses for the other word; 
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret1 }
        ])
        self.feature = ret1_
        self.log_player_action("\n\n\n=========================================   FEATURE ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        self.log_player_action("\n\n\nSummarized FEATURE:")
        self.log_player_action(ret1_)



        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.identify(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history= game_history, 
                vote_history = vote_history, feature = self.feature
            )}
        ])
        ret2_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. allocation of all players, which means the situation of assigning players to teams corresponding to two different words. (pending players should not be on these two teams.)
            2. Which camp do the two words correspond to (CIVILIAN or UNDERCOVER);
            - If either of these is not found, provide the related explanation from the text instead. (Don't say 'not found', just output the required content)
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret2 }
        ])
        self.identity = ret2_
        self.log_player_action("\n\n\n=========================================   IDENTITY REASONING   =========================================\n\n\n")
        self.log_player_action(ret2)
        self.log_player_action("\n\n\nSummarized REASONING:")
        self.log_player_action(ret2_)


        ret3 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.strategy(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, 
                vote_history = vote_history, feature = self.feature, identity = self.identity
            )}
        ])
        # ret3_ = call_api(input_messages = [
        #     {'role': 'system', 'content': """
        #         summarize the input content, output: 
        #     1. strategy's action;
        #     2. strategy's reason or purpose;
        #     - If either of these is not found, provide the explanation from the text.
        #     - do not have any additional extensions and additions, and the output should all come from the input text.
        #     """},
        #     {'role': 'user', 'content': ret3 }
        # ])
        self.strategy = ret3
        self.log_player_action("\n\n\n=========================================   STRATEGY   =========================================\n\n\n")
        self.log_player_action(ret3)
        # self.log_player_action("\n\n\nSummarized STRATEGY:")
        # self.log_player_action(ret3_)


        ret4 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.speak(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, 
                vote_history = vote_history, strategy = self.strategy, feature=self.feature, identity=self.identity
            )}
        ])
        ret = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                            Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.
            
                                            sample to change the subject:
                                            text:"Pencil is a tool."
                                            output:It is a tool.
            
                                            text:"both two words can be used for writing."
                                            output:it can be used for writing.
            
                                            text:"a common feature is that slender."
                                            output:this thing is slender.
            """},
            {'role': 'user', 'content': ret4}
        ])
        self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
        self.log_player_action(ret4)
        return ret





    def player_voting_ComMet(self, round_dialogue, game_history, dialogue_history, vote_history, alive):

        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.feature(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, vote_history = vote_history,
                feature = self.feature
            )}
        ])
        ret1_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. the features of the other word mentioned in the input 
            2. all the guesses for the other word; 
            - If either of these is not found, provide the explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret1 }
        ])
        self.feature = ret1_
        self.log_player_action("\n\n\n=========================================   FEATURE ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        self.log_player_action("\n\n\nSummarized FEATURE:")
        self.log_player_action(ret1_)



        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.identify(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history= game_history, 
                vote_history = vote_history, feature = self.feature
            )}
        ])
        ret2_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. allocation of all players, which means assigning players to teams corresponding to two different words. (pending players should not be on two teams.)
            2. camps of all players, which means the judgement about the camps (MAJORITY and MINORITY) corresponding to two words; 
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret2 }
        ])
        self.identity = ret2_
        self.log_player_action("\n\n\n=========================================   IDENTITY REASONING   =========================================\n\n\n")
        self.log_player_action(ret2)
        self.log_player_action("\n\n\nSummarized REASONING:")
        self.log_player_action(ret2_)
        

        alive_players = ",".join("player" + str(number) for number in alive)
        ret3 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue =round_dialogue, game_history = game_history, 
                alive= alive_players, feature= self.feature, identity= self.identity
            )}
        ])
        self.log_player_action("\n\n\n=========================================   VOTE   =========================================\n\n\n")
        self.log_player_action(ret3)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret3}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int = vot
        return vot_int


