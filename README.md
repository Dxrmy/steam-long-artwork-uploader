# Steam Long Artwork Uploader

Usually you have to paste JS into the browser to upload long Steam artwork. This script automates it by scraping your tokens and uploading the image directly.

## Prerequisites

- Python 3.x
- `requests` library

You can install the required library by running:
```bash
pip install requests
```

## Quick Run (No Download)

You can run the script directly from your terminal without needing to manually download any files. Ensure you have the `requests` library installed (`pip install requests`) before running.

### Windows (PowerShell or CMD)
```cmd
curl.exe -sL https://raw.githubusercontent.com/Dxrmy/SteamLongArtworkUploader/master/SteamLongArtworkUploader.py | python -
```

### macOS & Linux
```bash
curl -sL https://raw.githubusercontent.com/Dxrmy/SteamLongArtworkUploader/master/SteamLongArtworkUploader.py | python3 -
```

## Manual Execution

If you prefer to download the script manually:
1. Clone this repository or download `SteamLongArtworkUploader.py`.
2. Grab your Steam Cookies:
   - Log into Steam on your web browser.
   - Press `F12` to open Developer Tools.
   - Go to the **Application** tab (Chrome) or **Storage** tab (Firefox) -> **Cookies** -> `https://steamcommunity.com`.
   - Copy the values for `sessionid` and `steamLoginSecure`.
3. Run the script:
```bash
python SteamLongArtworkUploader.py
```
4. Paste your cookies when prompted, provide the path to your image, and choose whether you want to upload it as an Artwork or a Screenshot.

## Why does the image look invisible on Steam?

Because this script uses the long artwork exploit, it forces the image height to `1` pixel during upload. If you view the image directly on the artwork page, it will look like a microscopic black line.

**This is completely normal!** Go to your Steam Profile -> Edit Profile -> Featured Showcase, and select the image. It will stretch to its true, massive size.

## Troubleshooting

If the upload fails, the script will automatically dump Steam's error response into a file called `steam_upload_error.html` next to the script. Open it in any web browser to see exactly why Steam rejected your file (e.g., file too large, invalid cookies, etc.).

## Disclaimer

This script is provided for educational and customization purposes. Make sure the artwork you upload complies with the Steam Subscriber Agreement and Online Conduct rules.
