# web-scraper-poc 🌐

## Overview 🌟

Web scraper Python web service proof of concept (POC): template/starter/example built on the Flask framework and integrating a Celery job queue, offers solution for web scraping tasks. It's designed to perform authorization on websites, simulate human-like behavior, and handle asynchronous tasks effectively.

## Key Features 🛠️

-   **Proxy Support:** Configurable for proxy usage.
-   **Asynchronous Operations:** Uses Celery for task management.
-   **User Simulation:** Mimics human behavior for more effective scraping.
-   **Browser Emulation:** Utilizes pyppeteer for headless browser interactions.
-   **Captcha Solving:** Integrates 2captcha service for automated captcha resolution.

## Dependencies 📝

-   `flask`: Core web framework.
-   `gunicorn`: Preferred web server.
-   `redis`: In-memory data store, used with Celery.
-   `celery`: For managing asynchronous task queues.
-   `2captcha-python`: SDK for captcha solving service.
-   `pyppeteer` & `pyppeteer-stealth`: For browser automation and stealth operation.

## Application Logic 🔧

-   **Proxy Validation:** Root endpoint `/` checks proxy health.
-   **Authentication:** Generate a random key for API access, used in the `x-auth-token` HTTP header.
-   **Task Management:** Start scraping tasks via `/slots/<idx>` and check status with `/status/<task_id>`.

## Quick Start Guide 🚀

-   **Start the Web Service:** Run `gunicorn wsgi:app`.
-   **Start the Celery Worker:** Execute `celery -A main.celery worker`.

## Contributing 💡

Contributions to enhance the template, add new features, or improve documentation are highly appreciated. Feel free to fork the project and submit your pull requests!
