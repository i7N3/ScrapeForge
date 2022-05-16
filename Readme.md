# python-web-scraper-template

That is Python web service template built on Flask framework, using celery job queue to solve tasks asynchronously.

### This particular template is used for

-   Authorization on any site
-   Simulation human like behavior
-   Additionally the program might use proxies
-   Asynchronous captcha solution using the 2captcha service and celery
-   Headless browser emulation with pyppeteer to communicate with website

### Few words about dependencies

-   `gunicorn`: Web Server
-   `celery`: Aasynchronous task queue
-   `2captcha-python`: SDK of 2captcha.com
-   `Flask`: Micro web framework to build APIs
-   `redis`: In-memory data store (used with celery)
-   `pyppeteer-stealth`: pyppeteer plugin to prevent detection
-   `pyppeteer`: JavaScript (headless) chrome/chromium browser automation library

### Few words about application logic

-   Root `/` EP can help with proxies validation
-   To work with API you need to generate random key and put it into code. When you call EPs put that key into HTTP-header `x-auth-token`
-   To start the job call `/slots/<idx>` EP with account index
-   After sometime call `/status/<task_id>` EP to get the results of job

### How to run the app?

-   To start web service run: `gunicorn wsgi:app`
-   To start celery worker run: `celery -A main.celery worker`
