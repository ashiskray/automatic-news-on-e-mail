# Automatic News Sender
- A simple python script which will genrate a pdf of today's top 10 headlines and provide you on your given E-Mail.

## Requirements 
* pip install requests
* pip install BeautifulSoup
* pip install fpdf
* pip install ssl

## Working process 
- The script will go to the website "https://news.google.com/rss" 
- BeautifulSoup will extract the content  (XML) 
- fpdf will generate a pdf and save the generted content in that pdf 
- smtplib and email.message will sent a email to a receiver's@mail.com from sender's@mail.com

## Extra's information ||
 * fill the senders emial in sender_email and receiver's mail in receiver_email and app_passsword.
 
#### Run the script and everything is set to go...