import tkinter as tk 
from tkinter import *
from pytube import YouTube 
from tkinter import messagebox, filedialog 
import requests
import json
import os  
from tkinter.ttk import Progressbar 

def progress_function(stream, chunk, bytes_remaining):
    progress['value'] = round((1-bytes_remaining/stream.filesize)*100)
    root.update_idletasks()
    

def findall(res):
    all_positions=[]
    next_pos=-1
    while True:
        next_pos=res.find("ID",next_pos+1)
        if(next_pos<0):
            break
        idend=res.find(',',next_pos)
        all_positions.append(res[next_pos+4:idend])
        next_pos=res.find("VideoUrl",next_pos+1)
        idend=res.find(',',next_pos)
        all_positions.append(res[next_pos+11:idend-1])
    return all_positions

 
def Browse(): 
    download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH") 
    download_Path.set(download_Directory) 
  

def Download(): 
    Youtube_link = video_Link.get() 
    download_Folder = download_Path.get() 
    getVideo = YouTube(Youtube_link, on_progress_callback=progress_function) 
    videoStream = getVideo.streams.first() 
    videoStream.download(download_Folder)  
    messagebox.showinfo("SUCCESSFULLY",  
                        "DOWNLOADED AND SAVED IN\n" 
                        + download_Folder)

def apidownload():
    url = video_Link.get()
    myobj = {
        "Gender":"All",
        "MacAddress":"b8:27:eb:45:c7:21",
        "Location":"", 
        "Business":"",
        "Age":""
    }
    download_Folder = download_Path.get()
    x = requests.post(url, data = myobj)
    res = x.text
    res = json.loads(res)
    idvideo = findall(res)
    d =0
    while idvideo[d]:
        yt = YouTube(idvideo[d+1], on_progress_callback=progress_function)
        yt.streams.filter(progressive=True, file_extension='mp4').first().download(download_Folder)
        os.rename(download_Folder+"/"
                        + yt.streams.first().default_filename,download_Folder+"/"+ idvideo[d]+'.mp4')
        d=d+2
        messagebox.showinfo("SUCCESSFULLY",  
                        "DOWNLOADED AND SAVED IN\n" +download_Folder+"/"
                        + idvideo[d]+'.mp4') 
  

root = tk.Tk() 
   
 
root.geometry("600x150") 
root.resizable(False, False) 
root.title("YouTube_Video_Downloader") 
root.config(background="#000000") 

video_Link = StringVar() 
download_Path = StringVar() 
   

link_label = Label(root,  
                       text="URL Link         :",
                        bg="#E8D579")
link_label.grid(row=1, 
                    column=0, 
                    pady=5, 
                    padx=5) 
   
root.linkText = Entry(root, 
                          width=55, 
                          textvariable=video_Link) 
root.linkText.grid(row=1,  
                       column=1, 
                       pady=5, 
                       padx=5, 
                       columnspan = 2) 
   
destination_label = Label(root,  
                              text="Destination    :", 
                              bg="#E8D579") 
destination_label.grid(row=2, 
                           column=0, 
                           pady=5, 
                           padx=5) 
   
root.destinationText = Entry(root, 
                                 width=40, 
                                 textvariable=download_Path) 
root.destinationText.grid(row=2,  
                              column=1, 
                              pady=5, 
                              padx=5) 
   
browse_B = Button(root,  
                      text="Browse", 
                      command=Browse, 
                      width=10, 
                      bg="#05E8E0") 
browse_B.grid(row=2, 
                  column=2, 
                  pady=1, 
                  padx=1) 
progress = Progressbar(root, orient = HORIZONTAL, 
            length = 100, mode = 'determinate')
   
progress.grid(row=3,  column=1, 
                  pady=5, 
                  padx=5)
Download_B = Button(root, 
                        text="Download from url",  
                        command=Download,  
                        width=20, 
                        bg="#05E8E0")
Download_B.grid(row=4, 
                    column=0, 
                    pady=5, 
                    padx=5)
Download_c = Button(root, 
                        text="Download from api",  
                        command=apidownload,  
                        width=20, 
                        bg="#05E8E0")
Download_c.grid(row=4, 
                    column=1, 
                    pady=5, 
                    padx=5) 
   

root.mainloop() 
