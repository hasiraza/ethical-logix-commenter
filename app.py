from flask import Flask, render_template, request, jsonify
from performance import PerformanceBenchmark, make_track_performance
import os
from datetime import datetime
from chatbot import generate_linkedin_reply

# Try to find templates folder, fallback to current directory
template_folder = None
possible_paths = ['../templates', 'templates', './templates']
for path in possible_paths:
    if os.path.exists(path):
        template_folder = path
        break

app = Flask(__name__, template_folder=template_folder)

# Initialize benchmark
benchmark = PerformanceBenchmark()

# Create track_performance decorator with access to benchmark
track_performance = make_track_performance(benchmark)

# Import and decorate chatbot functions after creating the decorator
generate_linkedin_reply = track_performance(generate_linkedin_reply)

@app.route('/')
def index():
    # Return your custom HTML if templates don't exist
    if not template_folder:
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Ethicallogix Reply Generater Assistant </title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
            position: relative;
            min-height: 100vh;
        }

        header {
            background-color: #0077b5;
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 20px;
            text-align: center;
        }

        header h1 {
            margin: 0;
            color: white;
            font-size: 24px;
        }

        .nav {
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }

        .nav a {
            margin-right: 20px;
            text-decoration: none;
            color: #0077b5;
            font-weight: 500;
        }

        .nav a:hover {
            text-decoration: underline;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 60px;
        }

        h2, h3 {
            color: #0077b5;
        }

        .input-section {
            margin-bottom: 30px;
        }

        textarea {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 16px;
            margin: 10px 0;
            resize: vertical;
        }

        .options {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        select {
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }

        button {
            background-color: #0077b5;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #006097;
        }

        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }

        .result-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }

        .reply-box {
            background-color: #f0f7fc;
            padding: 20px;
            border-radius: 4px;
            margin: 15px 0;
            border-left: 4px solid #0077b5;
            min-height: 100px;
            white-space: pre-wrap;
        }

        .action-buttons {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .rating {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .rating span {
            color: #666;
        }

        .clear-btn {
            background-color: #f44336;
            color: white;
            margin-left: 10px;
        }

        .clear-btn:hover {
            background-color: #d32f2f;
        }

        footer {
            text-align: center;
            padding: 20px 0;
            color: #666;
            font-size: 14px;
            position: absolute;
            bottom: 0;
            width: 100%;
            left: 0;
        }

        @media (max-width: 600px) {
            .options {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .options select,
            .options button {
                width: 100%;
            }
            
            .rating {
                margin-left: 0;
                margin-top: 10px;
                width: 100%;
                flex-direction: column;
                align-items: flex-start;
            }

            .container {
                padding: 20px;
                margin-bottom: 50px;
            }

            header {
                padding: 15px;
            }

            header h1 {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Ethicallogix AI Assistant</h1>
    </header>
    
    <div class="nav">
        <a href="/">Home</a>
        <a href="/dashboard">Performance Dashboard</a>
        <a href="/simple-test">Debug Test</a>
    </div>
    
    <div class="container">
        <h2>LinkedIn Comment Reply Generator</h2>
        
        <div class="input-section">
            <h3>Enter LinkedIn Comment</h3>
            <textarea id="comment" placeholder="Paste the LinkedIn comment here..."></textarea>
            <div class="options">
                <label for="tone">Tone:</label>
                <select id="tone">
                    <option value="professional">Professional</option>
                    <option value="friendly">Friendly</option>
                    <option value="enthusiastic">Enthusiastic</option>
                    <option value="thoughtful">Thoughtful</option>
                </select>
                <button onclick="generateReply()">Generate Reply</button>
                <button onclick="clearComment()" class="clear-btn">Clear</button>
            </div>
        </div>
        
        <div id="result" class="result-section" style="display: none;">
            <h3>Generated Reply</h3>
            <div id="reply" class="reply-box" contenteditable="true"></div>
            <div class="action-buttons">
                <button onclick="copyToClipboard()">Copy Reply</button>
                <button onclick="regenerateReply()">Regenerate</button>
                <div class="rating">
                    <span>Rate this reply:</span>
                    <select id="rating">
                        <option value="10">10 - Excellent</option>
                        <option value="9">9</option>
                        <option value="8" selected>8 - Good</option>
                        <option value="7">7</option>
                        <option value="6">6 - Average</option>
                        <option value="5">5</option>
                        <option value="4">4 - Poor</option>
                    </select>
                    <button onclick="submitFeedback()">Submit Feedback</button>
                </div>
            </div>
        </div>
    </div>

    <footer>
        Made by Ethicallogix
    </footer>

    <script>
        let currentComment = '';
        
        async function generateReply() {
            currentComment = document.getElementById('comment').value;
            if (!currentComment.trim()) {
                alert('Please enter a comment');
                return;
            }
            
            const button = document.querySelector('.input-section button');
            button.disabled = true;
            button.textContent = 'Generating...';
            
            try {
                const tone = document.getElementById('tone').value;
                const response = await fetch('/generate-reply', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        comment: currentComment,
                        context: tone
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('reply').innerHTML = data.reply;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Error: ' + (data.error || 'Unknown error occurred'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = 'Generate Reply';
            }
        }
        
        function copyToClipboard() {
            const reply = document.getElementById('reply');
            navigator.clipboard.writeText(reply.innerText)
                .then(() => alert('Reply copied to clipboard!'))
                .catch(err => alert('Failed to copy: ' + err));
        }
        
        function regenerateReply() {
            if (currentComment) {
                generateReply();
            }
        }
        
        async function submitFeedback() {
            const rating = document.getElementById('rating').value;
            
            try {
                const response = await fetch('/feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({satisfaction: parseInt(rating)})
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('Thank you for your feedback!');
                }
            } catch (error) {
                alert('Error submitting feedback: ' + error.message);
            }
        }
        
        function clearComment() {
            document.getElementById('comment').value = '';
            document.getElementById('result').style.display = 'none';
            currentComment = '';
        }
    </script>
</body>
</html>'''
    
    try:
        return render_template('index.html')
    except Exception as e:
        # If template exists but there's an error, show the fallback
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Ethicallogix Reply Generater Assistant </title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
            position: relative;
            min-height: 100vh;
        }

        header {
            background-color: #0077b5;
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 20px;
            text-align: center;
        }

        header h1 {
            margin: 0;
            color: white;
            font-size: 24px;
        }

        .nav {
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }

        .nav a {
            margin-right: 20px;
            text-decoration: none;
            color: #0077b5;
            font-weight: 500;
        }

        .nav a:hover {
            text-decoration: underline;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 60px;
        }

        h2, h3 {
            color: #0077b5;
        }

        .input-section {
            margin-bottom: 30px;
        }

        textarea {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 16px;
            margin: 10px 0;
            resize: vertical;
        }

        .options {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        select {
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }

        button {
            background-color: #0077b5;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #006097;
        }

        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }

        .result-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }

        .reply-box {
            background-color: #f0f7fc;
            padding: 20px;
            border-radius: 4px;
            margin: 15px 0;
            border-left: 4px solid #0077b5;
            min-height: 100px;
            white-space: pre-wrap;
        }

        .action-buttons {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .rating {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .rating span {
            color: #666;
        }

        .clear-btn {
            background-color: #f44336;
            color: white;
            margin-left: 10px;
        }

        .clear-btn:hover {
            background-color: #d32f2f;
        }

        footer {
            text-align: center;
            padding: 20px 0;
            color: #666;
            font-size: 14px;
            position: absolute;
            bottom: 0;
            width: 100%;
            left: 0;
        }

        @media (max-width: 600px) {
            .options {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .options select,
            .options button {
                width: 100%;
            }
            
            .rating {
                margin-left: 0;
                margin-top: 10px;
                width: 100%;
                flex-direction: column;
                align-items: flex-start;
            }

            .container {
                padding: 20px;
                margin-bottom: 50px;
            }

            header {
                padding: 15px;
            }

            header h1 {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Ethicallogix AI Assistant</h1>
    </header>
    
    <div class="nav">
        <a href="/">Home</a>
        <a href="/dashboard">Performance Dashboard</a>
        <a href="/simple-test">Debug Test</a>
    </div>
    
    <div class="container">
        <h2>LinkedIn Comment Reply Generator</h2>
        
        <div class="input-section">
            <h3>Enter LinkedIn Comment</h3>
            <textarea id="comment" placeholder="Paste the LinkedIn comment here..."></textarea>
            <div class="options">
                <label for="tone">Tone:</label>
                <select id="tone">
                    <option value="professional">Professional</option>
                    <option value="friendly">Friendly</option>
                    <option value="enthusiastic">Enthusiastic</option>
                    <option value="thoughtful">Thoughtful</option>
                </select>
                <button onclick="generateReply()">Generate Reply</button>
                <button onclick="clearComment()" class="clear-btn">Clear</button>
            </div>
        </div>
        
        <div id="result" class="result-section" style="display: none;">
            <h3>Generated Reply</h3>
            <div id="reply" class="reply-box" contenteditable="true"></div>
            <div class="action-buttons">
                <button onclick="copyToClipboard()">Copy Reply</button>
                <button onclick="regenerateReply()">Regenerate</button>
                <div class="rating">
                    <span>Rate this reply:</span>
                    <select id="rating">
                        <option value="10">10 - Excellent</option>
                        <option value="9">9</option>
                        <option value="8" selected>8 - Good</option>
                        <option value="7">7</option>
                        <option value="6">6 - Average</option>
                        <option value="5">5</option>
                        <option value="4">4 - Poor</option>
                    </select>
                    <button onclick="submitFeedback()">Submit Feedback</button>
                </div>
            </div>
        </div>
    </div>

    <footer>
        Made by Ethicallogix
    </footer>

    <script>
        let currentComment = '';
        
        async function generateReply() {
            currentComment = document.getElementById('comment').value;
            if (!currentComment.trim()) {
                alert('Please enter a comment');
                return;
            }
            
            const button = document.querySelector('.input-section button');
            button.disabled = true;
            button.textContent = 'Generating...';
            
            try {
                const tone = document.getElementById('tone').value;
                const response = await fetch('/generate-reply', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        comment: currentComment,
                        context: tone
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('reply').innerHTML = data.reply;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Error: ' + (data.error || 'Unknown error occurred'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = 'Generate Reply';
            }
        }
        
        function copyToClipboard() {
            const reply = document.getElementById('reply');
            navigator.clipboard.writeText(reply.innerText)
                .then(() => alert('Reply copied to clipboard!'))
                .catch(err => alert('Failed to copy: ' + err));
        }
        
        function regenerateReply() {
            if (currentComment) {
                generateReply();
            }
        }
        
        async function submitFeedback() {
            const rating = document.getElementById('rating').value;
            
            try {
                const response = await fetch('/feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({satisfaction: parseInt(rating)})
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('Thank you for your feedback!');
                }
            } catch (error) {
                alert('Error submitting feedback: ' + error.message);
            }
        }
        
        function clearComment() {
            document.getElementById('comment').value = '';
            document.getElementById('result').style.display = 'none';
            currentComment = '';
        }
    </script>
</body>
</html>'''

@app.route('/dashboard')
def dashboard():
    stats_24h = benchmark.get_performance_stats(24)
    stats_1h = benchmark.get_performance_stats(1)
    return render_template('dashboard.html', stats_24h=stats_24h, stats_1h=stats_1h)

@app.route('/simple-test')
def simple_test():
    """Simple test page with inline HTML"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Test - LinkedIn Reply Generator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
            textarea { width: 100%; height: 150px; margin: 10px 0; padding: 10px; }
            button { background: #0077b5; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #005885; }
            .result { margin-top: 20px; padding: 15px; background: white; border-radius: 4px; }
            .debug { background: #e8e8e8; padding: 10px; margin: 10px 0; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>LinkedIn Reply Generator - Simple Test</h1>
            <p>This is a simple test page to debug the LinkedIn reply generation.</p>
            
            <form id="replyForm">
                <label for="comment">LinkedIn Post Content:</label>
                <textarea id="comment" name="comment" placeholder="Example: Just closed a major M&A deal after 6 months of negotiations. The due diligence process was incredibly complex with thousands of documents to review.">Just closed a major M&A deal after 6 months of negotiations. The due diligence process was incredibly complex with thousands of documents to review.</textarea>
                <button type="submit">Generate Reply</button>
            </form>
            
            <div id="debug" class="debug" style="display: none;"></div>
            <div id="result" class="result" style="display: none;"></div>
            
            <div style="margin-top: 20px;">
                <h3>Quick Tests:</h3>
                <button onclick="testDirect()">Test Direct Function</button>
                <button onclick="testAPI()">Test API Endpoint</button>
            </div>
        </div>
        
        <script>
            function showDebug(message) {
                const debugDiv = document.getElementById('debug');
                debugDiv.innerHTML += message + '\\n';
                debugDiv.style.display = 'block';
            }
            
            async function testDirect() {
                showDebug('Testing direct function call...');
                try {
                    const response = await fetch('/test-generate');
                    const data = await response.json();
                    showDebug('Direct test result: ' + JSON.stringify(data, null, 2));
                } catch (error) {
                    showDebug('Direct test error: ' + error.message);
                }
            }
            
            async function testAPI() {
                showDebug('Testing API endpoint...');
                const testComment = "Just implemented a new case management system and it saved us 10 hours per week.";
                
                try {
                    const response = await fetch('/generate-reply', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            comment: testComment,
                            context: 'professional'
                        })
                    });
                    
                    const data = await response.json();
                    showDebug('API test result: ' + JSON.stringify(data, null, 2));
                } catch (error) {
                    showDebug('API test error: ' + error.message);
                }
            }
            
            document.getElementById('replyForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const comment = document.getElementById('comment').value;
                const resultDiv = document.getElementById('result');
                const debugDiv = document.getElementById('debug');
                
                debugDiv.innerHTML = '';
                debugDiv.style.display = 'block';
                
                if (!comment.trim()) {
                    alert('Please enter a LinkedIn post to reply to');
                    return;
                }
                
                showDebug('Sending request with comment: ' + comment);
                
                try {
                    resultDiv.innerHTML = '<p>Generating reply...</p>';
                    resultDiv.style.display = 'block';
                    
                    const response = await fetch('/generate-reply', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            comment: comment,
                            context: 'professional'
                        })
                    });
                    
                    const data = await response.json();
                    showDebug('Response received: ' + JSON.stringify(data, null, 2));
                    
                    if (data.success) {
                        resultDiv.innerHTML = `
                            <h3>Generated Reply:</h3>
                            <p style="background: #e8f5e8; padding: 10px; border-radius: 4px;">${data.reply}</p>
                            <small>Generated at: ${data.timestamp}</small>
                        `;
                    } else {
                        resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                    }
                } catch (error) {
                    showDebug('JavaScript error: ' + error.message);
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/generate-reply', methods=['POST'])
def api_generate_reply():
    try:
        # Debug: Print raw request data
        print("DEBUG - Raw request data:")
        print(f"Content-Type: {request.content_type}")
        print(f"Request data: {request.data}")
        print(f"Request form: {request.form}")
        print(f"Request args: {request.args}")
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
            print(f"DEBUG - JSON data: {data}")
        else:
            data = request.form.to_dict()
            print(f"DEBUG - Form data: {data}")
        
        comment = data.get('comment', '')
        context = data.get('context', 'professional')
        
        # Debug: Print extracted values
        print(f"DEBUG - Extracted comment: '{comment}'")
        print(f"DEBUG - Comment length: {len(comment) if comment else 'None'}")
        print(f"DEBUG - Context: '{context}'")
        
        if not comment or not comment.strip():
            return jsonify({'error': 'Comment is required and cannot be empty'}), 400
        
        # Debug: Print before calling generate_linkedin_reply
        print(f"DEBUG - About to call generate_linkedin_reply with comment: '{comment[:100]}...'")
        
        reply = generate_linkedin_reply(comment, context)
        
        # Debug: Print the reply
        print(f"DEBUG - Generated reply: '{reply}'")
        
        return jsonify({
            'success': True,
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"DEBUG - Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def api_stats():
    hours = request.args.get('hours', 24, type=int)
    stats = benchmark.get_performance_stats(hours)
    return jsonify(stats)

@app.route('/feedback', methods=['POST'])
def api_feedback():
    try:
        data = request.json
        satisfaction = data.get('satisfaction', 0)
        
        metrics = {
            'user_satisfaction': satisfaction,
            'quality_score': satisfaction,
            'response_time': 0,
            'api_call_time': 0,
            'tokens_used': 0
        }
        benchmark.log_performance(metrics)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test route to verify function works
@app.route('/test-generate')
def test_generate():
    """Test route to verify the generate_linkedin_reply function works"""
    test_comment = "Just closed a major M&A deal after 6 months of negotiations. The due diligence process was incredibly complex."
    
    try:
        reply = generate_linkedin_reply(test_comment)
        return jsonify({
            'success': True,
            'test_comment': test_comment,
            'reply': reply
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Performance benchmark targets
PERFORMANCE_TARGETS = {
    'response_time': {
        'excellent': 1.0,  # < 1 second
        'good': 2.0,      # < 2 seconds
        'acceptable': 5.0, # < 5 seconds
        'poor': float('inf')
    },
    'api_call_time': {
        'excellent': 0.5,
        'good': 1.0,
        'acceptable': 2.0,
        'poor': float('inf')
    },
    'quality_score': {
        'excellent': 9.0,
        'good': 7.0,
        'acceptable': 5.0,
        'poor': 0
    },
    'error_rate': {
        'excellent': 0.1,  # < 0.1%
        'good': 1.0,      # < 1%
        'acceptable': 5.0, # < 5%
        'poor': float('inf')
    }
}

@app.route('/api/benchmark-targets')
def api_benchmark_targets():
    return jsonify(PERFORMANCE_TARGETS)

# For Vercel deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)