# Task Tracker

A tiny, clean, and delightful way to track tasks. Minimal setup, simple UI, and just enough features to stay focused.

Language: English | [Українська](README.uk.md)

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-EE4C2C?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![License](https://img.shields.io/github/license/fand1l/task_tracker)](LICENSE)

## Features
- ✍️ Create and edit tasks
- ✅ Mark tasks as done
- 🔎 Filter and focus on what's important
- 💾 Lightweight and fast (no heavy dependencies)
- 🧩 Minimal mental overhead: just tasks, status, and focus

## Quick Start
1. Clone the repo
   ```bash
   git clone https://github.com/fand1l/task_tracker.git
   cd task_tracker
   ```
2. Create a virtual environment
   ```bash
   python -m venv .venv
   # Activate:
   # Linux/macOS
   . .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```
3. Install dependencies (if present)
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app
   ```bash
   python manage.py runserver
   ```
5. Open your browser:
   - http://localhost:8000 or
   - http://localhost:5000 (depending on configuration)

## Tech Stack
- Backend: Python
- Frontend: HTML templates

Language composition:
- Python — 50.2%
- HTML — 49.8%

## Project Structure
| Path | Description |
|------|-------------|
| [`TaskTracker/`](TaskTracker) | Application modules |
| [`core/`](core) | Core project parts (shared/base logic) |
| [`manage.py`](manage.py) | Entry point to start the server |
| [`requirements.txt`](requirements.txt) | Dependency list |
| [`README.md`](README.md) | This file |
| [`LICENSE`](LICENSE) | License |

## Contributing
Contributions are welcome!
1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/short-description
   ```
3. Make changes with clear commits
4. Ensure style remains minimal and consistent
5. Open a Pull Request describing:
   - Motivation
   - Changes
   - Screenshots (if UI affected)

### Ideas / Possible Enhancements
- Task categories or tags
- Simple search bar
- Dark mode
- Export/import tasks (JSON)
- Priority flag

If you start one of these, mention it in your PR.

## License
This project is licensed under the terms of the [LICENSE](LICENSE).

## Acknowledgments
Built for simplicity and focus. No noise — just tasks.

---
Happy tracking!
