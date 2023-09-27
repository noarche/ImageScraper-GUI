import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import scrolledtext, messagebox, IntVar, ttk

def fetch_page_content(url):
    response = requests.get(url)
    return response.content

def extract_images(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    img_tags = soup.find_all('img')
    return [urljoin(base_url, img['src']) for img in img_tags if img.has_attr('src')]

def extract_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    a_tags = soup.find_all('a', href=True)
    return [urljoin(base_url, a['href']) for a in a_tags]

def download_image(img_url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    img_data = requests.get(img_url).content
    filename = os.path.join(dest_folder, os.path.basename(img_url))
    
    with open(filename, 'wb') as img_file:
        img_file.write(img_data)

def on_submit():
    urls = url_input.get("1.0", tk.END).strip().splitlines()
    follow_links = follow_links_var.get()
    
    progress_bar['maximum'] = len(urls)
    progress_bar['value'] = 0
    
    for url in urls:
        content = fetch_page_content(url)
        
        images = extract_images(content, url)
        for img in images:
            download_image(img, "downloaded_images")

        if follow_links:
            links = extract_links(content, url)
            for link in links:
                link_content = fetch_page_content(link)
                linked_images = extract_images(link_content, link)
                for img in linked_images:
                    download_image(img, "downloaded_images")
        
        progress_bar['value'] += 1
        root.update_idletasks()
    
    messagebox.showinfo("Info", "Download complete! Check downloaded_images directory.")
    progress_bar['value'] = 0

def show_about():
    messagebox.showinfo("About", "Version 1.1.3\nSeptember 25 2023\nWritten by noarch\nn0arch@pm.me\ngithub.com/noarche\nt.me/noarchdrops\n\nPaste links in text box and start scrape.\nImages are saved only if they meet both rules:\n1. Must be greater than 400x400 px\n2. Format must be: .jpg .jpeg .png .webp")

root = tk.Tk()
root.title("Image Scraper GUI v1.1.3")

label = tk.Label(root, text="Enter URLs (one per line):")
label.pack(pady=10)

url_input = scrolledtext.ScrolledText(root, width=50, height=10)
url_input.pack(pady=20)

follow_links_var = IntVar()
check_follow_links = tk.Checkbutton(root, text="Follow links 1 level deep, use if links are to thumbnails", variable=follow_links_var)
check_follow_links.pack(pady=5)

submit_button = tk.Button(root, text="Scrape", command=on_submit)
submit_button.pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=20)

# About button
about_button = tk.Button(root, text="About", command=show_about)
about_button.pack(pady=10)

root.mainloop()
