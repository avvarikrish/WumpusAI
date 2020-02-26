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
        self.direction_opposite = {"EAST": "WEST", "NORTH": "SOUTH", "WEST": "EAST", "SOUTH": "NORTH"}

        temp_dict = {
            'breeze': False,
            'bump': False,
            'stench': False,
            'visited': False,
            'scream': False,
            'glitter': False
        }
        # lets the agent know which direction he will be searching in
        self.searching_east = True
        self.searching_north = False
        self.possible_board = []
        for i in range(7):
            self.possible_board.append([])
            for j in range(7):
                self.possible_board[-1].append(dict(temp_dict))

        # checks to see if the agent is at the start of the world
        self.start = True

        # if you want to backtrack to a safe position
        self.backtrack = False
        self._go_back = False
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
        self.turning_back_to_before = False

        # string to see which direction our agent is currently facing
        self.orientation = "EAST"

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print(self.x, self.y)
        self._set_environment(stench, breeze, glitter, bump, scream, self.possible_board[self.y][self.x])
        for i in self.possible_board:
            for j in i:
                print(j['visited'], end=' ')
            print()
        print(self.moves)
        print(stench, breeze, glitter, bump, scream)
        if self.gold:
            move = self.moves[-1]
            self.moves.pop()
            backward_move = move
            return backward_move

        # if bump:
        #     self.possible_board[self.y][self.x]['wall'] = True

        if glitter:
            self.gold = True
            return Agent.Action.GRAB

        # need to reach target orientation
        if self.turning:
            # change orientation to left
            self._turn_left()
            # if reached target orientation, stop turning
            if self.orientation == self.target_orientation:
                self.turning = False
            return Agent.Action.TURN_LEFT

        if self._go_back and not self.turning:
            self._go_back = False
            if self.orientation == "EAST":
                self.x += 1
            if self.orientation == "WEST":
                self.x -= 1
            if self.orientation == "NORTH":
                self.y += 1
            if self.orientation == "SOUTH":
                self.y -= 1
            return Agent.Action.FORWARD

        # go back if reached breeze until reach no breeze/stench
        if self.backtrack and not self._go_back:
            # past_move = self.moves.pop()

            # if not self.possible_board[self.y][self.x]['breeze'] and not self.possible_board[self.y][self.x]['stench']:
            #     self.backtrack = False
            #     self.turning = True
            #     self.target_orientation = self.direction_opposite[self.orientation]
            #     self.orientation = self.direction_turn_left[self.orientation]
            #     return Agent.Action.TURN_LEFT
            # else:
            #     if self.orientation == 'WEST':
            #         self.x -= 1
            #     elif self.orientation == 'EAST':
            #         self.x += 1
            #     elif self.orientation == 'NORTH':
            #         self.y += 1
            #     elif self.orientation == 'SOUTH':
            #         self.y -= 1
            #
            #     return Agent.Action.FORWARD
            print(self.can_visit())
            if not self.can_visit():
                print(self.moves)
                m = self.moves[-1]
                print(m)
                self.target_orientation = self.direction_opposite[m]
                print(self.target_orientation)
                if self.orientation == self.target_orientation:
                    self.moves.pop()
                    if self.orientation == "EAST":
                        self.x += 1
                    if self.orientation == "WEST":
                        self.x -= 1
                    if self.orientation == "NORTH":
                        self.y += 1
                    if self.orientation == "SOUTH":
                        self.y -= 1
                    return Agent.Action.FORWARD
                else:
                    self.turning = True
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT
            else:
                print('yee haw')
                self.backtrack = False

        if bump:
            if self.orientation == "EAST" and self.x < 7:
                self.possible_board[self.y][self.x+1]['visited'] = True

            if self.orientation == "NORTH" and self.y < 7:
                self.possible_board[self.y+1][self.x]['visited'] = True
        if breeze or stench:
            # mark the board as having a breeze

            if self.x == 0 and self.y == 0:
                return Agent.Action.CLIMB

            # if at the bottom of the world
            # if self.y == 0:
            # if facing east, need to turn around



            self.turning = True
            self._go_back = True
            self.backtrack = True
            self.target_orientation = self.direction_opposite[self.orientation]
            self.orientation = self.direction_turn_left[self.orientation]
            return Agent.Action.TURN_LEFT


            # if self.orientation == 'EAST':
            #     self.turning = True
            #     self.target_orientation = 'WEST'
            #     self.orientation = 'NORTH'
            #     self.backtrack = True
            #     self.moves.append('left')
            #     return Agent.Action.TURN_LEFT
            # if self.orientation == 'NORTH':
            #     self.turning = True
            #     self.target_orientation = 'SOUTH'
            #     self.orientation = 'WEST'
            #     self.backtrack = True
            #     self.moves.append('left')
            #     return Agent.Action.TURN_LEFT

        # if scream:
        #     pass

        if not stench and not breeze and not glitter and not bump and not scream:

            # if self.checking:
            if self.x < 7 and not self.possible_board[self.y][self.x+1]['visited']:
                if self.orientation == 'EAST':
                    self.x += 1
                    self.moves.append('EAST')
                    return Agent.Action.FORWARD
                else:
                    self.target_orientation = 'EAST'
                    self.turning = True
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT

            elif self.y < 7 and not self.possible_board[self.y+1][self.x]['visited']:
                if self.orientation == 'NORTH':
                    self.y += 1
                    self.moves.append('NORTH')
                    return Agent.Action.FORWARD
                else:
                    self.target_orientation = 'NORTH'
                    self.turning = True
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT

            elif self.y > 0 and not self.possible_board[self.y-1][self.x]['visited']:
                if self.orientation == 'SOUTH':
                    self.y -= 1
                    self.moves.append('SOUTH')
                    return Agent.Action.FORWARD
                else:
                    self.target_orientation = 'SOUTH'
                    self.turning = True
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT

            elif self.x > 0 and not self.possible_board[self.y][self.x-1]['visited']:
                if self.orientation == 'WEST':
                    self.x -= 1
                    self.moves.append('WEST')
                    return Agent.Action.FORWARD
                else:
                    self.target_orientation = 'WEST'
                    self.turning = True
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT

            else:
                # backtrack call

                self.turning = True
                self.backtrack = True

                # self.target_orientation = self.direction_opposite[self.orientation]
                # self.orientation = self.direction_turn_left[self.orientation]
                # return Agent.Action.TURN_LEFT


            # if self.searching_north:
            #     self.y += 1
            #     self.moves.append('forward')
            #     return Agent.Action.FORWARD
            # if self.searching_east:
            #     self.x += 1
            #     self.moves.append('forward')
            #     return Agent.Action.FORWARD


        # self.x += 1
        # return Agent.Action.FORWARD
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

    def _set_environment(self, stench, breeze, glitter, bump, scream, temp_dict ):
        temp_dict['stench'] = stench
        temp_dict['breeze'] = breeze
        temp_dict['glitter'] = glitter
        temp_dict['bump'] = bump
        temp_dict['scream'] = scream
        temp_dict['visited'] = True

    def can_visit(self):
        return (self.y < 7 and not self.possible_board[self.y+1][self.x]['visited']) or (self.y > 0 and not self.possible_board[self.y-1][self.x]['visited']) or (self.x < 7 and not self.possible_board[self.y][self.x+1]['visited']) or (self.x > 0 and not self.possible_board[self.y][self.x-1]['visited'])


    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================