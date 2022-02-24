from time import perf_counter as pfc
from heapq import heappop, heappush
import argparse


class Puzzle:
    def __init__(self, infile):
        self.str = ""
        self.infile = infile
        self.start()
        self.energy = dict(A=1, B=10, C=100, D=1000)
        self.parc = [0, 1, 3, 5, 7, 9, 10]  # hallway indices
        self.stepout = dict(A=2, B=4, C=6, D=8)  # doorway indices
        self.target = {
            r: range(ord(r) - 54, len(self.str), 4) for r in "ABCD"
        }  # list of in-room indices
        self.targetI = {
            v: key for key, val in self.target.items() for v in val
        }  # unpack target indices and point to intended occupant
        self.solution = "." * 11 + "ABCD" * ((len(self.str) - 11) // 4)
        self.heap = [(0, self.str)]
        self.seen = {self.str: 0}

    def start(self):
        """
        Reads puzzle file and produces a string with first eleven characters
        the hallway and groups of four following representing the layer
        of each target room [A,B,C,D] repeated
        """
        with open(self.infile, "r") as f:
            for c in f.read():
                if c in "ABCD.":
                    self.str += c

    def solve(self):
        while self.heap:
            cost, state = heappop(self.heap)
            if state == self.solution:
                return cost
            self.str = state
            for a, b in self.possible_moves():
                p, r = (a, b) if a < b else (b, a)
                distance = abs(self.stepout[self.targetI[r]] - p) + (r - 7) // 4
                new_cost = cost + distance * self.energy[self.str[a]]
                moved = self.move(a, b)
                if self.seen.get(moved, 999999) <= new_cost:
                    continue
                self.seen[moved] = new_cost
                heappush(self.heap, (new_cost, moved))

    def move(self, a, b):
        """
        Swaps the characters in positions a and b of the string representing
        current puzzle state; returns new string
        """
        p = list(self.str)
        p[a], p[b] = p[b], p[a]
        return "".join(p)

    def blocked(self, a, b):
        """
        Checks if there is an amphipod between positions a and b in the
        hallway; returns True if blocked
        """
        step = 1 if a < b else -1
        for pos in range(a + step, b + step, step):
            if self.str[pos] != ".":
                return True

    def can_enter_room(self, a):
        """
        Finds deepest position amphipod at location a can land in its room;
        returns False if another amphipod is in the room
        returns nothing if if cannot reach the door to the rooom
        """
        amphi = self.str[a]
        b = self.stepout[amphi]
        room_pos = self.target[amphi]
        for pos in room_pos:
            if self.str[pos] == ".":
                best_pos = pos
            elif self.str[pos] != amphi:
                return False
        if not self.blocked(a, b):
            return best_pos

    def can_leave_room(self, room):
        """
        Returns the string index of the shallowest amphipod in the room
        """
        for a in self.target[room]:
            if self.str[a] == ".":
                continue
            return a

    def get_possible_parc_pos(self, a):
        for b in [pos for pos in self.parc if self.str[pos] == "."]:
            if self.blocked(a, b):
                continue
            yield b

    def possible_moves(self):
        for a in [pos for pos in self.parc if self.str[pos] != "."]:
            b = self.can_enter_room(a)
            if b:
                yield a, b
        for room in "ABCD":
            a = self.can_leave_room(room)
            if not a:
                continue
            for b in self.get_possible_parc_pos(self.stepout[room]):
                yield a, b


def main():
    puzzle = Puzzle(args.f)
    print(puzzle.solve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("f", type=str)
    args = parser.parse_args()
    main()
