import tkinter as tk
import csv

import currency_converter
import api_fetcher

price_fetcher = api_fetcher.Price()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # 3 rows x 2 columns grid.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.geometry("1024x576")

        addButton = tk.Button(self, text="Get item", command=self.selected_item)
        addButton.grid(row=2, column=1, sticky='se')

        self.create_skinlist()
        self.init_item_listbox()
        self.create_item_frame()

        # The initial update.
        self.on_tick()


    def create_skinlist(self):
        with open('item_fetch/csv/list.csv', newline='', encoding="utf8") as skinlist:
            reader = csv.reader(skinlist)
            skin_list = []
            skin_list.extend(reader)
        skin_list = [" ".join(row) for row in skin_list]
        self.items = [*skin_list]

    def init_item_listbox(self):
        # Put the filter in a frame at the top spanning across the columns.
        frame = tk.Frame(self, width=60)
        frame.grid(row=0, column=1, columnspan=1, sticky='e')

        self.filter_box = tk.Entry(frame, width=60)
        self.filter_box.pack(side='right', expand=True)
        self.listbox = tk.Listbox(self, width=60, height=20)
        self.listbox.grid(row=1, column=1, sticky='nes')

        # Scrollbar for listbox
        self.yscrollbar = tk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        self.yscrollbar.grid(row=1, column=2, sticky='ns')
        self.listbox.config(yscrollcommand=self.yscrollbar.set)

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None

    def on_tick(self):
        if self.filter_box.get() != self.curr_filter and self.items:
            # The contents of the filter box has changed.
            self.curr_filter = self.filter_box.get()

            # Refresh the listbox.
            self.listbox.delete(0, 'end')

            for item in self.items:
                if self.curr_filter in item:
                    self.listbox.insert('end', item)

        self.after(250, self.on_tick)


    def selected_item(self):
        if (self.listbox.curselection()):

            selected = self.listbox.get(self.listbox.curselection())
            print(selected)
            buff_name, buff_price, steam_price, image = price_fetcher.fetch_price(itemname=selected)
            print("buff name: ", buff_name)
            print("buff price:", buff_price)
            print("steam price:", steam_price)
            self.create_singleitem_grid(buff_name, buff_price, steam_price, image)

    def create_item_frame(self):
        self.item_frame = tk.Frame(self)
        self.item_frame.grid(row=1, column=0, sticky='nwe')
        self.item_frame.configure(height=45, width=90)
        self.item_frame.columnconfigure(index=1, weight=1)
        self.item_frame.columnconfigure(index=2, weight=2)
        clear_button = tk.Button(self, text="Clear items", command=self.clear_items)
        clear_button.grid(row=2, column=0, sticky="w")

    def clear_items(self):
        for widget in self.item_frame.winfo_children():
            widget.destroy()

    def create_singleitem_grid(self, buff_name, buff_price, steam_price, image):
        buff_to_eur = currency_converter.convert_value(buff_price, "CNY", "EUR")
        eur_diff, percentage_diff = currency_converter.calculate_difference(steam_price, buff_to_eur)
        if float(eur_diff) <= 0:
            col = "red"
        else:
            col = "green"


        buff_price += "¥ (" + str(buff_to_eur) + " €)"
        steam_price += " €"
        diff_price = "Difference in price: " + eur_diff + " € (" + percentage_diff + " %)"

        name_label = tk.Label(self.item_frame, text=buff_name, font=("Arial", 12))
        buff_label = tk.Label(self.item_frame, text=buff_price, font=("Arial", 12))
        steam_label = tk.Label(self.item_frame, text=steam_price, font=("Arial", 12))
        diff_label = tk.Label(self.item_frame, text=diff_price, fg=col, font=("Arial", 12))
        image_label = tk.Label(self.item_frame, image=image)
        image_label.image = image

        new_row_index = self.item_frame.grid_size()[1] * 2
        name_label.grid(column=1, row=new_row_index, sticky="w")
        buff_label.grid(column=2, row=new_row_index+1, sticky="w")
        steam_label.grid(column=2, row=new_row_index, sticky="w")
        diff_label.grid(column=1, row=new_row_index+1, sticky="w")
        image_label.grid(column=0, row=new_row_index, rowspan=2)

        self.update()

# TODO viivat tai vastaavat kenttien välille
# TODO clear-nappi joka tyhjentää gridin
# TODO scrollwheeli vasemmalle jos mahdollista

