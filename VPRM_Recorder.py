import tkinter as tk
import pandas as pd
import xlsxwriter
import datetime
from tkinter import messagebox

areas = [
    {"id": 1, "values": [], "differences": [], "dates": []},
    {"id": 2, "values": [], "differences": [], "dates": []},
    {"id": 3, "values": [], "differences": [], "dates": []}
]

def save_value(area):
    value = area["value_entry"].get()
    if value:
        value = float(value)
        if "values" not in area:
            area["values"] = []
            area["differences"] = []
            area["dates"] = []

        if len(area["values"]) > 0:
            previous_value = area["values"][-1]
            difference = value - previous_value
        else:
            difference = 0

        area["values"].append(value)
        area["differences"].append(difference)
        area["dates"].append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

        area["values_text"].insert(tk.END, f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}: {value}\n")

        area["difference_text"]["text"] = f"Difference from previous day: {difference}"
        area["cumulative_diff_text"]["text"] = f"Total coins mined from start: {sum(area['differences'])}"
        area["divided_diff_text"]["text"] = f"Blocks mined = Total/50: {difference / 50}"

        area["value_entry"].delete(0, tk.END)
    else:
        messagebox.showwarning("Empty Value", "Please enter a value.")

def clear_values(area):
    area["values"] = []
    area["differences"] = []
    area["dates"] = []
    area["values_text"].delete(1.0, tk.END)
    area["difference_text"]["text"] = "Difference from previous day: 0"
    area["cumulative_diff_text"]["text"] = "Total coins mined from start: 0"
    area["divided_diff_text"]["text"] = "Blocks mined = Total/50: 0"

def export_to_excel():
    filename = "all_areas_values.xlsx"
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Area")
    worksheet.write(0, 1, "Date")
    worksheet.write(0, 2, "Value")
    worksheet.write(0, 3, "Difference")

    row = 1
    for area in areas:
        area_id = area["id"]
        values = area["values"]
        differences = area["differences"]
        dates = area["dates"]

        for value, difference, date in zip(values, differences, dates):
            worksheet.write(row, 0, area_id)
            worksheet.write(row, 1, date)
            worksheet.write(row, 2, value)
            worksheet.write(row, 3, difference)
            row += 1

    workbook.close()
    messagebox.showinfo("Export Complete", "Data has been exported to Excel.")

def load_from_excel():
    try:
        filename = "all_areas_values.xlsx"
        data = pd.read_excel(filename)
        for _, row in data.iterrows():
            area_id = row["Area"]
            value = row["Value"]
            difference = row["Difference"]
            date = row["Date"]

            area = next((a for a in areas if a["id"] == area_id), None)
            if area is not None:
                area["values"].append(value)
                area["differences"].append(difference)
                area["dates"].append(date)
                area["values_text"].insert(tk.END, f"{date}: {value}\n")
    except FileNotFoundError:
        messagebox.showinfo("No Existing File", "No existing file found. A new Excel file will be created.")

def create_ui():
    window = tk.Tk()
    window.title("Vaporum Coin Recorder")
    window.geometry("800x600")
    window.configure(bg="black")

    instructions = tk.Label(window, text="INPUT EACH DAY'S TOTAL WALLET OR NODE VALUE TO SEE YOUR DAILY MINING REVENUE.", font=("Arial", 12), fg="white", bg="black")
    instructions.place(x=10, y=10)

    instruction2 = tk.Label(window, text="Press export to excel on first use.Export to excel before closing.", font=("Arial", 12), fg="white", bg="black")
    instruction2.place(x=10, y=30)

    for area in areas:
        area["frame"] = tk.Frame(window, bg="black")
        area["frame"].pack(side=tk.LEFT, padx=10)

        area["label"] = tk.Label(area["frame"], text=f"Wallet {area['id']}", font=("Arial", 14), fg="white", bg="black")
        area["label"].pack(pady=10)

        area["value_label"] = tk.Label(area["frame"], text="Enter today's value:", fg="white", bg="black")
        area["value_label"].pack()

        area["value_entry"] = tk.Entry(area["frame"])
        area["value_entry"].pack()

        area["record_button"] = tk.Button(area["frame"], text="Record", command=lambda a=area: save_value(a), bg="light green")
        area["record_button"].pack(pady=5)

        area["values_frame"] = tk.Frame(area["frame"])
        area["values_frame"].pack(pady=10)

        area["values_text"] = tk.Text(area["values_frame"], height=10, width=30)
        area["values_text"].pack(side=tk.LEFT)

        area["scrollbar"] = tk.Scrollbar(area["values_frame"])
        area["scrollbar"].pack(side=tk.RIGHT, fill=tk.Y)

        area["values_text"].config(yscrollcommand=area["scrollbar"].set)
        area["scrollbar"].config(command=area["values_text"].yview)

        area["difference_text"] = tk.Label(area["frame"], text="Difference from previous day: 0", fg="white", bg="black")
        area["difference_text"].pack()

        area["cumulative_diff_text"] = tk.Label(area["frame"], text="Total coins mined from start: 0", fg="white", bg="black")
        area["cumulative_diff_text"].pack()

        area["divided_diff_text"] = tk.Label(area["frame"], text="Blocks mined = Total/50: 0", fg="white", bg="black")
        area["divided_diff_text"].pack()

        area["clear_button"] = tk.Button(area["frame"], text="Clear Values", command=lambda a=area: clear_values(a), bg="light green")
        area["clear_button"].pack(pady=5)

    export_button = tk.Button(window, text="Export to Excel", command=export_to_excel, bg="yellow")
    export_button.place(x=10, y=570)

    load_from_excel()
    window.mainloop()

create_ui()
