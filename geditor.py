import Tkinter as tk
import ttk as ttk
from ScrolledText import ScrolledText
import tkMessageBox
from Tkinter import *
from ttk import *
#from main import Scm
import main
ShowDebugInfo = True
class Editor(ScrolledText):
    def __init__(self,*arg,**kw):
        ScrolledText.__init__(self,*arg,**kw)
##        frameText = Frame(self, relief=SUNKEN, height=700)
##        frameButtons = Frame(self)
##        self.buttonOk = Button(frameButtons, text='Close',
##                               command=self.Ok, takefocus=FALSE)
##        self.scrollbarView = Scrollbar(frameText, orient=VERTICAL,
##                                       takefocus=FALSE, highlightthickness=0)
##        self.textView = Text(frameText, wrap=WORD, highlightthickness=0,
##                             fg=self.fg, bg=self.bg)
##        self.scrollbarView.config(command=self.textView.yview)
##        self.textView.config(yscrollcommand=self.scrollbarView.set)
##        self.buttonOk.pack()
##        self.scrollbarView.pack(side=RIGHT,fill=Y)
##        self.textView.pack(side=LEFT,expand=TRUE,fill=BOTH)
##        frameButtons.pack(side=BOTTOM,fill=X)
##        frameText.pack(side=TOP,expand=TRUE,fill=BOTH)
    def text(self):
        pass
    def setText(self,text):
        pass
class Application(Frame):
    def runCode(self):
        import traceback
        reload(main) 
        s = main.Scm()
        #print self.editor.get("1.0", "end-1c")
        code = self.editor.get("1.0", "end-1c")
        try:
            code = s.sh("(begin %s)"%code)
            self.output.delete("1.0", "end-1c")
            self.output.insert("1.0", code)
        except Exception as e:
            code = str(e)
            self.output.delete("1.0", "end-1c")
            self.output.insert("1.0", code)
            traceback.format_exc()
            if ShowDebugInfo:
                tkMessageBox.showwarning("Error", traceback.format_exc())
            #traceback.print_exc()
        self.output.delete("1.0", "end-1c")
        self.output.insert("1.0", code)
    def help(self):
        code = """A Simple Editor For Casuistry Scheme"""
        self.output.delete("1.0", "end-1c")
        self.output.insert("1.0", code)

    def createWidgets(self):
        self.debug = Checkbutton(self,text="debug")
        self.quit = Button(self,text="Quit",command=self.quit)
        self.run = Button(self,text="Run",command= self.runCode)
        self.help = Button(self,text="Help",command=self.help)
        self.editor = ScrolledText(wrap="word")
        self.output = ScrolledText(wrap="word",height=7)
        
        self.debug.pack({"side": "left"})
        self.run.pack({"side": "left"})
        self.help.pack({"side": "left"}) 
        self.quit.pack({"side": "left"})
        
        self.output.pack(side=BOTTOM,expand=TRUE,fill=BOTH)
        self.editor.pack(side=BOTTOM,expand=TRUE,fill=BOTH)

        self.editor.focus_set()
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.title("Casuistry Scheme")
app = Application(master=root)
app.mainloop()
root.destroy()
