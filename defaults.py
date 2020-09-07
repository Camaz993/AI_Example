# You can manipulate these defaults to change the game parameters.

game_params = {

   #File implementing the agent playing as player 1 (exclude .py extension)
   "player1": "myAgent",

   # File implementing the agent playing as player 2 (exclude .py extension)
   "player2": "randomPlayer",

   # Game for which to show visualisations
   "show_games": [1,50,100,200,250,300,350,400, 500],

   # Games for which to save visualisations (for later re-viewing)
   "save_games": [1, 500],

   # Speed of visualisation ('slow','normal','fast')
   "visSpeed": 'fast',

   # Visualisation resolution
   "visResolution": (720, 480),

   # Size of the game grid - default is 24
   "gridSize": 24,

   # Number of turns per game - default is 100
   "nTurns": 100,

   # Number of agents of each player
   "nAgents": 34,

   # Number of walls in the grid
   "nWalls": 20,

   # Number of games to play allowing the agents to evolve
   "nGames": 500
}


