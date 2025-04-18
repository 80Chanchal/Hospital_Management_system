# GitHub Upload Instructions

Since you encountered an error pushing to GitHub from the command line, here are alternative methods to upload your project:

## Method 1: Using GitHub Desktop (Recommended)

1. Download and install GitHub Desktop from: https://desktop.github.com/

2. Open GitHub Desktop and sign in with your GitHub account (80Chanchal)

3. Click on "File" > "Add local repository"

4. Browse to your project folder: `C:\Users\hp\Desktop\Blog-Website\Hospital_system`

5. GitHub Desktop will detect that it's a Git repository and offer to add it

6. In the "Repository name" field, enter: `Hospital_Management_System`

7. Make sure "Push to GitHub" is selected and that visibility is set to "Public"

8. Click "Publish repository"

## Method 2: Manual Upload on GitHub

1. Go to: https://github.com/new

2. Create a new repository named "Hospital_Management_System"

3. Make it public and do NOT initialize with README, .gitignore, or license

4. After creating the repository, click "uploading an existing file"

5. Drag and drop all your project files into the browser window

6. Commit the changes

## Method 3: Command Line with Personal Access Token

1. Go to GitHub Settings > Developer Settings > Personal Access Tokens

2. Generate a new token with "repo" scope

3. Copy the token

4. Use this command to push your code:
   ```
   git remote set-url origin https://{YOUR_TOKEN}@github.com/80Chanchal/Hospital_Management_System.git
   git push -u origin main
   ```

Once your project is uploaded, you can view it at:
https://github.com/80Chanchal/Hospital_Management_System 