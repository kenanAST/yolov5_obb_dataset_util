import os


def write_sorted_filenames(folder_path, output_file):
    filenames = os.listdir(folder_path)
    filenames.sort()

    with open(output_file, 'w') as file:
        for filename in filenames:
            name_without_extension = os.path.splitext(filename)[0]
            file.write(name_without_extension + '\n')


# Example usage:
# Replace with the actual folder path
folder_path = './drone_dataset_lite/test/images'
output_file = 'imgnamefile.txt'  # Replace with the desired output file path

write_sorted_filenames(folder_path, output_file)
