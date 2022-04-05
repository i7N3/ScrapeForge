from twocaptcha import TwoCaptcha
from asgiref.sync import sync_to_async


# Docs: https://2captcha.com/2captcha-api

API_KEY = '<API_KEY_FROM_2captcha.com>'
solver = TwoCaptcha(API_KEY)


@sync_to_async
def report_solver_result(captcha_id: str, success: bool):
    print('Sending a message to 2captcha.com ..')

    if success:
        print('captcha solved correctly')
    else:
        print('captcha solved incorrectly')

    solver.report(captcha_id, success)


@sync_to_async
def captcha_solver():
    print('Solving image captcha ..')

    return solver.normal(
        minLen=6,
        maxLen=6,
        lang='en',
        numeric=4,
        caseSensitive=1,
        file='captcha.png',
        hintText='First symbol is small latin letter others 5 symbols are digits',
    )


@sync_to_async
def re_captcha_solver(proxy):
    print('Solving recaptcha ..')

    uri = None
    if proxy is not None:
        uri = proxy

    result = solver.recaptcha(
        sitekey='<TOKEN>',
        url='<WEBSITE_URL>',
        callback='<CALLBACK_NAME>',
        proxy={'type': 'HTTPS', 'uri': uri}
    )
    return result
