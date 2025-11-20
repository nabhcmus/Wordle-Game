import heapq
from collections import Counter

class AStarSolver:
    def __init__(self, api):
        self.api = api
        self.target = api.word
        self.words = api.words_list
        self.N = len(self.target)

    def heuristic(self, w):
        mismatch = sum(w[i] != self.target[i] for i in range(self.N))
        wc = Counter(w)
        tc = Counter(self.target)
        extra = sum(wc[ch] for ch in wc if ch not in tc)
        return mismatch + extra

    def feedback(self, guess, target):
        res = ["B"] * self.N
        t_left = list(target)

        for i in range(self.N):
            if guess[i] == target[i]:
                res[i] = "G"
                t_left[i] = None

        for i in range(self.N):
            if res[i] == "G":
                continue
            if guess[i] in t_left:
                res[i] = "Y"
                t_left[t_left.index(guess[i])] = None

        return "".join(res)

    def solve(self, start="AARON"):
        pq = []
        heapq.heappush(pq, (0, start, []))
        visited = set()

        while pq:
            f, guess, path = heapq.heappop(pq)

            if guess in visited:
                continue
            visited.add(guess)

            if guess == self.target:
                return path + [guess]

            for w in self.words:
                if w in visited:
                    continue

                g = len(path) + 1
                h = self.heuristic(w)
                heapq.heappush(pq, (g + h, w, path + [guess]))

        return []
