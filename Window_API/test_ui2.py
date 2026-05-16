# more practical test
from tkinter import *
from tkinter import ttk
from Backend.Entry_API import *
from Backend import DB_OBJ, initialize

# --- window colors ---
FG = "#ffffff"
BG = "#1e1e1e"
ENTRY_BG = "#2d2d2d"
ENTRY_FG = "#ffffff"
BTN_BG = "#3a3a3a"
BTN_FG = "#ffffff"
ERROR_FG = "#ff4d4d"

def sign_in():
    sign_in_window = Tk()
    sign_in_window.title("Sign In")
    sign_in_window.geometry("450x230")
    sign_in_window.configure(bg=BG)

    # --- Title Label ---
    title_label = Label(sign_in_window, text="Enter database password:", bg=BG, fg=FG)
    title_label.place(x=20, y=20)

    # --- Password Entry ---
    password_var = StringVar()

    password_entry = Entry(
        sign_in_window,
        textvariable=password_var,
        show="*",
        width=30,
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    password_entry.place(x=20, y=55)

    # --- Error Label ---
    error_label = Label(sign_in_window, text="", fg=ERROR_FG, bg=BG)
    error_label.place(x=20, y=85)

    # --- Show Password Checkbox ---
    show_var = IntVar()

    def toggle_password():
        password_entry.config(show="" if show_var.get() else "*")

    show_checkbox = Checkbutton(
        sign_in_window,
        text="Show Password",
        variable=show_var,
        command=toggle_password,
        bg=BG,
        fg=FG,
        selectcolor=BG,
        activebackground=BG,
        activeforeground=FG
    )
    show_checkbox.place(x=20, y=110)

    # --- Submit Button ---
    submit_btn = Button(
        sign_in_window,
        text="Submit",
        state=DISABLED,
        bg=BTN_BG,
        fg=BTN_FG,
        activebackground="#505050"
    )
    submit_btn.place(x=20, y=150)

    # Enable/Disable submit button
    def on_text_change(*args):
        submit_btn.config(state=NORMAL if password_var.get().strip() else DISABLED)

    password_var.trace_add("write", on_text_change)

    # --- Shake Animation (Entry Only) ---
    def shake_entry(widget):
        original_x = widget.winfo_x()
        for _ in range(4):
            widget.place(x=original_x + 5)
            widget.update()
            widget.after(30)
            widget.place(x=original_x - 5)
            widget.update()
            widget.after(30)
        widget.place(x=original_x)

    # --- Submit Handler ---
    def submit_password():
        password = password_var.get()

        try:
            DB_OBJ.encrypt(password)
            initialize()
            sign_in_window.destroy()
            main_screen()

        except Exception:
            error_label.config(text="Incorrect password. Try again.")
            password_entry.delete(0, END)
            submit_btn.config(state=DISABLED)
            shake_entry(password_entry)

    submit_btn.config(command=submit_password)

    sign_in_window.mainloop()

def main_screen():
    win = Tk()
    win.title("Password Manager")
    win.geometry("700x500")
    win.configure(bg=BG)

    # ============================
    # TABLE (Treeview)
    # ============================
    columns = DB_OBJ.columns

    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
    tree.place(x=20, y=20)

    # Scrollbar
    scrollbar = Scrollbar(win, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(x=660, y=20, height=330)

    # Column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Load entries
    def refresh_table():
        tree.delete(*tree.get_children())
        for row in get_all_entries():
            tree.insert("", END, values=row)

    refresh_table()

    # ============================
    # ADD ENTRY WINDOW
    # ============================
    def open_add_window():
        add_win = Toplevel(win)
        add_win.title("Add Entry")
        add_win.geometry("300x250")
        add_win.configure(bg=BG)

        Label(add_win, text="Website:", bg=BG, fg=FG).place(x=20, y=20)
        Label(add_win, text="Username:", bg=BG, fg=FG).place(x=20, y=70)
        Label(add_win, text="Password:", bg=BG, fg=FG).place(x=20, y=120)

        website_var = StringVar()
        user_var = StringVar()
        pw_var = StringVar()

        Entry(add_win, textvariable=website_var, bg=ENTRY_BG, fg=ENTRY_FG).place(x=100, y=20)
        Entry(add_win, textvariable=user_var, bg=ENTRY_BG, fg=ENTRY_FG).place(x=100, y=70)
        Entry(add_win, textvariable=pw_var, bg=ENTRY_BG, fg=ENTRY_FG).place(x=100, y=120)

        def save_entry():
            new_entry(websites=website_var.get(), users=user_var.get(), passwrds=pw_var.get())
            refresh_table()
            add_win.destroy()

        Button(add_win, text="Save", bg=BTN_BG, fg=BTN_FG, command=save_entry).place(x=100, y=170)

    # ============================
    # EDIT ENTRY WINDOW
    # ============================
    def open_edit_window():
        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")
        index = int(values[0])

        edit_win = Toplevel(win)
        edit_win.title("Edit Entry")
        edit_win.geometry("300x250")
        edit_win.configure(bg=BG)

        Label(edit_win, text="Website:", bg=BG, fg=FG).place(x=20, y=20)
        Label(edit_win, text="Username:", bg=BG, fg=FG).place(x=20, y=70)
        Label(edit_win, text="Password:", bg=BG, fg=FG).place(x=20, y=120)

        website_var = StringVar(value=values[1])
        user_var = StringVar(value=values[2])
        pw_var = StringVar(value=values[3])

        Entry(edit_win, textvariable=website_var, bg=ENTRY_BG, fg=ENTRY_FG).place(x=100, y=20)
        Entry(edit_win, textvariable=user_var, bg=ENTRY_BG, fg=ENTRY_FG).place(x=100, y=70)
        Entry(edit_win, textvariable=pw_var, bg=ENTRY_BG, fg=ENTRY_FG).place(x=100, y=120)

        def save_changes():
            change_entry(index, websites=website_var.get(), users=user_var.get(), passwrds=pw_var.get())
            refresh_table()
            edit_win.destroy()

        Button(edit_win, text="Save", bg=BTN_BG, fg=BTN_FG, command=save_changes).place(x=100, y=170)

    # ============================
    # DELETE ENTRY
    # ============================
    def delete_selected():
        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")
        index = int(values[0])

        delete_entry(index)
        refresh_table()

    # ============================
    # BUTTONS
    # ============================
    Button(win, text="Add Entry", bg=BTN_BG, fg=BTN_FG, command=open_add_window).place(x=20, y=370)
    Button(win, text="Edit Entry", bg=BTN_BG, fg=BTN_FG, command=open_edit_window).place(x=120, y=370)
    Button(win, text="Delete Entry", bg=BTN_BG, fg=BTN_FG, command=delete_selected).place(x=220, y=370)
    Button(win, text="Refresh", bg=BTN_BG, fg=BTN_FG, command=refresh_table).place(x=330, y=370)

    win.mainloop()