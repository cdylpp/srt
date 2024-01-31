import xml.etree.ElementTree as ET

def remove_prefix(file_tags, prefix):
    # Remove the specified prefix from each file tag
    result = [tag.replace(prefix, '') for tag in file_tags]
    return result

def update_paths(input_file, output_file, prefix):
    # Parse the XML content
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Collect paths within <file> tags
    file_tags = [file_elem.text for file_elem in root.iter('file')]

    # Remove the specified prefix from each path
    updated_file_tags = remove_prefix(file_tags, prefix)

    # Update paths within <file> tags
    for file_elem, updated_path in zip(root.iter('file'), updated_file_tags):
        file_elem.text = updated_path

    # Write the modified XML content to the output file
    tree.write(output_file)

if __name__ == "__main__":
    input_file = "resources/resources2.qrc"  # Replace with the actual input file path
    output_file = "output.xml"  # Replace with the desired output file path
    prefix_to_remove = 'resources/resource/'

    update_paths(input_file, input_file, prefix_to_remove)

