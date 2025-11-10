
import os
import time
import csv
import json
import random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError


load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not EMAIL or not PASSWORD:
    raise SystemExit("Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in environment or .env")


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def safe_text(locator):
    try:
        return locator.inner_text(timeout=3000).strip()
    except Exception:
        try:
            return locator.text_content(timeout=3000).strip()
        except Exception:
            return ""

def safe_attr(locator, attr):
    try:
        return locator.get_attribute(attr, timeout=3000) or ""
    except Exception:
        return ""

def login_linkedin(page):
    page.goto("https://www.linkedin.com/login", wait_until="networkidle")
    # logging in
    page.fill('input#username', EMAIL)
    page.fill('input#password', PASSWORD)
    page.click('button[type="submit"]')
    # waiting some time to make sure the site loads
    try:
        page.wait_for_url("https://www.linkedin.com/feed/*", timeout=15000)
        print("Logged in automatically.")
    except PWTimeoutError:
        print("Login did not complete automatically. If LinkedIn asked for verification (MFA/CAPTCHA), please complete it in the opened browser.")
        # give human 2 minutes to solve verification (adjust as needed)
        page.wait_for_timeout(120_000)
        
        print("Resuming after manual intervention.")

def parse_profile(page, url):
    # visiting the url
    page.goto(url, wait_until="domcontentloaded")
    # again waiting some time to make sure data is loaded
    time.sleep(random.uniform(2.0, 4.0))

    # extracting the linkedin id from the url
    slug = url.rstrip("/").split("/")[-1]
    
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    screenshot_path = OUTPUT_DIR / f"{slug}_{ts}.png"
    html_path = OUTPUT_DIR / f"{slug}_{ts}.html"
    
    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
    except Exception:
        pass
    
    try:
        html = page.content()
        html_path.write_text(html, encoding="utf-8")
    except Exception:
        html = ""

    # Name:
    full_name = ""
    try:
        full_name = safe_text(page.locator("div.ph5 h1")) or safe_text(page.locator("h1.text-heading-xlarge"))
        if not full_name:
            full_name = safe_text(page.locator("h1"))
    except Exception:
        pass

    # splitting name into first and last
    first_name = ""
    last_name = ""
    if full_name:
        parts = full_name.split()
        if len(parts) > 0:
            first_name = parts[0]
        if len(parts) > 1:
            last_name = " ".join(parts[1:])

    # Headline 
    headline = ""
    try:
        headline = safe_text(page.locator("div.text-body-medium")) or safe_text(page.locator(".pv-top-card--list li"))
        if not headline:
            headline = safe_text(page.locator("div.ph5 div.text-body-medium"))
    except Exception:
        pass

    # Location
    location = ""
    try:
        location = safe_text(page.locator("span.text-body-small.inline.t-black--light.break-words"))
        if not location:
            location = safe_text(page.locator(".pv-top-card--list-bullet li"))
    except Exception:
        pass

    # About
    about = ""
    try:
        about_section = page.locator("section:has(#about)")
        if about_section.count() > 0:
            about = safe_text(about_section.locator(".inline-show-more-text"))
        if not about:
            about = safe_text(page.locator("section.pv-about-section p"))
    except Exception:
        pass

    # Profile image URL
    profile_image_url = ""
    try:
        img = page.locator("img.pv-top-card-profile-picture__image")
        if img.count() == 0:
            img = page.locator("button.pv-top-card-profile-picture img")
        if img.count() == 0:
            img = page.locator("img[title*='profile']")
        profile_image_url = safe_attr(img.first, "src")
    except Exception:
        pass

    # Experience
    experiences = []
    current_company = ""
    current_title = ""
    
    try:
        #
        exp_section = page.locator("section:has(#experience)")
        if exp_section.count() > 0:
            exp_items = exp_section.locator("ul li.artdeco-list__item")
            count = min(exp_items.count(), 10)
            
            for i in range(count):
                item = exp_items.nth(i)
                
                # job title
                title = safe_text(item.locator("div.display-flex.align-items-center span[aria-hidden='true']"))
                if not title:
                    title = safe_text(item.locator("span.mr1.t-bold span"))
                
                # company Name
                company = safe_text(item.locator("span.t-14.t-normal span[aria-hidden='true']"))
                if not company:
                    company = safe_text(item.locator("span.t-14.t-normal"))
                
                # duration
                duration = safe_text(item.locator("span.t-14.t-normal.t-black--light span[aria-hidden='true']"))
                if not duration:
                    duration = safe_text(item.locator("span.pvs-entity__caption-wrapper"))
                
                # parsing dates
                from_date = ""
                to_date = ""
                if duration:
                    
                    if " - " in duration:
                        parts = duration.split(" - ")
                        from_date = parts[0].strip()
                        to_date = parts[1].strip() if len(parts) > 1 else "Present"
                
                if title or company:
                    experiences.append({
                        "company": company,
                        "title": title,
                        "from": from_date,
                        "to": to_date
                    })
                    
                    
                    if i == 0:
                        current_company = company
                        current_title = title
        
        # Fallback
        if not experiences:
            exp_sections = page.locator('section#experience-section li')
            count = min(exp_sections.count(), 10)
            for i in range(count):
                item = exp_sections.nth(i)
                title = safe_text(item.locator("h3"))
                company = safe_text(item.locator("p.pv-entity__secondary-title"))
                duration = safe_text(item.locator(".pv-entity__date-range span"))
                
                if title or company:
                    experiences.append({
                        "company": company,
                        "title": title,
                        "from": "",
                        "to": ""
                    })
                    
                    if i == 0:
                        current_company = company
                        current_title = title
    except Exception as e:
        print(f"Error parsing experience: {e}")

    # Education
    educations = []
    try:
        edu_section = page.locator("section:has(#education)")
        if edu_section.count() > 0:
            edu_items = edu_section.locator("ul li.artdeco-list__item")
            count = min(edu_items.count(), 5)
            
            for i in range(count):
                item = edu_items.nth(i)
                school = safe_text(item.locator("span.mr1.hoverable-link-text.t-bold span[aria-hidden='true']"))
                if not school:
                    school = safe_text(item.locator("span.mr1.t-bold span"))
                
                degree = safe_text(item.locator("span.t-14.t-normal span[aria-hidden='true']"))
                if not degree:
                    degree = safe_text(item.locator("span.t-14.t-normal"))
                
                if school:
                    educations.append({"school": school, "degree": degree})
        
        # Fallback
        if not educations:
            edu_sections = page.locator('#education-section li')
            count = min(edu_sections.count(), 5)
            for i in range(count):
                item = edu_sections.nth(i)
                school = safe_text(item.locator("h3"))
                degree = safe_text(item.locator(".pv-entity__degree-name"))
                if school:
                    educations.append({"school": school, "degree": degree})
    except Exception as e:
        print(f"Error parsing education: {e}")

    # Contact info
    contact_info = {}
    try:
        # clicking on contact info button if available on the page
        contact_btn = page.locator("a#top-card-text-details-contact-info, a:has-text('Contact info')")
        if contact_btn.count() > 0:
            contact_btn.first.click()
            time.sleep(2)
            
            # email
            email_elem = page.locator("section.pv-contact-info__contact-type.ci-email a")
            if email_elem.count() > 0:
                email = safe_text(email_elem.first)
                if email:
                    contact_info['email'] = email
            
            # phone
            phone_elem = page.locator("section.pv-contact-info__contact-type.ci-phone span.t-14")
            if phone_elem.count() > 0:
                phone = safe_text(phone_elem.first)
                if phone:
                    contact_info['phone'] = phone
            
            
            try:
                close_btn = page.locator("button[aria-label='Dismiss']")
                if close_btn.count() > 0:
                    close_btn.first.click()
                    time.sleep(1)
            except:
                pass
    except Exception as e:
        print(f"Error getting contact info: {e}")

   
    contact_info_str = ""
    if contact_info:
        parts = []
        if 'email' in contact_info:
            parts.append(f"Email: {contact_info['email']}")
        if 'phone' in contact_info:
            parts.append(f"Phone: {contact_info['phone']}")
        contact_info_str = " | ".join(parts)

    # Collected data
    record = {
        "profile_url": url,
        "scrape_date": datetime.now().isoformat(),
        "linkedin_id": slug,
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "headline": headline,
        "current_company": current_company,
        "current_title": current_title,
        "location": location,
        "about": about,
        "experience": json.dumps(experiences, ensure_ascii=False),
        "education": json.dumps(educations, ensure_ascii=False),
        "profile_image_url": profile_image_url,
        "contact_info": contact_info_str,
    }
    return record

def scrape_profiles(profile_urls, status_callback=None, stop_check=None):
    """Main scraping function that can be called from Flask app"""
    
    csv_path = OUTPUT_DIR / f"linkedin_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    browser = None
    
    try:
        with sync_playwright() as p:
            # launching browser in headless mode for Docker deployment
            # Use headless=False for local development with UI
            is_headless = os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
            
            browser = p.chromium.launch(
                headless=is_headless, 
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-plugins-discovery",
                    "--no-sandbox",  # Required for Docker
                    "--disable-setuid-sandbox",  # Required for Docker
                    "--disable-dev-shm-usage"  # Overcome limited resource problems
                ]
            )
            context = browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            
            page.on("pageerror", lambda err: None)
            page.on("console", lambda msg: None if msg.type == "error" else None)

            # Login
            if status_callback:
                status_callback(0, len(profile_urls), "Logging into LinkedIn...")
            
            try:
                login_linkedin(page)
            except Exception as e:
                print(f"Login error: {e}")
                if status_callback:
                    status_callback(0, len(profile_urls), f"Login failed: {str(e)}")
                
                time.sleep(5)
                if browser:
                    browser.close()
                raise

            results = []
            for idx, url in enumerate(profile_urls, start=1):
                
                if stop_check and stop_check():
                    print(f"Stopping scraper as requested by user")
                    if status_callback:
                        status_callback(idx - 1, len(profile_urls), "Stopped by user", str(csv_path))
                    break
                
                if status_callback:
                    status_callback(idx, len(profile_urls), f"Scraping profile {idx}/{len(profile_urls)}")
                
                print(f"[{idx}/{len(profile_urls)}] Visiting {url}")
                
                #error handling while parsing the profiles
                try:
                    # validating URL format
                    if not url.startswith('http'):
                        raise ValueError(f"Invalid URL format: {url}")
                    
                    rec = parse_profile(page, url)
                    results.append(rec)
                    
                    # Save intermediate results after each successful scrape
                    save_csv(csv_path, results)
                    
                    
                    if status_callback and len([r for r in results if 'error' not in r or not r['error']]) == 1:
                        status_callback(idx, len(profile_urls), f"Scraping profile {idx}/{len(profile_urls)}", str(csv_path), has_success=True)
                    elif status_callback:
                        status_callback(idx, len(profile_urls), f"Scraping profile {idx}/{len(profile_urls)}", str(csv_path))
                    
                    
                    delay = random.uniform(5.0, 12.0)
                    start_time = time.time()
                    while time.time() - start_time < delay:
                        if stop_check and stop_check():
                            print(f"Stop requested during delay, breaking immediately")
                            break
                        time.sleep(0.5)  # Check every 0.5 seconds
                    
                except PWTimeoutError as e:
                    error_msg = f"Timeout accessing profile"
                    print(f"Timeout error for {url}: {e}")
                    results.append({
                        "profile_url": url,
                        "scrape_date": datetime.now().isoformat(),
                        "linkedin_id": url.rstrip("/").split("/")[-1] if "/" in url else "unknown",
                        "error": error_msg,
                    })
                    # Save even error records
                    save_csv(csv_path, results)
                    # Notify failed URL
                    if status_callback:
                        status_callback(idx, len(profile_urls), f"Failed to scrape profile {idx}/{len(profile_urls)}", failed_url=url)
                    time.sleep(random.uniform(3.0, 6.0))
                    
                except ValueError as e:
                    error_msg = str(e)
                    print(f"Validation error for {url}: {e}")
                    results.append({
                        "profile_url": url,
                        "scrape_date": datetime.now().isoformat(),
                        "linkedin_id": url.rstrip("/").split("/")[-1] if "/" in url else "unknown",
                        "error": error_msg,
                    })
                    save_csv(csv_path, results)
                    # Notify failed URL
                    if status_callback:
                        status_callback(idx, len(profile_urls), f"Failed to scrape profile {idx}/{len(profile_urls)}", failed_url=url)
                    time.sleep(random.uniform(2.0, 4.0))
                    
                except Exception as e:
                    error_msg = f"Failed to scrape: {str(e)}"
                    print(f"Error parsing {url}: {e}")
                    results.append({
                        "profile_url": url,
                        "scrape_date": datetime.now().isoformat(),
                        "linkedin_id": url.rstrip("/").split("/")[-1] if "/" in url else "unknown",
                        "error": error_msg,
                    })
                    save_csv(csv_path, results)
                    # Notify failed URL
                    if status_callback:
                        status_callback(idx, len(profile_urls), f"Failed to scrape profile {idx}/{len(profile_urls)}", failed_url=url)
                    time.sleep(random.uniform(3.0, 6.0))

            print(f"Done. CSV saved to: {csv_path}")
            if browser:
                browser.close()
            
            return str(csv_path)
    
    except Exception as e:
        print(f"Fatal error in scraper: {e}")
        import traceback
        traceback.print_exc()
        if browser:
            try:
                browser.close()
            except:
                pass
        raise

def save_csv(csv_path, results):
    """Helper function to save results to CSV"""
    fieldnames = [
        "profile_url", "scrape_date", "linkedin_id", "full_name", "first_name",
        "last_name", "headline", "current_company", "current_title", "location",
        "about", "experience", "education", "profile_image_url",
        "contact_info", "error"
    ]
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            # ensure keys exist
            for k in fieldnames:
                if k not in r:
                    r[k] = ""
            writer.writerow(r)

if __name__ == "__main__":
    # For testing standalone
    test_urls = [
        "https://www.linkedin.com/in/satyanadella/",
    ]
    scrape_profiles(test_urls)
