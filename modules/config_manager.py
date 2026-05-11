import os
import re

CONFIG_DIR = 'config'

def get_config_file_path(filename):
    return os.path.join(CONFIG_DIR, filename)

def read_config_vars(filename):
    """Parses a config Python file and returns a dictionary of its variables."""
    filepath = get_config_file_path(filename)
    if not os.path.exists(filepath):
        return {}
    
    vars_dict = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Match variable assignments like `var_name = "value"  # comment`
            # or `var_name = True` or `var_name = []`
            match = re.match(r'^([a-zA-Z0-9_]+)\s*=\s*(.+?)(?:\s*#.*)?$', line.strip())
            if match:
                key, value_str = match.groups()
                # Basic parsing, eval is dangerous but okay here since it's local trusted config
                try:
                    # Clean up trailing comments if they weren't caught by the regex
                    if '#' in value_str and not ('"' in value_str or "'" in value_str):
                        value_str = value_str.split('#')[0].strip()
                    vars_dict[key] = eval(value_str)
                except:
                    # If eval fails, just store the string
                    vars_dict[key] = value_str.strip('"\'')
    return vars_dict

def update_config_var(filename, key, new_value):
    """Updates a single variable in a config Python file."""
    filepath = get_config_file_path(filename)
    if not os.path.exists(filepath):
        return False
        
    # Smart parsing of incoming strings
    if isinstance(new_value, str):
        if new_value.lower() == 'true': new_value = True
        elif new_value.lower() == 'false': new_value = False
        elif new_value.isdigit(): new_value = int(new_value)
        elif new_value.startswith('[') and new_value.endswith(']'):
            try: new_value = eval(new_value) # Handle list strings if passed
            except: pass

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    updated = False
    for i, line in enumerate(lines):
        # Match the variable assignment
        if re.match(rf'^{key}\s*=.*', line):
            # Format the new value
            if isinstance(new_value, str):
                formatted_value = f'"{new_value}"'
            elif isinstance(new_value, list):
                # Format lists cleanly
                formatted_value = '[' + ', '.join(f'"{v}"' if isinstance(v, str) else str(v) for v in new_value) + ']'
            else:
                formatted_value = str(new_value)
                
            # Replace while preserving the comment if it exists
            comment_part = ""
            if '#' in line:
                comment_part = '  #' + line.split('#', 1)[1]
            
            lines[i] = f'{key} = {formatted_value}{comment_part}'
            if not lines[i].endswith('\n'):
                lines[i] += '\n'
            updated = True
            break
            
    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    return updated

def get_all_configs():
    return {
        'search': read_config_vars('search.py'),
        'personals': read_config_vars('personals.py'),
        'settings': read_config_vars('settings.py'),
        'questions': read_config_vars('questions.py')
    }
