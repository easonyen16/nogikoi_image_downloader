import tkinter as tk
from tkinter import ttk
import requests
import os
import threading
import io
from PIL import Image, ImageTk

def update_canvas_image(img_data):
    img = Image.open(io.BytesIO(img_data))
    max_width = 200
    width, height = img.size
    new_height = int((max_width / width) * height)
    img = img.resize((max_width, new_height), Image.ANTIALIAS)
    img_tk = ImageTk.PhotoImage(img)
    canvas.config(width=img_tk.width(), height=img_tk.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk
    canvas.update()

def download_images(color, star, seg_from, seg_to):
    if color == "blue":
        card_a, card_b = card_dict["blue"][star]
    elif color == "green":
        card_a, card_b = card_dict["green"][star]
    elif color == "pink":
        card_a, card_b = card_dict["pink"][star]

    jpg_path = "https://prd-content.static.game.nogikoi.jp/assets/img/card/l"
    png_path = "https://prd-content.static.game.nogikoi.jp/assets/img/card/mypage"

    os.makedirs("images", exist_ok=True)

    total_images = 4 * (seg_to - seg_from + 1)
    downloaded_images = 0

    for i in range(seg_from, seg_to + 1):
        for card in [card_a, card_b]:
            for path, ext in [(jpg_path, "jpg"), (png_path, "png")]:
                url = f"{path}/{card}{i}.{ext}"
                response = requests.get(url)

                if response.status_code == 200:
                    update_canvas_image(response.content)
                    with open(f"images/{card}{i}.{ext}", "wb") as f:
                        f.write(response.content)
                elif response.status_code == 404:
                    print(f"File not found: {url}")
                    total_images -= 1
                else:
                    print(f"Error downloading {url}: {response.status_code}")

                downloaded_images += 1
                progress_var.set(downloaded_images / total_images * 100)
                root.update_idletasks()


def run_script():
    color = color_var.get()
    star = int(star_var.get())
    seg_from = int(from_entry.get())
    seg_to = int(to_entry.get())
    
    download_thread = threading.Thread(target=download_images, args=(color, star, seg_from, seg_to))
    download_thread.start()

root = tk.Tk()
root.title("Image Downloader")

canvas = tk.Canvas(root)
canvas.grid(column=4, row=0, rowspan=6, padx=10)

# Color radio buttons
color_var = tk.StringVar(value="blue")
color_label = ttk.Label(root, text="Color:")
color_label.grid(column=0, row=0)
blue_radio = ttk.Radiobutton(root, text="Blue", variable=color_var, value="blue")
blue_radio.grid(column=1, row=0)
green_radio = ttk.Radiobutton(root, text="Green", variable=color_var, value="green")
green_radio.grid(column=2, row=0)
pink_radio = ttk.Radiobutton(root, text="Pink", variable=color_var, value="pink")
pink_radio.grid(column=3, row=0)

#Star radio buttons
star_var = tk.StringVar(value="1")
star_label = ttk.Label(root, text="Star:")
star_label.grid(column=0, row=1)
star_1_radio = ttk.Radiobutton(root, text="1", variable=star_var, value="1")
star_1_radio.grid(column=1, row=1)
star_3_radio = ttk.Radiobutton(root, text="3", variable=star_var, value="3")
star_3_radio.grid(column=2, row=1)
star_5_radio = ttk.Radiobutton(root, text="5", variable=star_var, value="5")
star_5_radio.grid(column=3, row=1)
star_7_radio = ttk.Radiobutton(root, text="7", variable=star_var, value="7")
star_7_radio.grid(column=1, row=2)

#From and to entry fields
from_label = ttk.Label(root, text="From:")
from_label.grid(column=0, row=3)
from_entry = ttk.Entry(root, width=10)
from_entry.grid(column=1, row=3)
to_label = ttk.Label(root, text="To:")
to_label.grid(column=2, row=3)
to_entry = ttk.Entry(root, width=10)
to_entry.grid(column=3, row=3)

#Run button
run_button = ttk.Button(root, text="Run", command=run_script)
run_button.grid(column=1, row=5)

#Progress bar
progress_var = tk.DoubleVar()
progress_label = ttk.Label(root, text="Progress:")
progress_label.grid(column=0, row=6)
progress_bar = ttk.Progressbar(root, length=200, variable=progress_var)
progress_bar.grid(column=1, row=6, columnspan=3)

#Card dictionary
card_dict = {
    "blue": {
        1: (110, 121),
        3: (130, 141),
        5: (150, 161),
        7: (170, 181),
    },
    "green": {
        1: (310, 321),
        3: (330, 341),
        5: (350, 361),
        7: (370, 381),
    },
    "pink": {
        1: (210, 221),
        3: (230, 241),
        5: (250, 261),
        7: (270, 281),
    },
}

# Spacer label
spacer_label = ttk.Label(root, text="")
spacer_label.grid(column=0, row=7, columnspan=4, pady=10)

root.mainloop()