from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import random
import itertools

POS = 0
DIST = 1

WEIGHTS = {}

class MarioKartUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mario Kart Item Box")
        
        self.frm = ttk.Frame(root, padding=10)
        self.frm.grid()

        self.frame = tk.Frame(self.frm, width=200, height=200, bg="gray")
        self.frame.grid(column=4, row=2)
        
        ttk.Label(self.frm, text="No Item", font=("Helvetica", 28)).grid(column=4, row=2)
        
        self.base_path = "images/"
        self.characters_path = self.base_path + "characters/"
        self.items_path = self.base_path + "items/"
        
        self.load_images()
        
        ttk.Label(self.frm, image=self.kai_tk).grid(column=16, row=2)
        ttk.Label(self.frm, image=self.toad_tk).grid(column=2, row=2)
        
        ttk.Button(self.frm, text="Quit", command=root.destroy).grid(column=1, row=1)
        ttk.Button(self.frm, text="Item Box Checkpoint", command=self.animate_item_selection).grid(column=1, row=2)
        
        self.item_label = ttk.Label(self.frm, image=self.item_images[0])
        self.item_label.grid(column=4, row=2)
    
    def load_images(self):
        def load_image(path, size):
            img = Image.open(path).convert("RGBA")
            img = ImageOps.contain(img, size)  # Ensure uniform size without distortion
            new_img = Image.new("RGBA", size, (0, 0, 0, 0))  # Create a transparent background
            new_img.paste(img, ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2), img)  # Center image
            return ImageTk.PhotoImage(new_img)
        
        self.toad_tk = load_image(self.characters_path + "toad_kart.webp", (200, 200))
        self.kai_tk = load_image(self.characters_path + "kai.webp", (200, 200))
        
        item_names = ["redshell", "bobomb", "blueshell", "shock", "mushroom", "goldmushroom", "bill", "banana"]
        self.item_images = [load_image(self.items_path + f"{name}.webp", (200, 200)) for name in item_names]
    
    def animate_item_selection(self):
        def update_image(index=0):
            if index < 15:  # Limit the animation to 10 cycles
                self.item_label.configure(image=self.item_images[index % len(self.item_images)])
                self.root.after(100, update_image, index + 1)
            else:
                self.item_label.configure(image=random.choice(self.item_images))  # Final selection, add weights=weights(POS, DIST)
        
        self.root.after(0, update_image)

if __name__ == "__main__":
    root = Tk()
    app = MarioKartUI(root)
    root.mainloop()
