from bs4 import BeautifulSoup
import json
import tkinter as tk


def extract_schedule_data(html_file_name):
    # Read HTML content from a file
    with open(html_file_name, 'r') as html_file:
        html = html_file.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find the title
    title_element = soup.find('td', class_='PAGROUPDIVIDER')
    title = title_element.get_text()

    # Find all <td> tags with class "PSLEVEL2GRIDODDROW" and "PSLEVEL2GRIDEVENROW"
    schedule_rows = soup.find_all(
        'td', class_=['PSLEVEL2GRIDODDROW', 'PSLEVEL2GRIDEVENROW'])

    # Lists to store extracted information
    schedule_data = []
    data = {}  # Store data for the current entry

    for row in schedule_rows:
        # Find <div> with id "win0divMTG_SCHED$.." to get Days & Time
        days_times_div = row.find(
            'div', id=lambda x: x and x.startswith('win0divMTG_SCHED$'))
        days_times = days_times_div.get_text() if days_times_div else ""

        # Split "Days & Time" into separate fields for "Days" and "Time"
        days = ""
        time = ""
        if days_times:
            days, time = days_times.split(maxsplit=1)

        # Find <div> with id "win0divMTG_LOC$.." to get Room
        room_div = row.find(
            'div', id=lambda x: x and x.startswith('win0divMTG_LOC$'))
        room = room_div.get_text() if room_div else ""

        # Find <div> with id "win0divMTG_DATES$.." to get Start / End Dates
        dates_div = row.find(
            'div', id=lambda x: x and x.startswith('win0divMTG_DATES$'))
        start_end_dates = dates_div.get_text() if dates_div else ""

        # If the title is not empty, store it in data
        if title:
            data["Title"] = title

        # Store other data if any field is non-empty
        if days:
            data["Days"] = days
        if time:
            data["Time"] = time
        if room:
            data["Room"] = room
        if start_end_dates:
            data["Start / End Dates"] = start_end_dates

        # If all fields are filled, add the entry to the schedule_data list and reset data
        if "Title" in data and all(field in data for field in ["Days", "Time", "Room", "Start / End Dates"]):
            schedule_data.append(data)
            data = {}  # Reset data for the next entry

    # Write the data to a JSON file if there's any data
    if schedule_data:
        output_file_name = html_file_name.replace(
            '.html', '_schedule_data.json')
        with open(output_file_name, 'w') as json_file:
            json.dump(schedule_data, json_file, indent=4)
        print(f"Data has been saved to {output_file_name}")
    else:
        print("No data to save.")


# Call the function with the HTML file name


def button_click():
    extract_schedule_data(
        './dataSpecfic/win0divDERIVED_REGFRM1_DESCR20$0extracted.html')


# Create the main window
root = tk.Tk()
root.title("Button Example")

# Create a label
label = tk.Label(root, text="Press the button")
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click me!", command=button_click)
button.pack()

# Start the GUI event loop
root.mainloop()
