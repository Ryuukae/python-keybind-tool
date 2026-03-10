import argparse
import keyboard
import pyperclip
import configparser
import time
import os


# ---  Helper Functions ---
def save_to_history():
    """Reads the clipboard and appends it to a file."""
    time.sleep(0.1) # Wait for OS to catch up
    data = pyperclip.paste()
    
    with open("clips.txt", "a") as f:
        f.write(f"{data}\n---\n")
    print(f"Captured: {data[:50]}...")

def open_path(path):
    """Opens a file or directory at the given path."""
    print(f"Opening: {path}")
    os.startfile(path)

def load_config_keybinds():
  config = configparser.ConfigParser(interpolation=None)
  config.read('./config.ini')
  return format_config(config['Keybinds'])

def load_config_dir_paths():
  config = configparser.ConfigParser(interpolation=None)
  config.read('./config.ini')
  return format_config(config['Directory Paths'])

def load_config_app_paths():
  config = configparser.ConfigParser(interpolation=None)
  config.read('./config.ini')
  return format_config(config['Application Paths'])

def format_config(config):
  for entry in config:
    config[entry] = os.path.expandvars(config[entry])
  return config

def get_editable_config():
  config = configparser.ConfigParser(interpolation=None)
  config.read('./config.ini')
  return config  # We just return the raw object directly!

def save_config(config, item_name):
  with open('./config.ini', 'w') as configfile:
    config.write(configfile)
  print(f"Updated {item_name} successfully!")

# ---  The Main Execution Logic ---
def main():
    keybind_config = load_config_keybinds()
    dir_paths_config = load_config_dir_paths()
    app_paths_config = load_config_app_paths()
    # Load the config file for editing
    config = get_editable_config()
    
    parser = argparse.ArgumentParser(description="Smart Clipboard Manager")
    parser.add_argument("--set-default-paths", nargs='*')
    parser.add_argument("--add-custom-path", nargs=2)
    args = parser.parse_args()

    

    if args.set_default_paths is not None: 
        if len(args.set_default_paths) == 0:
            # Interactive one-by-one mode
            for directory in config['Directory Paths']:
              new_path = input(f"Enter the new path for {directory}: ")
              config['Directory Paths'][directory] = new_path
            # Save the changes
            save_config(config, directory)
              
        elif len(args.set_default_paths) == 2:
          folder_name = args.set_folder_paths[0] 
          new_path = args.set_folder_paths[1]
          config['Directory Paths'][folder_name] = new_path
          # Save the changes
          save_config(config, folder_name)
            
    elif args.add_custom_path is not None:
      if len(args.add_custom_path) == 2:
        # Add a new custom path
        name = args.add_custom_path[0]
        new_path = args.add_custom_path[1]
        base_path, file_extension = os.path.splitext(new_path)
        if file_extension == "":
          config['Directory Paths'][name] = new_path 
        else:
          config['Application Paths'][name] = new_path

      save_config(config, name)


    else:
        # Normal execution (no flags used)
        """Sets up the listeners and holds the script open."""
        print("--- Smart Clipboard Manager Started ---")
        print("Press Ctrl+C to copy. Press Esc to exit.")
    
  

        # Set the trigger
        keyboard.add_hotkey(keybind_config['save_to_history'], save_to_history)

        
        keyboard.add_hotkey(keybind_config['open_downloads'], lambda: open_path(dir_paths_config['downloads_path']))
        keyboard.add_hotkey(keybind_config['open_userprofile'], lambda: open_path(dir_paths_config['userprofile_path']))
        keyboard.add_hotkey(keybind_config['open_chrome'], lambda: open_path(app_paths_config['chrome_path']))
    
        # This keeps the script from instantly closing
        keyboard.wait('ctrl+esc')
        print("Shutting down... Goodbye!")

# --- 3. The Entry Point ---
if __name__ == "__main__":
    main()