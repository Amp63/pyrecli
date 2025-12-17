# pyrecli

Command line utilities for DiamondFire templates

## Installation

Run the following command in a terminal:

```sh
pip install pyrecli
```

## Commands

- `scan`: Scan all templates on the plot and dump them to a text file (requires [CodeClient](github.com/DFOnline/CodeClient))
- `send`: Send template items to DiamondFire (requires [CodeClient](github.com/DFOnline/CodeClient))
- `rename`: Rename all occurences of a variable (including text codes)
- `script`: Generate python scripts from template data
- `grabinv`: Save all templates in your Minecraft inventory to a file (requires [CodeClient](github.com/DFOnline/CodeClient))
- `docs`: Generate markdown documentation from template data
- `slice`: Slice a template into multiple smaller templates
- `cctoken`: Get a reusable CodeClient authentication token


## What is this useful for?

- Backing up a plot
- Getting an accurate text representation of DF code
- Open sourcing
- Version control
- Large scale refactoring


## Example Command Usages

### Scan

**[Requires CodeClient]**

Grabs all of the templates on your current plot and saves them to a file.
You will need to run `/auth` in-game to authorize this action.

Example:
```sh
# Dumps all template data into templates.dfts
pyrecli scan templates.dfts
```

### Send

**[Requires CodeClient]**

Sends all templates in a file back to your inventory.

Example:
```sh
pyrecli send templates.dfts
```

### Rename

Renames all occurences of a variable in a list of templates.
You can run this command on a single template, or on an entire plot if a variable is used in many places.

This command still requires thorough testing, so make sure you have a backup of your plot before using this command on a large scale.

Example:
```sh
# Changes all variables named `foo` to `bar`, then saves the new templates to 'renamed.dfts'.
pyrecli rename templates.dfts renamed.dfts foo bar

# You can also target a specific scope.
# This changes all occurences of the game variable `plotData` to `gameData`.
pyrecli rename templates.dfts renamed.dfts plotData gameData -s game
```

### Script

Generates Python scripts from template data.

Example:
```sh
# Convert templates into individual scripts and store them in directory `plot_templates`
pyrecli script templates.dfts plot_templates

# Convert templates into scripts and put them into a single file `plot_templates.py`
pyrecli script templates.dfts plot_templates.py --onefile
```


### Grabinv

**[Requires CodeClient]**

Scans your inventory for templates and saves them to a file.

Example:
```sh
# Save inventory templates to `templates.dfts`
pyrecli grabinv templates.dfts
```


### Docs

Generates a Markdown documentation file for a list of templates.

Example:
```sh
# Generate documentation and save it to `plot_docs.md`
pyrecli docs templates.dfts plot_docs.md "My Plot Docs"
```


### Slice

Slices a single template into multiple smaller templates.
This is useful for resizing templates to fit on a smaller plot.

If multiple templates are passed, only the first one will be used.

**NOTE: This feature is not fully implemented yet. Any templates with Control::Return blocks may not work properly if sliced.**

Example:
```sh
# Slices the first template in `templates.dfts` with a target length of 50 and stores them in `sliced_templates.dfts`
pyrecli slice templates.dfts sliced_templates.dfts 50
```


### CCToken

Returns a CodeClient authentication token that can be used in commands that require CodeClient authorization.
This is useful for reducing the amount of times you need to run `/auth`.

Example:
```sh
# Get a token with the read_plot and inventory scopes
pyrecli cctoken mytoken.txt "read_plot inventory"
```


### Command Chaining

You can combine the pipe operator (`|`) with hyphen (`-`) file paths to chain multiple commands together.

Example:
```sh
# Scans the plot, renames a variable, then sends renamed templates back to DiamondFire
pyrecli scan - | pyrecli rename - foo bar | pyrecli send -

```