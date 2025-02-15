
def system(word, id):
        p = f"""
        You are playing the game 'Who Is Undercover?' like a real human.
        Do not mention that you are an AI or describe your role as an AI.
        Just focus on your actions and decisions as a player in the game.

        """
        return p

def analyse(cnum, unum, word, id, game_history):

        p = f"""
        # the rules of the game:

        "Who is Undercover?" is a social deduction game in which multiple civilian players are mixed with a minority of undercover players. 
        Each player is secretly assigned a word, which is similar to the words of the other civilians but slightly different. 
        Players take turns briefly describing some of the characteristics of their words, but do not directly disclose them, while trying to avoid revealing too much information that may help others guess their identity.
        The goal is for the civilians to identify and eliminate the undercover players, while the undercover players must blend in, mislead the others, and avoid being discovered. 
        The game is divided into two phases: 
        speaking and voting. 
        During the speaking phase, players describe their words, balancing the need to share enough clues with the need to keep their identity hidden. Players are not alowed to talk to others, just describe the words.
        In the voting phase, players analyze previous descriptions, try to identify their teammates, and strategically vote to eliminate players based on incomplete information. 
        If only one civilian remains while there is still an undercover, the undercover team win; otherwise, the civilian team win.\n
        There are {cnum + unum} players in this game, {cnum} of whom are citizens and the other {unum} are undercover agents.
        

        # TASK:
        You should refer to the following steps in order:
        1. Analyze game history and extract valuable information.
        2. Use the extracted valid information to infer the current game situation, your identity situation, and winning goal.
        Note that you do not need to output the content of your speech or voting objectives, nor are you allowed to simulate other players' speeches. All you need to do is analyze the existing information and prepare for future actions.

        # INFORMATION
        You are <player {id}>. the word assigned to you is "{word}".

        game history:
        {game_history}
        """
        return p 
    


def speak(cnum, unum, word, id,  dialogue_history, analysis):
        p = f"""
        # the rules of the game:

        "Who is Undercover?" is a social deduction game in which multiple civilian players are mixed with a minority of undercover players. 
        Each player is secretly assigned a word, which is similar to the words of the other civilians but slightly different. 
        Players take turns briefly describing some of the characteristics of their words, but do not directly disclose them, while trying to avoid revealing too much information that may help others guess their identity.
        The goal is for the civilians to identify and eliminate the undercover players, while the undercover players must blend in, mislead the others, and avoid being discovered. 
        The game is divided into two phases: 
        speaking and voting. 
        During the speaking phase, players describe their words, balancing the need to share enough clues with the need to keep their identity hidden. Players are not alowed to talk to others, just describe the words.
        In the voting phase, players analyze previous descriptions, try to identify their teammates, and strategically vote to eliminate players based on incomplete information. 
        If only one civilian remains while there is still an undercover, the undercover team win; otherwise, the civilian team win.\n
        There are {cnum + unum} players in this game, {cnum} of whom are citizens and the other {unum} are undercover agents.
        

        # Task
        You need to describe a feature of the word as your speech. 
        **Please follow these steps in order**:
        1. Review your analysis, understand the requirements of strategy for your speak action.
        2. Based on the requirements that the features need to meet, list some candidate features to describe. 
        3. Refer to the game history and select one candidate feature that no other player has described. If all candidate features are used, try to give some new candidates and retry to choose one.
        4. Describe the selected feature in brief, without the need for additional explanation or exposure of other features. Be careful not to directly expose words, but to use pronouns instead.
                
        Correct sample:
        It can fly long distances.
        It has a wide wingspan.

        Wrong sample:
        It is a delicate and beautiful creature that undergoes a stunning transformation from a caterpillar to a winged adult Its presence in gardens and fields brings joy and beauty to the environment.
        (reason: Multiple features were mentioned in one sentence, like beautiful, transformation, winged, in gardens, etc.)


        # INFORMATION
        You are player {id}. Your word is "{word}".

        other players' descriptions:
        {dialogue_history}
        Your analysis:
        {analysis}
        """
        return p 
    



def vote(cnum, unum, word, id, analysis, alive):
        p = f"""
        # the rules of the game:

        "Who is Undercover?" is a social deduction game in which multiple civilian players are mixed with a minority of undercover players. 
        Each player is secretly assigned a word, which is similar to the words of the other civilians but slightly different. 
        Players take turns briefly describing some of the characteristics of their words, but do not directly disclose them, while trying to avoid revealing too much information that may help others guess their identity.
        The goal is for the civilians to identify and eliminate the undercover players, while the undercover players must blend in, mislead the others, and avoid being discovered. 
        The game is divided into two phases: 
        speaking and voting. 
        During the speaking phase, players describe their words, balancing the need to share enough clues with the need to keep their identity hidden. Players are not alowed to talk to others, just describe the words.
        In the voting phase, players analyze previous descriptions, try to identify their teammates, and strategically vote to eliminate players based on incomplete information. 
        If only one civilian remains while there is still an undercover, the undercover team win; otherwise, the civilian team win.\n
        There are {cnum + unum} players in this game, {cnum} of whom are citizens and the other {unum} are undercover agents.
        

        # TASK:
        You should refer to your analysis, then output a voting result in this round.
        You can only choose one player to vote, and that player must be alive. {alive} are still alive in this round.


        # INFORMATION
        You are player {id}. Your word is {word}.

        Your analysis:
        {analysis}


        """
        return p 












def naive_speak(cnum, unum, word, id,  dialogue_history, vote_history):
        p = f"""
        # BACKGROUND

        "Who is Undercover?" is a social deduction game in which multiple civilian players are mixed with a minority of undercover players. 
        Each player is secretly assigned a word, which is similar to the words of the other civilians but slightly different. 
        Players take turns briefly describing some of the characteristics of their words, but do not directly disclose them, while trying to avoid revealing too much information that may help others guess their identity.
        The goal is for the civilians to identify and eliminate the undercover players, while the undercover players must blend in, mislead the others, and avoid being discovered. 
        The game is divided into two phases: 
        speaking and voting. 
        During the speaking phase, players describe their words, balancing the need to share enough clues with the need to keep their identity hidden. Players are not alowed to talk to others, just describe the words.
        In the voting phase, players analyze previous descriptions, try to identify their teammates, and strategically vote to eliminate players based on incomplete information. 
        If only one civilian remains while there is still an undercover, the undercover team win; otherwise, the civilian team win.\n
        There are {cnum + unum} players in this game, {cnum} of whom are citizens and the other {unum} are undercover agents.
        

        # TASK
        You should analyse the information, then output: 1. Your analysis and reasoning process 2. A sentense as your speech in this round.
        
        The speech should be brief and concise, only describe one feature, and you can not directly expose the words, but use pronouns instead.
        Correct sample:
        1. It can fly long distances.
        2. It has a wide wingspan.

        Wrong sample:
        1. It is a delicate and beautiful creature that undergoes a stunning transformation from a caterpillar to a winged adult Its presence in gardens and fields brings joy and beauty to the environment.
        (wrong reason: Multiple features were mentioned in one sentence, like beautiful, transformation, winged, in gardens, etc.)
        2. Bees are a common sight in many parts of the world.
        (wrong reason: 'bees' expose the word directly. you can say: They are a common sight ...)

        # INFORMATION
        You are player {id}. Your word is "{word}".

        other players' descriptions:
        {dialogue_history}
        the voting result:
        {vote_history}
        """
        return p 







def naive_vote(cnum, unum, word, id,  dialogue_history, vote_history, alive):
        p = f"""
        # BACKGROUND

        "Who is Undercover?" is a social deduction game in which multiple civilian players are mixed with a minority of undercover players. 
        Each player is secretly assigned a word, which is similar to the words of the other civilians but slightly different. 
        Players take turns briefly describing some of the characteristics of their words, but do not directly disclose them, while trying to avoid revealing too much information that may help others guess their identity.
        The goal is for the civilians to identify and eliminate the undercover players, while the undercover players must blend in, mislead the others, and avoid being discovered. 
        The game is divided into two phases: 
        speaking and voting. 
        During the speaking phase, players describe their words, balancing the need to share enough clues with the need to keep their identity hidden. Players are not alowed to talk to others, just describe the words.
        In the voting phase, players analyze previous descriptions, try to identify their teammates, and strategically vote to eliminate players based on incomplete information. 
        If only one civilian remains while there is still an undercover, the undercover team win; otherwise, the civilian team win.\n
        There are {cnum + unum} players in this game, {cnum} of whom are citizens and the other {unum} are undercover agents.
        

        # TASK
        You should analyse the information, then output: 1. Your analysis and reasoning process 2. a number as your voting target in this round. 
        You can only choose one player to vote, and that player must be alive. {alive} are still alive in this round.
        The belows are some examples of output and the explaination.

        Wrong sample:
        player 1 (You should not output "player")
        1,2,3 (You can only vote one player)

        # INFORMATION
        You are player {id}. Your word is "{word}".

        other players' descriptions:
        {dialogue_history}
        the voting result:
        {vote_history}
        """
        return p 

