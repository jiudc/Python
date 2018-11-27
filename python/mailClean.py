import imapclient
import imaplib
import pyzmail
import pprint
imaplib._MAXLINE = 100000000


dstMail = "ldc10@126.com"
passWord = "Tozs9bqt"
imapObj = imapclient.IMAPClient("imap.126.com", ssl=True)
imapObj.login(dstMail, passWord)
imapObj.select_folder('INBOX', readonly=True)
folders = imapObj.list_folders()
# pprint.pprint(folders)

# UIDs = imapObj.search(['SINCE 01-Jul-2017', 'BEFORE 05-Jul-2017'])
# UIDs = imapObj.search(['FROM', 'noreply@github.com'])
UIDs = imapObj.search(['all'])
rawMessages = imapObj.fetch(UIDs, ['BODY[]'])
print(len(UIDs))
for id in UIDs:
    print(id)
    message = pyzmail.PyzMessage.factory(rawMessages[id][b'BODY[]'])
    print(message.get_subject())
