
def system(word, id):
    p = f"""
    You are playing the game 'Who Is Undercover?' like a real human.
    Do not mention that you are an AI or describe your role as an AI.
    Just focus on your actions and decisions as a player in the game.

    """
    return p

def feature(cnum, unum, word, id, dialogue_history, round_dialogue, game_history, vote_history, feature):
    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words.The two words share some similarities.  
    Players are divided into two teams based on their assigned words: the majority team and the minority team. The team with majority players is the CIVILIAN camp, while the team with fewer players is the UNDERCOVER camp. 
    During the game, players take turns describing a feature of their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have the same other word.
    \n\n
    



    # Task
    Now your task is to extract information from other people's descriptions, 
    Summarize the characteristics of the other word, and try to guess the word after having enough characteristics.
    
    Please follow the steps in order:
        1. Check if other players' description aligns with your word. Find those descriptions that not match your word, then they should be describing the other word.
        2. Analyze those suspicious descriptions, extract and summarize the unique features of the other word.
        - These features should not fit your word, but rather fit only the other word. They are the key information you use to identify the other word.
        3. Generate or adjust your guess for the other word:
        - The guess should be based on two pieces of information: one is the features you just summarized, and the other is the basic principle that the other word is similar to or related to your word.
        - If it is the first time generating a guess, you should generate multiple words or a range of guesses, unless some players have already made descriptions that provide enough clear information.
        - If it is not the first guess, you should narrow down the range of guesses using the new information or adjust the guess when errors are detected. Once enough clear information is obtained, lock in on a single word.        4. summary the features of the other word and your guesses about the other word.
    \n\n


    # Information
    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of another word's features** \n"{feature}"\n
    **history of other players' statements**   "{dialogue_history}"
    \n\n


    """
    return p






def identify(cnum, unum, word, id, dialogue_history, round_dialogue, game_history, vote_history, feature):
    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
    Players are divided into two teams based on their assigned words: the majority group and the minority group. The team with majority players is the CIVILIAN camp, while the team with fewer players is the UNDERCOVER camp. 
    During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.
    \n\n

    
    # Task
    Now your general task is to determine which word (Your word or the other word) the players have been assigned to, and which camps (MAJORITY or MINORITY) they belong to.
    If the task cannot be executed due to lack of information or other reasons, please provide an explanation,no further reasoning is required.
    
    Finish the task by follow these steps in order:
    1. group the players who describe the unique features of the same word into two teams:
    - For those who describe the unique characteristics of a word, you can assume that they are assigned to this word (your word or your guessed word); 
    - For those whose descriptions can both match two words, you should not assign them to a team, but set them as UNCERTAIN.
    - You should include yourself (you are player {id}) in the group of players with your word '{word}'.
    Sample:"Player with 'Word A': ...;  Player with 'Word B': ...;   Uncertain: ..."

    2. try to refer to the voting results to determine the uncertain players and assign them to a team:
    - if his voting object is always Team A, then he may belong to Team B
    - If his voting result is same with many players, then he may belong th the team with those players.

    3. determine the camps by finding the team with more than {unum} players:
    The premise of determining the camp is that you have found enough people (more than {unum}) with the same word, they should belong to the civilian camp, and the players with the other word belong to the undercover camp.
    You can only determine the camps by finding the team with many people and setting them as the majority, but not by finding a team with few people and setting them as the minority or undercover, because due to a lack of information, you will leave some players undetermined, and it is likely that you will not find all the players in the civilian camp.
    Because 'In this game, there are {cnum + unum} players in total. {cnum} civilian players have the same word, and the other {unum} undercover players have another same word.'
    If there are not enough players for you to find the majority team and judge them as civilian camp, you should not make a judgement about camps, but continue to observe the players.
    Sample:"'Word A' is corresponding to the CIVILIAN camp, 'Word B' is corresponding to the UNDERCOVER camp."
    Sample:"Camps undetermined due to lack of information."

        \n\n
    # Information

    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of another word's features** \n"{feature}"\n
    - Note that if you have more than one guess for another word, you should judge them as a whole, not separately: 
    your target for judging is “the other word”, not each possible guess you have for the other word.\n
    
    **history of other players' statements**   \n"{dialogue_history}"\n


    """
    return p



def strategy(cnum, unum, word, id, dialogue_history, round_dialogue, game_history, vote_history, feature, identity):
    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
    Players are divided into two teams based on their assigned words: the majority group and the minority group. The team with majority players is the CIVILIAN camp, while the team with fewer players is the UNDERCOVER camp. 
    During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.
    \n\n



    # Task
    Your task is to output a strategy for your speech in this round.
    Now, follow these steps in order:
    1. review your camp from [Your analysis of your camp and identity]
    2. Your division of camps determines which strategy you will choose. 
        Output a strategy, explained in two parts: 
        - What are the requirements for the features you want to choose in the ACTION part;
        - Reasons or Purposes to explain your action in the COMMENT part.
        
        You should not provide specific speech content, only focus on macro-strategy.
    You must deploy strategies based on your definition of camps and team allocations.
    When you confirmed your Camp, unless there is insufficient information to take action (such as not having guessed the other word), you should adopt an aggressive and proactive strategy.
    

    Refer to the following strategies:
    **SELF-PROTECTION**:
    action: Try to make your speech align with both your own word and all the words you guessed.
    - Your description will not directly expose your words, so you can remain unsuspected for the time being and gather more information.
    - You can choose this strategy if you are unsure about your camps, or unsure about the other word.
    - For these purpose, you can try to make your speech more vague and general by describing the category, characteristics rather than details and features.
    
    **DECEIVE AND INTEGRATE**:
    action: try to describe a unique feature of the other word, the feature should not align with your word.
    - Your description will reflect that you obviously know another word, and will enable the other word's team members to think of you as one of them.
    - This strategy can be used when you think you are in UNDERCOVER camp and you have already guessed the other word.
    - Note that if your guess is more than one word, you should look for common features between those guesses to describe it.

    **Cleverly reveal your camp**:
    action: try to describe a unique feature of your word, the feature should not align with the other word.
    - Your description will reflect that you obviously know your word, enable your teammates to identify you, then you can vote out the other opponent players.
    - You should try to make your description more subtle, because revealing unique characteristics risks exposing your words to your opponent's guesses.
    - This strategy can be used when you think you are in CIVILIAN camp. When you found yourself in the minority, you should not use this strategy.


    # Information
    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of your camp and identity** \n"{identity}"\n
    **Your analysis of another word's features** \n"{feature}"\n


    \n\n
    """
    return p 




def speak(cnum, unum, word, id, dialogue_history, round_dialogue, game_history, vote_history, feature, identity, strategy):
    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
    Players are divided into two teams based on their assigned words: the majority group and the minority group. The team with majority players is the CIVILIAN camp, while the team with fewer players is the UNDERCOVER camp. 
    During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.
    \n\n


    # Task
    You need to describe a feature of the word as your speech. Please follow these steps in order:
    1. Review your strategy and the guesses about the other word, understand the requirements of strategy for your action.
    2. Based on the requirements that the features need to meet, list some candidate features to describe. 
    3. Refer to the game history and select one candidate feature that no other player has described. If all candidate features are used, try to give some new candidates and retry to choose one.
    4. Describe the selected feature in brief, without the need for additional explanation or exposure of other features. Be careful not to directly expose words, but to use pronouns instead.
        
    Example: "It has <selected feature>.", "this thing is <selected feature>.", etc.

    # Information
    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of another word's features** \n{feature}\n
    **Your strategy** \n"{strategy}"\n
    **history of other players' statements**   \n"{dialogue_history}"\n

    \n\n

    """
    return p 





def vote(cnum, unum, word, id, dialogue_history, round_dialogue, game_history, alive, feature, identity):
    p = f"""

    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
    Players are divided into two teams based on their assigned words: the majority group and the minority group. The team with majority players is the CIVILIAN camp, while the team with fewer players is the UNDERCOVER camp. 
    During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.

    Now it is voting phase, and you should choose one player to vote from {alive}, the player with the most votes will be eliminated.
    voting rule:
    You can only choose one player to vote, and that player must be alive. {alive} are still alive in this round.
    \n\n



    # Task
    You need to choose an alive player to vote for expulsion. The player with the most votes will be expelled.
    Please follow the steps below in order:

    1. Review your definition of your own identity.
    2. Figure out your winning conditions based on your identity.
    3. Choose one player to vote.

    \n\n
    
    # Information

    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of another word's features** \n"{feature}"\n
    **Your analysis of your camp and identity** \n"{identity}"\n
    **history of other players' statements**   \n"{dialogue_history}"\n

    - {alive} are players who are still alive in this round, so you can only vote for players in this set. 

    \n\n

    """
    return p 


    