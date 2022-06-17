import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from maze_application import run


class Frame(tk.Frame):

    def __init__(self, container, **kwargs):
    
        super().__init__(container, **kwargs)
        
        
class App(tk.Tk):

    def __init__(self):
    
        super().__init__()
        self.window_setup()
        self.create_upper_below_frames()
        
    def quit_me(self):
        self.quit()
        self.destroy() 
        
    def window_setup(self):
        self.title("MazeRunner")
        self.iconbitmap("maze.ico")
        self.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.geometry("500x500+50+50")       
        
    def create_upper_below_frames(self):
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        upper_frame = Upper_Frame(self, width=500, bg="green", bd=5)
        upper_frame.grid(row=0, column=0, sticky="ns")
        
        start_frame = Start_Frame(self, upper_frame, width=300, bg="blue", bd=5)
        start_frame.grid(row=1, column=0, sticky="ns")
        start_frame.pack_propagate(False)
        
        
class Start_Frame(Frame):

    def __init__(self, container, upper_frame, **kwargs):
        super().__init__(container, **kwargs)
        self.upper_frame = upper_frame
        
        self.label = tk.Button(self, text="S T A R T", command=self.get_params_and_run)
        self.label.pack(expand=True, fill=tk.BOTH)        
        
    def get_params_and_run(self):
        row, col, algo, save_gen_gif, save_sol_gif = self.upper_frame.get_params()
        run(row, col, algo, save_gen_gif, save_sol_gif)

        
class Upper_Frame(Frame):

    def __init__(self, container, **kwargs):
    
        super().__init__(container, **kwargs)        
        self.create_gen_solve_frames()
        
    def create_gen_solve_frames(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.gen_frame = Generation_Frame(self, width=250, relief=tk.RIDGE, bd=5)
        self.gen_frame.grid(row=0, column=0, sticky="ns")
        self.gen_frame.grid_propagate(False)
        
        self.solve_frame = Solve_Frame(self, width=250, relief=tk.RIDGE, bd=5)
        self.solve_frame.grid(row=0, column=1, sticky="ns")
        self.solve_frame.grid_propagate(False)
        
    def get_params(self):
        return (
            self.gen_frame.row_IntVar.get(),
            self.gen_frame.col_IntVar.get(),
            self.solve_frame.algo,
            self.gen_frame.save_gen_gif,
            self.solve_frame.save_sol_gif
        )
        
        
class Generation_Frame(Frame):

    def __init__(self, container, **kwargs):
    
        super().__init__(container, **kwargs)
        self.save_gen_gif = 0
        
        for i in range(4):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
    
        self.generation_label = tk.Label(self, text="Generation", height=2, font=Font(family='Helvetica', size=14))
        self.generation_label.grid(row=0, column=0, pady=5, sticky="n")
        
        self.size_label = tk.Label(self, text="Size", font=Font(family='Helvetica', size=12))
        self.size_label.grid(row=1, column=0)
        
        self.row_label = tk.Label(self, text="row")
        self.row_label.grid(row=2, column=0, sticky="ne")
        
        self.row_IntVar = tk.IntVar(value=0)
        self.row_spin_box = tk.Spinbox(self, from_=0, to=15, width=5, textvariable=self.row_IntVar, wrap=True,
            font=Font(family='Helvetica', size=10)
        )
        self.row_spin_box.grid(row=2, column=1, sticky="nw")
        
        self.col_label = tk.Label(self, text="col")
        self.col_label.grid(row=2, column=2, sticky="ne")
        
        self.col_IntVar = tk.IntVar(value=0)
        self.col_spin_box = tk.Spinbox(self, from_=0, to=15, width=5, textvariable=self.col_IntVar, wrap=True,
            font=Font(family='Helvetica', size=10)
        )
        self.col_spin_box.grid(row=2, column=3, sticky="nw")

        def save_gen_gif_bool():
            if self.save_gen_gif:
                self.save_gen_gif = 0
            else:
                self.save_gen_gif = 1
        
        self.save_ckbtn = tk.Checkbutton(self, text='Save gif', command=save_gen_gif_bool, variable=self.save_gen_gif)
        self.save_ckbtn.grid(row=3, column=0, sticky="e")


        
class Solve_Frame(Frame):
    
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.save_sol_gif = 0
        self.algo = "DFS"
        
        for i in range(3):
            self.rowconfigure(i, weight=1)
        for j in range(2):
            self.columnconfigure(j, weight=1)
    
        self.solution_label = tk.Label(self, text="Solution", height=2, font=Font(family='Helvetica', size=14))
        self.solution_label.grid(row=0, column=0, pady=5, sticky="n")
        
        self.algo_label = tk.Label(self, text="Algo", font=Font(family='Helvetica', size=12))
        self.algo_label.grid(row=1, column=0, sticky="nw")
        
        def algo_var_changed(event):
            self.algo = algo_var.get()

        algo_var = tk.StringVar()
        self.algo_combobox = ttk.Combobox(self, textvariable=algo_var)
        self.algo_combobox["value"] = ("DFS", "BFS", "A*")
        self.algo_combobox.set("DFS")
        self.algo_combobox.bind('<<ComboboxSelected>>', algo_var_changed)
        self.algo_combobox.grid(row=1, column=0, sticky="e")
        
        def save_sol_gif_bool():
            if self.save_sol_gif:
                self.save_sol_gif = 0
            else:
                self.save_sol_gif = 1

        self.save_ckbtn = tk.Checkbutton(self, text='Save gif', command=save_sol_gif_bool, variable=self.save_sol_gif)
        self.save_ckbtn.grid(row=2, column=0)
        self.save_ckbtn["variable"]=1
        
def main():
 
    app = App()
    app.mainloop()

    
if __name__ == "__main__":
    main()
    