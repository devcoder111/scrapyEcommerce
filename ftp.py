from ftplib import FTP  
ftp = FTP('s17.wpxhosting.com')  
ftp.login('football1', ':4uT%J*r84')  
ftp.cwd('/domains/privatedeal.co.il/public_html/wp-content/uploads/wpallimport/files/')
with open('newbalance.csv', 'rb') as f:
    ftp.storbinary('STOR %s' % 'newbalance.csv', f)  
ftp.quit()
