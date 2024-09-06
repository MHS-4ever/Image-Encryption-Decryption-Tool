import tkinter as tk
from tkinter import filedialog, messagebox


class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        #self.root.geometry("300x200")
        self.root.title("Image Encryptor")

        self.create_widgets()
        self.current_file = None

    def create_widgets(self):
        # Create a frame for padding and organization
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Key entry field
        self.key_label = tk.Label(frame, text="Encryption Key:")
        self.key_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.key_entry = tk.Entry(frame, width=20)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        # Encrypt button
        self.encrypt_button = tk.Button(frame, text="Encrypt Image", command=self.encrypt_image)
        self.encrypt_button.grid(row=1, column=0, padx=5, pady=10)

        # Decrypt button
        self.decrypt_button = tk.Button(frame, text="Decrypt Image", command=self.decrypt_image)
        self.decrypt_button.grid(row=1, column=1, padx=5, pady=10)

    def encrypt_image(self):
        self.current_file = filedialog.askopenfilename(
            filetypes=[('JPEG files', '*.jpeg')]
        )
        if self.current_file:
            key = self.get_key()
            if key is not None:
                if not self.is_image_encrypted(self.current_file, key):
                    self.process_image(self.current_file, key, encrypt=True)
                else:
                    messagebox.showinfo("Info", "Image is already encrypted.")

    def decrypt_image(self):
        self.current_file = filedialog.askopenfilename(
            filetypes=[('JPEG files', '*.jpeg')]
        )
        if self.current_file:
            key = self.get_key()
            if key is not None:
                if self.is_image_encrypted(self.current_file, key):
                    self.process_image(self.current_file, key, encrypt=False)
                else:
                    messagebox.showinfo("Info", "Image is not encrypted or is already decrypted.")

    def get_key(self):
        key_str = self.key_entry.get().strip()
        if not key_str.isdigit():
            messagebox.showerror("Invalid Input", "Key must be a number.")
            return None
        return int(key_str)

    def is_image_encrypted(self, file_path, key):
        try:
            # Check if the file is encrypted by seeing if XORing with the key returns readable data
            with open(file_path, 'rb') as file:
                image_data = bytearray(file.read())

            # Try to decrypt and see if it results in valid JPEG data
            decrypted_data = bytearray(b ^ key for b in image_data)
            return self.is_valid_jpeg(decrypted_data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return False

    def is_valid_jpeg(self, data):
        # Basic check for JPEG file validity (start and end markers)
        return len(data) > 2 and data[0:2] == b'\xff\xd8' and data[-2:] == b'\xff\xd9'

    def process_image(self, file_path, key, encrypt=True):
        try:
            with open(file_path, 'rb') as file:
                image_data = bytearray(file.read())

            # Encrypt or decrypt the image
            image_data = bytearray(b ^ key for b in image_data)

            with open(file_path, 'wb') as file:
                file.write(image_data)

            operation = "encrypted" if encrypt else "decrypted"
            messagebox.showinfo("Success", f"Image {operation} successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
