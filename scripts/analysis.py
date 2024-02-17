import os

root_directory = '/home/chispitas/Documents/TFG/samples/malware_bazaar'

# List all directories within the root directory
directories = [os.path.join(root_directory, d) for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d))]

# Iterate through each directory
for directory in directories:
    # List all files within the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Iterate through each file and print its name
    for file in files:
        # Execute the command peframe on the file
        output_peframe = os.system('peframe ' + os.path.join(directory, file))
