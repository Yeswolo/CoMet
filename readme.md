# Introduction

This project includes the main body of our designed undercover game, where users can play as civilians and undercovers using CoT and our proposed CoMet.

# File structure
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

# Startup method
1. Fill in the necessary API URL and API key in config.py
2. Run main.py

# Configure different parameters
Change directly in config.py
You can modify the parameters of the running rounds/LLM/specific parameters of the game, including the number of players, the use of agent mode in the game, etc

# Structure Introduction
Game.py defines the initialization of the game, assigning roles, judging victory conditions, etc;

Player.py defines the interactive actions of each individual player during gameplay;

Prompt specifies the input messages that the player agent needs to pass when calling the large model;

Word contains phrases from different themes that we have collected for the Undercover game



Main.py is the entrance to start the game

Config.py defines various parameters

Utils.py defines the relevant functions for calling LLM



# Related Work

We recommend that you use our follow-up work, CK-Arena: https://CK-Arena.site to conduct research on Undercover games. This is our LLM testing benchmark designed based on Undercover, which includes better game logic, anti-crash mechanisms, and prompts. We are still working on the follow-up work of undercover, mainly updating it on the CK-Arena homepage.


