left = 0
up = 1
right = 2
down = 3

directions = [0, 1, 2, 3]

def get_opposite(self, direction):
    if direction == left:
        return right
    if direction == right:
        return left
    if direction == up:
        return down
    return up