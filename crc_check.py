# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import showwarning
import hashlib
import os


def getHash(file, mode):
    # 选择hash方式
    if mode == 0:
        m = hashlib.md5()
    elif mode == 1:
        m = hashlib.sha1()
    elif mode == 2:
        m = hashlib.sha256()
    elif mode == 3:
        m = hashlib.sha512()
    
    while True:
        data = file.read(102400)
        if not data:
            break
        m.update(data)
    return m.hexdigest()
    

class myApp:
    def __init__(self, root) -> None:
        self.hashAlg = ['MD2', 'SHA1', 'SHA256', 'SHA512']
        self.root = root
        root.title('HASH Check Tool')
        root.geometry('820x280')
        root.resizable(False, False)
        # 组件定义
        self.appName = tk.Label(root, text="HASH校验小工具", font=("微软雅黑", 22))
        self.crcModeName = tk.Label(root, text="选择校验方式", font=("微软雅黑", 14))
        self.fileSelLabel = tk.Label(root, text="打开文件", font=("微软雅黑", 14))
        self.crcTargetName = tk.Label(root, text="HASH目标值", font=("微软雅黑", 14))
        self.crcResultName = tk.Label(root, text="HASH校验值", font=("微软雅黑", 14))
        self.startButton = tk.Button(root, text="开始校验", font=("微软雅黑", 14), command=self.startCheck)
        self.exitButton = tk.Button(root, text=("退出"), font=("微软雅黑", 14), command=self.exitApp)
        self.crcMode = tk.IntVar()
        self.crcMode.set(1)
        self.crcMD5 = tk.Radiobutton(root, text="MD5", variable=self.crcMode, value=0, font=("微软雅黑", 14))
        self.crcSHA1 = tk.Radiobutton(root, text="SHA1", variable=self.crcMode, value=1, font=("微软雅黑", 14))
        self.crcSHA256 = tk.Radiobutton(root, text="SHA256", variable=self.crcMode, value=2, font=("微软雅黑", 14))
        self.crcSHA512 = tk.Radiobutton(root, text="SHA512", variable=self.crcMode, value=3, font=("微软雅黑", 14))
        self.filePathVal = tk.StringVar()
        self.filePath = tk.Entry(root, width=60, textvariable=self.filePathVal, font=("微软雅黑", 14))
        self.filePath.delete(0, "end")
        self.filePath.insert(0, "Please select a file")
        self.fileOpenButton = tk.Button(root, text="...", font=("微软雅黑", 12), command=self.getFilePath)
        self.hashTargetInfo = tk.StringVar()
        self.hashTarget = tk.Entry(root, width=60, textvariable=self.hashTargetInfo, font=("微软雅黑", 14))
        self.hashResultInfo = tk.StringVar()
        self.hashResult = tk.Entry(root, width=60, textvariable=self.hashResultInfo, font=("微软雅黑", 14))
        # 组件摆放
        self.appName.pack()
        self.crcModeName.place(x=10, y=50)
        self.crcMD5.place(x=140, y=50)
        self.crcSHA1.place(x=240, y=50)
        self.crcSHA256.place(x=340, y=50)
        self.crcSHA512.place(x=460, y=50)
        self.fileSelLabel.place(x=10, y=90)
        self.fileOpenButton.place(x=95, y=85)
        self.filePath.place(x=140, y=90)
        self.crcTargetName.place(x=10, y=130)
        self.hashTarget.place(x=140, y=130)
        self.crcResultName.place(x=10, y=170)
        self.hashResult.place(x=140, y=170)
        self.startButton.place(x=320, y=220)
        self.exitButton.place(x=430, y=220)

    def getFilePath(self):
        # 路径清空，hash值清空
        self.filePath.delete(0, "end")
        self.hashTarget.delete(0, "end")
        self.hashResult.delete(0, "end")
        # 选择文件
        path = askopenfilename()
        self.filePathVal.set(path)

    def startCheck(self):
        with open(self.filePathVal.get(), 'rb') as f:
            crcResult = getHash(f, self.crcMode.get())
            self.hashResultInfo.set(crcResult)
            if self.hashTarget.get() != "":
                if crcResult == self.hashTargetInfo.get():
                    showinfo('通知', '文件HASH校验通过')
                else:
                    showerror('错误', '文件哈希校验未通过！')
            else:
                dir = os.path.dirname(self.filePathVal.get())
                txtName = dir + '/' + 'HASH_Result_' + os.path.split(self.filePathVal.get())[1] + '.txt'
                msg = self.hashAlg[self.crcMode.get()] + ": " + self.hashResultInfo.get()
                f = open(txtName, "a")
                f.write(msg)
                f.close
                showwarning('警告', '目标哈希值为空，已经HASH校验结果写入文件所在目录！')


    def exitApp(self):
        self.root.destroy()

    def run_app(self):
        self.root.mainloop()

window = tk.Tk()
crc_check_app = myApp(root=window)
crc_check_app.run_app()
