from Queue import Queue, PriorityQueue

class Solver():

    def checkRow(self,row, rule):
        counts = map(len, ''.join(row).split())
        if len(counts) > len(filter(int, rule)) or max(counts if counts else [0]) > max(rule):
            return False
        for i, j in zip(counts, filter(int, rule)):
            if i > j:
                return False
        return True

    def makeRows(self,rule, size):
        marks = ['x' * r for r in rule if r != 0]
        num_marks = sum(map(len, marks))
        queue = Queue()
        queue.put([[], marks, [' '] * (size - num_marks)])
        out = []
        while queue.qsize():
            curr = queue.get()
            if not curr[1] or not curr[2]:
                out += [''.join(curr[0] + curr[1] + curr[2])]
            else:
                queue.put([curr[0] + [curr[1][0]], curr[1][1:], curr[2]])
                queue.put([curr[0] + [curr[2][0]], curr[1], curr[2][1:]])
        valid_combos = sorted(filter(lambda x: self.checkRow(x, rule), set(out)))
        return valid_combos

    def checkState(self,state, rules):
        for i, row in enumerate(state):
            if not self.checkRow(row, rules[i]):
                return False
        return True

    def solve(self,top,left):
        #input = [map(lambda x: map(int, x), map(str.split, i.strip().split('\n'))) for i in input.split('-')]
        top = zip(*top)
        left = map(tuple, left)
        rules = map(lambda x: self.makeRows(x, len(top)), top)
        queue = PriorityQueue()
        queue.put([0, [], rules])
        count = 0
        list_sol = []
        while queue.qsize():
            count += 1
            curr = queue.get()
            if not self.checkState(zip(*curr[1]), left):
                continue
            if not curr[2] and self.checkState(zip(*curr[1]), left):
                for row in zip(*curr[1]):
                    print ''.join(row)
                    list_sol.append(row)
                break
            for r in curr[2][0]:
                queue.put([len(curr[2]) - 1, curr[1] + [r], curr[2][1:]])
        # print count, '/', reduce(lambda x, y: x * y, map(len, rules)), 1.0 * count / reduce(lambda x, y: x * y, map(len, rules))
        return list_sol

if __name__ == '__main__':
    top = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]
    left = [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
    obj = Solver()
    obj.solve(top,left)
