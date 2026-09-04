import customtkinter as ctk
from tkinter import messagebox
import audit_log
import security

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DashboardApp(ctk.CTk):
    def __init__(self, logged_in_user="Admin"):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.inactivity_timer = None
        self.TIMEOUT_SECONDS = 300
        self.title("🕵️ Criminal Face Detection - Secure Suite")

        # --- NEW: Dynamic Window Sizing & Center on Screen ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.6)
        height = int(screen_height * 0.7)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(True, True)  # Allow resizing

        self.bind_all("<Key>", self.reset_timer)
        self.bind_all("<Button-1>", self.reset_timer)

        # Header (Packed to stretch horizontally)
        self.header_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=0)
        self.header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(self.header_frame, text="🔍 CRIMINAL FACE DETECTION SYSTEM",
                     font=ctk.CTkFont(size=28, weight="bold"), text_color="#e94560").pack(pady=(20, 5))
        ctk.CTkLabel(self.header_frame, text=f"Welcome, {self.logged_in_user} (👮 Active Session)",
                     font=ctk.CTkFont(size=16), text_color="#a8d8ea").pack(pady=(0, 15))

        # Grid Frame (Packed to fill and expand with the window)
        self.grid_frame = ctk.CTkFrame(self, fg_color="#1a1a2e")
        self.grid_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Configure grid to stretch buttons evenly
        for i in range(3):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        buttons = [
            ("📝 Criminal Registration", self.open_registration, "#3b2a4d", "#5a3d72"),
            ("🖼️ Image Recognition", self.open_comparator, "#7e5109", "#a06d12"),
            ("💬 Case Notes", self.open_chatbox, "#145a32", "#1e7a45"),
            ("🔎 DB Face Search", self.open_search, "#b7950b", "#d4ac0d"),
            ("📊 Audit Trail", self.view_audit, "#1b4f72", "#2e6b92"),
            ("🔑 Change Password", self.change_password, "#7d3c98", "#9b59b6")
        ]
        for idx, (text, cmd, color, hover) in enumerate(buttons):
            row, col = divmod(idx, 2)
            btn = ctk.CTkButton(self.grid_frame, text=text, command=cmd, fg_color=color, hover_color=hover,
                                corner_radius=15, height=100, font=ctk.CTkFont(size=16, weight="bold"))
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Status Label (Packed to the bottom)
        self.status_label = ctk.CTkLabel(self, text="🟢 System Ready | AES-256 Encrypted | HMAC Audit",
                                         font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(side="bottom", pady=10)
        self.reset_timer()

    def reset_timer(self, event=None):
        if self.inactivity_timer:
            self.after_cancel(self.inactivity_timer)
        self.inactivity_timer = self.after(self.TIMEOUT_SECONDS * 1000, self.lock_screen)

    def lock_screen(self):
        audit_log.log_audit(self.logged_in_user, "SESSION_LOCK", details="Auto-lock due to inactivity")
        self.destroy()
        import subprocess, os
        subprocess.Popen(["python3", "login.py"])
        os._exit(0)

    def open_registration(self):
        audit_log.log_audit(self.logged_in_user, "OPEN_REGISTRATION")
        self.status_label.configure(text="⏳ Loading Registration...")
        try:
            from cri_reg import CriminalRegistrationApp
            CriminalRegistrationApp(self)
            self.status_label.configure(text="🟢 System Ready")
        except Exception as e:
            messagebox.showerror("Error", "Module load failed. Check logs.")

    def open_comparator(self):
        audit_log.log_audit(self.logged_in_user, "OPEN_COMPARATOR")
        self.status_label.configure(text="⏳ Loading Comparator...")
        try:
            from img_compare import ImageCompareApp
            ImageCompareApp(self)
            self.status_label.configure(text="🟢 System Ready")
        except Exception as e:
            messagebox.showerror("Error", "Module load failed.")

    def open_chatbox(self):
        audit_log.log_audit(self.logged_in_user, "OPEN_NOTES")
        self.status_label.configure(text="⏳ Loading Notes...")
        try:
            from chatbox import ChatBoxApp
            ChatBoxApp(self)
            self.status_label.configure(text="🟢 System Ready")
        except Exception as e:
            messagebox.showerror("Error", "Module load failed.")

    def open_search(self):
        audit_log.log_audit(self.logged_in_user, "OPEN_SEARCH")
        self.status_label.configure(text="⏳ Loading Search Engine...")
        try:
            from show import FaceDatabaseSearchApp
            FaceDatabaseSearchApp(self)
            self.status_label.configure(text="🟢 System Ready")
        except Exception as e:
            messagebox.showerror("Error", "Module load failed.")

    def view_audit(self):
        audit_log.log_audit(self.logged_in_user, "VIEW_AUDIT")
        logs = audit_log.get_audit_trail(limit=100)
        if not logs:
            messagebox.showinfo("Audit Trail", "No logs found.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("🛡️ Secure Audit Forensics")
        # Make popup responsive too
        popup.geometry(f"{int(self.winfo_screenwidth() * 0.7)}x{int(self.winfo_screenheight() * 0.7)}")
        popup.grab_set()
        popup.configure(fg_color="#1a1a2e")

        header = ctk.CTkFrame(popup, fg_color="#16213e", corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="🔐 Cryptographic Audit Trail", font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#e94560").pack(pady=(10, 0))
        ctk.CTkLabel(header, text="HMAC-SHA256 Signed. Tampered logs will show a warning.", font=ctk.CTkFont(size=13),
                     text_color="gray").pack(pady=(0, 10))

        toolbar = ctk.CTkFrame(popup, fg_color="transparent")
        toolbar.pack(fill="x", padx=30, pady=5)

        def integrity_check():
            tampered, total = audit_log.verify_audit_logs()
            if tampered:
                messagebox.showerror("⚠️ Integrity Breach!",
                                     f"{len(tampered)} out of {total} logs TAMPERED!\nIDs: {tampered[:10]}")
            else:
                messagebox.showinfo("✅ Verified!", f"All {total} logs are cryptographically valid.")

        ctk.CTkButton(toolbar, text="🔍 Run Integrity Check", command=integrity_check, fg_color="#3b2a4d",
                      height=35).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Close", command=popup.destroy, fg_color="#4a4a4a", height=35).pack(side="right",
                                                                                                        padx=5)

        scroll = ctk.CTkScrollableFrame(popup, fg_color="#0f0f1a", corner_radius=10)
        scroll.pack(pady=10, padx=20, fill="both", expand=True)

        headers = ["Status", "Timestamp", "Officer", "Action", "Target", "Details"]
        hf = ctk.CTkFrame(scroll, fg_color="#16213e", corner_radius=5)
        hf.pack(fill="x", pady=(0, 5))
        for i, h in enumerate(headers):
            ctk.CTkLabel(hf, text=h, font=ctk.CTkFont(size=13, weight="bold"), text_color="#a8d8ea").grid(row=0,
                                                                                                          column=i,
                                                                                                          padx=10,
                                                                                                          pady=8,
                                                                                                          sticky="w")

        for row in logs:
            rid, ts, officer, action, target, details, sig = row
            is_valid = security.verify_audit_signature(rid, ts, action, officer, details, sig)
            status_text = "✅ Valid" if is_valid else "⚠️ TAMPERED"
            status_color = "#00ff88" if is_valid else "#ff4444"

            rf = ctk.CTkFrame(scroll, fg_color="transparent")
            rf.pack(fill="x", pady=2)
            ctk.CTkLabel(rf, text=status_text, font=ctk.CTkFont(size=12, weight="bold"), text_color=status_color).grid(
                row=0, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(rf, text=ts[:19], font=ctk.CTkFont(size=11), text_color="white").grid(row=0, column=1, padx=10,
                                                                                               pady=5, sticky="w")
            ctk.CTkLabel(rf, text=officer, font=ctk.CTkFont(size=11), text_color="white").grid(row=0, column=2, padx=10,
                                                                                               pady=5, sticky="w")
            ctk.CTkLabel(rf, text=action, font=ctk.CTkFont(size=11, weight="bold"), text_color="#ffcc00").grid(row=0,
                                                                                                               column=3,
                                                                                                               padx=10,
                                                                                                               pady=5,
                                                                                                               sticky="w")
            ctk.CTkLabel(rf, text=str(target), font=ctk.CTkFont(size=11), text_color="white").grid(row=0, column=4,
                                                                                                   padx=10, pady=5,
                                                                                                   sticky="w")
            ctk.CTkLabel(rf, text=details[:40], font=ctk.CTkFont(size=11), text_color="gray").grid(row=0, column=5,
                                                                                                   padx=10, pady=5,
                                                                                                   sticky="w")

    def change_password(self):
        audit_log.log_audit(self.logged_in_user, "PASSWORD_CHANGE_ATTEMPT")
        popup = ctk.CTkToplevel(self)
        popup.title("🔐 Change Admin Password")
        popup.geometry("400x320")
        popup.grab_set()
        popup.configure(fg_color="#1a1a2e")

        ctk.CTkLabel(popup, text="Update Admin Credentials", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#e94560").pack(pady=(20, 10))
        ctk.CTkLabel(popup, text="Enter new password (min 8 chars).", font=ctk.CTkFont(size=13),
                     text_color="gray").pack(pady=(0, 10))

        pw1 = ctk.CTkEntry(popup, placeholder_text="New Password", show="*", height=45, corner_radius=10)
        pw1.pack(pady=10, padx=30, fill="x")
        pw2 = ctk.CTkEntry(popup, placeholder_text="Confirm Password", show="*", height=45, corner_radius=10)
        pw2.pack(pady=10, padx=30, fill="x")
        status = ctk.CTkLabel(popup, text="", font=ctk.CTkFont(size=12))
        status.pack(pady=5)

        def submit():
            if len(pw1.get()) < 8:
                status.configure(text="❌ Min 8 characters.", text_color="#ff4444")
                return
            if pw1.get() != pw2.get():
                status.configure(text="❌ Passwords do not match.", text_color="#ff4444")
                return
            try:
                security.update_password_hash(pw1.get())
                audit_log.log_audit(self.logged_in_user, "PASSWORD_CHANGE_SUCCESS")
                status.configure(text="✅ Password updated!", text_color="#00ff88")
                popup.after(1500, popup.destroy)
                messagebox.showinfo("Success", "Admin password has been securely updated.")
            except Exception as e:
                audit_log.log_audit(self.logged_in_user, "PASSWORD_CHANGE_FAIL", details=str(e))
                status.configure(text=f"❌ {str(e)[:30]}", text_color="#ff4444")

        ctk.CTkButton(popup, text="🔒 Update Password", command=submit, height=45, fg_color="#e94560").pack(pady=20,
                                                                                                           padx=30,
                                                                                                           fill="x")


if __name__ == "__main__":
    DashboardApp().mainloop()