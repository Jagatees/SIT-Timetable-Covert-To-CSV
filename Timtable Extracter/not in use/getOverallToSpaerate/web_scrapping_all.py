from bs4 import BeautifulSoup

# Read the original HTML file
with open('./getOverallToSpaerate/original.html', 'r') as f:
    html_content = f.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <div> element by its ID
# Replace with the actual div ID you're targeting
div_id_to_extract = 'win0divDERIVED_REGFRM1_DESCR20$1'
target_div = soup.find('div', id=div_id_to_extract)

if target_div:
    # Extract all content under the <div> element
    extracted_content = target_div.encode_contents().decode('utf-8')

    # Create a new HTML file and write the extracted content
    with open('extracted_content.html', 'w') as f:
        # Write a basic HTML structure
        f.write(
            "<!DOCTYPE html>\n<html>\n<head><title>Extracted Content</title></head>\n<body>\n")
        f.write(extracted_content)
        f.write("\n</body>\n</html>")
else:
    print("Specified div ID not found in the HTML.")
