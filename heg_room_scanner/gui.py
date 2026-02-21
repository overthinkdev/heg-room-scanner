import tkinter as tk
from tkinter import ttk
import threading
import webbrowser
from heg_room_scanner.core import scan_rooms
from heg_room_scanner.utils import format_room_display, display_to_query

SPINNER_SIZE = 30
SPINNER_WIDTH = 4
SPINNER_SPEED = 5

class HEGRoomScannerApp:

    def __init__(self, root):
        self.root = root
        self.spinner_angle = 0
        self.animation_running = False

        self.root.title("HEG Room Scanner")
        self.root.geometry("800x600")

        self.progress_var = tk.DoubleVar()
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(2, weight=1)

        scan_button = ttk.Button(
            top_frame,
            text="Lancer le scan",
            command=lambda: threading.Thread(target=self.update_gui).start()
        )
        scan_button.grid(row=0, column=0, padx=(0, 10))

        self.spinner_canvas = tk.Canvas(
            top_frame,
            width=SPINNER_SIZE,
            height=SPINNER_SIZE,
            highlightthickness=0
        )
        self.spinner_canvas.grid(row=0, column=1, padx=(0, 10))

        self.status_label = ttk.Label(
            top_frame,
            text="Prêt",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.grid(row=0, column=2, sticky="w")

        progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100
        )
        progress_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        notebook = ttk.Notebook(self.root)
        notebook.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        free_frame = ttk.Frame(notebook)
        notebook.add(free_frame, text="Salles libres")

        self.free_tree = ttk.Treeview(free_frame)
        self.free_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.free_tree.bind("<Double-Button-1>", self.open_room_link)

        occ_frame = ttk.Frame(notebook)
        notebook.add(occ_frame, text="Salles occupées")

        self.occ_tree = ttk.Treeview(occ_frame)
        self.occ_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.occ_tree.bind("<Double-Button-1>", self.open_room_link)

        log_frame = ttk.LabelFrame(self.root, text="Debug Log, Made with love by Rami <3", padding=10)
        log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=8, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def animate_spinner(self):
        if self.animation_running:
            self.spinner_canvas.delete("all")
            self.spinner_canvas.create_arc(
                2, 2,
                SPINNER_SIZE - 2,
                SPINNER_SIZE - 2,
                start=self.spinner_angle,
                extent=270,
                style="arc",
                width=SPINNER_WIDTH
            )
            self.spinner_angle = (self.spinner_angle + SPINNER_SPEED) % 360
            self.root.after(50, self.animate_spinner)
        else:
            self.spinner_canvas.delete("all")

    def update_gui(self):
        for tree in (self.free_tree, self.occ_tree):
            for item in tree.get_children():
                tree.delete(item)

        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state="disabled")

        self.status_label.config(text="Scan en cours...")
        self.progress_var.set(0)

        self.spinner_angle = 0
        self.animation_running = True
        self.animate_spinner()

        free_rooms, occupied_rooms = scan_rooms(
            progress_callback=self.progress_var.set,
            log_callback=self.log_message
        )

        self.animation_running = False
        self.status_label.config(text="Scan terminé")

        self.populate_tree(self.free_tree, free_rooms)
        self.populate_tree(self.occ_tree, occupied_rooms)

    def populate_tree(self, tree, rooms):
        floors = {}
        for room in rooms:
            floor = int(room[1]) if room[1].isdigit() else 0
            floors.setdefault(floor, []).append(room)

        for floor in sorted(floors):
            parent = tree.insert("", tk.END, text=f"Étage {floor}")
            for room in sorted(floors[floor]):
                tree.insert(parent, tk.END, text=format_room_display(room))

    def open_room_link(self, event):
        widget = event.widget
        item = widget.identify('item', event.x, event.y)
        if widget.get_children(item) == ():
            room_display = widget.item(item, "text")
            room_query = display_to_query(room_display)
            url = f"https://www.hesge.ch/heg/salle/{room_query}"
            webbrowser.open_new(url)
