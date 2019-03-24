import csv
from tkinter import Frame, Tk, BOTH, LEFT, X, N, Text, RIGHT, CENTER, TOP, END
from tkinter.ttk import Button, Style, Label, Entry
from sudoku import Sudoku
from os import path


class GUI(Frame):
    entries = []
    values = [[None for _ in range(9)] for _ in range(9)]
    report_label = None

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        self.center_window()

    def init_ui(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=True)

        Style().configure("TButton", padding=(0, 5, 0, 5),
                          font='serif 16')

        buttons_frame = Frame(self, width=100)
        buttons_frame.pack(side=LEFT)

        action_button1 = Button(buttons_frame, text="Resolve", command=self.resolve)
        action_button1.pack(side=TOP, padx=5, pady=5)
        action_button2 = Button(buttons_frame, text="Deep resolve", command=self.deep_resolve)
        action_button2.pack(side=TOP, padx=5, pady=5)
        sample1_button = Button(buttons_frame, text="Sample1", command=self.sample1)
        sample1_button.pack(side=TOP, padx=5, pady=5)
        sample2_button = Button(buttons_frame, text="Sample2", command=self.sample2)
        sample2_button.pack(side=TOP, padx=5, pady=5)
        sample3_button = Button(buttons_frame, text="Sample3", command=self.sample3)
        sample3_button.pack(side=TOP, padx=5, pady=5)

        entries_frame = Frame(self)
        entries_frame.pack(side=LEFT)

        labels_frame = Frame(entries_frame)
        labels_frame.pack(side=TOP)

        in_label = Label(labels_frame, width=20, text='input')
        in_label.pack(side=LEFT, padx=70)

        out_label = Label(labels_frame, width=20, text='output')
        out_label.pack(side=LEFT, padx=10)

        for i in range(9):
            self.entries.append([])
            curr_frame = Frame(entries_frame)
            curr_frame.pack(padx=10)
            if i % 3 == 2:
                empty = Frame(entries_frame)
                empty.pack(fill=X, pady=4)
            for j in range(18):
                entry = Entry(curr_frame, width=2)
                entry.pack(side=LEFT, padx=0, pady=0)
                self.entries[-1].append(entry)
                if j % 3 == 2:
                    pad = '          ' if j % 9 == 8 else ''
                    empty = Label(curr_frame, text=pad)
                    empty.pack(side=LEFT)

        report_frame = Frame(entries_frame)
        report_frame.pack(side=TOP)
        self.report_label = Label(report_frame, text='result')
        self.report_label.pack(side=LEFT)

    def center_window(self):
        w = 550
        h = 270

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def resolve(self):
        self.action(deep_mode=False)

    def deep_resolve(self):
        self.action(deep_mode=True)

    def action(self, deep_mode):
        self.get_input()
        monitor = [e[9:] for e in self.entries]
        sudoku = Sudoku(self.values, monitor)
        if not sudoku.is_empty():
            sudoku.resolve(deep_mode)
            self.set_sample_or_response(sudoku.a)
            self.report_label['text'] = sudoku.result

    def get_input(self):
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value:
                    try:
                        self.values[i][j] = int(value)
                        if int(value) > 9 or int(value) < 1:
                            raise ValueError
                    except ValueError:
                        self.values[i][j] = None
                        self.entries[i][j].delete(0, END)
                else:
                    self.values[i][j] = None

    def sample1(self):
        inp = self.get_from_csv(path.join('samples', 'input1.csv'))
        self.set_sample_or_response(inp, True)

    def sample2(self):
        inp = self.get_from_csv(path.join('samples', 'input2.csv'))
        self.set_sample_or_response(inp, True)

    def sample3(self):
        inp = self.get_from_csv(path.join('samples', 'input3.csv'))
        self.set_sample_or_response(inp, True)

    def set_sample_or_response(self, values, is_sample=False):
        start = 0 if is_sample else 9
        for i in range(9):
            for j in range(9):
                self.entries[i][start+j].delete(0, END)
                value = str(values[i][j]) if values[i][j] is not None else ''
                self.entries[i][start+j].insert(0, value)

    @staticmethod
    def get_from_csv(path):
        res = [[None for _ in range(9)] for _ in range(9)]
        with open(path, 'r') as f:
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
                    res[i][j] = value
        return res


def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
else:
    main()
