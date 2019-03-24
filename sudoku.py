from copy import deepcopy
import csv


class Sudoku:
    a = [[None for _ in range(9)] for _ in range(9)]
    input_path = 'input.csv'
    output_path = 'output.csv'
    result = ''

    def __init__(self, a=None, monitor=None):
        if a is not None:
            self.a = a
        else:
            self.__init_from_csv()
        self.monitor = monitor

    def __repr__(self):
        r = ""
        for i in range(9):
            for j in range(9):
                r += str(self.a[i][j]) + ' '
                if j % 3 == 2:
                    r += '  '
            r += '\n'
            if i % 3 == 2:
                r += '\n'
        return r

    @staticmethod
    def cluster(i, j):
        i_cluster = i // 3 * 3
        j_cluster = j // 3 * 3
        i_indexes = [i_cluster + k for k in [0, 1, 2]]
        j_indexes = [j_cluster + k for k in [0, 1, 2]]
        cluster = []
        for ii in i_indexes:
            for jj in j_indexes:
                cluster.append((ii, jj))
        return cluster

    def cluster_by_i_j(self, i, j):
        i_cluster = i // 3 * 3
        j_cluster = j // 3 * 3
        i_indexes = [i_cluster + k for k in [0, 1, 2]]
        j_indexes = [j_cluster + k for k in [0, 1, 2]]
        cluster = []
        for ii in i_indexes:
            for jj in j_indexes:
                cluster.append(self.a[ii][jj])
        return cluster

    def row(self, i):
        return self.a[i]

    def column(self, j):
        return [self.a[i][j] for i in range(9)]

    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.a[i][j] is None:
                    return False
        return True

    def is_empty(self):
        for i in range(9):
            for j in range(9):
                if self.a[i][j] is not None:
                    return False
        return True

    def variants(self, i, j):
        variants = []
        for v in range(1, 10):
            if v not in self.cluster_by_i_j(i, j) and v not in self.row(i) and v not in self.column(j):
                variants.append(v)
        return variants

    def iteration(self, i, j):
        variants = self.variants(i, j)
        if len(variants) == 0:
            self.result = 'Unresolved!'
            print(f'Unresolved {i} {j}')
            return False
        elif len(variants) == 1:
            self.a[i][j] = variants[0]
            return True
        if len(variants) > 1:
            # for ii in range(9):
            #     for jj in range(9):
            #         if ii != i and jj != j:
            #             for v in variants:
            #                 if v in self.variants(ii, jj):
            #                     variants.remove(v)
            # if len(variants) == 1:
            #     self.a[i][j] = variants[0]
            #     print('CASE WORK')
            #     return True

            row_variants = []
            column_variants = []
            cluster_variants = []
            for jj in range(9):
                if jj != j:
                    if self.a[i][jj] is None:
                        row_variants.extend(self.variants(i, jj))
                    else:
                        row_variants.append(self.a[i][jj])
            for ii in range(9):
                if ii != i:
                    if self.a[ii][j] is None:
                        column_variants.extend(self.variants(ii, j))
                    else:
                        column_variants.append(self.a[ii][j])
            for ii, jj in self.cluster(i, j):
                if not (ii == i and jj == j):
                    if self.a[ii][jj] is None:
                        cluster_variants.extend(self.variants(ii, jj))
                    else:
                        cluster_variants.append(self.a[ii][jj])
            for method in (row_variants, cluster_variants, column_variants):
                v = set(variants) - set(method)
                if len(v) == 1:
                    self.a[i][j] = v.pop()
                    return True
        return True

    def resolve(self, deep_mode=True, tree_story=''):
        while not self.is_full():
            success = False
            for i in range(9):
                for j in range(9):
                    if self.a[i][j] is None:
                        resolvable = self.iteration(i, j)
                        if not resolvable:
                            return False
                        if self.a[i][j] is not None:
                            success = True
            if not success and not deep_mode:
                self.result = 'Partial solution. Try deep mode.'
                self.__save_to_csv()
                return False
            elif not success:
                tree = {i: [] for i in range(10)}
                for i in range(9):
                    for j in range(9):
                        if self.a[i][j] is None:
                            i_j_variants = self.variants(i, j)
                            tree[len(i_j_variants)].append({
                                'i': i,
                                'j': j,
                                'choices': i_j_variants
                            })
                source = deepcopy(self.a)
                for c in range(9):
                    variants = tree[c]
                    for v in variants:
                        t = 1
                        for choice in v['choices']:
                            tree_story += ' => ' if tree_story else ''
                            tree_story += f'({t}/{len(v["choices"])})'
                            t += 1
                            print(tree_story)
                            self.a = deepcopy(source)
                            self.a[v['i']][v['j']] = choice
                            if self.resolve():
                                return True
        self.result = 'Resolved successfully!'
        print('Resolved successfully!')
        self.__save_to_csv()
        return True

    def monitor_state(self):
        if self.monitor:
            try:
                from tkinter import END
                for i in range(9):
                    for j in range(9):
                        self.monitor[i][j].delete(0, END)
                        if self.a[i][j]:
                            self.monitor[i][j].insert(0, self.a[i][j])
            except Exception: pass

    def __init_from_csv(self):
        with open(self.input_path, 'r') as f:
            reader = csv.reader(f)
            cells = []
            for row in reader:
                cells.append([])
                for cell in row:
                    cells[-1].append(cell)
            for i in range(9):
                for j in range(9):
                    value = None
                    try:
                        value = int(cells[i][j])
                        if value < 1 or value > 9:
                            value = None
                    except ValueError:
                        pass
                    self.a[i][j] = value

    def __save_to_csv(self):
        prepared = deepcopy(self.a)
        for i in range(len(prepared)):
            for j in range(len(prepared[i])):
                prepared[i][j] = str(prepared[i][j]) if prepared[i][j] else '_'

        with open(self.output_path, 'w') as f:
            f.write('\n'.join([','.join(row) for row in prepared]))


test1 = [
    [6, 3, None, 5, 1, 2, 8, 4, 7],
    [8, 7, 1, 9, None, 3, 2, 6, 5],
    [2, None, 5, None, None, 7, None, 1, 9],
    [7, None, 4, None, 6, None, None, 3, None],
    [None, 8, 6, 4, 2, None, 9, None, 1],
    [5, None, 2, None, 3, 1, None, 8, 4],
    [4, 2, 7, None, 9, None, 1, 5, None],
    [None, 6, None, None, 5, None, 7, 2, 3],
    [1, 5, 3, 2, 7, None, 4, None, 6],
]
test2 = [
    [None, 8, None, None, None, None, 2, None, None],
    [None, None, None, None, 8, 4, None, 9, None],
    [None, None, 6, 3, 2, None, None, 1, None],
    [None, 9, 7, None, None, None, None, 8, None],
    [8, None, None, 9, None, 3, None, None, 2],
    [None, 1, None, None, None, None, 9, 5, None],
    [None, 7, None, None, 4, 5, 8, None, None],
    [None, 3, None, 7, 1, None, None, None, None],
    [None, None, 8, None, None, None, None, 4, None],
]
test3 = [
    [2, None, 8, 9, 3, 6, None, None, 5],
    [4, None, 9, None, None, 1, 3, 8, 2],
    [None, 7, 3, 4, 8, 2, 1, 6, None],
    [None, 5, 7, 2, 9, None, 6, None, 4],
    [None, 9, 4, 6, None, 3, 5, 2, None],
    [None, 3, None, 7, None, 5, 9, 1, 8],
    [3, None, 1, None, 5, 9, None, 7, 6],
    [9, 4, None, None, 2, None, None, 5, 1],
    [7, 8, 5, 1, None, 4, 2, None, 3],
]
test4 = [
    [None, 1, 4, None, 6, None, 2, None, None],
    [None, None, 5, 2, None, 4, None, None, 6],
    [3, None, None, 5, None, None, None, 7, 8],
    [None, 3, None, None, None, None, 1, 6, None],
    [6, None, None, None, 1, None, None, None, 5],
    [None, 5, 2, None, None, None, None, 4, None],
    [8, 6, None, None, None, 5, None, None, 2],
    [5, None, None, 7, None, 9, 6, None, None],
    [None, None, 1, None, 3, None, 5, 9, None],
]
