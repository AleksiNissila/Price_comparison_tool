import tkinter as tk
from tkinter import ttk
import csv

import currency_converter
import api_fetcher
import settings

price_fetcher = api_fetcher.Price()


currency= settings.get_currency()[0]



class App(tk.Tk):
    def __init__(self):
        """
        Initiate the GUI and its different parts
        """
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
        """
        Initiate a part of GUI containing items and their prices
        :param price_tab: GUI element to be edited
        :return: nothing
        """
        # 3 rows x 2 columns grid.
        price_tab.grid_columnconfigure(0, weight=1)
        price_tab.grid_columnconfigure(1, weight=0)
        price_tab.grid_columnconfigure(2, weight=0)
        price_tab.grid_rowconfigure(0, weight=0)
        price_tab.grid_rowconfigure(1, weight=1)
        price_tab.grid_rowconfigure(2, weight=0)

        self.init_item_listbox(price_tab)
        self.create_item_frame(price_tab)


    def init_settings_tab(self, settings_tab):
        """
        Initiate a part of GUI containing settings
        :param settings_tab: GUI element to be edited
        :return: nothing
        """

        default_curr, curr_list = settings.get_currency()[0], settings.get_currency_list()
        currency_box = tk.ttk.Combobox(settings_tab,state='readonly', textvariable=default_curr)
        currency_box['values'] = curr_list
        currency_box.current(curr_list.index(default_curr))
        currency_box.bind("<<ComboboxSelected>>", lambda event : settings.set_currency(currency_box.get()))
        currency_box.pack()

    def init_inventory_tab(self, inventory_tab):
        """
        Initiate a part of GUI containing inventory
        :param inventory_tab: GUI element to be edited
        :return: nothing
        """
        label = tk.Label(inventory_tab, text="Inventory will go here!")
        label.pack()

    def create_skinlist(self):
        """
        Read a CSV file to populate a list of item names
        :return: nothing
        """
        with open('item_fetch/csv/list.csv', newline='', encoding="utf8") as skinlist:
            reader = csv.reader(skinlist)
            skin_list = []
            skin_list.extend(reader)
        skin_list = [" ".join(row) for row in skin_list]
        self.items = [*skin_list]

    def init_item_listbox(self, price_tab):
        """
        Function for populating the listbox with item names
        :param price_tab: GUI element which the items will be added to
        :return: nothing
        """
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
        """
        Function for filtering the list of item names as text gets written
        :return: nothing
        """
        if self.filter_box.get() != self.curr_filter and self.items:
            # The contents of the filter box has changed.
            self.curr_filter = self.filter_box.get()


            # Refresh the listbox.
            self.listbox.delete(0, 'end')

            for item in self.items:
                if str.lower(self.curr_filter) in str.lower(item):
                    self.listbox.insert('end', item)

        self.after(250, self.on_tick)


    def selected_item(self, price_tab):
        """
        Function for getting prices for a certain item, and calling a function to show the item in the GUI
        :param price_tab: GUI element in which the item will be shown on
        :return: nothing
        """
        if (self.listbox.curselection()):

            selected = self.listbox.get(self.listbox.curselection())
            print(selected)
            buff_name, buff_price, steam_price, image = price_fetcher.fetch_price(itemname=selected)
            print("buff name: ", buff_name)
            print("buff price:", buff_price)
            print("steam price:", steam_price)
            self.create_singleitem_grid(price_tab, buff_name, buff_price, steam_price, image)

    def create_item_frame(self, price_tab):
        """
        Function for creating a grid that will contain information about an item
        :param price_tab: GUI element in which the item will be shown on
        :return: nothing
        """
        self.item_frame = tk.Frame(price_tab)
        self.item_frame.grid(row=0, rowspan=2, column=0, sticky='nwe')
        self.item_frame.columnconfigure(index=1, weight=1)
        self.item_frame.columnconfigure(index=2, weight=2)
        clear_button = tk.Button(price_tab, text="Clear items", command=self.clear_items)
        clear_button.grid(row=2, column=0, sticky="w", pady=5, padx=5)

    def clear_items(self):
        """
        Function for emptying the GUI element which contains all searched items
        :return: nothing
        """
        for widget in self.item_frame.winfo_children():
            widget.destroy()

    def create_singleitem_grid(self, price_tab, buff_name, buff_price, steam_price, image):
        """
        Function for populating a grid component with the gathered information about an item
        :param price_tab: GUI element in which the item will be shown on
        :param buff_name: Name of the item from Buff
        :param buff_price: Price of the item from Buff
        :param steam_price: Price of the item from Steam
        :param image: Image of the item from Buff
        :return: nothing
        """
        cny_to_curr = currency_converter.convert_value(buff_price, "CNY", settings.get_currency()[0])
        print(cny_to_curr)
        print(steam_price)
        if steam_price != "-.--":
            flat_diff, percentage_diff = currency_converter.calculate_difference(steam_price, cny_to_curr)
            if float(flat_diff) <= 0:
                col = "red"
            else:
                col = "green"
            diff_price = f"Difference in price: {currency} {flat_diff} ( {percentage_diff} %)"
        else:
            diff_price = "Difference in price: -"
            col = "black"

        buff_price = f"Price in Buff: {buff_price} ¥ ({currency} {str(cny_to_curr)})"
        steam_price = f"Price in Steam: {currency} {steam_price}"


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




# Bugs:
# All items not found. e.g. nomad fade minimal wear should exists but it doesnt.
# Error if item (or price) is not found on buff
