# How to Upload WeatherReportAPP to GitHub

## Prerequisites
You need to install Git on your Windows system first.

### Step 1: Install Git
1. Go to https://git-scm.com/download/win
2. Download Git for Windows
3. Run the installer and follow the setup wizard
4. During installation, make sure to select "Git from the command line and also from 3rd-party software"

### Step 2: Configure Git (First time setup)
Open PowerShell or Command Prompt and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

## Uploading to GitHub Repository

### Method 1: Using Git Commands (Recommended)

1. **Navigate to your project folder**
   ```bash
   cd E:\WeatherReportAPP
   ```

2. **Initialize Git repository**
   ```bash
   git init
   ```

3. **Add remote repository**
   ```bash
   git remote add origin https://github.com/Shreyas901/Shreyas.git
   ```

4. **Create .gitignore file** (to exclude unnecessary files)
   ```bash
   echo "__pycache__/
   *.pyc
   *.pyo
   .env
   node_modules/
   .vscode/
   *.log" > .gitignore
   ```

5. **Add all files to staging**
   ```bash
   git add .
   ```

6. **Create initial commit**
   ```bash
   git commit -m "Add WeatherReportAPP - Advanced Weather Dashboard with MCP integration"
   ```

7. **Push to GitHub**
   ```bash
   git push -u origin main
   ```

   If you get an error about 'main' branch, try:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### Method 2: Using GitHub Desktop (Alternative)

1. Download and install GitHub Desktop from https://desktop.github.com/
2. Sign in with your GitHub account
3. Click "Add an existing repository from your hard drive"
4. Select the E:\WeatherReportAPP folder
5. Click "Publish repository"
6. Choose "Shreyas901/Shreyas" as the repository
7. Click "Publish Repository"

### Method 3: Upload via GitHub Web Interface

1. Go to https://github.com/Shreyas901/Shreyas
2. Click "Add file" > "Upload files"
3. Drag and drop all files from E:\WeatherReportAPP folder
4. Add commit message: "Add WeatherReportAPP - Advanced Weather Dashboard"
5. Click "Commit changes"

## Troubleshooting

### If you get authentication errors:
1. Make sure you're signed in to GitHub
2. You might need to use a Personal Access Token instead of password
3. Go to GitHub Settings > Developer settings > Personal access tokens
4. Generate a new token with repo permissions
5. Use the token as your password when prompted

### If repository already has content:
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

## Project Structure Being Uploaded

```
WeatherReportAPP/
├── app.py                 # Main Flask application
├── mcp_weather_client.py  # MCP client integration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend JavaScript
├── .env                  # Environment variables (will be ignored)
└── mcp_config.json       # MCP configuration
```

## After Upload Success

Your WeatherReportAPP will be available at:
https://github.com/Shreyas901/Shreyas/tree/main/WeatherReportAPP

You can then:
- Share the repository link
- Clone it on other machines
- Collaborate with others
- Set up GitHub Pages for live demo (if desired)