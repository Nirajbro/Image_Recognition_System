import os
import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv
import security
import audit_log

load_dotenv()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Secure Biometric Login")

        # --- Dynamic Window Sizing & Center on Screen ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set window to 60% of screen width and 70% of screen height
        width = int(screen_width * 0.6)
        height = int(screen_height * 0.7)

        # Calculate center coordinates
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        # Apply dynamic geometry to center it
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Allow the window to be resized
        self.resizable(True, True)

        # --- Responsive Centered Frame ---
        # Create the main frame
        self.frame = ctk.CTkFrame(self, corner_radius=20)

        # Use 'place' to perfectly center the frame and allow it to scale with the window
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.8)

        # --- Rest of your layout ---
        ctk.CTkLabel(self.frame, text="🔒 Zero-Trust Auth", font=ctk.CTkFont(size=32, weight="bold"),
                     text_color="#FF6B6B").pack(pady=(30, 10))
        ctk.CTkLabel(self.frame, text="Secure Biometric Verification System", font=ctk.CTkFont(size=14)).pack(
            pady=(0, 30))

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="👤 Username", height=45, corner_radius=10)
        self.username_entry.pack(pady=10, padx=30, fill="x")
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="🔑 Password", show="*", height=45,
                                           corner_radius=10)
        self.password_entry.pack(pady=10, padx=30, fill="x")

        self.login_button = ctk.CTkButton(self.frame, text="🖥️ Authenticate", height=50, command=self.authenticate,
                                          fg_color="#FF6B6B", hover_color="#E55555", corner_radius=10)
        self.login_button.pack(pady=(30, 10), padx=30, fill="x")

        self.status_label = ctk.CTkLabel(self.frame, text="Enter credentials to access the system",
                                         font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(pady=(5, 10))

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        self.status_label.configure(text="⏳ Verifying credentials...")
        self.update()
        try:
            is_valid = security.verify_password(password, self.stored_hash)
        except:
            messagebox.showerror("Error", "System authentication error. Check logs.")
            return

        if is_valid:
            audit_log.log_audit(username, "LOGIN_SUCCESS")
            self.status_label.configure(text="✅ Login Successful!")
            self.destroy()
            from dashboard import DashboardApp
            DashboardApp(logged_in_user=username).mainloop()
        else:
            audit_log.log_audit(username, "LOGIN_FAIL", details="Invalid password")
            self.status_label.configure(text="❌ Invalid credentials")
            messagebox.showerror("Access Denied", "Invalid username or password.")


if __name__ == "__main__":
    LoginApp().mainloop()