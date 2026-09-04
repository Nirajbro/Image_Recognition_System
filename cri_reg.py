import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import json
from PIL import Image
import security
import audit_log

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CriminalRegistrationApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("📝 Criminal Registration System")

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
        self.image_path = None
        self.preview_ctk = None

        self.init_db()
        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_db(self):
        conn = sqlite3.connect('criminals.db')
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS criminals
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT,
                           age
                           INTEGER,
                           gender
                           TEXT,
                           father_name
                           TEXT,
                           crime
                           TEXT,
                           image_path
                           TEXT,
                           face_encoding
                           TEXT
                       )
                       ''')
        conn.commit()
        conn.close()

    def build_ui(self):
        # Header stretches horizontally
        header = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=0)
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="👮 Criminal Registration", font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#e94560").pack(pady=(20, 5))
        ctk.CTkLabel(header, text="AI face encoding will be AES-256 encrypted", font=ctk.CTkFont(size=13),
                     text_color="gray").pack(pady=(0, 15))

        # Main Form Frame - fills and expands to take up available space
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(pady=10, padx=40, fill="both", expand=True)

        fields = ["Full Name:", "Age:", "Father's Name:", "Crime Committed:"]
        self.entries = {}
        for i, label in enumerate(fields):
            ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=14)).grid(row=i, column=0, sticky="w", pady=12)
            e = ctk.CTkEntry(f, height=40, corner_radius=10)
            e.grid(row=i, column=1, pady=12, padx=(10, 0), sticky="ew")
            self.entries[label] = e

        ctk.CTkLabel(f, text="Gender:", font=ctk.CTkFont(size=14)).grid(row=4, column=0, sticky="w", pady=12)
        self.gender_var = ctk.StringVar(value="Male")
        gf = ctk.CTkFrame(f, fg_color="transparent")
        gf.grid(row=4, column=1, pady=12, padx=(10, 0), sticky="w")
        ctk.CTkRadioButton(gf, text="Male", variable=self.gender_var, value="Male").pack(side="left", padx=10)
        ctk.CTkRadioButton(gf, text="Female", variable=self.gender_var, value="Female").pack(side="left", padx=10)

        ctk.CTkLabel(f, text="Face Photo:", font=ctk.CTkFont(size=14)).grid(row=5, column=0, sticky="nw", pady=12)
        uf = ctk.CTkFrame(f, fg_color="transparent")
        uf.grid(row=5, column=1, pady=12, padx=(10, 0), sticky="ew")

        # Add some padding to make it look good on a wider screen
        ctk.CTkButton(uf, text="📁 Browse", command=self.browse_image, height=40, fg_color="#3b2a4d").pack(side="left",
                                                                                                          padx=(0, 15))
        self.preview_label = ctk.CTkLabel(uf, text="No image", width=100, height=100, fg_color="#0f0f1a",
                                          corner_radius=10)
        self.preview_label.pack(side="right", padx=(0, 20), pady=10)  # added padding

        # Registration Button - stretches horizontally
        self.register_btn = ctk.CTkButton(f, text="✅ Register Criminal", command=self.register, height=50,
                                          font=ctk.CTkFont(size=16, weight="bold"), fg_color="#e94560")
        self.register_btn.grid(row=6, column=0, columnspan=2, pady=30, sticky="ew")

        f.grid_columnconfigure(1, weight=1)

    def browse_image(self):
        filename = filedialog.askopenfilename(filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp"),))
        if not filename: return
        try:
            from deepface import DeepFace
            DeepFace.represent(img_path=filename, model_name="Facenet512", enforce_detection=True)
            self.image_path = filename
            pil_img = Image.open(filename)
            pil_img.thumbnail((100, 100))
            self.preview_ctk = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
            self.preview_label.configure(image=self.preview_ctk, text="")
            messagebox.showinfo("✅ Face Detected", "Face detected. Ready to register.")
        except Exception as e:
            messagebox.showerror("No Face", f"Face detection failed: {e}")
            self.image_path = None

    def register(self):
        name = self.entries["Full Name:"].get().strip()
        age = self.entries["Age:"].get().strip()
        father = self.entries["Father's Name:"].get().strip()
        crime = self.entries["Crime Committed:"].get().strip()
        if not all([name, age, father, crime, self.image_path]):
            messagebox.showwarning("Incomplete", "All fields and image required.")
            return
        try:
            self.register_btn.configure(text="⏳ Encoding...", state="disabled")
            self.update()
            from deepface import DeepFace
            embedding = \
            DeepFace.represent(img_path=self.image_path, model_name="Facenet512", enforce_detection=True)[0][
                "embedding"]
            encrypted_encoding = security.encrypt_embedding(embedding)  # AES-256!

            conn = sqlite3.connect('criminals.db')
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO criminals (name, age, gender, father_name, crime, image_path, face_encoding)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           ''',
                           (name, int(age), self.gender_var.get(), father, crime, self.image_path, encrypted_encoding))
            conn.commit()
            criminal_id = cursor.lastrowid
            conn.close()

            audit_log.log_audit("Admin", "REGISTER_CRIMINAL", target_id=criminal_id,
                                details=f"Name: {name}, Crime: {crime}")
            messagebox.showinfo("✅ Success", f"Criminal '{name}' registered with AES-256 encrypted face!")
            self.clear_form()
        except Exception as e:
            audit_log.log_audit("Admin", "REGISTER_FAIL", details=str(e))
            messagebox.showerror("Error", str(e))
        finally:
            self.register_btn.configure(text="✅ Register Criminal", state="normal")

    def clear_form(self):
        for e in self.entries.values(): e.delete(0, ctk.END)
        self.gender_var.set("Male")
        self.image_path = None
        self.preview_label.configure(image=None, text="No image")

    def on_close(self):
        self.grab_release()
        self.destroy()