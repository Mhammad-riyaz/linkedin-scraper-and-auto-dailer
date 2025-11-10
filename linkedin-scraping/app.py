# app.py
import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
from scraper import scrape_profiles
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Store scraping status
scraping_status = {
    'is_scraping': False,
    'current_profile': 0,
    'total_profiles': 0,
    'message': '',
    'csv_path': None,
    'stop_requested': False,
    'has_successful_scrape': False,
    'failed_urls': []
}

# default LinkedIn profiles
DEFAULT_PROFILES = [
    "https://www.linkedin.com/in/satyanadella/",  # Satya Nadella - Microsoft CEO
    "https://www.linkedin.com/in/sundarpichai/",  # Sundar Pichai - Google CEO
    "https://www.linkedin.com/in/jeffweiner08/",  # Jeff Weiner - LinkedIn
    "https://www.linkedin.com/in/williamhgates/",  # Bill Gates
    "https://www.linkedin.com/in/rbranson/",  # Richard Branson
    "https://www.linkedin.com/in/johnlegere/",  # John Legere
    "https://www.linkedin.com/in/johnrampton/",  # John Rampton
    "https://www.linkedin.com/in/andrewyng/",  # Andrew Ng
    "https://www.linkedin.com/in/andrej-karpathy-9a650716/",  # Andrej Karpathy
    "https://www.linkedin.com/in/timcook/",  # Tim Cook - Apple CEO
    "https://www.linkedin.com/in/markmcgrath01/",  # Mark McGrath
    "https://www.linkedin.com/in/reidhoffman/",  # Reid Hoffman - LinkedIn Co-founder
    "https://www.linkedin.com/in/arianaahuffington/",  # Arianna Huffington
    "https://www.linkedin.com/in/ian-goodfellow-b7187213/",  # Ian Goodfellow
    "https://www.linkedin.com/in/sherylsandberg/",  # Sheryl Sandberg - Meta
    "https://www.linkedin.com/in/adamgrant/",  # Adam Grant - Author
    "https://www.linkedin.com/in/simonsinek/",  # Simon Sinek
    "https://www.linkedin.com/in/garyvee/",  # Gary Vaynerchuk
    "https://www.linkedin.com/in/danielpink/",  # Daniel Pink
    "https://www.linkedin.com/in/yann-lecun/",  # Yann LeCun
]

@app.route('/')
def index():
    return render_template('index.html', default_profiles=DEFAULT_PROFILES)

@app.route('/scrape', methods=['POST'])
def scrape():
    global scraping_status
    
    if scraping_status['is_scraping']:
        return jsonify({'error': 'Scraping already in progress'}), 400
    
    data = request.json
    profile_urls = [url.strip() for url in data.get('profiles', []) if url.strip()]
    
    if not profile_urls:
        return jsonify({'error': 'No profile URLs provided'}), 400
    
    # Reset status
    scraping_status = {
        'is_scraping': True,
        'current_profile': 0,
        'total_profiles': len(profile_urls),
        'message': 'Starting scraper...',
        'csv_path': None,
        'stop_requested': False,
        'has_successful_scrape': False,
        'failed_urls': []
    }
    
    # Run scraping in background thread
    thread = threading.Thread(target=run_scraper, args=(profile_urls,))
    thread.start()
    
    return jsonify({'success': True, 'message': 'Scraping started'})

def run_scraper(profile_urls):
    global scraping_status
    print(f"[DEBUG] Starting scraper with {len(profile_urls)} URLs")
    try:
        csv_path = scrape_profiles(profile_urls, status_callback=update_status, stop_check=check_stop)
        print(f"[DEBUG] Scraper completed. CSV path: {csv_path}")
        scraping_status['is_scraping'] = False
        if scraping_status['stop_requested']:
            scraping_status['message'] = 'Scraping stopped by user!'
        else:
            scraping_status['message'] = 'Scraping completed!'
        scraping_status['csv_path'] = csv_path
    except Exception as e:
        print(f"[ERROR] Scraper failed with error: {e}")
        import traceback
        traceback.print_exc()
        scraping_status['is_scraping'] = False
        scraping_status['message'] = f'Error: {str(e)}'
        # Keep csv_path if we have partial results
        if not scraping_status['csv_path']:
            scraping_status['csv_path'] = None

def update_status(current, total, message, csv_path=None, has_success=False, failed_url=None):
    global scraping_status
    scraping_status['current_profile'] = current
    scraping_status['total_profiles'] = total
    scraping_status['message'] = message
    if csv_path:
        scraping_status['csv_path'] = csv_path
    if has_success:
        scraping_status['has_successful_scrape'] = True
    if failed_url:
        if failed_url not in scraping_status['failed_urls']:
            scraping_status['failed_urls'].append(failed_url)

def check_stop():
    global scraping_status
    return scraping_status['stop_requested']

@app.route('/status')
def status():
    return jsonify(scraping_status)

@app.route('/stop', methods=['POST'])
def stop_scraping():
    global scraping_status
    if scraping_status['is_scraping']:
        scraping_status['stop_requested'] = True
        return jsonify({'success': True, 'message': 'Stop requested'})
    return jsonify({'error': 'No scraping in progress'}), 400

@app.route('/download')
def download():
    if scraping_status['csv_path'] and os.path.exists(scraping_status['csv_path']):
        return send_file(
            scraping_status['csv_path'],
            as_attachment=True,
            download_name='linkedin_profiles.csv'
        )
    return jsonify({'error': 'No CSV file available'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
