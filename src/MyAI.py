# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        
        # the board can be as big as 7x7

        self.direction_turn_left = {"EAST": "NORTH", "NORTH": "WEST", "WEST": "SOUTH", "SOUTH": "EAST"}
        self.direction_turn_right = {"EAST": "SOUTH", "NORTH": "EAST", "WEST": "NORTH", "SOUTH": "WEST"}

        temp_dict = {
            'breeze': False,
            'wall': False,
            'stench': False,
            'safe': False
        }
        self.possible_board = []
        for i in range(7):
            self.possible_board.append([])
            for j in range(7):
                self.possible_board[-1].append(dict(temp_dict))

        # checks to see if the agent is at the start of the world
        self.start = True

        # if you want to backtrack to a safe position
        self.backtrack = False

        # list of moves that we iterate through backwards once we find the gold
        self.moves = []

        # bool if we have the gold
        self.gold = False

        # grid coordinates
        self.x = 0
        self.y = 0

        # orientation to get to for the agent
        self.target_orientation = "EAST"
        # checks to see if the agent needs to get to target orientation
        self.turning = False

        # string to see which direction our agent is currently facing
        self.orientation = "EAST"

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        print(stench, breeze, glitter, bump, scream)
        if self.gold:
            move = self.moves[-1]
            self.moves.pop()
            backward_move = move
            return backward_move

        if bump:
            self.possible_board[self.y][self.x]['wall'] = True

        if glitter:
            return Agent.Action.GRAB

        # need to reach target orientation
        if self.turning:
            # change orientation to left
            self._turn_left()
            # if reached target orientation, stop turning
            if self.orientation == self.target_orientation:
                self.turning = False
            return Agent.Action.TURN_LEFT

        # go back if reached breeze until reach no breeze
        if self.backtrack and not self.turning:
            print(self.possible_board)
            print(self.possible_board[self.y][self.x]['breeze'])
            if not self.possible_board[self.y][self.x]['breeze']:
                self._turn_right()
                return Agent.Action.TURN_RIGHT
            else:
                self.x -= 1
                return Agent.Action.FORWARD

        if breeze:
            # mark the board as having a breeze
            self.possible_board[self.y][self.x]['breeze'] = True
            self.possible_board[self.y][self.x]['safe'] = True

            if self.x == 0 and self.y == 0:
                return Agent.Action.CLIMB

            # if at the bottom of the world
            if self.y == 0:
                # if facing east, need to turn around
                if self.orientation == 'EAST':
                    self.turning = True
                    self.target_orientation = 'WEST'
                    self.orientation = 'NORTH'
                    self.backtrack = True
                    return Agent.Action.TURN_LEFT

        if stench:
            self.possible_board[self.y][self.x]['stench'] = True
            self.possible_board[self.y][self.x]['safe'] = True

        if scream:
            pass

        if not stench and not breeze and not glitter and not bump and not scream:
            self.possible_board[self.y][self.x]['safe'] = True

        for i in self.possible_board:
            print(i)
        self.x += 1
        return Agent.Action.FORWARD
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def _turn_left(self) -> None:
        self.orientation = self.direction_turn_left[self.orientation]

    def _turn_right(self) -> None:
        self.orientation = self.direction_turn_right[self.orientation]
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================