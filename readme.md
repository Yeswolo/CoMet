# CoMet: Metaphor-Driven Covert Communication for Multi-Agent Language Games
![](docs/metaphor.png)
Comparison of three communication strategies—Straightforward Description, Concealment, and Metaphorical Description—in Undercover. In this example, a civilian describes a “butterfly”, and the reactions of the two players are shown. In the Straightforward method, the civilian successfully identifies their teammate, but the undercover agent guesses the word. In Concealment, the civilian’s vague clue leads to confusion, with the undercover agent failing to guess the word and the civilian unable to identify their teammate. The Metaphor method allows the civilian to subtly describe the word, leading to a correct identification by the civilian agent, while the undercover agent fails to guess the word.


You can Check our paper
<a href="https://arxiv.org/abs/2505.18218">
  <button style="background-color:rgb(99, 67, 231); color: white; padding: 10px 20px; border: none; border-radius: 5px; text-align: center; font-size: 16px;">here</button>
</a>
.

## Introduction

This project includes the main body of our designed undercover game.

## File structure
```
Project/
│
├── gamelist/
│   └──Undercover/
│   ├── game.py
│   ├── player.py
│   ├── prompt
│   └── words
├── config.py
├── main.py
├── utils.py
├── requirements.txt
└── README.md
```

## Startup method
1. Fill in the necessary API URL and API key in config.py
2. Run main.py

## Configure different parameters
Change directly in config.py
You can modify the parameters of the running rounds/LLM/specific parameters of the game, including the number of players, the use of agent mode in the game, etc

## Structure Introduction
Game.py defines the initialization of the game, assigning roles, judging victory conditions, etc;

Player.py defines the interactive actions of each individual player during gameplay;

Prompt specifies the input messages that the player agent needs to pass when calling the large model;

Word contains phrases from different themes that we have collected for the Undercover game



Main.py is the entrance to start the game

Config.py defines various parameters

Utils.py defines the relevant functions for calling LLM

## Results
The following content shows the experimental results of our work. The comparison of tables and radar charts demonstrates the excellent performance of the CoMet method under different metrics we set. For details, please read the article.


![](docs/table.png)
Performance comparison of different methods relative to two baselines in Undercover game



![](docs/radar.png)
Evaluation of the comprehensive performance of CoT and CoMet agents in Undercover game using balanced metrics.




## Related Work

We recommend that you use our follow-up work, CK-Arena: https://CK-Arena.site to conduct research on Undercover games. This is our LLM testing benchmark designed based on Undercover, which includes better game logic, anti-crash mechanisms, and prompts. We are still working on the follow-up work of undercover, mainly updating it on the CK-Arena homepage.


