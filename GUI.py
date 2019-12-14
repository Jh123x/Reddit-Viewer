import tkinter, os
from tkinter import messagebox
from PIL import ImageTk, Image, ImageOps
from redditbot import RedditBot
from dotenv import load_dotenv

class rGUI(tkinter.Frame):
    def __init__(self, rbot, master = None):
        '''Initialise rGUI'''
        self.master = master
        self.rbot = rbot
        super().__init__(master)
        self.create_widgets()

    def resize(self, img : Image):
        '''Resize the image to the correct size'''
        height = 400
        hpercent = (height/float(img.size[1]))
        wsize = int(float(img.size[0])*float(hpercent))

        #If the width is too wide
        if(wsize > 700):
            width = 700
            wpercent = (width/float(img.size[1]))
            hsize = int(float(wpercent) * img.size[1])
            return img.resize((width,hsize), Image.ANTIALIAS)
        else:
            return img.resize((wsize,height), Image.ANTIALIAS)

    def refresh(self):
        '''Refresh the meme'''
        self.rbot.set_subreddit(self.sub.get())
        self.rbot.load_meme()
        image = ImageTk.PhotoImage(self.resize(Image.open('temp/temp.png')))
        self.img_lbl.configure(image = image)
        self.img_lbl.image = image
    
    def create_widgets(self):
        '''Create the widgets within the tkinter application'''

        #Creating the string variable
        self.sub = tkinter.StringVar()

        #Creating the main label
        self.mainlbl = tkinter.Label(self, text = "Random Meme viewer")

        #Entry to key in the subreddit
        self.sub_entry = tkinter.Entry(self,textvariable = self.sub)

        #Insert the default subreddit to the page
        self.sub_entry.insert(0,'memes')

        #Button to allow the user to refresh
        self.refresh_btn = tkinter.Button(self, text = "New Meme", command = self.refresh)

        #Image box for the image
        img = self.resize(Image.open('temp/temp.png'))
        image = ImageTk.PhotoImage(img)
        self.img_lbl = tkinter.Label(self,image = image)
        self.img_lbl.image = image

        #Assign grid space to all of the items
        self.mainlbl.grid(row = 0, column = 5)
        self.sub_entry.grid(row = 1, column = 4)
        self.refresh_btn.grid(row = 1, column = 6)
        self.img_lbl.grid(row = 2, column = 0, columnspan = 10)

#Main function
def main():
    #load the environment
    load_dotenv()

    #Load the reddit tokens
    secret = os.getenv('REDDIT_SECRET')
    id = os.getenv('REDDIT_ID')
    password = os.getenv('REDDIT_PASSWORD')
    username = os.getenv('REDDIT_USERNAME')

    #Call the redditbot
    rbot = RedditBot(username, password, secret, id)

    #Loading the GUI
    root = tkinter.Tk()
    app = rGUI(rbot,root)
    app.pack()

    #Set the geometry for the root
    root.geometry("700x500")

    #Set the title for the window
    root.title('Random Reddit Posts')

    #Run the GUI
    root.mainloop()

if(__name__ == '__main__'):
    main()