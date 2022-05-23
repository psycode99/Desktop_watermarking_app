import cv2 as cv
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import os

images = []
watermarks = []

window = Tk()
window.title('Water Marking App')
window.config(padx=50, pady=50)


def upload_image():
    images.clear()
    f_types = [('JPG files', '*.jpg'), ('PNG files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    resized_img = img.resize((200, 200))
    img = ImageTk.PhotoImage(resized_img)
    display_button = Button(window, image=img, highlightthickness=0, )
    display_button.imageList = []
    display_button.grid(row=2, column=1)
    display_button.imageList.append(img)
    images.append(filename)


def upload_watermarker():
    watermarks.clear()
    f_types = [('JPG files', '*.jpg'), ('PNG files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    resized_img = img.resize((50, 50))
    img = ImageTk.PhotoImage(resized_img)
    display_button = Button(window, image=img, highlightthickness=0, )
    display_button.imageList = []
    display_button.grid(row=4, column=1)
    display_button.imageList.append(img)
    watermarks.append(filename)


def watermarked():
    for image, wat in zip(images, watermarks):
        img = cv.imread(image)
        water_img = cv.imread(wat)
        resized_img = cv.resize(img, (400, 400))
        resized_water_img = cv.resize(water_img, (150, 100))

        rows, columns, channels = resized_water_img.shape
        roi = resized_img[0:rows, 0:columns]

        # Now create a mask of logo and create its inverse mask also
        img2gray = cv.cvtColor(resized_water_img, cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
        # mask_inv = cv.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        # removed the mask keyword argument so as not to black out the content of the main picture
        img1_bg = cv.bitwise_and(roi, roi, )

        # Take only region of logo from logo image.
        img2_fg = cv.bitwise_and(resized_water_img, resized_water_img, mask=mask)

        dst = cv.addWeighted(img1_bg, 0.7, img2_fg, 0.7, 0)
        resized_img[0:rows, 0:columns] = dst

        # path to store watermarked images. Can be changed at will
        path = 'C:/Users/GREATFAITH CHURCH/Desktop/watermarked images'

        # shows watermarked image
        cv.imshow('res', resized_img)

        # rename and save watermarked image to given path
        new_name = rename_entry.get()
        cv.imwrite(os.path.join(path, f'{new_name}.jpg'), resized_img)
        cv.waitKey(0)


# GUI userinterface
title = Label(text='WaterMarker', font=('Arial', 25))
title.grid(row=0, column=1)

upload_img = Button(text='Upload Image', command=upload_image)
upload_img.grid(row=1, column=1)

upload_watermark = Button(text='Upload Watermarker', command=upload_watermarker)
upload_watermark.grid(row=3, column=1)

rename = Label(text='Rename File:')
rename.grid(row=5, column=0)

rename_entry = Entry(width=20)
rename_entry.grid(row=5, column=1, columnspan=2)

watermark = Button(text='Watermark and Save', command=watermarked)
watermark.grid(row=6, column=1)

window.mainloop()
