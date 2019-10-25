# Progress Tracker Application Help
Progress Tracker Application help documentation.

## Operations

Operations are actions which can be done by typing commands. Each command has its own action. Arguments can be input and configured in each command.

### Append Data

Command `append` is used to append data into a specific storage. After typing in `append` command, an input line will be shown up.

#### Arguments

`-add INTEGER`

`-cus INTEGER`

### Create Charts

Command `chart` is used to create charts in SVG format. Created charts will be in the folder `/charts`, which can be viewed with any web browser application.

#### Arguments

`-average INTEGER`

`-days INTEGER`

`-max-y INTEGER`

`-style STYLE_NAME`

`-allow-float`

`-dynamic`

`-open`

`-today`

### Help

Command `help` is used to open help documentation, this documentation, named `HELP.md`.

### Reload Storage

Command `reload` is used to reload the storage. This command can be used to refresh storage to its current file state. Recommends in 2 situations.

1. When you have added wrong data, but have not saved it yet. Use `reload` command to refresh the storage to its newly loaded or lastest saved version.

2. When you have manually edited the storage file and want the application to update its storage data to the current
version without needing to restart the application.

### Save Storage

Command `save` is used to save the current storage data to the storage file. As appending data does not make any changes to the storage file, saving is required to make changes. By saving, the storage will be reloaded automatically.

### View Storage

Command `view` is used to view storage data.

#### Arguments

`-open`

### Exit Application

Command `exit` is used to exit the application.
