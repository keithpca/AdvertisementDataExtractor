# Final Working Script: Extract and Save Newspaper Ads to MySQL (With Testing)

import cv2
import pytesseract
import re
import mysql.connector
from PIL import Image
import os

# Step 1: Preprocess image
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshed

# Step 2: Extract text from image
def extract_text(image):
    return pytesseract.image_to_string(image)

# Step 3: Split and parse ads
def parse_ads(text):
    ads = text.split('\n\n')
    parsed_ads = []
    for ad in ads:
        pincode_match = re.search(r'\b\d{6}\b', ad)
        locality_match = re.search(r'\b(Borivali|Ghatkopar|Andheri|Malad|Kandivali|Dadar|Bandra|Bengaluru)\b', ad, re.I)
        if pincode_match and locality_match:
            parsed_ads.append({
                'ad_text': ad.strip(),
                'pincode': pincode_match.group(),
                'locality': locality_match.group().title()
            })
    return parsed_ads

# Step 4: Save to database
def save_to_database(ads):
    print("🚀 save_to_database() function started")
    try:
        print("📡 Trying to connect to MySQL...")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Keith123',
            database='newspaper_ads'
        )
        print("🟢 Connected to MySQL database.")
        
        cursor = conn.cursor()
        for ad in ads:
            print("📥 Inserting:", ad)
            cursor.execute("""
                INSERT INTO ads (ad_text, locality, pincode)
                VALUES (%s, %s, %s)
            """, (ad['ad_text'], ad['locality'], ad['pincode']))
        conn.commit()
        print("✅ Data committed to database.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
    except Exception as e:
        print(f"❌ General Error: {e}")




# Step 5: Full flow with debug and fallback test insert
def main():
    image_path = 'sample2.jpg'  # Replace with your actual image file name

    if os.path.exists(image_path):
        image = preprocess_image(image_path)
        text = extract_text(image)

        print("OCR TEXT PREVIEW:\n", text[:500])

        ads = parse_ads(text)
        print("Parsed Ads:", ads)

        if ads:
            print("✅ Ads found, inserting into database...")
            save_to_database(ads)
        else:
            print("⚠️ No valid ads with pincode and locality found from OCR. Running test insert...")
            # Fallback test insert
            test_ads = [{
                'ad_text': 'FOR SALE: 1BHK in Ghatkopar. Address: XYZ Tower, Ghatkopar, Mumbai - 400077',
                'locality': 'Ghatkopar',
                'pincode': '400077'
            }]
            save_to_database(test_ads)
    else:
        print(f"❌ Image file '{image_path}' not found. Please check path.")

if __name__ == '__main__':
    main()