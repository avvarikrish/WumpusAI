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

        # count of how many stenches
        self._stench_locations = []
        self._kill_wumpus = False
        self._killed_wumpus = False

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        try:
            # set the environment
            self._set_environment(stench, breeze, glitter, bump, scream, self.possible_board[self.y][self.x])

            # if at the start and can't visit anywhere else or found gold
            if self._at_start() and (not self.can_visit_around() or self.gold):
                return Agent.Action.CLIMB

            # if have gold, backtrack the moves
            if self.gold:

                # turn the dude to the opposite direction orientation
                self.target_orientation = self.direction_opposite[self.moves[-1]]

                # keep turning until the dude is in the right orientation
                if self.target_orientation != self.orientation:
                    self.turning = True
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT
                else:
                    return self._backtrack()

            # grab the gold
            if glitter:
                self.gold = True
                return Agent.Action.GRAB

            # kill the wumpus
            if self._kill_wumpus:
                if self.orientation == self.target_orientation:
                    self._kill_wumpus = False
                    self._killed_wumpus = True
                    self._mark_unvisited()
                    return Agent.Action.SHOOT
                else:
                    self.orientation = self.direction_turn_left[self.orientation]
                    return Agent.Action.TURN_LEFT

            # need to reach target orientation
            if self.turning:
                # change current orientation to left
                self._turn_left()

                # if reached target orientation, stop turning
                if self.orientation == self.target_orientation:
                    self.turning = False

                return Agent.Action.TURN_LEFT

            # backtrack if can't search around
            if self._go_back and not self.turning:
                self._go_back = False
                return self._backtrack()

            # go back if reached breeze until reach no breeze/stench
            if self.backtrack and not self._go_back:
                # backtrack if can't search around
                if not self.can_visit_around():
                    m = self.moves[-1]
                    self.target_orientation = self.direction_opposite[m]
                    if self.orientation == self.target_orientation:
                        return self._backtrack()
                    # turn the dude around to the right backtrack direction
                    else:
                        self.turning = True
                        self.orientation = self.direction_turn_left[self.orientation]
                        return Agent.Action.TURN_LEFT
                else:
                    self.backtrack = False

            if bump:
                self.moves.pop()
                if self.orientation == "EAST" and self.x < 7:
                    self.x -= 1
                    for i in range(7):
                        self.possible_board[i][self.x+1]['visited'] = True

                if self.orientation == "NORTH" and self.y < 7:
                    self.y -= 1
                    for i in range(7):
                        self.possible_board[self.y+1][i]['visited'] = True
                return Agent.Action.CLIMB

            if breeze:
                if stench:
                    self._stench_locations.append((self.x, self.y))
                if self.x == 0 and self.y == 0:
                    return Agent.Action.CLIMB

                self.turning = True
                self._go_back = True
                self.backtrack = True
                self.target_orientation = self.direction_opposite[self.orientation]
                self.orientation = self.direction_turn_left[self.orientation]
                return Agent.Action.TURN_LEFT

            if stench and not self._killed_wumpus:
                if self.x == 0 and self.y == 0:
                    return Agent.Action.CLIMB

                self.turning = True
                self._go_back = True
                self.backtrack = True
                self.target_orientation = self.direction_opposite[self.orientation]
                self.orientation = self.direction_turn_left[self.orientation]
                if len(self._stench_locations) > 0:
                    wumpus_location = self._wumpus_location()
                    if wumpus_location is not None:
                        self._kill_wumpus = True
                        self._go_back = False
                        self.target_orientation = wumpus_location
                else:
                    self._stench_locations.append((self.x, self.y))
                return Agent.Action.TURN_LEFT

            if not breeze and not glitter and not bump:
                if self.x < 6 and not self.possible_board[self.y][self.x+1]['visited']:
                    if self.orientation == 'EAST':
                        self.x += 1
                        self.moves.append('EAST')
                        return Agent.Action.FORWARD
                    else:
                        self.target_orientation = 'EAST'
                        self.turning = True
                        self.orientation = self.direction_turn_left[self.orientation]
                        return Agent.Action.TURN_LEFT
                elif self.y < 6 and not self.possible_board[self.y+1][self.x]['visited']:
                    if self.orientation == 'NORTH':
                        self.y += 1
                        self.moves.append('NORTH')
                        return Agent.Action.FORWARD
                    else:
                        self.target_orientation = 'NORTH'
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


                else:
                    # backtrack call
                    self.turning = True
                    self.backtrack = True
        finally:
            pass
            print(self.moves)

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

    def can_visit_around(self):
        return (self.y < 6 and not self.possible_board[self.y+1][self.x]['visited']) or (self.y > 0 and not self.possible_board[self.y-1][self.x]['visited']) or (self.x < 6 and not self.possible_board[self.y][self.x+1]['visited']) or (self.x > 0 and not self.possible_board[self.y][self.x-1]['visited'])

    def _at_start(self):
        return self.x == 0 and self.y == 0

    def _backtrack(self):
        self.moves.pop()
        if self.orientation == 'WEST':
            self.x -= 1
        if self.orientation == 'EAST':
            self.x += 1
        if self.orientation == 'SOUTH':
            self.y -= 1
        if self.orientation == 'NORTH':
            self.y += 1
        return Agent.Action.FORWARD

    def _wumpus_location(self):
        if len(self._stench_locations) == 1:
            last_move = self.moves[-1]
            location = self._stench_locations[0]
            if location[0] > self.x and location[1] > self.y:
                if last_move == 'WEST':
                    return 'NORTH'
                else:
                    return 'EAST'
            elif location[0] > self.x and location[1] < self.y:
                if last_move == 'WEST':
                    return 'SOUTH'
                else:
                    return 'EAST'
            elif location[0] < self.x and location[1] > self.y:
                if last_move == 'EAST':
                    return 'NORTH'
                else:
                    return 'WEST'
            elif location[0] < self.x and location[1] < self.y:
                if last_move == 'EAST':
                    return 'SOUTH'
                else:
                    return 'WEST'
        else:
            return None

    def _mark_unvisited(self):
        for location in self._stench_locations:
            self.possible_board[location[1]][location[0]]['visited'] = False



    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================

