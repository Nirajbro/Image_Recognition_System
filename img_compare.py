import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import security
import audit_log

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ImageCompareApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("🖼️ Face Comparator")

        # --- NEW: Dynamic Window Sizing & Center on Screen ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.6)
        height = int(screen_height * 0.7)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Allow resizing so the content stretches
        self.resizable(True, True)

        self.grab_set()
        self.focus_force()
        self.image1_path = None
        self.image2_path = None
        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        # Header stretches horizontally
        header = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=0)
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="🔍 Face Similarity Verifier", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#e94560").pack(pady=(15, 5))
        ctk.CTkLabel(header, text="AES-256 decryption of stored embeddings", font=ctk.CTkFont(size=13),
                     text_color="gray").pack(pady=(0, 15))

        # Main Image Frame - fills and expands to take up available space
        self.img_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.img_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Left and Right panels expand
        self.left_panel = ctk.CTkFrame(self.img_frame, fg_color="#0f0f1a", corner_radius=15)
        self.left_panel.pack(side="left", padx=15, fill="both", expand=True)
        self.img1_label = ctk.CTkLabel(self.left_panel, text="No Image", font=ctk.CTkFont(size=14))
        self.img1_label.pack(pady=20, fill="both", expand=True)

        self.right_panel = ctk.CTkFrame(self.img_frame, fg_color="#0f0f1a", corner_radius=15)
        self.right_panel.pack(side="right", padx=15, fill="both", expand=True)
        self.img2_label = ctk.CTkLabel(self.right_panel, text="No Image", font=ctk.CTkFont(size=14))
        self.img2_label.pack(pady=20, fill="both", expand=True)

        # Control frame - stretches horizontally
        cf = ctk.CTkFrame(self, fg_color="transparent")
        cf.pack(pady=20, fill="x", padx=50)
        cf.grid_columnconfigure(0, weight=1)
        cf.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(cf, text="📁 Browse Face 1", command=lambda: self.browse(1), fg_color="#3b2a4d", height=40).grid(
            row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(cf, text="📁 Browse Face 2", command=lambda: self.browse(2), fg_color="#1b4f72", height=40).grid(
            row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(cf, text="⚡ Compare Faces", command=self.compare, fg_color="#e94560", height=50,
                      font=ctk.CTkFont(size=16, weight="bold")).grid(row=1, column=0, columnspan=2, padx=10, pady=15,
                                                                     sticky="ew")

    def browse(self, num):
        filename = filedialog.askopenfilename(filetypes=(("Images", "*.png *.jpg *.jpeg"),))
        if not filename: return
        img = cv2.imread(filename)
        if img is None: return
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        pil_img.thumbnail((300, 300))
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)

        if num == 1:
            self.image1_path = filename
            self.img1_label.configure(image=ctk_img, text="")
        else:
            self.image2_path = filename
            self.img2_label.configure(image=ctk_img, text="")

    def compare(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showwarning("Incomplete", "Load both images.")
            return
        try:
            from deepface import DeepFace
            result = DeepFace.verify(img1_path=self.image1_path, img2_path=self.image2_path, model_name="Facenet512",
                                     enforce_detection=True)
            sim = max(0, (1 - result["distance"]) * 100)
            msg = f"✅ MATCH! {sim:.2f}%" if result["verified"] else f"❌ NO MATCH. {sim:.2f}%"
            audit_log.log_audit("Admin", "FACE_COMPARE", details=f"Similarity: {sim:.2f}%")
            messagebox.showinfo("Result", msg)
        except Exception as e:
            audit_log.log_audit("Admin", "COMPARE_FAIL", details=str(e))
            messagebox.showerror("Error", str(e))

    def on_close(self):
        self.grab_release()
        self.destroy()