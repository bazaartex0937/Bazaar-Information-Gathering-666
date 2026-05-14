from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openai
import os

app = Flask(__name__)

# Set OpenAI API key (replace with your key)
openai.api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    # Here you can save to database or send email
    return jsonify({'status': 'success', 'message': 'Contact submitted'})

@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL required'})
    
    try:
        # Simple crawling with requests and BeautifulSoup
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        text = soup.get_text()[:500]  # First 500 chars
        return jsonify({'title': title, 'content': text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/social_crawl', methods=['POST'])
def social_crawl():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL required'})
    
    try:
        # Use Selenium for dynamic content
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        title = driver.title
        content = driver.find_element_by_tag_name('body').text[:500]
        driver.quit()
        return jsonify({'title': title, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)