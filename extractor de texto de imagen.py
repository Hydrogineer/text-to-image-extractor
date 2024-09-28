import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import os

# Especifica la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'J:\tesseract/tesseract.exe'

class OCRApp:
    def __init__(self, master):
        self.master = master
        master.title("OCR App")
        master.geometry("600x700")  # Tamaño inicial de la ventana

        self.label = tk.Label(master, text="Selecciona una imagen para extraer texto")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Seleccionar Imagen", command=self.select_image)
        self.select_button.pack(pady=5)

        self.image_label = tk.Label(master)
        self.image_label.pack(pady=10)

        self.text_area = tk.Text(master, height=20, width=70)
        self.text_area.pack(pady=10)

        self.save_button = tk.Button(master, text="Guardar Texto", command=self.save_text)
        self.save_button.pack(pady=5)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            self.process_image(file_path)

    def process_image(self, file_path):
        try:
            # Abrir y mostrar la imagen
            image = Image.open(file_path)
            image.thumbnail((300, 300))  # Redimensionar para mostrar
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Extraer texto
            text = pytesseract.image_to_string(Image.open(file_path))
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, text)
        except pytesseract.TesseractNotFoundError:
            messagebox.showerror("Error", "Tesseract no está instalado o no se encuentra en el PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar la imagen: {str(e)}")

    def save_text(self):
        text = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                messagebox.showinfo("Éxito", "El texto se ha guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

def check_tesseract():
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        messagebox.showerror("Error", "Tesseract no está instalado o la ruta es incorrecta. "
                                      "Por favor, instale Tesseract o corrija la ruta en el código.")
        return False
    return True

if __name__ == "__main__":
    root = tk.Tk()
    if check_tesseract():
        app = OCRApp(root)
        root.mainloop()
    else:
        root.destroy()
