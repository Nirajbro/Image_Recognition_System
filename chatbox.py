import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import audit_log

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatBoxApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("💬 Case Notes Manager")

        # --- NEW: Dynamic Window Sizing & Center on Screen ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.6)
        height = int(screen_height * 0.7)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Allow resizing so content stretches
        self.resizable(True, True)

        self.grab_set()
        self.focus_force()
        self.current_criminal_id = None
        self.init_db()
        self.build_ui()
        self.load_criminals()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_db(self):
        conn = sqlite3.connect('criminals.db')
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS case_notes
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           criminal_id
                           INTEGER,
                           officer_name
                           TEXT,
                           note_text
                           TEXT,
                           timestamp
                           TEXT,
                           FOREIGN
                           KEY
                       (
                           criminal_id
                       ) REFERENCES criminals
                       (
                           id
                       ) ON DELETE CASCADE
                           )
                       ''')
        conn.commit()
        conn.close()

    def build_ui(self):
        # Header stretches horizontally
        header = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=0)
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="💬 Case Investigation Notes", font=ctk.CTkFont(size=26, weight="bold"),
                     text_color="#e94560").pack(pady=(20, 5))
        ctk.CTkLabel(header, text="Timestamped remarks with audit trail", font=ctk.CTkFont(size=13),
                     text_color="gray").pack(pady=(0, 15))

        # Main Form Frame - fills and expands to take up available space
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(pady=15, padx=30, fill="both", expand=True)

        ctk.CTkLabel(main, text="Select Criminal:", font=ctk.CTkFont(size=15)).grid(row=0, column=0, sticky="w",
                                                                                    pady=10)
        self.dropdown = ctk.CTkOptionMenu(main, values=["Loading..."], command=self.on_select, height=40,
                                          fg_color="#0f0f1a", button_color="#3b2a4d")
        self.dropdown.grid(row=0, column=1, pady=10, padx=(15, 0), sticky="ew")

        ctk.CTkLabel(main, text="Officer Name:", font=ctk.CTkFont(size=15)).grid(row=1, column=0, sticky="w", pady=10)
        self.officer_entry = ctk.CTkEntry(main, placeholder_text="Your name", height=40)
        self.officer_entry.grid(row=1, column=1, pady=10, padx=(15, 0), sticky="ew")

        ctk.CTkLabel(main, text="Investigation Note:", font=ctk.CTkFont(size=15)).grid(row=2, column=0, sticky="nw",
                                                                                       pady=10)
        self.note_box = ctk.CTkTextbox(main, height=150, corner_radius=10, fg_color="#0f0f1a")
        self.note_box.grid(row=2, column=1, pady=10, padx=(15, 0), sticky="ew")

        bf = ctk.CTkFrame(main, fg_color="transparent")
        bf.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")
        bf.grid_columnconfigure(0, weight=1);
        bf.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(bf, text="💾 Save Note", command=self.save_note, height=45, fg_color="#e94560").grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          sticky="ew")
        ctk.CTkButton(bf, text="🔄 Refresh", command=self.refresh_notes, height=45, fg_color="#1b4f72").grid(row=0,
                                                                                                            column=1,
                                                                                                            padx=10,
                                                                                                            sticky="ew")

        # Notes display area - will stretch to fill the rest of the window
        self.notes_display = ctk.CTkScrollableFrame(main, fg_color="#0f0f1a", corner_radius=10)
        self.notes_display.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky="nsew")
        main.grid_columnconfigure(1, weight=1);
        main.grid_rowconfigure(4, weight=1)

    def load_criminals(self):
        conn = sqlite3.connect('criminals.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM criminals ORDER BY name')
        records = cursor.fetchall()
        conn.close()
        if not records:
            self.dropdown.configure(values=["No criminals"])
            self.dropdown.set("No criminals")
            return
        options = [f"{r[0]}: {r[1]}" for r in records]
        self.dropdown.configure(values=options)
        self.dropdown.set(options[0])
        self.on_select(options[0])

    def on_select(self, val):
        if val == "No criminals": return
        self.current_criminal_id = int(val.split(":")[0])
        self.refresh_notes()

    def save_note(self):
        if not self.current_criminal_id:
            messagebox.showwarning("No Selection", "Select a criminal.")
            return
        note = self.note_box.get("1.0", "end-1c").strip()
        if not note:
            messagebox.showwarning("Empty", "Write a note.")
            return
        officer = self.officer_entry.get().strip() or "Unknown"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect('criminals.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO case_notes (criminal_id, officer_name, note_text, timestamp) VALUES (?,?,?,?)',
                       (self.current_criminal_id, officer, note, ts))
        conn.commit()
        conn.close()
        audit_log.log_audit(officer, "ADD_NOTE", target_id=self.current_criminal_id, details=f"Note: {note[:50]}...")
        messagebox.showinfo("✅ Success", "Note saved.")
        self.note_box.delete("1.0", "end")
        self.refresh_notes()

    def refresh_notes(self):
        for w in self.notes_display.winfo_children(): w.destroy()
        if not self.current_criminal_id:
            ctk.CTkLabel(self.notes_display, text="Select a criminal.", text_color="gray").pack(pady=30)
            return
        conn = sqlite3.connect('criminals.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT officer_name, note_text, timestamp FROM case_notes WHERE criminal_id = ? ORDER BY timestamp DESC',
            (self.current_criminal_id,))
        notes = cursor.fetchall()
        conn.close()
        if not notes:
            ctk.CTkLabel(self.notes_display, text="No notes yet.", text_color="gray").pack(pady=30)
            return
        for officer, note, ts in notes:
            card = ctk.CTkFrame(self.notes_display, fg_color="#1e1e32", corner_radius=8)
            card.pack(fill="x", pady=6, padx=5)
            hf = ctk.CTkFrame(card, fg_color="transparent")
            hf.pack(fill="x", padx=10, pady=(5, 0))
            ctk.CTkLabel(hf, text=f"🕒 {ts}", font=ctk.CTkFont(size=11), text_color="#a8d8ea").pack(side="left")
            ctk.CTkLabel(hf, text=f"👤 {officer}", font=ctk.CTkFont(size=11, weight="bold"), text_color="#e94560").pack(
                side="right")
            # Note: Added a dynamically calculated wraplength to prevent notes from breaking weirdly on wide screens
            note_label = ctk.CTkLabel(card, text=note, font=ctk.CTkFont(size=13), text_color="white", wraplength=550)
            note_label.pack(anchor="w", padx=10, pady=(5, 10))

    def on_close(self):
        self.grab_release()
        self.destroy()