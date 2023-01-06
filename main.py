import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


class Main(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Pengolahan Citra")
        self.geometry("1080x900")

        self.resizable(True, True)
        self.config(bg="#B7F397")
        self.create_widgets()

    def _event_pilih_gambar(self):
        path_image = filedialog.askopenfilename()
        if len(path_image) > 0:
            self.image = ImageTk.PhotoImage(file=path_image)
            self.textbox_path_gambar.delete(0, tk.END)
            self.textbox_path_gambar.insert(0, path_image)
            self._event_after_browse(path_image)
        else:
            messagebox.showerror("Error", "Please select an image")

    def _event_after_browse(self, path_image=None):
        self.pil_image1 = Image.open(path_image)
        self.pil_image1 = self.pil_image1.resize((350, 350), Image.ANTIALIAS)
        self.image1 = ImageTk.PhotoImage(self.pil_image1)
        self.Label_1 = tk.Label(self.frame_gambar_asli, image=self.image1)
        self.Label_1.place(x=10, y=0, width=350, height=350)

    def _event_setelah_manipulasi_gambar(self):
        self.pil_image = Image.open(self.result_image)
        self.pil_image = self.pil_image.resize((350, 350), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.pil_image)
        self.Label_2 = tk.Label(self.frame_gambar_hasil, image=self.image)
        self.Label_2.place(x=10, y=0, width=350, height=350)

    def _event_setelah_manipulasi_gambar1(self):
        self.pil_image = Image.open(self.result_image)
        self.image = ImageTk.PhotoImage(self.pil_image)
        self.Label_2 = tk.Label(self.frame_gambar_hasil, image=self.image)
        self.Label_2.place(x=10, y=0, width=350, height=350)

    def _event_dilasi_gambar(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), 0)
        kernel = np.ones((1, 1), np.uint8)
        kernel2 = np.ones((15, 15), np.uint8)

        imgCanny = cv2.Canny(imggambar, 10, 150)
        imgdilation = cv2.dilate(imgCanny, kernel, iterations=1)
        imgdilation2 = cv2.dilate(imgCanny, kernel2, iterations=1)
        imgdilation3 = ~imgdilation2

        tampil_hor = np.concatenate((imggambar, imgdilation), axis=0)
        cv2.imwrite("hasil/hasil_dilasi.jpg", tampil_hor)

        self.result_image = 'hasil/hasil_dilasi.jpg'
        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())

    def _event_erosi_gambar(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), 0)
        kernel = np.ones((5, 5), np.uint8)
        kernel2 = np.ones((1, 1), np.uint8)

        imgCanny = cv2.Canny(imggambar, 10, 150)
        imgdilation5 = cv2.dilate(imgCanny, kernel, iterations=1)
        imgErode = cv2.erode(imgdilation5, kernel2, iterations=1)

        tampil_hor = np.concatenate((imgCanny, imgErode), axis=1)
        cv2.imwrite("hasil/hasil_erosi.jpg", tampil_hor)

        self.result_image = 'hasil/hasil_erosi.jpg'
        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())

    def _event_closing_gambar(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), 0)

        kernel = np.ones((15, 15), np.uint8)

        imgCanny = cv2.Canny(imggambar, 10, 150)
        imgclosing = cv2.morphologyEx(imggambar, cv2.MORPH_CLOSE, kernel)

        # imgmg=cv2.morphologyEx(imggambar,cv2.MORPH_GRADIENT,kernel)

        tampil_hor = np.concatenate((imggambar, imgclosing), axis=0)
        cv2.imwrite("hasil/hasil_closing.jpg", tampil_hor)

        self.result_image = 'hasil/hasil_closing.jpg'
        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())

    def _event_opening_gambar(self):
        imggambara = cv2.imread(self.textbox_path_gambar.get(), 0)
        imggambar = cv2.cvtColor(imggambara, cv2.THRESH_BINARY)
        kernel = np.ones((15, 15), np.uint8)
        imgopening = cv2.morphologyEx(imggambar, cv2.MORPH_OPEN, kernel)

        tampil_hor = np.concatenate((imggambar, imgopening), axis=0)
        cv2.imwrite("hasil/hasil_opening.jpg", tampil_hor)
        self.result_image = 'hasil/hasil_opening.jpg'
        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())

    def _event_invers_gambar(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), 0)
        kernel = np.ones((1, 1), np.uint8)
        kernel2 = np.ones((14, 14), np.uint8)

        thresh = 150
        imgbinary = cv2.threshold(imggambar, thresh, 255, cv2.THRESH_BINARY)[1]

        imginvers = ~imgbinary
        imgdilation = cv2.dilate(imggambar, kernel2, iterations=1)

        tampil_hor = np.concatenate((imgbinary, imginvers), axis=0)

        cv2.imwrite("hasil/hasil_invers.jpg", tampil_hor)
        self.result_image = 'hasil/hasil_invers.jpg'
        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())

    def _event_crop_gambar(self):

        newWindow = tk.Toplevel(self.master)
        newWindow.title("Crop Gambar")
        newWindow.geometry("500x500")
        newWindow.resizable(False, False)
        newWindow.configure(background="#ffffff")

        self.newWindow = newWindow

        self.frame_crop_gambar = tk.Frame(newWindow)
        self.frame_crop_gambar.place(x=0, y=0, width=500, height=500)
        self.frame_crop_gambar.configure(background="#ffffff")

        self.Label_1 = tk.Label(self.frame_crop_gambar)
        self.Label_1["text"] = "Koordinat X1"
        self.Label_1["bg"] = "#ffffff"
        self.Label_1.place(x=10, y=10, width=100, height=25)

        self.textbox_x1 = tk.Entry(self.frame_crop_gambar)
        self.textbox_x1["bg"] = "#ffffff"
        self.textbox_x1.place(x=120, y=10, width=100, height=25)

        self.Label_2 = tk.Label(self.frame_crop_gambar)
        self.Label_2["text"] = "Koordinat Y1"
        self.Label_2["bg"] = "#ffffff"
        self.Label_2.place(x=10, y=50, width=100, height=25)

        self.textbox_y1 = tk.Entry(self.frame_crop_gambar)
        self.textbox_y1["bg"] = "#ffffff"
        self.textbox_y1.place(x=120, y=50, width=100, height=25)

        self.Label_3 = tk.Label(self.frame_crop_gambar)
        self.Label_3["text"] = "Koordinat X2"
        self.Label_3["bg"] = "#ffffff"
        self.Label_3.place(x=10, y=90, width=100, height=25)

        self.textbox_x2 = tk.Entry(self.frame_crop_gambar)
        self.textbox_x2["bg"] = "#ffffff"
        self.textbox_x2.place(x=120, y=90, width=100, height=25)

        self.Label_4 = tk.Label(self.frame_crop_gambar)
        self.Label_4["text"] = "Koordinat Y2"
        self.Label_4["bg"] = "#ffffff"
        self.Label_4.place(x=10, y=130, width=100, height=25)

        self.textbox_y2 = tk.Entry(self.frame_crop_gambar)
        self.textbox_y2["bg"] = "#ffffff"
        self.textbox_y2.place(x=120, y=130, width=100, height=25)

        self.button_crop = tk.Button(self.frame_crop_gambar)
        self.button_crop["text"] = "Crop"
        self.button_crop["bg"] = "#ffffff"
        self.button_crop["command"] = self._event_crop
        self.button_crop.place(x=10, y=170, width=100, height=25)

    def _event_crop(self):

        try:

            imggambar = cv2.imread(self.textbox_path_gambar.get(), 0)

            x1 = int(self.textbox_x1.get())
            y1 = int(self.textbox_y1.get())
            x2 = int(self.textbox_x2.get())
            y2 = int(self.textbox_y2.get())
            imgcrop = imggambar[y1:y2, x1:x2]
            cv2.imwrite("hasil/hasil_crop.jpg", imgcrop)
            self.result_image = 'hasil/hasil_crop.jpg'
            self._event_setelah_manipulasi_gambar1()
            self._event_after_browse(self.textbox_path_gambar.get())
            self.newWindow.destroy()

        except Exception as e:
            messagebox.showerror("Error", "Koordinat yang diinputkan melebihi ukuran gambar")

    def _event_resize(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), -1)

        imgresize = cv2.resize(imggambar, (int(self.textbox_lebar.get()), int(self.textbox_panjang.get())))
        cv2.imwrite("hasil/hasil_resize.jpg", imgresize)
        self.result_image = 'hasil/hasil_resize.jpg'
        self._event_setelah_manipulasi_gambar1()
        self._event_after_browse(self.textbox_path_gambar.get())
        self.newWindow.destroy()

    def _event_resize_gambar(self):

        newWindow = tk.Toplevel(self.master)
        newWindow.title("Resize Gambar")
        newWindow.geometry("500x500")
        newWindow.resizable(False, False)
        newWindow.configure(background="#ffffff")

        self.newWindow = newWindow

        self.frame_resize_gambar = tk.Frame(newWindow)
        self.frame_resize_gambar.place(x=0, y=0, width=500, height=500)
        self.frame_resize_gambar.configure(background="#ffffff")

        self.Label_1 = tk.Label(self.frame_resize_gambar)
        self.Label_1["text"] = "Lebar"
        self.Label_1["bg"] = "#ffffff"
        self.Label_1.place(x=10, y=10, width=100, height=25)

        self.textbox_lebar = tk.Entry(self.frame_resize_gambar)
        self.textbox_lebar["bg"] = "#ffffff"
        self.textbox_lebar.place(x=120, y=10, width=100, height=25)

        self.Label_2 = tk.Label(self.frame_resize_gambar)
        self.Label_2["text"] = "Panjang"
        self.Label_2["bg"] = "#ffffff"
        self.Label_2.place(x=10, y=50, width=100, height=25)

        self.textbox_panjang = tk.Entry(self.frame_resize_gambar)
        self.textbox_panjang["bg"] = "#ffffff"
        self.textbox_panjang.place(x=120, y=50, width=100, height=25)

        self.button_resize = tk.Button(self.frame_resize_gambar)
        self.button_resize["text"] = "Resize"
        self.button_resize["bg"] = "#ffffff"
        self.button_resize["command"] = self._event_resize
        self.button_resize.place(x=10, y=90, width=100, height=25)

    def _event_rotasi(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), -1)

        rows, cols = imggambar.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), int(self.textbox_sudut.get()), 1)
        imgrotasi = cv2.warpAffine(imggambar, M, (cols, rows))
        tampil_hor = np.concatenate((imggambar, imgrotasi), axis=1)

        cv2.imwrite("hasil/hasil_rotasi.jpg", tampil_hor)
        self.result_image = 'hasil/hasil_rotasi.jpg'
        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())
        self.newWindow.destroy()

    def _event_rotasi_gambar(self):
        newWindow = tk.Toplevel(self.master)
        newWindow.title("Rotasi Gambar")
        newWindow.geometry("500x500")
        newWindow.resizable(False, False)
        newWindow.configure(background="#ffffff")

        self.newWindow = newWindow

        self.frame_rotasi_gambar = tk.Frame(newWindow)
        self.frame_rotasi_gambar.place(x=0, y=0, width=500, height=500)
        self.frame_rotasi_gambar.configure(background="#ffffff")

        self.Label_1 = tk.Label(self.frame_rotasi_gambar)
        self.Label_1["text"] = "Rotasi"
        self.Label_1["bg"] = "#ffffff"
        self.Label_1.place(x=10, y=10, width=100, height=25)

        self.textbox_sudut = tk.Entry(self.frame_rotasi_gambar)
        self.textbox_sudut["bg"] = "#ffffff"
        self.textbox_sudut.place(x=120, y=10, width=100, height=25)

        self.button_rotasi = tk.Button(self.frame_rotasi_gambar)
        self.button_rotasi["text"] = "Rotasi"
        self.button_rotasi["bg"] = "#ffffff"
        self.button_rotasi["command"] = self._event_rotasi
        self.button_rotasi.place(x=10, y=50, width=100, height=25)

    def _event_equalize_gambar(self):
        imggambar = cv2.imread(self.textbox_path_gambar.get(), 0)
        img_equalized = cv2.equalizeHist(imggambar)
        tampil_hor = np.concatenate((imggambar, img_equalized), axis=0)
        cv2.imwrite("hasil/hasil_equalized.jpg", tampil_hor)

        # show histogram
        plt.hist(img_equalized.ravel(), 256, [0, 256])
        plt.savefig("hasil/histogram_gambar_sesudah.jpg")

        plt.hist(tampil_hor.ravel(), 256, [0, 256])
        plt.savefig("hasil/histogram_gambar_sebelum.jpg")

        histogram_gambar_sebelum = cv2.imread("hasil/histogram_gambar_sebelum.jpg")
        cv2.imshow("Histogram Sebelum", histogram_gambar_sebelum)

        histogram_gambar_sesudah = cv2.imread("hasil/histogram_gambar_sesudah.jpg")
        cv2.imshow("Histogram Sesudah", histogram_gambar_sesudah)

        self.result_image = 'hasil/hasil_equalized.jpg'

        self._event_setelah_manipulasi_gambar()
        self._event_after_browse(self.textbox_path_gambar.get())

    def _panel_atas(self):
        self.label_judul = tk.Label(self)
        self.label_judul["bg"] = "#B7F397"
        ft = tkFont.Font(family='Times', size=30)
        self.label_judul["font"] = ft
        self.label_judul["fg"] = "#333333"
        self.label_judul["justify"] = "center"
        self.label_judul["text"] = "OpenCV"
        self.label_judul.place(x=300, y=40, width=400, height=49)

        # label frame
        self.groupbox_path_gambar = tk.LabelFrame(self)
        self.groupbox_path_gambar["bg"] = "#B7F397"
        self.groupbox_path_gambar["fg"] = "#333333"
        self.groupbox_path_gambar["text"] = "Masukan Path Gambar"
        self.groupbox_path_gambar.place(x=240, y=100, width=500, height=100)

        # place button in label frame

        self.button_path_gambar = tk.Button(self.groupbox_path_gambar)
        self.button_path_gambar["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_path_gambar["font"] = ft
        self.button_path_gambar["fg"] = "#fff"
        self.button_path_gambar["justify"] = "center"
        self.button_path_gambar["text"] = "Pilih Gambar"
        self.button_path_gambar.place(x=400, y=30, width=80, height=30)
        self.button_path_gambar["command"] = self._event_pilih_gambar

        # text box in label frame path image
        self.textbox_path_gambar = tk.Entry(self.groupbox_path_gambar)
        self.textbox_path_gambar["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.textbox_path_gambar["font"] = ft
        self.textbox_path_gambar["fg"] = "#333333"
        self.textbox_path_gambar["justify"] = "center"
        self.textbox_path_gambar["text"] = "Path Image"
        self.textbox_path_gambar.place(x=10, y=30, width=380, height=30)
        self.textbox_path_gambar["state"] = "normal"

        self.frame_gambar_asli = tk.LabelFrame(self)
        self.frame_gambar_asli["bg"] = "#ffffff"
        self.frame_gambar_asli["text"] = "Gambar Asli"
        self.frame_gambar_asli.place(x=20, y=200, width=500, height=500)

        self.frame_gambar_hasil = tk.LabelFrame(self)
        self.frame_gambar_hasil["bg"] = "#ffffff"
        self.frame_gambar_hasil["text"] = "Gambar Hasil"
        self.frame_gambar_hasil.place(x=550, y=200, width=500, height=500)

    def _panel_bawah(self):
        # label frame
        self.groupbox_menu_pilihan = tk.LabelFrame(self)
        self.groupbox_menu_pilihan["bg"] = "#B7F397"
        self.groupbox_menu_pilihan["fg"] = "#333333"
        self.groupbox_menu_pilihan["text"] = "Menu Pilihan"
        self.groupbox_menu_pilihan.place(x=20, y=720, width=1030, height=100)

        # place button in label frame
        self.button_dilasi = tk.Button(self.groupbox_menu_pilihan)
        self.button_dilasi["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_dilasi["font"] = ft
        self.button_dilasi["fg"] = "#fff"
        self.button_dilasi["justify"] = "center"
        self.button_dilasi["text"] = "Dilasi"
        self.button_dilasi.place(x=10, y=30, width=80, height=30)
        self.button_dilasi["command"] = self._event_dilasi_gambar

        self.button_erosi = tk.Button(self.groupbox_menu_pilihan)
        self.button_erosi["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_erosi["font"] = ft
        self.button_erosi["fg"] = "#fff"
        self.button_erosi["justify"] = "center"
        self.button_erosi["text"] = "Erosi"
        self.button_erosi["command"] = self._event_erosi_gambar
        self.button_erosi.place(x=100, y=30, width=80, height=30)

        self.button_closing = tk.Button(self.groupbox_menu_pilihan)
        self.button_closing["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_closing["font"] = ft
        self.button_closing["fg"] = "#fff"
        self.button_closing["justify"] = "center"
        self.button_closing["text"] = "Closing"
        self.button_closing["command"] = self._event_closing_gambar
        self.button_closing.place(x=190, y=30, width=80, height=30)

        self.button_opening = tk.Button(self.groupbox_menu_pilihan)
        self.button_opening["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_opening["font"] = ft
        self.button_opening["fg"] = "#fff"
        self.button_opening["justify"] = "center"
        self.button_opening["text"] = "Opening"
        self.button_opening["command"] = self._event_opening_gambar
        self.button_opening.place(x=280, y=30, width=80, height=30)

        self.button_invers = tk.Button(self.groupbox_menu_pilihan)
        self.button_invers["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_invers["font"] = ft
        self.button_invers["fg"] = "#fff"
        self.button_invers["justify"] = "center"
        self.button_invers["text"] = "Invers"
        self.button_invers["command"] = self._event_invers_gambar
        self.button_invers.place(x=370, y=30, width=80, height=30)

        self.button_crop = tk.Button(self.groupbox_menu_pilihan)
        self.button_crop["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_crop["font"] = ft
        self.button_crop["fg"] = "#fff"
        self.button_crop["justify"] = "center"
        self.button_crop["text"] = "Crop"
        self.button_crop["command"] = self._event_crop_gambar
        self.button_crop.place(x=460, y=30, width=80, height=30)

        self.button_resize = tk.Button(self.groupbox_menu_pilihan)
        self.button_resize["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_resize["font"] = ft
        self.button_resize["fg"] = "#fff"
        self.button_resize["justify"] = "center"
        self.button_resize["text"] = "Resize"
        self.button_resize["command"] = self._event_resize_gambar
        self.button_resize.place(x=550, y=30, width=80, height=30)

        self.button_rotasi = tk.Button(self.groupbox_menu_pilihan)
        self.button_rotasi["bg"] = "#386A20"
        ft = tkFont.Font(family='Times', size=10)
        self.button_rotasi["font"] = ft
        self.button_rotasi["fg"] = "#fff"
        self.button_rotasi["justify"] = "center"
        self.button_rotasi["text"] = "Rotasi"
        self.button_rotasi["command"] = self._event_rotasi_gambar
        self.button_rotasi.place(x=640, y=30, width=80, height=30)

        self.button_save = tk.Button(self.groupbox_menu_pilihan)
        self.button_save["bg"] = "#386A20"
        self.button_save["fg"] = "#fff"
        ft = tkFont.Font(family='Times', size=10)
        self.button_save["font"] = ft
        self.button_save["justify"] = "center"
        self.button_save["text"] = "Histogram Gambar"
        self.button_save["command"] = self._event_equalize_gambar
        self.button_save.place(x=730, y=30, width=120, height=30)

    def create_widgets(self):
        self._panel_atas()
        self._panel_bawah()


if __name__ == "__main__":
    Main().mainloop()
