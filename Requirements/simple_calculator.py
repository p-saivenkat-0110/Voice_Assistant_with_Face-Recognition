import tkinter
root = tkinter.Tk()

root.title("Calculator")
root.iconbitmap(r"C:\Users\saive\OneDrive\Desktop\CODING WORK\Python programs\Voice assistant(Mini project)\calculator.ico")
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

root.geometry(f"360x460+{(sw+650)//2}+{(sh-650)//2}")
root.configure(padx=15,bg="#dbaf86")
root.resizable(0,0)

e1L1 = tkinter.Label(root,text="Expression : ",borderwidth=4)
e2L2 = tkinter.Label(root,text="Result        : ",borderwidth=4)
e1L1.grid(row=0,column=0)
e2L2.grid(row=1,column=0)

entry1 = tkinter.Entry(root,bg="white",borderwidth=5,width=32)
entry1.grid(row=0,rowspan=1,column=1,columnspan=6,padx=10,pady=10)
entry2 = tkinter.Entry(root,bg="white",borderwidth=5,width=32)
entry2.grid(row=1,rowspan=1,column=1,columnspan=6,padx=10,pady=10)

empty = tkinter.Label(root,bg="#dbaf86")
empty.grid(row=2,column=0,columnspan=6)

tmp1=[]

def number(x):
    if x=="clear":
        entry1.delete(0,"end")
        entry2.delete(0,"end")
    elif x=="=":
        try:
            entry2.delete(0, "end")
            exp = entry1.get()
            if "x" in exp:
                tmp = list(exp)
                tmp[tmp.index("x")] = "*"
                exp = "".join(tmp)
            result = eval(exp)
            entry2.insert(0,result)
            tmp1.append(1)

        except ZeroDivisionError:
            entry2.insert(0, "Cannot divide by 0")
        except:
            entry2.insert(0, "Invalid Expression")
    else:
        if len(tmp1)!=0:
            entry1.delete(0,"end")
            entry2.delete(0,"end")
            tmp1.clear()

        if x!="=":
            if x=="*":
                x="x"
            entry1.insert("end",str(x))

padx = 15
pady = 15
bw = 5

b0 = tkinter.Button(root,text="0",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(0))
b1 = tkinter.Button(root,text="1",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(1))
b2 = tkinter.Button(root,text="2",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(2))
b3 = tkinter.Button(root,text="3",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(3))
b4 = tkinter.Button(root,text="4",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(4))
b5 = tkinter.Button(root,text="5",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(5))
b6 = tkinter.Button(root,text="6",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(6))
b7 = tkinter.Button(root,text="7",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(7))
b8 = tkinter.Button(root,text="8",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(8))
b9 = tkinter.Button(root,text="9",bg="#95cacf",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number(9))

Ba = tkinter.Button(root,text="+",bg="#faa70c",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number("+"))
Bs = tkinter.Button(root,text="-",bg="#faa70c",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number("-"))
Bc = tkinter.Button(root,text="C",bg="#a7d685",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number("clear"))
Bm = tkinter.Button(root,text="x",bg="#faa70c",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number("*"))
Bd = tkinter.Button(root,text="/",bg="#faa70c",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number("/"))
Be = tkinter.Button(root,text="=",bg="#faa70c",width=5,height=2,borderwidth=bw,padx=padx,pady=pady,command=lambda: number("="))

b0.grid(row=6,column=1)
b1.grid(row=5,column=0)
b2.grid(row=5,column=1)
b3.grid(row=5,column=2)
b4.grid(row=4,column=0)
b5.grid(row=4,column=1)
b6.grid(row=4,column=2)
b7.grid(row=3,column=0)
b8.grid(row=3,column=1)
b9.grid(row=3,column=2)

Ba.grid(row=3,column=3)
Bs.grid(row=4,column=3)
Bc.grid(row=6,column=0)
Bm.grid(row=5,column=3)
Bd.grid(row=6,column=3)
Be.grid(row=6,column=2)

root.mainloop()