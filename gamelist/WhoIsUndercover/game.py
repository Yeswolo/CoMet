import os
import json
import time
import config
import datetime
import csv
import random
from gamelist.WhoIsUndercover.player import Player
from utils import call_api

class Game:

    def __init__(self, civ_count, und_count, civ_word, und_word, logdir):
        self.civ_word = civ_word
        self.und_word = und_word
        self.civ_count = civ_count
        self.und_count = und_count
        self.turn = 1
        self.players = {}
        self.player_alive = set()
        self.logdir = logdir
        self.experience_pool_file = "data/WhoIsUndercover/experience_pool_ingame_generate.json"
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        self.dialogue_history = [f"Player {i+1}:\n This player has not said anything yet. You should wait for them to speak before considering them.\n " for i in range(civ_count + und_count)]  # 初始化为字符串
        # self.dialogue_history = [["This player has not said anything yet."] for _ in range(civ_count + und_count)]      #成组储存玩家的历史发言
        self.game_history = ""
        self.vote_history = ""
        self.player_csv = [None] * (civ_count + und_count)
        self.initialize_csv()
        self._initialize_players()
        



    def _initialize_players(self):

        role_list = ['civilian'] * self.civ_count + ['undercover'] * self.und_count
        

        random.shuffle(role_list)

        # role_list = ['civilian','civilian','civilian','civilian','undercover', 'undercover']


        player_id = 1
        for role in role_list:
            # assign role
            if role == 'civilian':
                word = self.civ_word
                other_word = self.und_word
                mode = config.WIU_c_mode 
            elif role == 'undercover':
                word = self.und_word
                other_word = self.civ_word
                mode = config.WIU_u_mode
            
            # initialize players
            self.players[player_id] = Player(role, word, mode, player_id, other_word=other_word, csv_name = self.player_csv[player_id - 1])
            self.player_alive.add(player_id)
            player_id += 1



    def start(self) -> bool:

        # game start!

        while True:
            round_dialogue = ""
            round_votes = {}
            turn_vote_history = ""
            self.game_history += f"**round {self.turn}**\n"
            action = 'speak'
            # record the game state
            self.log_game_state('', 'host', '', '', '**speak phase!**')
            self.game_history += f"speaking content:\n"

            player_alive_list = list(self.player_alive)
            random.shuffle(player_alive_list)

            for player_id in player_alive_list:
                dialogue = self.players[player_id].speak(game_history=self.game_history
                                                                , dialogue_history=self.dialogue_history
                                                                , round_dialogue=round_dialogue
                                                                , vote_history = self.vote_history
                                                                )  

                round_dialogue += f"Player{player_id}: {dialogue} \n"
                # self.dialogue_history[player_id - 1].append((self.turn, dialogue))
                if self.dialogue_history[player_id - 1] == f"Player {player_id}:\n This player has not said anything yet. You should wait for them to speak before considering them.\n ":
                    self.dialogue_history[player_id - 1] = f"Player{player_id}:\n Round 1: {dialogue};  "
                else:
                    self.dialogue_history[player_id - 1] += f"Round {self.turn}: {dialogue};  "

                
                self.game_history += f"Player{player_id}: {dialogue}\n"
                self.log_game_state(self.turn, player_id, self.players[player_id].word, action, dialogue)

            # Record all the round dialogue

            action = 'vote'
            self.log_game_state('', 'host', '', '', '**vote phase!**')
            self.game_history += f"voting result:\n"
            vote_ = ""
            # Vote
            for player_id in self.player_alive.copy():
                vote_result = self.players[player_id].vote( game_history = self.game_history
                                                            ,   dialogue_history=self.dialogue_history
                                                            ,   round_dialogue=round_dialogue
                                                            ,   alive = self.player_alive
                                                            ,   vote_history = self.vote_history
                                                            )  
                if vote_result in round_votes:
                    round_votes[vote_result] += 1
                else:
                    round_votes[vote_result] = 1

                vote_ += f"Round {self.turn}: Player{player_id} has voted player{vote_result}.\n"
                self.log_game_state(self.turn, player_id, self.players[player_id].word, action, vote_result)
                turn_vote_history += f"in round {self.turn}, {player_id} voted {vote_result}\n"

            self.game_history += vote_
            self.vote_history += turn_vote_history

            # Eliminated the player with the most votes
            eliminated_player = self.find_most_voted_player(round_votes)
            if eliminated_player is not None:
                remove = int(eliminated_player)
                self.player_alive.remove(remove)
                host_elimi = f"**The player {eliminated_player} was eliminated!**"
                self.game_history += f"{host_elimi}\n"
                alive_players = ', '.join(map(str, self.player_alive))
                host_alive = f"**Still alive players: {alive_players}**"

                self.log_game_state(self.turn, 'host', '', '', host_elimi)
                self.log_game_state(self.turn, 'host', '', '', host_alive)
            if config.WIU_self_evolving:
                self.experience_improvement()
            if self.turn == 10:
                return True
            
            if self.check_game_end() == 1:
                self.log_game_state('', 'host', '', '', '**Civilians win!**')
                result = f'Civ{config.WIU_c_mode}(winner)_VS_Und{config.WIU_u_mode}'
                new_filename = f'{result}.csv'
                new_csv_filename = os.path.join(self.folder_path, new_filename)
                os.rename(self.csv_filename, new_csv_filename)
                
                return True
            
            elif self.check_game_end() == -1:
                self.log_game_state('', 'host', '', '', '**Undercovers win!**')
                result = f'Civ{config.WIU_c_mode}_VS_Und{config.WIU_u_mode}(winner)'
                new_filename = f'{result}.csv'
                new_csv_filename = os.path.join(self.folder_path, new_filename)
                os.rename(self.csv_filename, new_csv_filename)

                return False
            else:  
                self.round_dialogue = []
                self.turn += 1
                continue


    def find_most_voted_player(self, votes: dict):

        if not votes:
            return None 

        max_votes = max(votes.values())
        if max_votes == 0:
            return None

        most_voted_players = [player_id for player_id, vote in votes.items() if vote == max_votes]
        if len(most_voted_players) > 1:
            return None 
        else:
            return most_voted_players[0]

    def check_game_end(self) -> int:

        remaining_civilian = sum(1 for player_id in self.player_alive if self.is_civilian(player_id))
        remaining_undercovers = sum(1 for player_id in self.player_alive if self.is_undercover(player_id))

        if remaining_civilian == 1 and remaining_undercovers > 0:
            return -1  
        elif remaining_undercovers == 0:
            return 1  
        return 0

    def is_civilian(self, player_id: int) -> bool:
        return self.players[player_id].role == 'civilian'

    def is_undercover(self, player_id: int) -> bool:
        return self.players[player_id].role == 'undercover'





    def initialize_csv(self):
        time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'game_history_{time_stamp}.csv'
        folder_name = f'game_history_{time_stamp}'
        self.folder_path = os.path.join(self.logdir, folder_name)
        os.makedirs(self.folder_path, exist_ok=True)

        filename = 'game_history.csv'
        self.csv_filename = os.path.join(self.folder_path, filename)
        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['round', 'word', 'player_id', 'action', 'details'])

        for i in range(self.civ_count + self.und_count):
            filename = f'player_{i+1}.csv'
            self.player_csv[i] = os.path.join(self.folder_path, filename)
            with open(self.player_csv[i], mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['content'])


    def log_game_state(self, round = '', player_id = '',word = '', action = '', details = ''):
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([round, word, player_id, action, details])







