# pyrecli

Command line utilities for DiamondFire templates

## Commands

- `scan`: Scan all templates on the plot and dump them to a text file (requires [CodeClient](github.com/DFOnline/CodeClient))
- `send`: Send template items to DiamondFire (requires [CodeClient](github.com/DFOnline/CodeClient))
- `rename`: Rename all occurences of a variable (including text codes)
- `script`: Generate python scripts from template data
- `grabinv`: Save all templates in your Minecraft inventory to a file (requires [CodeClient](github.com/DFOnline/CodeClient))
- `docs`: Generate markdown documentation from template data


## What is this useful for?

- Backing up a plot
- Getting an accurate text representation of DF code
- Open sourcing
- Version control
- Large scale refactoring


## Example Usage

These two commands will scan your plot, convert each template into a python script, then place the scripts into a directory called `myplot`.

```sh
pyrecli scan templates.dfts
pyrecli script templates.dfts myplot
```

If you prefer the templates to be outputted to a single file, use the `--onefile` flag:

```sh
pyrecli scan templates.dfts
pyrecli script templates.dfts myplot.py --onefile
```

For more information about generating scripts, run `pyrecli script -h`.
