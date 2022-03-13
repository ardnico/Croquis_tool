import sys
import os
import tkinter
from tkinter import font
from PIL import Image, ImageTk
import threading
from glob import glob
import time

files = glob("./img/*.*")
start_img = "./source/start.jpg"
wait_img = "./source/wait.jpg"
end_img = "./source/finish.jpg"

if os.path.exists("setting.txt"):
    with open("setting.txt",mode="r") as f:
        text = f.read()
    for line in text.split("\n"):
        line = line.replace(" ","")
        try:
            if line.find("width:") > -1:
                w = int(line.replace("width:",""))
            elif line.find("height:") > -1:
                h = int(line.replace("height:",""))
            elif line.find("time_list:") > -1:
                time_list = line.replace("time_list:","").split(",")
        except:
            print("Please check the file 'setting.txt'")
            raise Exception
else:
    with open("setting.txt",mode="w") as f:
        f.write("width:640\n")
        f.write("height:480\n")
        f.write("time_list:60,60,60,60,120,120,120,300,300,600")

def resize_img(img,w,h):
    tmp_h = img.height
    tmp_w = img.width
    while True:
        if tmp_h > h:
            tmp_w = int(tmp_w * h / tmp_h)
            tmp_h = h
        if tmp_w > w:
            tmp_h = int(tmp_h * w / tmp_w)
            tmp_w = w
        if tmp_h <= h and tmp_w <= w:
            break
    return img.resize((tmp_w,tmp_h))

def show_image():
    global item, canvas, label
    root = tkinter.Tk()
    root.title('Croquis')
    root.geometry(f"{w}x{h}")
    img = Image.open(start_img)
    img = resize_img(img,w,h)
    img = ImageTk.PhotoImage(img)
    canvas = tkinter.Canvas(bg = "black", width=w, height=h)
    canvas.place(x=0, y=0)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW )
    label = tkinter.Label(root, text="Will start soon")
    label.place(x=1, y=1)
    label.pack()
    root.mainloop()

thread1 = threading.Thread(target=show_image)
thread1.start()
time.sleep(5)

img_wait = Image.open(wait_img)
img_wait = resize_img(img_wait,w,h)
img_wait = ImageTk.PhotoImage(img_wait)
for j in range(10,-1,-1):
        time.sleep(1)
        label['text'] = str(j)

for i in range(len(files)):
    img2 = Image.open(files[i])
    img2 = resize_img(img2,w,h)
    img2 = ImageTk.PhotoImage(img2)
    canvas.itemconfig(item,image=img2)
    for j in range(int(time_list[i])*60,-1,-1):
        time.sleep(1)
        label['text'] = str(j)
    for ij in range(4,-1,-1):
        if i != (len(files)-1):
            canvas.itemconfig(item,image=img_wait)
            label['text'] = str(ij)
        else:
            label['text'] = "Congratulation!"
            img_end = Image.open(end_img)
            img_end = resize_img(img_end,w,h)
            img_end = ImageTk.PhotoImage(img_end)
        time.sleep(1)

canvas.quit()
