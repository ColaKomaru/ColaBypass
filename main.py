from flask import Flask, request, jsonify
import re
import requests
import os

app = Flask(__name__)

rekonise_regex = r"https?://rekonise\.com/[\w\-]+"

@app.route('/bypass', methods=['GET'])
def bypass_link():
    try:
        # Get link from query parameter
        link = request.args.get('link', '').strip()
        
        if not link:
            return jsonify({
                'success': False,
                'error': 'No link provided. Use ?link=your_rekonise_url'
            }), 400
        
        match = re.search(rekonise_regex, link)
        
        if match:
            rekonise_link = match.group(0)
            api_link = rekonise_link.replace(
                "https://rekonise.com/", "https://api.rekonise.com/social-unlocks/"
            )
            
            response = requests.get(api_link)
            api_data = response.json()
            
            if "url" in api_data:
                return jsonify({
                    'success': True,
                    'url': api_data['url']
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not find final URL in API response'
                }), 404
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid Rekonise link. Expected format: https://rekonise.com/idk'
            }), 400
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def info():
    return jsonify({
        'service': 'Rekonise Link Bypass API',
        'usage': 'GET /bypass?link=https://rekonise.com/your-id',
        'example': f'{request.url_root}bypass?link=https://rekonise.com/example-id'
    })

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
