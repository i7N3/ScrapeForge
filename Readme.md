# ScrapeForge 🌐

## Overview 🌟

ScrapeForge is a Python-based web scraper as a web service. Built with Flask and Celery, it specializes in scraping tasks that require human-like interaction and asynchronous processing. ScrapeForge is a proof of concept (POC).

## Key Features 🛠️

-   **Human-Like Scraping:** Includes proxy support, user behavior simulation, and browser emulation using pyppeteer.
-   **Asynchronous & Efficient:** Leverages Celery for task management and integrates captcha-solving capabilities.

## Application Logic 🔧

-   **Proxy Health Check:** Via the root endpoint /.
-   **API Authentication:** Generate a random key for API access, used in the `x-auth-token` HTTP request header.
-   **Task Management:** Start scraping tasks via `/slots/<idx>` and check status with `/status/<task_id>`.

## Prerequisites

Before getting started, ensure you have:

-   Python 3.x installed.
-   Redis server for managing Celery tasks.
-   Access to a 2captcha account for captcha solving (if needed).

## Quick Start Guide 🚀

-   **Start the Web Service:** Run `gunicorn wsgi:app`.
-   **Start the Celery Worker:** Execute `celery -A main.celery worker`.

## Dependencies 📝

-   `flask`: Core web framework.
-   `gunicorn`: Preferred web server.
-   `redis`: In-memory data store, used with Celery.
-   `celery`: For managing asynchronous task queues.
-   `2captcha-python`: SDK for captcha solving service.
-   `pyppeteer` & `pyppeteer-stealth`: For browser automation and stealth operation.

## Contributing 💡

Your contributions to improve ScrapeForge are welcome! Enhance the template, add features, or improve the documentation by forking the project and submitting PRs.
