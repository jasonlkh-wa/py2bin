py_file_full_path=$1
py2bin_temp=$2

new_exec_file="${py_file_full_path%???}"

# Check if the destination file already exists
if [ -e "$new_exec_file" ]; then
    # Prompt for confirmation before overwriting
    echo -n "File '$new_exec_file' already exists. Overwrite? (y/n): "
    read answer
    if [[ $answer == [Yy] ]]; then
        # Remove the destination file before copying
        rm "$new_exec_file"
    else
        echo "No action is performed.\n"
        exit 1
    fi
fi

cp -i -p $py2bin_temp $new_exec_file
chmod u+x $new_exec_file
