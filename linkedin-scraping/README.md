# LinkedIn Profile Scraper

A modern web-based LinkedIn profile scraper that allows you to scrape up to 20 LinkedIn profiles at once.

## Features

-  Scrapes comprehensive profile data including:
  - Full name, first name, last name
  - Headline and current position
  - Location and about section
  - Work experience (with company, title, dates)
  - Education history
  - Profile image URL
  - Contact information (when available)
-  Real-time progress tracking
-  CSV export functionality

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

3. **Configure LinkedIn credentials:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your LinkedIn credentials:
     ```
     LINKEDIN_EMAIL=your_email@example.com
     LINKEDIN_PASSWORD=your_password
     ```

## Usage

1. **Start the web application:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Navigate to `http://localhost:5000`

3. **Use the interface:**
   - 20 famous LinkedIn profiles are pre-filled by default
   - Modify any URLs as needed
   - Click "Scrape Profiles" to start
   - Watch the browser window as it scrapes each profile
   - If LinkedIn prompts for verification (MFA/CAPTCHA), complete it in the browser
   - Download the CSV file when scraping is complete


## Notes

- The scraper runs with a visible browser window
- Random delays are added between profiles to be respectful to LinkedIn
- Contact information may not always be available due to privacy settings

