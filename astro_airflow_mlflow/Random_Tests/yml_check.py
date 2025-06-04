import yaml
import os

print("Current working directory:", os.getcwd())

# Write to status.yaml
data = {'Validation': True}
with open('status.yaml', 'w') as f:
  yaml.dump(data, f)

# Load and print the value
with open('status.yaml', 'r') as f:
  loaded_data = yaml.safe_load(f)
  print(loaded_data['Validation'])  # Should print True if the file was written correctly
  print(type(loaded_data['Validation']))  # Should print <class 'bool'>
  print(loaded_data)  # Should print the entire dictionary {'Validation': True}