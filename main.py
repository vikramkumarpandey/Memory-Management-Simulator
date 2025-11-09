
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time

# Local modules
from algorithms import first_fit, best_fit, worst_fit, simulate_paging
from monitor import get_memory_stats, get_process_list, get_memory_values

# ------------------------------
# Memory Simulator (Animated)
# ------------------------------
class MemorySimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Management Simulator - Team CodeStorm (Animated)")
        self.geometry("1280x760")
        self.configure(bg="#f6f6f6")

        # --- Simulation State ---
        # Total capacities per block (fixed); memory_blocks holds remaining free
        self.block_total = [500, 200, 300, 600]
        self.memory_blocks = self.block_total.copy()   # remaining free in each block
        self.allocated_processes = []                  # list of tuples: (pid, size, block_index)
        self.block_rects = []                          # rectangles for visualization (outer)
        self.block_fill_rects = []                     # fill rectangles (used portion)
        self.block_labels = []                         # text labels
        self.selected_algorithm = tk.StringVar(value="First Fit")
        self.selected_os = tk.StringVar(value="Windows")
        self.auto_refresh = tk.BooleanVar(value=True)
        self.anim_speed = tk.DoubleVar(value=1.0)      # 0.5x..2x
        self.animating = False

        self.setup_ui()
        self.refresh_stats()
        self.start_auto_refresh()

    # ---------------- UI LAYOUT ----------------
    def setup_ui(self):
        top_frame = tk.Frame(self, bg="#f6f6f6", height=52)
        top_frame.pack(fill="x", padx=16, pady=8)
        top_frame.pack_propagate(False)

        tk.Label(top_frame, text="OS Mode:", font=("Segoe UI", 11), bg="#f6f6f6").pack(side="left")
        os_combo = ttk.Combobox(top_frame, textvariable=self.selected_os, state="readonly", width=26,
                                values=["Windows", "Linux (/proc + psutil)"])
        os_combo.pack(side="left", padx=(6, 16))

        ttk.Button(top_frame, text="Reload", command=self.refresh_stats).pack(side="left")

        ttk.Checkbutton(top_frame, text="Auto Refresh", variable=self.auto_refresh).pack(side="left", padx=10)

        tk.Label(top_frame, text="Step Speed:", font=("Segoe UI", 10), bg="#f6f6f6").pack(side="left", padx=(20,4))
        speed = ttk.Scale(top_frame, from_=0.5, to=2.0, variable=self.anim_speed, orient="horizontal")
        speed.pack(side="left", ipadx=40)

        # Main container
        main_frame = tk.Frame(self, bg="#f6f6f6")
        main_frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Left panel
        left_panel = tk.Frame(main_frame, width=420, bg="#f6f6f6")
        left_panel.pack(side="left", fill="y", padx=(0, 12))
        left_panel.pack_propagate(False)

        # Right panel
        right_panel = tk.Frame(main_frame, bg="#f6f6f6")
        right_panel.pack(side="left", fill="both", expand=True)

        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)

    def setup_left_panel(self, parent):
        # Memory Usage Section
        memory_frame = tk.LabelFrame(parent, text="Memory Usage", font=("Segoe UI", 11, "bold"),
                                     bg="#ffffff", padx=10, pady=10)
        memory_frame.pack(fill="x", pady=(0, 10))

        self.memory_info_label = tk.Label(memory_frame, text="", font=("Consolas", 10),
                                          bg="#ffffff", justify="left")
        self.memory_info_label.pack(anchor="w")

        # Memory visualization canvas
        self.memory_canvas = tk.Canvas(memory_frame, width=360, height=170, bg="#ffffff", highlightthickness=1)
        self.memory_canvas.pack(pady=10)

        # Swap Section
        swap_frame = tk.LabelFrame(parent, text="Swap", font=("Segoe UI", 11, "bold"),
                                   bg="#ffffff", padx=10, pady=10)
        swap_frame.pack(fill="x", pady=(0, 10))

        self.swap_info_label = tk.Label(swap_frame, text="", font=("Consolas", 10),
                                        bg="#ffffff", justify="left")
        self.swap_info_label.pack(anchor="w")

        # System Details Section
        system_frame = tk.LabelFrame(parent, text="System Details", font=("Segoe UI", 11, "bold"),
                                     bg="#ffffff", padx=10, pady=10)
        system_frame.pack(fill="x")

        self.system_info_label = tk.Label(system_frame, text="", font=("Consolas", 10),
                                          bg="#ffffff", justify="left")
        self.system_info_label.pack(anchor="w")

    def setup_right_panel(self, parent):
        # Process Monitor Section
        proc_frame = tk.LabelFrame(parent, text="Process Monitor", font=("Segoe UI", 11, "bold"),
                                   bg="#ffffff", padx=10, pady=10)
        proc_frame.pack(fill="x", pady=(0, 12))

        columns = ("PID", "Process Name", "Memory (MB)", "CPU %")
        self.process_tree = ttk.Treeview(proc_frame, columns=columns, show="headings", height=7)
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=140 if col != "Process Name" else 240, anchor="center")
        scrollbar = ttk.Scrollbar(proc_frame, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        self.process_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Memory Allocation Simulator Section
        sim_frame = tk.LabelFrame(parent, text="Memory Allocation Simulator (Animated)",
                                  font=("Segoe UI", 11, "bold"), bg="#ffffff", padx=10, pady=10)
        sim_frame.pack(fill="both", expand=True)

        # Algorithm selection
        algo_frame = tk.Frame(sim_frame, bg="#ffffff")
        algo_frame.pack(anchor="w", pady=(0, 12))
        tk.Label(algo_frame, text="Algorithm:", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(side="left", padx=(0, 8))
        for algo in ["First Fit", "Best Fit", "Worst Fit", "Paging"]:
            ttk.Radiobutton(algo_frame, text=algo, value=algo, variable=self.selected_algorithm).pack(side="left", padx=8)

        # Video-like steps log
        self.step_log = tk.Listbox(sim_frame, height=6, font=("Consolas", 10))
        self.step_log.pack(fill="x", pady=(0, 8))

        # Memory blocks visualization
        self.sim_canvas = tk.Canvas(sim_frame, width=720, height=120, bg="#f0f0f0", highlightthickness=1)
        self.sim_canvas.pack(pady=6)

        # Status label
        self.sim_status_label = tk.Label(sim_frame, text="Ready to simulate...",
                                         font=("Consolas", 10), bg="#ffffff", anchor="w")
        self.sim_status_label.pack(fill="x", pady=(4, 0))

        # Input + controls
        input_frame = tk.Frame(sim_frame, bg="#ffffff")
        input_frame.pack(anchor="w", pady=10)
        tk.Label(input_frame, text="Process ID:", bg="#ffffff").pack(side="left")
        self.process_id_entry = ttk.Entry(input_frame, width=12)
        self.process_id_entry.pack(side="left", padx=6)

        tk.Label(input_frame, text="Memory Size (MB):", bg="#ffffff").pack(side="left", padx=(12,0))
        self.memory_size_entry = ttk.Entry(input_frame, width=12)
        self.memory_size_entry.pack(side="left", padx=6)

        btn_frame = tk.Frame(sim_frame, bg="#ffffff")
        btn_frame.pack(anchor="w", pady=4)
        ttk.Button(btn_frame, text="Add Process", command=self.add_process).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Remove Process", command=self.remove_process).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Reset", command=self.reset_simulation).pack(side="left", padx=6)

        # Initial canvas draw
        self.draw_memory_blocks()

    # --------------- Drawing helpers -----------------
    def draw_memory_blocks(self):
        self.sim_canvas.delete("all")
        self.block_rects.clear()
        self.block_fill_rects.clear()
        self.block_labels.clear()

        block_width = 150
        block_height = 80
        start_x = 20
        start_y = 20
        gap = 14

        for i, total in enumerate(self.block_total):
            x1 = start_x + i * (block_width + gap)
            y1 = start_y
            x2 = x1 + block_width
            y2 = y1 + block_height

            # Outer rect
            rect = self.sim_canvas.create_rectangle(x1, y1, x2, y2, fill="#e8eef7", outline="#2b6cb0", width=2)
            self.block_rects.append(rect)

            # Used portion as overlay (left-to-right)
            remaining = self.memory_blocks[i]
            used = max(0, total - remaining)
            used_w = int((used / total) * block_width) if total > 0 else 0
            fill_rect = self.sim_canvas.create_rectangle(x1, y1, x1 + used_w, y2, fill="#4CAF50", outline="")
            self.block_fill_rects.append(fill_rect)

            # Label
            label = self.sim_canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                                text=f"Block {i+1}\n{remaining} / {total} MB",
                                                font=("Segoe UI", 10, "bold"))
            self.block_labels.append(label)

    def update_block_visual(self, idx, highlight=None):
        # highlight: None, 'checking', 'ok', 'fail'
        if idx < 0 or idx >= len(self.block_rects):
            return
        colors = {
            None: "#2b6cb0",
            "checking": "#ff9800",
            "ok": "#2e7d32",
            "fail": "#c62828"
        }
        self.sim_canvas.itemconfig(self.block_rects[idx], outline=colors.get(highlight, "#2b6cb0"))

        # Update fill & label to reflect remaining/used
        total = self.block_total[idx]
        remaining = self.memory_blocks[idx]
        used = max(0, total - remaining)
        block_width = 150
        block_height = 80
        # Get coordinates of outer rect to compute left x
        x1, y1, x2, y2 = self.sim_canvas.coords(self.block_rects[idx])
        used_w = int((used / total) * (x2 - x1)) if total > 0 else 0
        self.sim_canvas.coords(self.block_fill_rects[idx], x1, y1, x1 + used_w, y2)
        self.sim_canvas.itemconfig(self.block_labels[idx],
                                   text=f"Block {idx+1}\n{remaining} / {total} MB")

    def log(self, msg):
        self.step_log.insert(tk.END, msg)
        self.step_log.yview_moveto(1.0)

    # --------------- Stats refresh -----------------
    def draw_memory_chart(self):
        self.memory_canvas.delete("all")
        total, used, available = get_memory_values()
        if total <= 0:
            return
        cx, cy, r = 180, 80, 60
        used_pct = used / total
        avail_pct = available / total
        # Used arc
        self.memory_canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=0, extent=360*used_pct,
                                      fill="#FF5722", outline="#333333")
        # Available arc
        self.memory_canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=360*used_pct,
                                      extent=360*avail_pct, fill="#4CAF50", outline="#333333")
        self.memory_canvas.create_text(cx, cy-10, text=f"{used:.1f} GB", font=("Segoe UI", 12, "bold"))
        self.memory_canvas.create_text(cx, cy+10, text="Used", font=("Segoe UI", 10))

        # Legend
        self.memory_canvas.create_rectangle(270, 20, 290, 30, fill="#FF5722")
        self.memory_canvas.create_text(295, 25, text="Used", anchor="w", font=("Segoe UI", 9))
        self.memory_canvas.create_rectangle(270, 40, 290, 50, fill="#4CAF50")
        self.memory_canvas.create_text(295, 45, text="Available", anchor="w", font=("Segoe UI", 9))

    def refresh_stats(self):
        try:
            mem_info, swap_info, sys_info = get_memory_stats()
            self.memory_info_label.config(text=mem_info)
            self.swap_info_label.config(text=swap_info)
            self.system_info_label.config(text=sys_info)
            # Update process list
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)
            for process in get_process_list():
                self.process_tree.insert('', 'end', values=process)
            self.draw_memory_chart()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh stats: {str(e)}")

    def start_auto_refresh(self):
        def worker():
            while True:
                if self.auto_refresh.get():
                    self.after(0, self.refresh_stats)
                time.sleep(2)
        threading.Thread(target=worker, daemon=True).start()

    # --------------- Simulation actions -----------------
    def _sleep_step(self, seconds):
        # Use Tk's after to keep UI responsive
        ms = int(max(0.05, seconds / max(0.1, self.anim_speed.get())) * 1000)
        self.update_idletasks()
        self.after(ms)

    def animate_allocation(self, process_id, memory_size, algorithm):
        """Video-like, step-by-step animation of allocation."""
        if self.animating:
            self.log("Another animation is in progress. Please wait...")
            return False
        self.animating = True
        self.sim_status_label.config(text=f"Allocating {memory_size}MB for '{process_id}' using {algorithm}...")

        # Work on a copy to find candidate index the same way as algorithm
        alloc_idx = -1
        blocks_copy = self.memory_blocks.copy()
        if algorithm == "First Fit":
            res = first_fit(blocks_copy, [memory_size])
            alloc_idx = res[0]
        elif algorithm == "Best Fit":
            res = best_fit(blocks_copy, [memory_size])
            alloc_idx = res[0]
        elif algorithm == "Worst Fit":
            res = worst_fit(blocks_copy, [memory_size])
            alloc_idx = res[0]
        else:  # Paging (simplified)
            alloc_idx = 0  # dummy

        # Step through blocks visually
        for i in range(len(self.memory_blocks)):
            self.update_block_visual(i, highlight="checking")
            self.log(f"Checking Block {i+1}: Free {self.memory_blocks[i]}MB, Need {memory_size}MB")
            self._sleep_step(0.6)
            # Is this the chosen block?
            if i == alloc_idx and algorithm != "Paging":
                self.update_block_visual(i, highlight="ok")
                self.log(f"Block {i+1} selected ✔")
                self._sleep_step(0.5)
                # Animate fill growth
                target_remaining = self.memory_blocks[i] - memory_size
                if target_remaining < 0:
                    target_remaining = 0
                steps = 10
                start_remaining = self.memory_blocks[i]
                for s in range(1, steps+1):
                    # linear interpolation
                    new_remaining = int(start_remaining + (target_remaining - start_remaining) * (s/steps))
                    self.memory_blocks[i] = new_remaining
                    self.update_block_visual(i, highlight="ok")
                    self._sleep_step(0.12)
                self.allocated_processes.append((process_id, memory_size, i))
                self.sim_status_label.config(text=f"Process '{process_id}' allocated {memory_size}MB → Block {i+1}")
                self.animating = False
                return True
            else:
                # If not the chosen block, show fail if it can't fit
                if self.memory_blocks[i] < memory_size and algorithm != "Paging":
                    self.update_block_visual(i, highlight="fail")
                    self.log(f"Block {i+1}: Not enough space ✖")
                self._sleep_step(0.25)
                self.update_block_visual(i, highlight=None)

        # Paging path or failure
        if algorithm == "Paging":
            self.log("Paging simulation: allocation always succeeds (simplified).")
            self.sim_status_label.config(text=f"Process '{process_id}' paged (simulated).")
            self.allocated_processes.append((process_id, memory_size, 0))
            self.animating = False
            return True

        # No allocation
        self.sim_status_label.config(text=f"Failed to allocate {memory_size}MB for '{process_id}'")
        self.animating = False
        return False

    def add_process(self):
        try:
            process_id = self.process_id_entry.get().strip()
            memory_size = int(self.memory_size_entry.get().strip())
            if not process_id or memory_size <= 0:
                messagebox.showwarning("Invalid Input", "Please enter valid process ID and memory size")
                return

            algorithm = self.selected_algorithm.get()
            ok = self.animate_allocation(process_id, memory_size, algorithm)
            if ok:
                # Clear entries
                self.process_id_entry.delete(0, tk.END)
                self.memory_size_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Memory size must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add process: {str(e)}")

    def remove_process(self):
        process_id = simpledialog.askstring("Remove Process", "Enter Process ID to remove:")
        if not process_id:
            return
        for i, (pid, size, block) in enumerate(self.allocated_processes):
            if pid == process_id:
                # animate deallocation
                self.sim_status_label.config(text=f"Deallocating '{process_id}' ({size}MB) from Block {block+1}")
                self.update_block_visual(block, highlight="checking")
                self._sleep_step(0.5)
                target_remaining = self.memory_blocks[block] + size
                steps = 10
                start_remaining = self.memory_blocks[block]
                for s in range(1, steps+1):
                    new_remaining = int(start_remaining + (target_remaining - start_remaining) * (s/steps))
                    self.memory_blocks[block] = min(self.block_total[block], new_remaining)
                    self.update_block_visual(block, highlight="ok")
                    self._sleep_step(0.12)
                self.allocated_processes.pop(i)
                self.update_block_visual(block, highlight=None)
                self.sim_status_label.config(text=f"Process '{process_id}' removed and memory deallocated")
                return
        self.sim_status_label.config(text=f"Process '{process_id}' not found")

    def reset_simulation(self):
        if self.animating:
            messagebox.showinfo("Please wait", "Animation in progress. Try again after it completes.")
            return
        self.memory_blocks = self.block_total.copy()
        self.allocated_processes.clear()
        self.step_log.delete(0, tk.END)
        self.sim_status_label.config(text="Simulation reset - Ready to simulate...")
        self.draw_memory_blocks()

if __name__ == "__main__":
    try:
        app = MemorySimulatorApp()
        app.mainloop()
    except Exception as e:
        import traceback
        print("Error starting application:")
        print(traceback.format_exc())
