from python.util.log import creatlog
import pprint
import imapclient
import pyzmail

logger = creatlog("excelProcess ")

dstMail = "ldc10@126.com"
passWord = "Tozs9bqt"
imapObj = imapclient.IMAPClient("imap.126.com", ssl=True)
imapObj.login(dstMail, passWord)
folders = imapObj.list_folders()
# pprint.pprint(folders)
imapObj.select_folder('INBOX', readonly=True)
UIDS = imapObj.search(['ALL'])
rawMessages = imapObj.fetch(UIDS, ['BODY[]'])
# pprint.pprint(rawMessages)
message = pyzmail.PyzMessage.factory(rawMessages[1320241627][b'BODY[]'])
if message.text_part:
    messageTxt = message.text_part.get_payload().decode(message.text_part.charset)
    print(message)
if message.html_part:
    messageHtml = message.html_part.get_payload().decode(message.html_part.charset)
    print(messageHtml)
