import pytube
import tkinter as tk

from tkinter import ttk, filedialog, messagebox

class YouTubeDownLoader():
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Ahndrenaline's YouTube DownLoader Ver 0.1")
        self.app.geometry('650x350')
        self.app.resizable(False, False)
        self.create_Widgets()

    def click_Treeview(self, event):
        self.selected_Item = self.treeview.focus()
        self.choice = int((self.treeview.item(self.selected_Item)['text']))
        self.itag = self.videos[self.choice].itag
        self.filesize = self.videos[self.choice].filesize
        self.label_progressbar['text'] = 'Selected itag : ' + str(self.itag) + ', Selected Row File size : ' + str(self.filesize)
        # self.yt.register_on_progress_callback(self.progressbar_Checker)
        self.yt.register_on_complete_callback(self.progressbar_Complete)

    def click_Browse(self):
        self.downpath_value.set(filedialog.askdirectory(parent=self.app))

    def click_Clear(self):
        self.btn['text'] = 'Scan'
        self.label_progressbar['text'] = 'Ready ...'
        self.url_value.set('')
        self.downpath_value.set('')
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def btn_action(self):
        if self.btn['text'] == 'Scan':
            self.scan_Content()
            self.label_progressbar['text'] = 'Contents Scan Completed'
            self.btn['text'] = 'Download'
        elif self.btn['text'] == 'Download':
            self.videos[self.choice].download(str(self.downpath_value.get()))

    def progressbar_Checker(self, stream=None, chunk=None, file_handle=None, bytes_remaining=None):
        self.label_progressbar['text'] = 'Down Loading bytes Remaining ... :  ' + str(bytes_remaining)
        print(type(bytes_remaining))
        print(bytes_remaining)
        print(type(self.filesize))
        self.progressbar['value'] = (100 * (self.filesize - int(bytes_remaining)) / self.filesize)
        self.progressbar.update()

    def progressbar_Complete(self, stream=None, file_handle=None):
        self.progressbar['value'] = 0
        self.progressbar.update()
        self.label_progressbar['text'] = 'Down Ready ...'
        messagebox.showinfo(title='Download Info', message='Download Success ~!!')

    def create_Widgets(self):
        # YouTube URL
        self.label_url = ttk.Label(self.app, text='YouTube URL : ')
        self.label_url.grid(row=0, column=0, sticky=tk.E)

        self.url_value = tk.StringVar()
        self.entry_url = ttk.Entry(self.app, textvariable=self.url_value, width=65)
        self.entry_url.grid(row=0, column=1)

        self.btn = ttk.Button(self.app, text='Scan', command=self.btn_action)
        self.btn.grid(row=0, column=2, sticky=tk.NW)

        # Download
        self.label_down = ttk.Label(self.app, text='Download Path : ')
        self.label_down.grid(row=1, column=0, sticky=tk.E)

        self.downpath_value = tk.StringVar()
        self.entry_down = ttk.Entry(self.app, textvariable=self.downpath_value, width=65)
        self.entry_down.grid(row=1, column=1)

        self.btn_filedialog = ttk.Button(self.app, text='Browse', command=self.click_Browse)
        self.btn_filedialog.grid(row=1, column=2, sticky=tk.NW)

        # Treeview
        self.treeview = ttk.Treeview(self.app)
        self.treeview['column'] = ('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7')

        self.treeview.column('#0', width=42)
        self.treeview.column('col1', width=50)
        self.treeview.column('col2', width=100)
        self.treeview.column('col3', width=75)
        self.treeview.column('col4', width=100)
        self.treeview.column('col5', width=75)
        self.treeview.column('col6', width=100)
        self.treeview.column('col7', width=100)

        self.treeview.heading('#0', text='No')
        self.treeview.heading('col1', text='itag')
        self.treeview.heading('col2', text='mime_type')
        self.treeview.heading('col3', text='res')
        self.treeview.heading('col4', text='abr')
        self.treeview.heading('col5', text='fps')
        self.treeview.heading('col6', text='vcodec')
        self.treeview.heading('col7', text='acodec')

        self.treeview.bind('<ButtonRelease-1>', self.click_Treeview)

        self.treeview.grid(row=2, column=0, columnspan=3)

        # LabelFrame
        self.label_frame = ttk.LabelFrame(self.app, text='Download Information')
        self.label_frame.grid(row=3, column=0, columnspan=3)

        # Progress Bar
        self.label_progressbar = ttk.Label(self.label_frame, text='Ready ...')
        self.label_progressbar.grid(row=4, column=0, sticky=tk.W)

        self.progressbar = ttk.Progressbar(self.label_frame, orient=tk.HORIZONTAL, length=550)
        self.progressbar['maximum'] = 100
        self.progressbar.grid(row=5, column=0)

        # Clear Button
        self.btn_clear = ttk.Button(self.label_frame, text='Clear', command=self.click_Clear)
        self.btn_clear.grid(row=5, column=2, sticky=tk.NW)

    def scan_Content(self):
        self.yt = pytube.YouTube(self.url_value.get())
        # self.videos = self.yt.streams.all()
        self.videos = self.yt.streams.filter(progressive=True)
        for i, elements in enumerate(self.videos):
            self.treeview.insert('', i, text=str(i), values=(elements.itag
                                                             ,elements.mime_type
                                                             ,elements.resolution
                                                             ,elements.abr
                                                             ,elements.fps
                                                             ,elements.video_codec
                                                             ,elements.audio_codec))

if __name__ == '__main__':
    youtubedownloader = YouTubeDownLoader()
    youtubedownloader.entry_url.focus()
    youtubedownloader.app.mainloop()
