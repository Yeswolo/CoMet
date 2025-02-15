import os
import config
import time
import datetime

from gamelist.Undercover.game import Game
from utils import get_word_config


def main():
        logdir = config.WIU_logdir
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        civilian_win_round = 0
        undercover_win_round = 0
        count = 0
        turn = 1 



        for i in range(config.run_turns):

            if config.WIU_self_depend_word == 1:
                civilian_word = config.WIU_c_word
                undercover_word = config.WIU_u_word
            elif config.WIU_self_depend_word == 2:
                civilian_word, undercover_word = get_word_config(i)

            game = Game(civ_word=civilian_word, und_word=undercover_word, civ_count=config.WIU_c_num, und_count=config.WIU_u_num, logdir=logdir)

            result = game.start()
            if result == True:
                print("civilian wins!")
                civilian_win_round += 1
            else :
                print("Undercover wins!")
                undercover_win_round += 1
            count += 1 



        print("game round:", count)
        print("civilian wins:", civilian_win_round)
        print("Undercover wins:", undercover_win_round)










if __name__ == "__main__":
    main()
