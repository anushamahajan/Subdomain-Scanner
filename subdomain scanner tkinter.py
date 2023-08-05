import requests
import concurrent.futures
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

url = "https://raw.githubusercontent.com/theMiddleBlue/DNSenum/master/wordlist/subdomains-top1mil-20000.txt"
response = requests.get(url)

if response.status_code == 200:
    contents = response.text
    words = contents.splitlines()

    def check_url(url, results):
        try:
            response = requests.get(url)
        except Exception as ex:
            pass
        else:
            if response.status_code == 200:
                results.append(url)

    def scan_subdomains(link, progress_var, results_label):
        urls_https = ["https://{}.{}".format(s, link) for s in words]

        subdomains_found = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures_https = [executor.submit(check_url, url, subdomains_found) for url in urls_https]

            concurrent.futures.wait(futures_https)

        results_label.config(text="\n".join(subdomains_found))
        progress_var.set(100)

    def start_scan():
        link = url_entry.get()
        if not link:
            messagebox.showwarning("Warning", "Please enter a domain.")
            return

        loading_label.grid(row=3, column=0, columnspan=2)
        progress_var.set(0)
        scan_thread = threading.Thread(target=scan_subdomains, args=(link, progress_var, results_label))
        scan_thread.start()

    root = tk.Tk()
    root.title("Subdomain Scanner")

    
    url_label = tk.Label(root, text="Enter the URL:")
    url_label.grid(row=0, column=0, padx=10, pady=10)

    url_entry = tk.Entry(root)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    scan_button = tk.Button(root, text="Scan", command=start_scan, width=8, height=1, bg="#00008B", fg="white", font=("Helvetica", 10, "bold"))
    scan_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    


    loading_label = tk.Label(root, text="Loading...", font=("Helvetica", 16))
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    results_label = tk.Label(root, text="", font=("Helvetica", 12))
    results_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()