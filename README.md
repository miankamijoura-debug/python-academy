# Python Academy

A free static learning website built from the original Flask project for GitHub Pages.

## Features
- 50 Python chapters and 15 topics per chapter (750 topics).
- Code examples and expected output.
- Six-question chapter tests with randomized answer order.
- Automatic marking, answer explanations, and Learn Again / Good / Excellent feedback.
- Lesson completion and best test scores saved in the visitor's browser using localStorage.

## Publish with GitHub Pages
1. Open the repository **Settings**.
2. Select **Pages** in the left sidebar.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select branch **main** and folder **/(root)**, then click **Save**.
5. Wait for GitHub Pages to publish. The site URL will be:
   https://miankamijoura-debug.github.io/python-academy/

## Important technical note
GitHub Pages serves static files. This version uses HTML, CSS, and JavaScript; it does not run Flask or Python on GitHub's servers. Tests are checked in the browser, and progress is stored locally in each visitor's browser. It does not provide shared accounts or a central database.

The original `python_academy.py` and `requirements.txt` are kept unchanged.
