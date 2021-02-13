from tkinter import filedialog
from tkinter.filedialog import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import simpledialog

dirpath = os.getcwd()

program_name = "HTML editor"
file_name = None
# Mato

keywords = ["<!DOCTYPE>",
             "<html>", "</html>",
             "<head>", "</head>",
             "<title>", "</title>",
             "<body>", "</body>",
             "<p>", "</p>",
             "<br>", "</br>",
             "<hr>", "</hr>",
             "<b>", "</b>",
             "<img>", "<img>",
             "<a>", "</a>",
             "<div>", "</div>",
             "<header>", "</header>",
             "<article>", "</article>",
             "<style>", "</style>",
             "<meta>", "</meta>",
             "<form>", "</form>",
             "<textarea>", "</textarea>",
             "<button>", "</button>",
             "<select>", "</select>"]

root = Tk()
root.geometry('800x600')
root.title(program_name)
root.iconbitmap(dirpath + '\editor.ico')

# Samo
# IKONY
img_undo = ImageTk.PhotoImage(Image.open("undo.png"))
img_redo = ImageTk.PhotoImage(Image.open("redo.png"))
img_copy = ImageTk.PhotoImage(Image.open("copy.png"))
img_cut = ImageTk.PhotoImage(Image.open("cut.png"))
img_paste = ImageTk.PhotoImage(Image.open("paste.png"))
img_save = ImageTk.PhotoImage(Image.open("save.png"))
img_file = ImageTk.PhotoImage(Image.open("file.png"))
img_open_file = ImageTk.PhotoImage(Image.open("open_file.png"))
img_theme = ImageTk.PhotoImage(Image.open("theme.png"))
img_exit = ImageTk.PhotoImage(Image.open("exit.png"))
img_saveAs = ImageTk.PhotoImage(Image.open("saveAs.png"))
img_save_as = ImageTk.PhotoImage(Image.open("save_as.png"))
img_select_all = ImageTk.PhotoImage(Image.open("select_all.png"))
img_about = ImageTk.PhotoImage(Image.open("about.png"))
img_help = ImageTk.PhotoImage(Image.open("help.png"))
img_search = ImageTk.PhotoImage(Image.open("search.png"))


# Mato, Samo, Arina
# OPERACIE
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)


def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)


def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')


def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)


def toggle_highlight(event=None):
    highlight_line()


def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()
    try:
        content_text.tag_remove("search", "1.0", END)
    finally:
        pass


def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for k in range(1, int(row)):
            output += str(k) + '\n'
    return output


def display_about_messagebox():
    messagebox.showinfo("Autori", "{}{}".format(program_name, "\nxdubec00\nxspisa00\nxsharl00"))


def display_help_messagebox():
    messagebox.showinfo("O aplikácií:", "Projekt do predmetu ITU\nZadanie: Editor zdrojových textov", icon='question')


def exit_editor():
    if messagebox.askokcancel("Ukončiť", "Naozaj ukončiť?\n Uistite sa, že ste si svoju robotu uložili."):
        root.destroy()


def new_file(event=None):
    root.title("Nepomenovaný")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed()


def open_file(event=None):
    input_file_name = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), program_name))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
        on_content_changed()


def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        messagebox.showwarning("Uložiť", "Nepodarilo sa uložiť súbor.")


def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"


def save_as(event=None):
    input_file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), program_name))
    return "break"


def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return "break"


def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"


def copy():
    content_text.event_generate("<<Copy>>")
    return "break"


def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"


def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return "break"


def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return 'break'

# Arina
def find_in_file(event=None):
    findString = simpledialog.askstring("Find....", "Enter text")

    matches_found = 0
    start_pos = "1.0"
    while True:
        start_pos = content_text.search(findString, start_pos, stopindex=END)
        if not start_pos:
            break

        end_pos = '{}+{}c'.format(start_pos, len(findString))
        content_text.tag_add("search", start_pos, end_pos)
        matches_found += 1
        start_pos = end_pos
    content_text.tag_config("search", foreground="red", background="yellow")
    if matches_found == 0:
        messagebox.showinfo("Not Found", "No results")

# Samo
def highlight(event=None):
    length = IntVar()
    for keyword in keywords:
        start = 1.0
        idx = content_text.search(keyword, start, stopindex=END, count=length, regexp=1)
        while idx:
            end = f"{idx}+{length.get()}c"
            content_text.tag_add("keyword", idx, end)

            start = end
            idx = content_text.search(keyword, start, stopindex=END, regexp=1)

        highlight_regex(r"[\'][^\']*[\']", "string")
        highlight_regex(r"[\"][^\']*[\"]", "string")


def highlight_regex(regex, tag):
    length = IntVar()
    start = 1.0
    idx = content_text.search(regex, start, stopindex=END, regexp=1, count=length)
    while idx:
        end = f"{idx}+{length.get()}c"
        content_text.tag_add(tag, idx, end)

        start = end
        idx = content_text.search(regex, start, stopindex=END, regexp=1, count=length)


def on_key_release(event=None):
    highlight()

def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(background=background_color, fg=foreground_color)



# Mato, Samo
# HORNA LISTA
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', underline=0, command=new_file, image=img_file)
file_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left', underline=0, command=find_in_file, image=img_search)

file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', underline=0, command=open_file, image=img_open_file)
file_menu.add_command(label='Save', accelerator='Ctrl+S', compound='left', underline=0, command=save, image=img_save)

file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', compound='left', command=save_as, image=img_save_as)

file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', compound='left', command=exit_editor, image=img_exit)

menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left', command=undo, image=img_undo)

edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', command=redo, image=img_redo)

edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left', command=cut, image=img_cut)

edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left', command=copy, image=img_copy)

edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left', command=paste, image=img_paste)

edit_menu.add_separator()
edit_menu.add_command(label='Select All', underline=7, accelerator='Ctrl+A', compound='left', command=select_all, image=img_select_all)

menu_bar.add_cascade(label='Edit', menu=edit_menu)

view_menu = Menu(menu_bar, tearoff=0)
show_line_number = IntVar()
show_line_number.set(1)

show_cursor_info = IntVar()
show_cursor_info.set(1)

# Menu - About
about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label='Authors', compound='left', command=display_about_messagebox, image=img_about)
about_menu.add_command(label='Info', compound='left', command=display_help_messagebox, image=img_help)
menu_bar.add_cascade(label='About',  menu=about_menu)
root.config(menu=menu_bar)

shortcut_bar = Frame(root,  height=25, background='DeepSkyBlue4')
shortcut_bar.pack(expand='no', fill='x')

themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)

color_schemes = {
    'Default': '#000000.#FFFFFF',

    'Night Mode': '#FFFFFF.#3c4a40',
}

theme_choice = StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(
        label=k, variable=theme_choice, command=change_theme)
menu_bar.add_cascade(label='View', menu=view_menu)

# Mato
# TOOLBAR S IKONAMI
tool_bar_icon = img_file
tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=new_file)
tool_bar.image = tool_bar_icon
tool_bar.pack(side='left')

tool_bar_icon = img_open_file
tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=open_file)
tool_bar.image = tool_bar_icon
tool_bar.pack(side='left')

tool_bar_icon = img_save
tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=save)
tool_bar.image = tool_bar_icon
tool_bar.pack(side='left')

tool_bar_icon = img_undo
tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=undo)
tool_bar.image = tool_bar_icon
tool_bar.pack(side='left')

tool_bar_icon = img_redo
tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=redo)
tool_bar.image = tool_bar_icon
tool_bar.pack(side='left')

tool_bar_icon = img_search
tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=find_in_file)
tool_bar.image = tool_bar_icon
tool_bar.pack(side='left')

# VLASTNOSTI
line_number_bar = Text(root, width=4, padx=3, takefocus=0,  border=0, background='DeepSkyBlue2', state='disabled',  wrap='none')

line_number_bar.pack(side='left',  fill='y')

content_text = Text(root, wrap='word', undo=1)
content_text.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

content_text.tag_configure("keyword", foreground='red')
content_text.tag_configure("string", foreground='green')

# Arina
# NABINDOVANE SKRATKY
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-F>', find_in_file)
content_text.bind('<Control-f>', find_in_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.tag_configure('active_line', background='#cac9f2')

# PRAVY KLIK MYSOU
popup_menu = Menu(content_text, tearoff=0)

popup_menu.add_command(label='cut', compound='left', command=cut)
popup_menu.add_command(label='copy', compound='left', command=copy)
popup_menu.add_command(label='paste', compound='left', command=paste)
popup_menu.add_command(label='undo', compound='left', command=undo)
popup_menu.add_command(label='redo', compound='left', command=redo)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=select_all)


content_text.bind('<Button-3>', show_popup_menu)
content_text.bind('<KeyRelease>', on_key_release)

toggle_highlight()

content_text.focus_set()
root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()
