def merge_files(file1, file2, output_file):
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out:
            # Read the contents of the first file and write to the output file
            for line in f1:
                out.write(line)
            
            # Read the contents of the second file and append to the output file
            for line in f2:
                out.write(line)
        
        print("Files merged successfully!")
    except FileNotFoundError:
        print("One of the input files was not found.")
    except Exception as e:
        print("An error occurred:", e)

# Example usage:
file1 = "close.t1.txt"
file2 = "open.t1.txt"
output_file = "merged_file.t1.txt"
merge_files(file1, file2, output_file)
