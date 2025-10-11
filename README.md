# VOD Auto Update Workflow

This repository contains a GitHub Actions workflow that automatically fetches, converts, and updates VOD (Video On Demand) source data. The main components of the system are:

- **Python script** to fetch and convert VOD data from remote URLs to the desired format.
- **GitHub Actions workflow** to automate the process of fetching, converting, and committing the updated files to the repository.

## Workflow Overview

The GitHub Actions workflow is set to trigger on a schedule (daily at 9 AM Beijing time) or when manually triggered. The workflow performs the following steps:

1. **Fetch VOD Data**: It fetches VOD data from the specified remote URLs.
2. **Convert Data**: The fetched data is converted into a desired JSON structure.
3. **Commit Changes**: If there are any changes in the `vod.json` or `xvod.json` files, the workflow commits and pushes them to the repository.

## Files

### `convert_vod.py`

The Python script `convert_vod.py` performs the following:

1. **Fetches VOD Data**: Downloads JSON data from remote VOD URLs.
2. **Converts Data**: Transforms the fetched data into a specific format.
3. **Saves Data**: Writes the transformed data into local `vod.json` and `xvod.json` files in the repository.

### `.github/workflows/update.yml`

This YAML file configures the GitHub Actions workflow. It includes the following steps:

1. **Checkout Repository**: Fetches the latest version of the repository.
2. **Setup Python**: Sets up the Python environment.
3. **Install Dependencies**: Installs required Python packages (`requests` and `base58`).
4. **Run Python Script**: Executes the Python script to fetch and convert VOD data.
5. **Commit and Push Changes**: Adds, commits, and pushes the changes to the repository if any updates are made to the `vod.json` and `xvod.json` files.

## How to Use

### Prerequisites

1. **Python 3.x**: Ensure that Python 3 is installed. The GitHub Actions workflow automatically installs the required version.
2. **GitHub Repository**: The workflow assumes that the repository is hosted on GitHub.

### Setup

1. **Configure GitHub Actions**: 
   - Make sure that your repository contains the `.github/workflows/update.yml` file with the workflow configuration.
   
2. **Configure VOD URLs**:
   - Update the `VOD_SOURCES` list in `convert_vod.py` with the URLs of the remote VOD data sources.
   - The script will fetch data from these URLs and save the resulting files as `vod.json` and `xvod.json`.

3. **Run Workflow**:
   - The workflow will automatically run based on the schedule defined in the `.github/workflows/update.yml` file. 
   - You can also manually trigger the workflow from the GitHub Actions tab.

### Example Workflow Trigger

```yaml
on:
  schedule:
    # Runs every day at 9 AM Beijing time (UTC 1 AM)
    - cron: "0 1 * * *"
  workflow_dispatch:
