import tkinter as tk
from tkinter import ttk
import csv

import currency_converter
import api_fetcher

price_fetcher = api_fetcher.Price()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        tabControl = tk.ttk.Notebook(self)
        price_tab = ttk.Frame(tabControl)
        settings_tab = ttk.Frame(tabControl)
        inventory_tab = ttk.Frame(tabControl)
        tabControl.add(price_tab, text='Prices')
        tabControl.add(settings_tab, text='Settings')
        tabControl.add(inventory_tab, text='Inventory')
        tabControl.pack(expand = 1, fill = "both")
        self.geometry("1024x576")

        self.create_skinlist()
        self.init_price_tab(price_tab)
        self.init_settings_tab(settings_tab)
        self.init_inventory_tab(inventory_tab)

        # The initial update.
        self.on_tick()

    def init_price_tab(self, price_tab):
        # 3 rows x 2 columns grid.
        price_tab.grid_columnconfigure(0, weight=1)
        price_tab.grid_columnconfigure(1, weight=0)
        price_tab.grid_columnconfigure(2, weight=0)
        price_tab.grid_rowconfigure(0, weight=0)
        price_tab.grid_rowconfigure(1, weight=1)
        price_tab.grid_rowconfigure(2, weight=0)

        self.init_item_listbox(price_tab)
        self.create_item_frame(price_tab)

    # TODO implement this
    def init_settings_tab(self, settings_tab):
        label = tk.Label(settings_tab, text="Settings will go here!")
        label.pack()

    # TODO implement this
    def init_inventory_tab(self, inventory_tab):
        label = tk.Label(inventory_tab, text="Inventory will go here!")
        label.pack()

    def create_skinlist(self):
        with open('item_fetch/csv/list.csv', newline='', encoding="utf8") as skinlist:
            reader = csv.reader(skinlist)
            skin_list = []
            skin_list.extend(reader)
        skin_list = [" ".join(row) for row in skin_list]
        self.items = [*skin_list]

    def init_item_listbox(self, price_tab):
        # Put the filter in a frame at the top spanning across the columns.
        frame = tk.Frame(price_tab)
        frame.grid(row=0, column=1, columnspan=1, sticky='we', pady=5)

        self.filter_box = tk.Entry(frame)
        self.filter_box.pack(side='right', expand=True, fill='x')
        self.listbox = tk.Listbox(price_tab, width=60, height=20)
        self.listbox.grid(row=1, column=1, sticky='nes')

        # Scrollbar for listbox
        yscrollbar = tk.Scrollbar(price_tab, orient='vertical', command=self.listbox.yview)
        yscrollbar.grid(row=1, column=2, sticky='ns')
        self.listbox.config(yscrollcommand=yscrollbar.set)

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None

        add_button = tk.Button(price_tab, text="Get item", command=lambda: self.selected_item(price_tab), width=10)
        add_button.grid(row=2, column=1, sticky='se', pady=5)

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


    def selected_item(self, price_tab):
        if (self.listbox.curselection()):

            selected = self.listbox.get(self.listbox.curselection())
            print(selected)
            buff_name, buff_price, steam_price, image = price_fetcher.fetch_price(itemname=selected)
            print("buff name: ", buff_name)
            print("buff price:", buff_price)
            print("steam price:", steam_price)
            self.create_singleitem_grid(price_tab, buff_name, buff_price, steam_price, image)

    def create_item_frame(self, price_tab):
        self.item_frame = tk.Frame(price_tab)
        self.item_frame.grid(row=0, rowspan=2, column=0, sticky='nwe')
        self.item_frame.columnconfigure(index=1, weight=1)
        self.item_frame.columnconfigure(index=2, weight=2)
        clear_button = tk.Button(price_tab, text="Clear items", command=self.clear_items)
        clear_button.grid(row=2, column=0, sticky="w", pady=5, padx=5)

    def clear_items(self):
        for widget in self.item_frame.winfo_children():
            widget.destroy()

    def create_singleitem_grid(self, price_tab, buff_name, buff_price, steam_price, image):
        buff_to_eur = currency_converter.convert_value(buff_price, "CNY", "EUR")
        print(steam_price)
        if steam_price != "-.--":
            eur_diff, percentage_diff = currency_converter.calculate_difference(steam_price, buff_to_eur)
            if float(eur_diff) <= 0:
                col = "red"
            else:
                col = "green"
            diff_price = "Difference in price: " + eur_diff + " € (" + percentage_diff + " %)"
        else:
            diff_price = "Difference in price: -"
            col = "black"

        buff_price = "Price in Buff: " + buff_price + " ¥ (" + str(buff_to_eur) + " €)"
        steam_price = "Price in Steam: " + steam_price + "€"


        name_label = tk.Label(self.item_frame, text=buff_name, font=("Arial", 10))
        buff_label = tk.Label(self.item_frame, text=buff_price, font=("Arial", 10))
        steam_label = tk.Label(self.item_frame, text=steam_price, font=("Arial", 10))
        diff_label = tk.Label(self.item_frame, text=diff_price, fg=col, font=("Arial", 10))
        image_label = tk.Label(self.item_frame, image=image)
        image_label.image = image

        new_row_index = self.item_frame.grid_size()[1] * 2

        if new_row_index != 0:
            buffer_label = tk.Label(self.item_frame, bg="#E9E9E9")
            buffer_label.config(font=("Arial", 1))
            buffer_label.grid(column=0, columnspan=3, row=new_row_index, sticky="ew")


        name_label.grid(column=1, row=new_row_index+1, sticky="nw", ipady=5, ipadx=5)
        buff_label.grid(column=2, row=new_row_index+2, sticky="nw")
        steam_label.grid(column=2, row=new_row_index+1, sticky="nw", ipady=5)
        diff_label.grid(column=1, row=new_row_index+2, sticky="nw", ipadx=5)
        image_label.grid(column=0, row=new_row_index+1, rowspan=2, ipady=5)
        #buffer_label.grid(column=0, columnspan=3, row=new_row_index+2, sticky="ew")


        self.update()


# TODO scrollwheeli vasemmalle jos mahdollista
# TODO latausiconi kun itemiä haetaan
# TODO let capitalization not matter in search bar
# Bugs:
# All items not found. e.g. nomad fade minimal wear should exists but it doesnt.
# Error if item (or price) is not found on buff
