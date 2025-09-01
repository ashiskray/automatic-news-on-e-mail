import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fpdf import FPDF
import ssl
import smtplib 
from email.message import EmailMessage

email = EmailMessage()

def clean_text(text):
    """Remove or replace characters that can't be encoded in latin1"""
    text = text.replace('“', '"').replace('”', '"')  # Smart quotes
    text = text.replace('’', "'").replace('‘', "'")  # Smart apostrophes
    text = text.replace('—', '-').replace('–', '-')  # Em and en dashes
    text = text.replace('…', '...')  # Ellipsis
    text = text.encode('latin1', errors='ignore').decode('latin1')
    return text

def get_news():
    try:
        url = "https://news.google.com/rss"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "xml")
        headlines = soup.find_all("title")[2:12]  # Skip metadata
        
        if not headlines:
            print("No headlines found!")
            return None
        
        today = datetime.now().strftime("%d-%m-%y")
        filename = f"headlines_{today}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        
        title_text = clean_text(f"Top 10 News of {today}")
        pdf.cell(0, 10, title_text, ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Helvetica", '', 12)
        
        for i, headline in enumerate(headlines, 1):
            clean_headline = clean_text(headline.text)
            headline_text = f"{i}. {clean_headline}"
            
            try:
                pdf.multi_cell(0, 10, headline_text)
                pdf.ln(2)
            except:
                pdf.multi_cell(0, 10, f"{i}. [Unsupported characters]")
                pdf.ln(2)
        
        pdf.output(filename)
        print(f"Headlines saved as '{filename}' successfully!")
        return filename   # return path
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    pdf_file = get_news()
    if pdf_file:
        subject = "Today's Top 10 News Headlines 📰"
        body = "Attached is the PDF containing today's top 10 news headlines."
        
        sender_email = "senders.mail@gmail.com"      # senders mail here 
        receiver_email = "receiver.mail@gmail.com"   # receivers mail here 
        app_password = "app_password"                # your app password here 
        
        email['from'] = sender_email
        email['to'] = receiver_email
        email['subject'] = subject
        email.set_content(body)
        
        # Attach PDF
        with open(pdf_file, "rb") as f:
            file_data = f.read()
            file_name = f.name
        email.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        
        # Send Email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(email)
        
        print("✅ Email sent with PDF attachment!")