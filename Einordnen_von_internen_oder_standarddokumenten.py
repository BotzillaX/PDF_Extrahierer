import os
import glob
from PyPDF2 import PdfReader, PdfWriter
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence





def get_latest_download_path():
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    list_of_pdf_files = glob.glob(downloads_path + '/*.pdf')
    if not list_of_pdf_files:  
        return None
    latest_pdf_file = max(list_of_pdf_files, key=os.path.getctime)
    return latest_pdf_file


def generate_unique_filename(directory, base_name, extension, number_of_pages):
    file_name = f"{base_name}_Seiten_{number_of_pages}{extension}"
    final_path = os.path.join(directory, file_name)
    counter = 1
    while os.path.exists(final_path):
        file_name = f"{counter}_{base_name}_Seiten_{number_of_pages}{extension}"
        final_path = os.path.join(directory, file_name)
        counter += 1
    return file_name


def extract_and_save_pdf(source_path):
    target_path = locationEntry.get()
    from_page = firstPage.get()
    to_page = secondPage.get()
    base_name = baseName.get()
    print(target_path)
    print(from_page)
    print(base_name)
    print(to_page)
    from_page = int(from_page)
    to_page = int(to_page)
    reader = PdfReader(source_path.strip('"'))
    writer = PdfWriter()
    num_pages = len(reader.pages)
    if to_page > num_pages:
        to_page = num_pages
    for i in range(from_page - 1, to_page):
        writer.add_page(reader.pages[i])
    number_of_pages = to_page - from_page + 1
    folder_name = base_name
    final_directory = os.path.join(target_path.strip('"'), folder_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory, exist_ok=True)
    unique_file_name = generate_unique_filename(final_directory, base_name, ".pdf", number_of_pages)
    final_path = os.path.join(final_directory, unique_file_name)
    with open(final_path, 'wb') as f_out:
        writer.write(f_out)
    print(f"PDF erfolgreich gespeichert unter: {final_path}")


root = tk.Tk()
root.geometry("700x230")  # Adjust the size as needed to fit the GIF and entries
root.attributes("-topmost", -1)
root.title("Speichern der Dokumente von Kevin Fritsch")
frameCnt = 12
new_height = 200  # New height for the GIF
frames = []
current_path = os.getcwd()+"\\giphy.gif"
gif_path = current_path


with Image.open(gif_path) as img:
    for i, frame in enumerate(ImageSequence.Iterator(img)):
        # Calculate new width to maintain aspect ratio
        original_width, original_height = frame.size
        aspect_ratio = original_width / original_height
        new_width = int(aspect_ratio * new_height)
        
        # Resize the frame
        img_resized = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert the resized frame to a format Tkinter can use
        frame = ImageTk.PhotoImage(img_resized)
        frames.append(frame)
        
        if i + 1 == frameCnt:
            break


def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)


label = Label(root)
label.grid(row=1, column=6, rowspan=8, padx=(50, 0)) 
root.after(0, update, 0)
# Erstellen des ersten Eintragsfeldes mit Beschriftung
locationLabel = tk.Label(root, text="Wo es gespeichert werden soll")
locationLabel.grid(row=3, column=1, sticky="e")
locationEntry = tk.Entry(root)
locationEntry.grid(row=3, column=2, pady=(10, 0))  # Hinzufügen von Abstand oben
# Erstellen des zweiten Eintragsfeldes mit Beschriftung
firstPageLabel = tk.Label(root, text="Erste Seite")
firstPageLabel.grid(row=4, column=1, sticky="e")
firstPage = tk.Entry(root)
firstPage.grid(row=4, column=2, pady=5)  # Hinzufügen von Abstand oben und unten
# Erstellen des dritten Eintragsfeldes mit Beschriftung
secondPageLabel = tk.Label(root, text="Letzte Seite")
secondPageLabel.grid(row=5, column=1, sticky="e")
secondPage = tk.Entry(root)
secondPage.grid(row=5, column=2, pady=(0, 10))  # Hinzufügen von Abstand unten
baseNameLabel = tk.Label(root, text="Name des Dokumentes")
baseNameLabel.grid(row=6, column=1, sticky="e")
baseName = tk.Entry(root)
baseName.grid(row=6, column=2, pady=(0, 10))  # Hinzufügen von Abstand unten
takeInput = tk.Button(root, text="Eingaben übernehmen", command=lambda: extract_and_save_pdf(get_latest_download_path()))
takeInput.grid()

root.mainloop()



