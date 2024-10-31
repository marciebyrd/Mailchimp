import csv
import os

def sanitize_filename(name):
    """Replace spaces with underscores and remove any non-alphanumeric characters."""
    return ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in name.replace(' ', '_'))

def generate_html_files(csv_file):
    # Create the output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            # Check if the row has enough values
            if len(row) < 5:
                print(f"Skipping row due to insufficient data: {row}")
                continue
            
            name, age, occupation, hobby, location = row
            
            # Create the filename using occupation and location
            filename = f"{sanitize_filename(occupation)}-{sanitize_filename(location)}.html"
            
            # Create the full file path
            file_path = os.path.join(output_dir, filename)
            
            # Create a simple HTML content (you can customize this as needed)
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{name}'s Profile</title>
            </head>
            <body>
                <h1>{name}</h1>
                <p>Age: {age}</p>
                <p>Occupation: {occupation}</p>
                <p>Hobby: {hobby}</p>
                <p>Location: {location}</p>
            </body>
            </html>
            """
            
            # Write the HTML file
            with open(file_path, 'w') as html_file:
                html_file.write(html_content)
            
            print(f"Created: {file_path}")

# Run the function
generate_html_files('data.csv')
