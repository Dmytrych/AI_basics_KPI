class GhostMoveTracker():
    def __init__(self, ghosts):
        self.ghosts = ghosts
        self.update_current_info()

    def ghosts_moved(self):
        if self.ghosts[0].current_tile is self.current_tiles[0]:
            return False
        return True

    def update_current_info(self):
        current_tiles = []
        last_turn_sides = []
        for ghost in self.ghosts:
            current_tiles.append(ghost.current_tile)
            last_turn_sides.append(ghost.selected_move_direction)
        self.current_tiles = current_tiles
        self.last_turn_sides = last_turn_sides