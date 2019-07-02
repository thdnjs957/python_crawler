import ssl
from urllib.request import Request, urlopen
import sys
from datetime import datetime

def crawling(
    url='',
    encoding='utf-8',
    err=lambda e: print(f'{e} : {datetime.now()}', file=sys.stderr),
    proc1=lambda data: data,  # default 함수 지정
    proc2=lambda data: data   # default 함수 지정
    ):

    try:
        request = Request(url)
        ssl._create_default_https_context = ssl._create_unverified_context

        response = urlopen(request)

        print(f'{datetime.now()}: success for request [{url}]')

        receive = response.read()

        # html = receive.decode(encoding, errors='replace')
        result = proc2(proc1(receive.decode(encoding, errors='replace')))

        # if proc is not None:
        #     result = proc(html)
        # else:
        #     result = html

        return result

    except Exception as e:
        err(e)

