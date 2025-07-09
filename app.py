import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class BulkFileRenamer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bulk File Renamer")
        self.geometry("1200x800")

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Directory selection
        dir_frame = ttk.LabelFrame(main_frame, text="Directory Selection")
        dir_frame.pack(fill=tk.X, padx=5, pady=5)

        self.dir_path_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_path_var, width=100)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        browse_button = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Filter options
        filter_frame = ttk.LabelFrame(main_frame, text="Filtering")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        self.recursive_var = tk.BooleanVar()
        recursive_check = ttk.Checkbutton(filter_frame, text="Include Subdirectories", variable=self.recursive_var, command=self.load_files)
        recursive_check.pack(side=tk.LEFT, padx=5, pady=5)

        self.file_types_var = tk.StringVar(value=".jpg, .jpeg, .png, .gif, .bmp, .tiff, .raw")
        file_types_entry = ttk.Entry(filter_frame, textvariable=self.file_types_var, width=50)
        file_types_entry.pack(side=tk.LEFT, padx=5, pady=5)
        file_types_entry.bind("<Return>", lambda event: self.load_files())


        # File list
        file_list_frame = ttk.LabelFrame(main_frame, text="Files to Rename")
        file_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.file_list = ttk.Treeview(file_list_frame, columns=("new_name"), show="headings")
        self.file_list.heading("new_name", text="New Name")
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Renaming operations
        ops_frame = ttk.LabelFrame(main_frame, text="Renaming Operations")
        ops_frame.pack(fill=tk.X, padx=5, pady=5)

        # Prefix/Suffix
        prefix_suffix_frame = ttk.Frame(ops_frame)
        prefix_suffix_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(prefix_suffix_frame, text="Prefix:").pack(side=tk.LEFT, padx=5)
        self.prefix_var = tk.StringVar()
        ttk.Entry(prefix_suffix_frame, textvariable=self.prefix_var).pack(side=tk.LEFT, padx=5)

        ttk.Label(prefix_suffix_frame, text="Suffix:").pack(side=tk.LEFT, padx=5)
        self.suffix_var = tk.StringVar()
        ttk.Entry(prefix_suffix_frame, textvariable=self.suffix_var).pack(side=tk.LEFT, padx=5)

        # Numbering
        numbering_frame = ttk.Frame(ops_frame)
        numbering_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_numbers_var = tk.BooleanVar()
        ttk.Checkbutton(numbering_frame, text="Add Sequential Numbers", variable=self.add_numbers_var).pack(side=tk.LEFT, padx=5)

        ttk.Label(numbering_frame, text="Start at:").pack(side=tk.LEFT, padx=5)
        self.start_num_var = tk.StringVar(value="1")
        ttk.Entry(numbering_frame, textvariable=self.start_num_var, width=5).pack(side=tk.LEFT, padx=5)

        ttk.Label(numbering_frame, text="Padding:").pack(side=tk.LEFT, padx=5)
        self.padding_var = tk.StringVar(value="3")
        ttk.Entry(numbering_frame, textvariable=self.padding_var, width=3).pack(side=tk.LEFT, padx=5)

        # Text replacement
        replace_frame = ttk.Frame(ops_frame)
        replace_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(replace_frame, text="Find:").pack(side=tk.LEFT, padx=5)
        self.find_var = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.find_var).pack(side=tk.LEFT, padx=5)

        ttk.Label(replace_frame, text="Replace:").pack(side=tk.LEFT, padx=5)
        self.replace_var = tk.StringVar()
        ttk.Entry(replace_frame, textvariable=self.replace_var).pack(side=tk.LEFT, padx=5)

        self.case_sensitive_var = tk.BooleanVar()
        ttk.Checkbutton(replace_frame, text="Case Sensitive", variable=self.case_sensitive_var).pack(side=tk.LEFT, padx=5)

        # Date/Time
        date_frame = ttk.Frame(ops_frame)
        date_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_date_var = tk.BooleanVar()
        ttk.Checkbutton(date_frame, text="Add Date/Time", variable=self.add_date_var).pack(side=tk.LEFT, padx=5)

        self.date_type_var = tk.StringVar(value="creation")
        ttk.Combobox(date_frame, textvariable=self.date_type_var, values=["creation", "modification", "exif"], width=12).pack(side=tk.LEFT, padx=5)

        ttk.Label(date_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        self.date_format_var = tk.StringVar(value="%Y-%m-%d")
        ttk.Entry(date_frame, textvariable=self.date_format_var, width=15).pack(side=tk.LEFT, padx=5)

        # Pattern
        pattern_frame = ttk.LabelFrame(ops_frame, text="Pattern Builder")
        pattern_frame.pack(fill=tk.X, padx=5, pady=5)

        pattern_controls_frame = ttk.Frame(pattern_frame)
        pattern_controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Button(pattern_controls_frame, text="Add Prefix", command=lambda: self.add_to_pattern("{prefix}")).pack(fill=tk.X)
        ttk.Button(pattern_controls_frame, text="Add Suffix", command=lambda: self.add_to_pattern("{suffix}")).pack(fill=tk.X)
        ttk.Button(pattern_controls_frame, text="Add Name", command=lambda: self.add_to_pattern("{name}")).pack(fill=tk.X)
        ttk.Button(pattern_controls_frame, text="Add Number", command=lambda: self.add_to_pattern("{num}")).pack(fill=tk.X)
        ttk.Button(pattern_controls_frame, text="Add Date", command=lambda: self.add_to_pattern("{date}")).pack(fill=tk.X)
        ttk.Button(pattern_controls_frame, text="Add Separator", command=self.add_separator).pack(fill=tk.X)
        ttk.Button(pattern_controls_frame, text="Remove Selected", command=self.remove_from_pattern).pack(fill=tk.X, pady=(10,0))


        self.pattern_listbox = tk.Listbox(pattern_frame, height=6)
        self.pattern_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.pattern_listbox.insert(tk.END, "{prefix}")
        self.pattern_listbox.insert(tk.END, "{name}")
        self.pattern_listbox.insert(tk.END, "{suffix}")
        self.pattern_listbox.insert(tk.END, "{num}")
        self.pattern_listbox.insert(tk.END, "{date}")


        pattern_order_frame = ttk.Frame(pattern_frame)
        pattern_order_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(pattern_order_frame, text="Up", command=self.move_pattern_item_up).pack()
        ttk.Button(pattern_order_frame, text="Down", command=self.move_pattern_item_down).pack()


        preview_button = ttk.Button(ops_frame, text="Preview Changes", command=self.preview_rename)
        preview_button.pack(pady=5)

        rename_button = ttk.Button(ops_frame, text="Rename Files", command=self.rename_files)
        rename_button.pack(pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)

        # Undo button
        self.undo_stack = []
        undo_button = ttk.Button(main_frame, text="Undo Last Rename", command=self.undo_rename, state=tk.DISABLED)
        undo_button.pack(pady=5)
        self.undo_button = undo_button


    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path_var.set(directory)
            self.load_files()

    def load_files(self):
        # Clear existing files
        for i in self.file_list.get_children():
            self.file_list.delete(i)

        path = self.dir_path_var.get()
        if not path:
            return

        import os
        file_types = [ft.strip() for ft in self.file_types_var.get().split(',')]

        if self.recursive_var.get():
            for root, _, files in os.walk(path):
                for filename in files:
                    if any(filename.lower().endswith(ft) for ft in file_types):
                        full_path = os.path.join(root, filename)
                        self.file_list.insert("", "end", text=full_path, values=(filename,))
        else:
            for filename in os.listdir(path):
                if os.path.isfile(os.path.join(path, filename)):
                    if any(filename.lower().endswith(ft) for ft in file_types):
                        self.file_list.insert("", "end", text=os.path.join(path, filename), values=(filename,))

    def preview_rename(self):
        import os
        import re
        import datetime
        from PIL import Image, ExifTags

        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        add_numbers = self.add_numbers_var.get()
        start_num = int(self.start_num_var.get())
        padding = int(self.padding_var.get())
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        case_sensitive = self.case_sensitive_var.get()
        add_date = self.add_date_var.get()
        date_type = self.date_type_var.get()
        date_format = self.date_format_var.get()
        
        pattern_parts = self.pattern_listbox.get(0, tk.END)
        pattern = "".join(pattern_parts)


        for i, item in enumerate(self.file_list.get_children()):
            full_path = self.file_list.item(item, "text")
            original_filename = os.path.basename(full_path)
            
            name, ext = os.path.splitext(original_filename)
            
            # Apply find and replace
            if find_text:
                if case_sensitive:
                    name = name.replace(find_text, replace_text)
                else:
                    name = re.sub(find_text, replace_text, name, flags=re.IGNORECASE)

            # Number
            num_str = ""
            if add_numbers:
                num_str = str(start_num + i).zfill(padding)

            # Date
            date_str = ""
            if add_date:
                try:
                    if date_type == "creation":
                        timestamp = os.path.getctime(full_path)
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime(date_format)
                    elif date_type == "modification":
                        timestamp = os.path.getmtime(full_path)
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime(date_format)
                    elif date_type == "exif":
                        img = Image.open(full_path)
                        exif_data = img._getexif()
                        if exif_data:
                            for tag, value in exif_data.items():
                                tag_name = ExifTags.TAGS.get(tag, tag)
                                if tag_name == 'DateTimeOriginal':
                                    dt_original = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                                    date_str = dt_original.strftime(date_format)
                                    break
                except Exception as e:
                    print(f"Could not get date for {full_path}: {e}")

            new_name_base = pattern.format(
                name=name,
                prefix=prefix,
                suffix=suffix,
                num=num_str,
                date=date_str
            )

            new_name = f"{new_name_base}{ext}"
            self.file_list.item(item, values=(new_name,))

    def rename_files(self):
        self.preview_rename()
        if messagebox.askyesno("Confirm Rename", "Are you sure you want to rename these files?"):
            import os
            import logging

            logging.basicConfig(filename='rename.log', level=logging.INFO, format='%(asctime)s - %(message)s')

            items = self.file_list.get_children()
            self.progress_bar["maximum"] = len(items)
            self.progress_bar["value"] = 0

            renamed_files = []

            for i, item in enumerate(items):
                old_path = self.file_list.item(item, "text")
                new_name = self.file_list.item(item, "values")[0]
                new_path = os.path.join(os.path.dirname(old_path), new_name)

                try:
                    os.rename(old_path, new_path)
                    renamed_files.append((new_path, old_path))
                    logging.info(f"Renamed '{old_path}' to '{new_path}'")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not rename {old_path}:\n{e}")
                    logging.error(f"Error renaming '{old_path}' to '{new_path}': {e}")

                self.progress_bar["value"] = i + 1
                self.update_idletasks()
            
            if renamed_files:
                self.undo_stack.append(renamed_files)
                self.undo_button["state"] = tk.NORMAL

            self.load_files()

    def undo_rename(self):
        if not self.undo_stack:
            return

        if messagebox.askyesno("Confirm Undo", "Are you sure you want to undo the last rename operation?"):
            import os
            last_rename = self.undo_stack.pop()
            for new_path, old_path in reversed(last_rename):
                try:
                    os.rename(new_path, old_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not undo rename for {new_path}:\n{e}")
            
            if not self.undo_stack:
                self.undo_button["state"] = tk.DISABLED

            self.load_files()

    def add_to_pattern(self, part):
        self.pattern_listbox.insert(tk.END, part)

    def add_separator(self):
        from tkinter import simpledialog
        separator = simpledialog.askstring("Input", "Enter separator text:", parent=self)
        if separator:
            self.pattern_listbox.insert(tk.END, separator)

    def remove_from_pattern(self):
        selected_indices = self.pattern_listbox.curselection()
        for i in reversed(selected_indices):
            self.pattern_listbox.delete(i)

    def move_pattern_item_up(self):
        selected_indices = self.pattern_listbox.curselection()
        if not selected_indices:
            return
        for i in selected_indices:
            if i > 0:
                text = self.pattern_listbox.get(i)
                self.pattern_listbox.delete(i)
                self.pattern_listbox.insert(i - 1, text)
                self.pattern_listbox.selection_set(i - 1)

    def move_pattern_item_down(self):
        selected_indices = self.pattern_listbox.curselection()
        if not selected_indices:
            return
        for i in reversed(selected_indices):
            if i < self.pattern_listbox.size() - 1:
                text = self.pattern_listbox.get(i)
                self.pattern_listbox.delete(i)
                self.pattern_listbox.insert(i + 1, text)
                self.pattern_listbox.selection_set(i + 1)


if __name__ == "__main__":
    app = BulkFileRenamer()
    app.mainloop()
