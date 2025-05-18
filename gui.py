import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import sys
from tree_operations import insert_bst_iter, insert_avl_iter
from visualization import plot_tree, setup_plot_for_trees
from complexity_analysis import bst_frequency_analysis, avl_frequency_analysis, space_analysis

class WindowManager:
    active_windows = set()
    
    @classmethod
    def add_window(cls, window):
        cls.active_windows.add(window)
        
    @classmethod
    def remove_window(cls, window):
        if window in cls.active_windows:
            cls.active_windows.remove(window)
        if not cls.active_windows:
            # Check if this is the main Tk instance before exiting
            # This might need refinement if we have non-window objects in active_windows
            # For now, assuming all are Tk or Toplevel
            is_main_tk_closed = True
            for win in cls.active_windows:
                if isinstance(win, tk.Tk): # Check if any tk.Tk instance is still alive
                    is_main_tk_closed = False
                    break
            if is_main_tk_closed or not any(isinstance(w, tk.Tk) for w in cls.active_windows if w.winfo_exists()):
                 # Check if the root window itself is being closed or no other main window exists
                if isinstance(window, tk.Tk) or not any(isinstance(w, tk.Tk) for w in cls.active_windows if w.winfo_exists()):
                    sys.exit(0)


class InputWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BST vs AVL Tree Analysis - Input")
        WindowManager.add_window(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        window_width = 500 # Increased width for more fields
        window_height = 400 # Increased height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_input_section(main_frame)
        
        self.all_roots_bst = []
        self.all_roots_avl = []
        self.all_values_lists = []
        self.all_node_counts = []
        
    def on_closing(self):
        is_root = self.root.master is None # Check if it's the root window
        WindowManager.remove_window(self.root)
        self.root.destroy()
        if is_root and not WindowManager.active_windows: # Extra check if it was the root
            sys.exit(0)

    def create_input_section(self, parent):
        row_idx = 0
        ttk.Label(parent, text="Number of Tree Pairs:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.num_tree_pairs_var = tk.StringVar(value="1")
        ttk.Entry(parent, textvariable=self.num_tree_pairs_var).grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(parent, text="Node counts for each pair (e.g., 10,7,12):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.node_counts_var = tk.StringVar(value="10")
        ttk.Entry(parent, textvariable=self.node_counts_var).grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1
        
        self.input_type = tk.StringVar(value="random")
        ttk.Radiobutton(parent, text="Random Values", variable=self.input_type, 
                       value="random").grid(row=row_idx, column=0, sticky="w", pady=5)
        ttk.Radiobutton(parent, text="Manual Input", variable=self.input_type, 
                       value="manual").grid(row=row_idx, column=1, sticky="w", pady=5)
        row_idx += 1
        
        ttk.Label(parent, text="Manual values (e.g., 1,2,3; 4,5; 6,7,8):").grid(row=row_idx, column=0, columnspan=2, sticky="w", pady=5)
        self.manual_values_str_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.manual_values_str_var, width=50).grid(row=row_idx+1, column=0, columnspan=2, sticky="ew", pady=5)
        row_idx += 2
        
        ttk.Button(parent, text="Generate Trees", command=self.generate_trees).grid(row=row_idx, column=0, columnspan=2, pady=20)
        
        parent.grid_columnconfigure(1, weight=1) # Allow entry fields to expand

    def generate_trees(self):
        try:
            num_pairs_str = self.num_tree_pairs_var.get()
            if not num_pairs_str.isdigit() or int(num_pairs_str) <= 0:
                raise ValueError("Number of Tree Pairs must be a positive integer.")
            num_pairs = int(num_pairs_str)

            node_counts_str = self.node_counts_var.get().split(',')
            self.all_node_counts = []
            for nc_str in node_counts_str:
                nc_str = nc_str.strip()
                if not nc_str.isdigit() or int(nc_str) <= 0:
                    raise ValueError("Node counts must be positive integers.")
                self.all_node_counts.append(int(nc_str))

            if len(self.all_node_counts) != num_pairs:
                raise ValueError(f"Number of node counts ({len(self.all_node_counts)}) does not match specified Number of Tree Pairs ({num_pairs}).")

            self.all_values_lists = []
            if self.input_type.get() == "random":
                for count in self.all_node_counts:
                    self.all_values_lists.append(random.sample(range(1, 200), count))
            else: # Manual input
                manual_data_for_trees_str = self.manual_values_str_var.get().split(';')
                if len(manual_data_for_trees_str) != num_pairs:
                    raise ValueError(f"Number of manually provided tree data sets ({len(manual_data_for_trees_str)}) does not match Number of Tree Pairs ({num_pairs}).")
                
                for i, tree_data_str in enumerate(manual_data_for_trees_str):
                    current_tree_values_str = tree_data_str.strip().split(',')
                    current_tree_values = []
                    if all(s.strip() == "" for s in current_tree_values_str) and self.all_node_counts[i] == 0: # Allow empty for 0 nodes
                         current_tree_values = []
                    elif any(s.strip() == "" for s in current_tree_values_str) and self.all_node_counts[i] > 0 :
                        raise ValueError(f"Empty value found in manual input for tree pair {i+1}.")
                    else:
                        for val_str in current_tree_values_str:
                            val_str = val_str.strip()
                            if not val_str.isdigit(): # Or more robust parsing if non-integers are allowed
                                raise ValueError(f"Invalid value '{val_str}' in manual input for tree pair {i+1}. Values must be integers.")
                            current_tree_values.append(int(val_str))
                    
                    if len(current_tree_values) != self.all_node_counts[i]:
                        raise ValueError(f"Number of values for tree pair {i+1} ({len(current_tree_values)}) does not match specified node count ({self.all_node_counts[i]}).")
                    self.all_values_lists.append(current_tree_values)
            
            self.all_roots_bst = []
            self.all_roots_avl = []
            for values_list in self.all_values_lists:
                current_root_bst = None
                current_root_avl = None
                for val in values_list:
                    current_root_bst = insert_bst_iter(current_root_bst, val)
                    current_root_avl = insert_avl_iter(current_root_avl, val)
                self.all_roots_bst.append(current_root_bst)
                self.all_roots_avl.append(current_root_avl)
            
            # For now, VisualizationWindow and AnalysisWindow will need adaptation.
            # Let's assume they are adapted to take lists of roots/values/counts.
            # This will likely cause errors until visualization.py is updated.
            if self.all_roots_bst: # Check if any trees were generated
                 VisualizationWindow(self.root, self.all_roots_bst, self.all_roots_avl, self.all_values_lists, self.all_node_counts)
            else:
                messagebox.showinfo("No Trees", "No tree data to visualize.")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

class VisualizationWindow:
    def __init__(self, parent, all_roots_bst, all_roots_avl, all_values_lists, all_node_counts):
        self.window = tk.Toplevel(parent)
        self.window.title("Tree Visualization (Multiple Pairs - Needs Update)")
        self.window.state('zoomed')
        WindowManager.add_window(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.all_roots_bst = all_roots_bst
        self.all_roots_avl = all_roots_avl
        self.all_values_lists = all_values_lists
        self.all_node_counts = all_node_counts
        
        # --- VISUALIZATION LOGIC NEEDS COMPLETE OVERHAUL ---
        # For now, let's just display a message or the first tree pair.
        if not self.all_roots_bst:
            ttk.Label(self.window, text="No trees to display.").pack(padx=20, pady=20)
            return

        # TEMPORARY: Display only the first tree pair
        root_bst_first = self.all_roots_bst[0]
        root_avl_first = self.all_roots_avl[0]
        values_first = self.all_values_lists[0]
        # node_count_first = self.all_node_counts[0] # This is an int, setup_plot_for_trees expects root nodes

        fig, ax1, ax2, node_count_viz = setup_plot_for_trees(root_bst_first, root_avl_first) # setup_plot_for_trees uses roots to count
        
        plot_tree(ax1, root_bst_first, x=0, y=0, dx=fig.get_figwidth()*30, node_count=node_count_viz)
        plot_tree(ax2, root_avl_first, x=0, y=0, dx=fig.get_figwidth()*30, node_count=node_count_viz)
        
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        value_label = ttk.Label(button_frame, 
                              text=f"Input Values (First Pair): {', '.join(map(str, values_first))}")
        value_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Show Complexity Analysis", 
                  command=self.show_analysis).pack(side=tk.RIGHT, padx=5)
        # --- END TEMPORARY DISPLAY ---
        
    def on_closing(self):
        is_root = self.window.master.master is None # Check if parent is the root window
        WindowManager.remove_window(self.window)
        self.window.destroy()
        # if is_root and not WindowManager.active_windows: # sys.exit is now handled more centrally
        #     sys.exit(0)

    def show_analysis(self):
        # AnalysisWindow will also need adaptation for multiple counts
        if self.all_node_counts:
            AnalysisWindow(self.window, self.all_node_counts) # Pass all counts
        else:
            messagebox.showinfo("No Analysis", "No node counts available for analysis.")


class AnalysisWindow:
    def __init__(self, parent, all_node_counts): # Modified to accept list of counts
        self.window = tk.Toplevel(parent)
        self.window.title("Complexity Analysis (Multiple Sets - Needs Update)")
        WindowManager.add_window(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        window_width = 800
        window_height = 600
        # ... (centering code as before) ...
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=80, height=30)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        analysis_output_all = ""
        import io
        from contextlib import redirect_stdout

        if not all_node_counts:
            analysis_output_all = "No node counts provided for analysis."
        else:
            for i, n_count in enumerate(all_node_counts):
                analysis_output_all += f"--- Analysis for Tree Pair {i+1} (Node count: {n_count}) ---\\n"
                with io.StringIO() as buf, redirect_stdout(buf):
                    bst_frequency_analysis(n_count)
                    avl_frequency_analysis(n_count)
                    space_analysis(n_count)
                    analysis_output_all += buf.getvalue() + "\\n\\n"
        
        self.text_area.insert(tk.END, analysis_output_all)
        self.text_area.configure(state='disabled')
        
    def on_closing(self):
        is_root = self.window.master.master.master is None # Check if grandparent is the root
        WindowManager.remove_window(self.window)
        self.window.destroy()
        # if is_root and not WindowManager.active_windows:
        #     sys.exit(0)

def main():
    app = InputWindow()
    app.root.mainloop()

if __name__ == "__main__":
    main() 