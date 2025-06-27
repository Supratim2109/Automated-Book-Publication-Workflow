from flask import Flask, request, render_template_string, redirect, url_for
from scraper.scraper import scrape_website
from db.chroma import save_version, search_versions
from orchestrator.pipeline import run_pipeline
from uuid import uuid4

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        raw = scrape_website(url)
        spun, reviewed = run_pipeline(raw)
        return redirect(url_for('hitl_edit', step=1, raw=raw, spun=spun, reviewed=reviewed))

    return '''
        <h1>Automated Book Publication Workflow</h1>
        <form method="POST">
            <label>Chapter URL:</label>
            <input type="text" name="url" size="80">
            <input type="submit" value="Submit">
        </form>
        <br>
        <a href="/retrieve"> Retrieve Saved Version</a>
    '''

@app.route('/hitl_edit', methods=['GET', 'POST'])
def hitl_edit():
    step = int(request.args.get("step", 1))
    raw = request.args.get("raw")
    spun = request.args.get("spun")
    content = request.args.get("reviewed")

    if request.method == 'POST':
        edited = request.form['edited']
        revised = run_pipeline(edited)[1]
        return redirect(url_for('hitl_edit', step=step+1, raw=raw, spun=spun, reviewed=revised))

    return render_template_string('''
        <h2>Original Extracted Chapter</h2>
        <pre>{{ raw }}</pre>
        <h2>AI Writer Output</h2>
        <pre>{{ spun }}</pre>
        <h2>AI Reviewer Output (Editable)</h2>
        <form method="POST">
            <textarea name="edited" rows="25" cols="100">{{ content }}</textarea><br>
            <input type="submit" value="Revise Again">
        </form>
        <form action="{{ url_for('finalize') }}" method="POST">
            <input type="hidden" name="final_text" value="{{ content }}">
            <input type="submit" value="Finalize">
        </form>
    ''', raw=raw, spun=spun, content=content, step=step)

@app.route('/finalize', methods=['POST'])
def finalize():
    final_text = request.form['final_text']
    version_id = str(uuid4())[:8]
    save_version(version_id, final_text)
    return f"""
        <h3>Saved Successfully</h3>
        <b>Version ID:</b> {version_id}<br>
        <pre>{final_text}</pre>
        <a href='/'>Back</a>
    """

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = search_versions(query)
        html = "<h2>Results:</h2><ul>"
        for res in results:
            html += f"<li><b>{res['id']}</b><br><pre>{res['text'][:300]}...</pre></li><hr>"
        html += "</ul><a href='/'>Back</a>"
        return html

    return '''
        <h2> Search Versions</h2>
        <form method="POST">
            <input name="query" size="60">
            <input type="submit" value="Search">
        </form>
    '''

@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        version_id = request.form['version_id']
        results = search_versions("", return_all=True)
        for res in results:
            if res["id"] == version_id:
                return f"""
                    <h2> Retrieved Version: {version_id}</h2>
                    <pre>{res['text']}</pre>
                    <a href='/'>Back</a>
                """
        return f"<p> No version found with ID {version_id}</p><a href='/retrieve'>Try again</a>"

    return '''
        <h2> Retrieve Saved Version</h2>
        <form method="POST">
            <label>Enter Version ID:</label>
            <input name="version_id" size="40">
            <input type="submit" value="Retrieve">
        </form>
        <a href="/">Back</a>
    '''

if __name__ == '__main__':
    app.run(debug=False)
