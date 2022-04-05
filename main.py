import random
import socket
import pyppeteer
import threading
import urllib.request
from celery import Celery
from pyppeteer_stealth import stealth
from asgiref.sync import async_to_sync
from flask import Flask, jsonify, request, abort
from captcha_solver import captcha_solver, report_solver_result

print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)


EP_SECRET = '<YOUR_SECRET_KEY_TO_ACCESS_EP>'
REDIS_URL = '<REDIS_URL>'


# Configure the redis server
app.config['RESULT_BACKEND'] = f'redis://{REDIS_URL}/0'
app.config['CELERY_BROKER_URL'] = f'redis://{REDIS_URL}/0'


# Creates a Celery object
celery = Celery(
    app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['RESULT_BACKEND'])
celery.conf.update(app.config)
celery.conf.task_acks_late = True
celery.conf.worker_max_tasks_per_child = 1
celery.conf.result_expires = 1200  # 20 min

socket.setdefaulttimeout(40)

"""
Email accounts
"""
accounts = [
    'email:pass'
]


"""
Proxies
"""
proxy_list = [
    'ip:port:login:pass'
]


def get_proxy_obj(pip: str):
    proxy_info = pip.split(':')

    ip = proxy_info[0]
    port = proxy_info[1]
    username = proxy_info[2]
    password = proxy_info[3]

    return {
        'ip': ip,
        'port': port,
        'username': username,
        'password': password
    }


def is_bad_proxy(pip: str):
    proxy = get_proxy_obj(pip)

    ip = proxy['ip']
    port = proxy['port']
    username = proxy['username']
    password = proxy['password']

    try:
        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        password_mgr.add_password(None, f'{ip}:{port}', username, password)

        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        # create "opener" (OpenerDirector instance)
        opener = urllib.request.build_opener(handler)

        urllib.request.install_opener(opener)
        sock = urllib.request.urlopen('http://www.google.com')
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR: ", detail)
        return 1
    return 0


def is_valid_proxy(pip: str) -> bool:
    return not bool(is_bad_proxy(pip))


async def parse(idx: int):
    print('Starting the script .. ')

    args = [
        '--no-sandbox',
        '--ignore-certificate-errors',
    ]

    proxy = proxy_list[idx]

    if proxy is not None:
        proxy_obj = get_proxy_obj(proxy)
        proxy_ip = proxy_obj['ip']
        proxy_port = proxy_obj['port']
        proxy_username = proxy_obj['username']
        proxy_password = proxy_obj['password']
        args.append(f'--proxy-server={proxy_ip}:{proxy_port}')
        print(f'Using proxy: {proxy_ip}:{proxy_port}')
    else:
        print(f'WARNING! Something wrong with proxy. Going without it!')

    account_credentials = accounts[idx].split(':')
    email = account_credentials[0]
    pwd = account_credentials[1]

    print(f'Using account: {email}')

    browser = await pyppeteer.launch(
        args=args,
        headless=True,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        ignoreHTTPSErrors=True,
        # executablePath=<PATH_TO_BROWSER>
    )

    page = await browser.newPage()

    await stealth(page)

    # await page.setCookie(cookies)
    await page.setJavaScriptEnabled(True)

    await page.setViewport({'width': 1366, 'height': 768})
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36')

    if proxy is not None:
        await page.authenticate({
            'username': proxy_username,
            'password': proxy_password
        })

    website_url = 'https://example.com/'

    try:
        await page.goto(f'{website_url}')
        print(f'Opening {website_url} page ..')
    except Exception as e:
        print(e)
        return {'result': 0, 'msg': 'Something went wrong while navigation'}

    """
    Don't forget to fake user behaviour at least with timeouts:

    Example:
        await page.waitFor(random.randint(800, 2200))



    1. Fill out the inputs with pyppeteer:

        ...



    2. Save a captcha image:

    Example:
        captcha_img = await page.querySelector('#captcha')
        await captcha_img.screenshot({'path': 'captcha.png'})



    3. Solve captcha with 2captcha:

    Example:
        try:
            solver_result = await captcha_solver()
        except Exception as e:
            print(e)
            return {'result': 0, 'msg': 'Something went wrong while solving captcha'}



    4. Put solver result to captcha input and logged in:

        ...



    5. Validate that logged in was succes and report to 2captcha:

    Don't forget to check if everything is ok and you are not banned.

    Example:
        is_success = True
        await report_solver_result(solver_result['captchaId'], is_succes)



    6. Do what you need to do after logged in and don't forget this at the end:

        finally:
            await browser.close()
    """


@celery.task(bind=True)
def available_slots(self, idx: int):
    self.update_state(state='PROGRESS')
    return async_to_sync(parse)(idx)


@app.route("/", methods=["GET"])
def index():
    result = []

    for pip in proxy_list:
        proxy_obj = get_proxy_obj(pip)

        ip = proxy_obj['ip']
        port = proxy_obj['port']

        is_valid = is_valid_proxy(pip)

        result.append({
            'ip': f'{ip}:{port}',
            'is_valid': is_valid
        })

    return jsonify(result)


@app.route("/slots/<idx>", methods=["GET"])
def slots(idx: str):
    # Custom HTTP header to protect EP
    auth_token = request.headers.get('x-auth-token')

    if auth_token == EP_SECRET and idx is not None:
        idx_as_int = int(idx)

        if idx_as_int < 0 or idx_as_int > len(accounts) - 1:
            abort(500)

        task = available_slots.apply_async(args=[idx_as_int])
        return jsonify({'task_id': task.id})

    else:
        abort(401)


@app.route("/status/<task_id>", methods=["GET"])
def status(task_id: str):
    auth_token = request.headers.get('x-auth-token')

    if auth_token == EP_SECRET and task_id is not None:
        task = available_slots.AsyncResult(task_id)

        if task.state == 'PENDING':
            response = {
                'msg': '',
                'result': 0,
                'state': task.state,
            }
            if task.info is not None:
                if 'msg' in task.info:
                    response['msg'] = task.info['msg']
        elif task.state != 'FAILURE':
            response = {
                'result': 0,
                'state': task.state,
                'msg': '',
            }
            if task.state == 'SUCCESS':
                if task.info is not None:
                    if 'result' in task.info:
                        response['result'] = task.info['result']
                    if 'msg' in task.info:
                        response['msg'] = task.info['msg']
        else:
            # something went wrong in the background job
            response = {
                'result': 0,
                'state': task.state,
                'msg': 'Something went wrong in the background job',
            }
        return jsonify(response)
    else:
        abort(401)
