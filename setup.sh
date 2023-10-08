parent_dir=$(dirname "$(readlink -f "$0")")

# create the function list csv
csv_path="$parent_dir/resources/cmd2.csv"
echo "cmd,file,description" >"$csv_path"

# create the shell script path
shell_script_path="$parent_dir/shell-scripts/custom-commands.sh"
mkdir -p "$(dirname "$shell_script_path")"
touch "$shell_script_path"

# rename example.env to .env
env_path="$parent_dir/2.env"
mv "$parent_dir/example.env" "$env_path"

# replace the configuration in .env
csv_line_number=2
new_csv_source="CSV_SOURCE=\"$csv_path\""
sed -i '' "${csv_line_number}s?.*?${new_csv_source}?" "$env_path"

shell_script_line_number=1
new_shell_script_path="SHELL_SCRIPT_PATH=\"$shell_script_path\""
sed -i '' "${shell_script_line_number}s?.*?${new_shell_script_path}?" "$env_path"
