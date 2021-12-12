# coding:utf-8
import argparse
import base64
import logging
import os
import xml.etree.cElementTree as ET
from base64 import b64decode
from string import Template

import requests
from urllib3.exceptions import InsecureRequestWarning
from Get_mails import GetMails



requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

TARGET = "mail.iob.vo.th"
templatesFolder = "ews_template/"
# exchangeVersion = "Exchange2010_SP2"
exchangeNamespace = {'m': 'http://schemas.microsoft.com/exchange/services/2006/messages',
                     't': 'http://schemas.microsoft.com/exchange/services/2006/types'}
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36."


def convertFromTemplate(shellcode, templateFile):
    try:
        with open(templateFile) as f:
            src = Template(f.read())
            result = src.substitute(shellcode)
            f.close()
            return result
    except IOError as e:
        print("[!] Could not open or read template file [{}]".format(templateFile))
        return e

print(GetMails(TARGET))