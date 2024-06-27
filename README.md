# GitCCPy - Selective File Copy for FTP Deployment

## Overview

In website development, developers often need to upload only changed files to an FTP server. However, most FTP client applications do not include this feature. To address this, I have created a solution using Python.

## What does this solution do?

This solution provides a Python script that executes the `git diff-tree` command to identify changed files. It then copies all changed files into a specified location, allowing developers to upload only those changed files to the FTP server using their preferred FTP client software.

## Instructions

### Step 1: Create Configuration File

Create a `.gitccpy` configuration file in the directory where Git is initialized. Below is an example of the content:

```
LOCAL_PREFIX=specific/path/
DESTINATION_PATH=des/path
```

- `LOCAL_PREFIX`: Specifies the directory within the project from which to copy changed files. It can be left empty (e.g., `LOCAL_PREFIX=`) to copy all changes from the entire project.
- `DESTINATION_PATH`: Specifies the destination path where the changed files will be copied. This includes creating the necessary containing folders.

### Step 2: Usage with Python

Run the script with the following command structure:

```
python gitccpy.py <commit-id>
```

- `<commit-id>`: The commit ID to compare against. The default value is `HEAD`.

### Step 3: Usage with Executable

If you have an executable version of the script, use the following command structure:

```
gitccpy <commit-id>
```

- `<commit-id>`: The commit ID to compare against. The default value is `HEAD`.

## Example

To copy changed files from a specific directory to the destination path, set the configuration as follows:

```
LOCAL_PREFIX=src/
DESTINATION_PATH=/var/www/html/
```

To run the script and copy the changed files based on the latest commit:

```
python gitccpy.py
```

Or using the executable:

```
gitccpy
```

This will copy all changed files in the `src/` directory to the `/var/www/html/` directory, preserving the folder structure.

## Conclusion

With this script, developers can efficiently upload only the changed files to an FTP server, streamlining the deployment process and saving time.
