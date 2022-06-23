"""
This file implements the board for the game Hive.

"""

"""
Hive Rules:

Queen: 1 tile in any direction, if surrounded game is lost
Beetle: 1 tile in any direction, can climb, climbed tiles can't move: if a tile is being climbed on its list of neighbours is increased 
Grasshopper: Can jump over any number of tiles in any direction
Ant: Can go any number of tiles in any direction
Spider: Can go three tiles in any direction



Tile Placement:

A tile can be placed adjacent to any tile of the same colour provided it is not adjacent to a tile of the opposite colour


Tile Movement:

A tile moves following its rules, in order to make a move, the move must be physically possible.
At no point along a trajectory must a move be made in a direction that is adjacent to two occupied tiles.
At no point can the Hive be broken (ie. moving a tile cannot cause two unconnected islands of tiles to form)
"""



import numpy as np

"""
We implement the hive as a board of tiles. The board is a numpy array of shape (height, width). The board is indexed by (y, x).
The board is a 2D array of tiles. Each tile is a list integegers corresponding to the pieces in that tile. The list is ordered
top to bottom.

Since the hive board is hexagonal and infinite we use the following convention:

  / \ / \ / \ 
 |0,0|1,0|2,0|
  \ / \ / \ / \ 
   |0,1|1,1|2,1|
  / \ / \ / \ /
 |0,2|1,2|2,2|
  \ / \ / \ /

Since the maximal board size is 22x22, we use a numpy array of shape (22,22). should the hive move beyond these boundaries, we can 
impose a symmetric boundary condition.


"""
class Hive:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = np.zeros((height, width, 5), dtype=object)
        self.pieces = {}
        self.turn = 0
        self.turn_count = 0
    
    def place_piece(self, piece, x, y, z = 0):
        self.board[y,x,z] = piece
        self.pieces[piece] =  self.adjacent(x, y, z)

    def crawl_piece(self, piece, direction):
        position = np.where(self.board == piece)
        if not self.can_move(piece):
            return False
        if self.board[position + direction]:
            return False
        if direction == (1,0,0):
            if self.board[position[0], position[1]+1] and self.board[position[0], position[1]-1]:
                return False
        elif direction == (-1,0,0):
            if self.board[position[0], position[1]+1] and self.board[position[0], position[1]-1]:
                return False
        elif direction == (0,1,0):
            if self.board[position[0]+1, position[1]] and self.board[position[0]-1, position[1]]:
                return False
        elif direction == (0,-1,0):
            if self.board[position[0]+1, position[1]] and self.board[position[0]-1, position[1]]:
                return False
        elif direction == (1, -1,0):
            if self.board[position[0]+1, position[1]] and self.board[position[0]-1, position[1]]:
                return False
        elif direction == (1, 1,0):
            if self.board[position[0]+1, position[1]] and self.board[position[0]-1, position[1]]:
                return False

        self.board[position] = 0
        self.board[position + direction] = piece
        self.pieces[piece] = self.adjacent(position + direction)

        return True


    def move_piece(self, piece):
        """

        return 
        """

        if not self.can_move(piece):
            return False

        

        return True


    def adjacent(self, x, y, z = 0):
        """
        Returns a list of all adjacent tiles.
        """
        adjacents = []
        for dx, dy in [(0,-1), (1,-1), (-1,0), (1,0), (0,1), (1,1)]:
            adjacents.append(self.board[(y+dy)%self.height, (x+dx)%self.width, z])

        return adjacents

    def climbed(self, x, y, z = 1):
        """
        Returns True if the piece has climbed any tiles.
        """
        return self.board[y,x,z] > 0

    def hop(self, new_position, direction):
        """
        Returns True if the piece can jump in the given direction. And jumps in that direction.
        """
        while self.board[(new_position + direction)%22]:
            self.hop(new_position, direction)

        return (new_position + direction) % 22


    def jump(self, piece, direction):
        """
        Returns True if the piece can jump in the given direction. And jumps in that direction.
        """
        position = self.pieces[piece]
        if not self.can_move(piece):
            return False
        if not self.board[(new_position + direction) % 22]:
            return False
        
        new_position = self.hop(piece, direction)
        
        

        self.board[position] = 0
        self.board[new_position] = piece
        self.pieces[piece] = new_position

        return True

    def DFSUtil(self, v, visited):
        """
        Recursive helper function for DFS.
        """
        visited[v] = True
        for i in self.pieces[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)

    def one_hive(self, v):
        """
        Returns True if the hive is in one piece.
        """
        visited = set()
        self.DFSUtil(v, visited)

        return len(visited) ==  len(self.pieces)

    

