# Define the input and output directories
input_file = 'rules.tex'
output_directory = './rules/'

# Read the content of the input file
with open(input_file, 'r') as f:
    content = f.read()

# Split the content based on the delimiter
parts = content.split('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

# Create the output directory if it doesn't exist
import os
os.makedirs(output_directory, exist_ok=True)

# Write each part to separate files
for i, part in enumerate(parts):
    output_file = os.path.join(output_directory, f'{i + 1}.md')
    with open(output_file, 'w') as f:
        f.write(part)
