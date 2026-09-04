import customtkinter as ctk
from tkinter import filedialog, messagebox
import sqlite3
import numpy as np
from PIL import Image
import security
import audit_log

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FaceDatabaseSearchApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("🔎 AI Database Face Search")

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
        self.suspect_embedding = None
        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        # Header stretches horizontally
        header = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=0)
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="🔎 AI Suspect Matching Engine", font=ctk.CTkFont(size=26, weight="bold"),
                     text_color="#e94560").pack(pady=(20, 5))
        ctk.CTkLabel(header, text="Upload suspect photo to search AES-256 encrypted database",
                     font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 15))

        # Main Form Frame - fills and expands to take up available space
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(pady=15, padx=30, fill="both", expand=True)

        uf = ctk.CTkFrame(main, fg_color="#0f0f1a", corner_radius=15)
        uf.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        uf.grid_columnconfigure(0, weight=1)

        self.browse_btn = ctk.CTkButton(uf, text="📁 Upload Suspect Photo", command=self.upload_face, height=50,
                                        fg_color="#3b2a4d", font=ctk.CTkFont(size=15, weight="bold"))
        self.browse_btn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.status = ctk.CTkLabel(uf, text="No image loaded", font=ctk.CTkFont(size=13), text_color="gray")
        self.status.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        self.preview = ctk.CTkLabel(uf, text="🖼️ Preview", width=150, height=150, fg_color="#1a1a2e", corner_radius=10)
        self.preview.grid(row=0, column=1, rowspan=2, padx=20, pady=20)

        self.search_btn = ctk.CTkButton(main, text="⚡ SEARCH DATABASE", command=self.search_db, height=55,
                                        fg_color="#e94560", font=ctk.CTkFont(size=18, weight="bold"), state="disabled")
        self.search_btn.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")

        self.results_frame = ctk.CTkScrollableFrame(main, fg_color="#0f0f1a", corner_radius=10, height=280)
        self.results_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15), sticky="nsew")

        # Configure grid so the results frame expands to fill the remaining space
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self.results_frame, text="Upload a suspect photo and click Search.", text_color="gray").pack(
            pady=50)

    def upload_face(self):
        filename = filedialog.askopenfilename(filetypes=(("Images", "*.png *.jpg *.jpeg"),))
        if not filename: return
        try:
            from deepface import DeepFace
            self.status.configure(text="⏳ Encoding...")
            self.update()
            embedding = DeepFace.represent(img_path=filename, model_name="Facenet512", enforce_detection=True)[0][
                "embedding"]
            self.suspect_embedding = np.array(embedding)
            pil_img = Image.open(filename)
            pil_img.thumbnail((150, 150))
            self.preview.configure(image=ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size),
                                   text="")
            self.status.configure(text="✅ Encoded & encrypted ready.", text_color="#00ff88")
            self.search_btn.configure(state="normal")
            messagebox.showinfo("✅ Success", "Face encoded. Ready to search database.")
        except Exception as e:
            self.status.configure(text=f"❌ Error: {str(e)[:30]}", text_color="#ff4444")
            self.suspect_embedding = None
            self.search_btn.configure(state="disabled")

    def search_db(self):
        if self.suspect_embedding is None:
            return
        for w in self.results_frame.winfo_children(): w.destroy()
        self.search_btn.configure(text="⏳ Searching...", state="disabled")
        self.update()

        try:
            conn = sqlite3.connect('criminals.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, age, crime, face_encoding FROM criminals WHERE face_encoding IS NOT NULL')
            records = cursor.fetchall()
            conn.close()

            results = []
            for rid, name, age, crime, enc_json in records:
                try:
                    decrypted = security.decrypt_embedding(enc_json)  # AES-256 decryption!
                    if decrypted is None: continue
                    stored = np.array(decrypted)
                    norm_s = self.suspect_embedding / np.linalg.norm(self.suspect_embedding)
                    norm_db = stored / np.linalg.norm(stored)
                    sim = max(0, (np.dot(norm_s, norm_db) + 1) / 2 * 100)
                    results.append((sim, rid, name, age, crime))
                except:
                    continue

            results.sort(reverse=True, key=lambda x: x[0])
            top = results[:5]

            if not top:
                ctk.CTkLabel(self.results_frame, text="No valid face encodings found.", text_color="gray").pack(pady=50)
            else:
                hf = ctk.CTkFrame(self.results_frame, fg_color="#16213e", corner_radius=8)
                hf.pack(fill="x", pady=(0, 10))
                for i, h in enumerate(["Match %", "ID", "Name", "Age", "Crime"]):
                    ctk.CTkLabel(hf, text=h, font=ctk.CTkFont(size=14, weight="bold"), text_color="#a8d8ea").grid(row=0,
                                                                                                                  column=i,
                                                                                                                  padx=15,
                                                                                                                  pady=10,
                                                                                                                  sticky="w")

                for sim, rid, name, age, crime in top:
                    rf = ctk.CTkFrame(self.results_frame, fg_color="transparent")
                    rf.pack(fill="x", pady=3)
                    color = "#00ff88" if sim > 70 else "#ffcc00" if sim > 50 else "#ff4444"
                    badge = "✅" if sim > 70 else "⚠️" if sim > 50 else "❌"
                    ctk.CTkLabel(rf, text=f"{badge} {sim:.2f}%", font=ctk.CTkFont(size=13, weight="bold"),
                                 text_color=color).grid(row=0, column=0, padx=15, pady=6, sticky="w")
                    ctk.CTkLabel(rf, text=f"#{rid}", font=ctk.CTkFont(size=13), text_color="white").grid(row=0,
                                                                                                         column=1,
                                                                                                         padx=15,
                                                                                                         pady=6,
                                                                                                         sticky="w")
                    ctk.CTkLabel(rf, text=name, font=ctk.CTkFont(size=13), text_color="white").grid(row=0, column=2,
                                                                                                    padx=15, pady=6,
                                                                                                    sticky="w")
                    ctk.CTkLabel(rf, text=str(age), font=ctk.CTkFont(size=13), text_color="white").grid(row=0, column=3,
                                                                                                        padx=15, pady=6,
                                                                                                        sticky="w")
                    ctk.CTkLabel(rf, text=crime[:20], font=ctk.CTkFont(size=13), text_color="gray").grid(row=0,
                                                                                                         column=4,
                                                                                                         padx=15,
                                                                                                         pady=6,
                                                                                                         sticky="w")

                if top[0][0] < 50:
                    ctk.CTkLabel(self.results_frame, text="⚠️ No strong matches found.", text_color="#ffcc00",
                                 font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)

                audit_log.log_audit("Admin", "DATABASE_SEARCH",
                                    details=f"Top match: {top[0][2]} ({top[0][0]:.2f}%)" if top else "No matches")
        except Exception as e:
            audit_log.log_audit("Admin", "SEARCH_FAIL", details=str(e))
            messagebox.showerror("Error", str(e))
        finally:
            self.search_btn.configure(text="⚡ SEARCH DATABASE", state="normal")

    def on_close(self):
        self.grab_release()
        self.destroy()