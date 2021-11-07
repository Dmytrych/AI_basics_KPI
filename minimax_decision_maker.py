
from os import stat

algos = ["minimax", "expectimax"]
class MinimaxDecisionMaker():
    def __init__(self, pacman, ghost, ghost_tracker, algo_index):
        self.current_state = StateNode(None, [])
        self.current_state.walked_tiles = []
        self.max_depth = 4
        self.players = [pacman, ghost]
        self.max_player = pacman
        self.ghost_tracker = ghost_tracker
        self.algo_index = algo_index

    def make_desision(self):
        ghost_turn_directions = self.ghost_tracker.last_turn_sides
        self.current_state = self.evaluate_tree(ghost_turn_directions)
        return self.current_state.turns[0].side

    def build_subtree(self):
        self.build_subtree_recursive(self.current_state, self.get_player_root_positions(), 0)

    def evaluate_tree(self, ghost_real_choices):
        print("Evaluating subree for " + algos[self.algo_index])




        best_state = None
        for state in self.current_state.children:
            if not self.is_current_situation(state, ghost_real_choices):
                continue
            if best_state is None:
                best_state = state
                continue
            state_value = self.evaluate_best_cost(state)
            state.max_children_value = state_value
            if best_state.max_children_value < state_value:
                best_state = state
        return best_state

    def is_current_situation(self, state, ghost_real_choices):
        for i in range(len(state.turns) - 1):
            if i == 0:
                continue
            if ghost_real_choices[i] != state.turns[i]:
                return False
        return True


    def evaluate_best_cost(self, state):
        best_value = None
        for child_state in state.children:
            state_value = self.evaluate_best_cost(child_state)
            if best_value is None:
                best_value = state_value
                continue
            if best_value < state_value:
                best_value = state_value
        
        if best_value is None:
            return state.cost
        return best_value + state.cost

    def build_subtree_recursive(self, current_state, player_positions, depth):
        if(depth > self.max_depth):
            return

        turn_matrix = []

        for i in range(len(self.players)):
            if i != 0 and player_positions[i] == player_positions[0]:
                current_state.cost -= 100
            turn_matrix.append(self.get_walkable_neighbours(player_positions[i]))

        all_combinations = self.get_all_turn_combinations(turn_matrix)

        if player_positions[0].is_empty and player_positions[0] not in current_state.walked_tiles:
            current_state.cost += 1
            current_state.walked_tiles.append(player_positions[0])

        child_states = []

        if depth < self.max_depth:
            for combination in all_combinations:
                child_states.append(StateNode(current_state, combination))

        current_state.set_children(child_states)

        for state in child_states:
            state.walked_tiles = current_state.walked_tiles.copy()
            state.cost = current_state.cost
            self.build_subtree_recursive(state, self.get_player_positions(state.turns), depth + 1)

    def get_player_root_positions(self):
        tiles = []
        for player in self.players:
            tiles.append(player.current_tile)
        return tiles

    def get_player_positions(self, turns):
        player_tiles = []
        for turn in turns:
            player_tiles.append(turn.tile)
        return player_tiles

    def get_all_turn_combinations(self, turn_matrix):
        return self.get_combinations_recursive(turn_matrix, len(turn_matrix) - 1)

    def get_combinations_recursive(self, turn_matrix, current_row_index):
        turn_combinations = []
        if current_row_index == 0:
            for turn in turn_matrix[current_row_index]:
                turn_combinations.append([turn])
            return turn_combinations

        turn_subcombinations = self.get_combinations_recursive(turn_matrix, current_row_index - 1)

        for turn in turn_matrix[current_row_index]:
            for subcombination in turn_subcombinations:
                array_copy = subcombination.copy()
                array_copy.append(turn)
                turn_combinations.append(array_copy)
        
        return turn_combinations

    def get_walkable_neighbours(self, current_position):
        result = []
        for tile in current_position.neighbours:
            if tile.tile.is_empty:
                result.append(tile)
        return result

class StateNode():
    def __init__(self, parent_node, turns):
        self.walked_tiles = []
        self.cost = 0
        self.children = []
        self.parent = parent_node
        self.turns = turns
        self.max_children_value = 0
        if parent_node is not None:
            parent_node.children.append(self)

    def set_children(self, children):
        self.children = children