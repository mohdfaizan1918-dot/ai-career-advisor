from flask import Flask, request, render_template_string
from granite_api import call_granite
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Career Advisor</title>
</head>
<body>
    <h1>AI Career Advisor</h1>
    <form method="post">
        <label>Skills:</label><br>
        <input type="text" name="skills"><br>
        <label>Education:</label><br>
        <input type="text" name="education"><br>
        <label>Interests:</label><br>
        <input type="text" name="interests"><br><br>
        <input type="submit" value="Get Advice">
    </form>
    {% if advice %}
    <h2>Career Advice</h2>
    <p>{{ advice }}</p>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    advice = None
    if request.method == "POST":
        skills = request.form["skills"]
        education = request.form["education"]
        interests = request.form["interests"]
        prompt = f"You are an AI Career Advisor. Suggest possible career paths for someone with the following details:\nSkills: {skills}\nEducation: {education}\nInterests: {interests}"
        advice = call_granite(prompt)
    return render_template_string(HTML_TEMPLATE, advice=advice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
