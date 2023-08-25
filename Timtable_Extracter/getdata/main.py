from bs4 import BeautifulSoup
import tkinter as tk
import os
import json
import csv
from datetime import datetime


def extract_schedule_data(html_file_name):
    # Read HTML content from a file
    with open(html_file_name, 'r') as html_file:
        html = html_file.read()

    # Remove extra whitespace and newline characters
    html = html.replace('\n', '').replace('  ', '')

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
        days, time_range = days_times.split(
            maxsplit=1) if days_times else ("", "")

        # Split time range into "Start Time" and "End Time"
        start_time, end_time = map(
            str.strip, time_range.split('-')) if time_range else ("", "")

        # Remove first two characters from "Days" and "Time"
        # if len(days) > 2:
        #     days = days[2:]
        # if len(time) > 2:
        #     time = time[2:]

        # Find <div> with id "win0divMTG_LOC$.." to get Room
        room_div = row.find(
            'div', id=lambda x: x and x.startswith('win0divMTG_LOC$'))
        room = room_div.get_text() if room_div else ""

        # Find <div> with id "win0divMTG_DATES$.." to get Start / End Dates
        dates_div = row.find(
            'div', id=lambda x: x and x.startswith('win0divMTG_DATES$'))
        start_end_dates = dates_div.get_text() if dates_div else ""
        start_end_dates = start_end_dates.split(
            '-')[0].strip()  # Keep only the start date

        # If the title is not empty, store it in data
        if title:
            data["Subject"] = title

        if start_end_dates:
            data["Start Date"] = start_end_dates
        # Store other data if any field is non-empty
        # Store other data if any field is non-empty
        if days:
            data["Start Time"] = start_time
            data["End Time"] = end_time
        if room:
            data["Location"] = room

        if room:
            data["Location"] = room

        # If all fields are filled, add the entry to the schedule_data list and reset data
        if "Subject" in data and all(field in data for field in ["Start Date", "Start Time", "End Time", "Location"]):
            schedule_data.append(data)
            data = {}  # Reset data for the next entry

    # Write the data to a JSON file if there's any data
    if schedule_data:
        output_file_name = html_file_name.replace(
            '.html', '_schedule_data.json')
        with open(output_file_name, 'w') as json_file:
            json.dump(schedule_data, json_file, indent=4)
        # print(f"Data has been saved to {output_file_name}")
    else:
        print("No data to save.")


def searchforsubject(div_id_to_extract):
    print('div is : ' + div_id_to_extract + 'doing')

    target_div = soup.find('div', id=div_id_to_extract)

    if target_div:
        # Extract all content under the <div> element
        extracted_content = target_div.encode_contents().decode('utf-8')

        # Create a folder if it doesn't exist
        folder_name = 'extracted_html'
        os.makedirs(folder_name, exist_ok=True)

        # Create a new HTML file and write the extracted content
        with open(os.path.join(folder_name, div_id_to_extract + '.html'), 'w') as f:
            # Write a basic HTML structure
            f.write(
                "<!DOCTYPE html>\n<html>\n<head><title>Extracted Content</title></head>\n<body>\n")
            f.write(extracted_content)
            f.write("\n</body>\n</html>")
    else:
        print("Specified div ID not found in the HTML.")


def additional_function(div_ids):
    for div_id in div_ids:
        file_path = os.path.join('extracted_html', div_id + '.html')
        try:
            extract_schedule_data(file_path)
        except Exception as e:
            # print(f"An error occurred while processing {file_path}: {e}")
            break  # Stop the loop on error


# Read the original HTML file
with open('./Timtable_Extracter/getdata/original.html', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

# Find all the course title elements
course_title_elements = soup.select(
    "div[id^='win0divDERIVED_REGFRM1_DESCR20']")

# Initialize an array to store course titles
course_titles = []
div_ids = []

# Extract and store the course titles and div_ids in the arrays
for title_element in course_title_elements:
    course_title = title_element.find("td", class_="PAGROUPDIVIDER")
    if course_title:
        course_titles.append(course_title.get_text())
        div_ids.append(title_element["id"])


def create_button_with_function(title, div_id):
    print('div is : ' + div_id)
    button = tk.Button(
        root, text=title, command=lambda: searchforsubject(div_id))
    button.pack()


def format_time(time_str):
    # Convert input time string to datetime object
    time_obj = datetime.strptime(time_str, '%I:%M%p')

    # Format the datetime object as desired
    formatted_time = time_obj.strftime('%I:%M:%S %p')
    return formatted_time


def generateCSV():
    # Read JSON data from file

    for item in div_ids:
        with open('./extracted_html/' + item + '_schedule_data.json', 'r') as json_file:
            json_data = json.load(json_file)

        # Format the time fields in the JSON data
        for entry in json_data:
            entry["Start Time"] = format_time(entry["Start Time"])
            entry["End Time"] = format_time(entry["End Time"])

        # Specify the CSV file path with the folder
        folder_name = 'OPEN ME'  # Change this to your desired folder name
        # Create the folder if it doesn't exist
        os.makedirs(folder_name, exist_ok=True)

        csv_file_path = os.path.join(folder_name, item + "output.csv")

        # Define the desired field order for CSV
        field_order = ["Subject", "Start Date",
                       "Start Time", "End Time", "Location"]

        # Write JSON data to CSV
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = json_data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=field_order)

            writer.writeheader()
            writer.writerows(json_data)


def generateICS():
    print('Apple Calender')
    # convert the json to ics , might need to do some re arrange of data


# Create the main window
root = tk.Tk()
root.title("Buttons Based on Array Length")

# Create a label
label = tk.Label(
    root, text="Click a button to extract the data from its table into another file ")
label.pack(pady=10)

# # Create buttons with attached functions
# for i in range(len(course_titles)):
#     create_button_with_function(course_titles[i], div_ids[i])


# Create a single button that generates JSON for all courses
def generate_all_json():
    additional_function(div_ids)


def generate_all_html():
    for div_id in div_ids:
        searchforsubject(div_id)


generate_button = tk.Button(
    root, text="Generate HTML for All Courses", command=generate_all_html)
generate_button.pack()

generate_button = tk.Button(
    root, text="Generate JSON for All Courses", command=generate_all_json)
generate_button.pack()

# buttontwo = tk.Button(
#     root, text='Generate JSON', command=lambda: additional_function(div_ids))
# buttontwo.pack()

buttonthree = tk.Button(
    root, text='Generate .CSV for Google Calender', command=lambda: generateCSV())
buttonthree.pack()

# working on ICS Convertion
# buttonfour = tk.Button(
#     root, text='Generate .ICS for Apple Calender', command=lambda: generateICS(), )
# buttonfour.pack()

# Start the Tkinter event loop
root.mainloop()
