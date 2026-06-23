import requests
import os
import sys

def upload_long_image(file_path, title, sessionid, steamLoginSecure, is_screenshot=False):
    """
    Uploads an image to Steam as a long artwork or screenshot.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"Uploading '{file_path}' as {'Screenshot' if is_screenshot else 'Artwork'}...")

    import re
    
    session = requests.Session()
    session.cookies.update({
        'sessionid': sessionid,
        'steamLoginSecure': steamLoginSecure
    })
    
    print("Fetching upload tokens from Steam...")
    try:
        r = session.get("https://steamcommunity.com/sharedfiles/edititem/767/3/")
        
        if "Sign In" in r.text or not r.request.headers.get('Cookie'):
            print("\n[X] Error: You are not logged in. Your cookies are invalid or expired.")
            return


        action_match = re.search(r'action="(https://[^"]+)"', r.text[r.text.find('id="SubmitItemForm"'):])
        if not action_match:
            print("\n[X] Error: Could not find the upload endpoint in the page HTML.")
            return
        post_url = action_match.group(1)


        data = {}
        for match in re.finditer(r'<input type="hidden" name="([^"]+)"(?: id="[^"]+")? value="([^"]*)"', r.text):
            data[match.group(1)] = match.group(2)
            

        prefix_match = re.search(r"cloudfilenameprefix\.value\s*=\s*'([^']+)';", r.text)
        if prefix_match:
            data['cloudfilenameprefix'] = prefix_match.group(1)


        data['image_width'] = '1000'
        data['image_height'] = '1'
        data['title'] = title
        data['description'] = ''
        data['visibility'] = '0' # Public
        data['agree_terms'] = 'on'
        
        if is_screenshot:
            data['file_type'] = '5' # 5 is Screenshot

        ext = file_path.lower().split('.')[-1]
        mime_type = 'image/gif' if ext == 'gif' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/png'

        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        with open(file_path, 'rb') as f:
            files = { 'file': (os.path.basename(file_path), f, mime_type) }
            
            print(f"Uploading to Steam server...")
            response = session.post(post_url, data=data, files=files, allow_redirects=False, verify=False)
            

            if response.status_code in [301, 302, 303] and "filedetails" in response.headers.get('Location', ''):
                print(f"\n[SUCCESS] Uploaded! View it here: {response.headers.get('Location')}")

            elif "filedetails" in response.text or "filedetails" in response.url:
                print("\n[SUCCESS] Uploaded successfully!")
            else:
                print("\n[X] Upload failed! The server rejected the file.")
                print("Make sure your file is a valid image under 5MB.")
                
                error_file = "steam_upload_error.html"
                with open(error_file, 'w', encoding='utf-8') as ef:
                    ef.write(response.text)
                print(f"[!] Saved error page to: {os.path.abspath(error_file)}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("--- Steam Long Image Uploader ---")
    
    print("\n[!] You will need your Steam cookies to upload.")
    print("[!] You can find them by logging into Steam on your web browser, pressing F12, and checking the Application/Storage -> Cookies tab.")
    
    SESSION_ID = input("Enter your 'sessionid' cookie: ").strip()
    STEAM_LOGIN_SECURE = input("Enter your 'steamLoginSecure' cookie: ").strip()
    
    if not SESSION_ID or not STEAM_LOGIN_SECURE:
        print("Error: Both cookies are required. Exiting...")
        sys.exit(1)

    file_path = input("Enter the path to your image/gif: ").strip('"')
    title = input("Enter a title for your artwork: ")
    choice = input("Upload as (1) Artwork or (2) Screenshot? [1/2]: ")
    
    is_screenshot = (choice.strip() == '2')
    
    upload_long_image(file_path, title, SESSION_ID, STEAM_LOGIN_SECURE, is_screenshot)
