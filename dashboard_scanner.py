import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading

# --- Scanning Logic ---
def scan_port(target, port, table):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        result = s.connect_ex((target, port))
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            
            # Table mein data insert karna
            table.insert("", "end", values=(port, "OPEN ✅", service.upper()))
        s.close()
    except:
        pass

def start_scanning():
    target = ip_entry.get().strip()
    
    if not target:
        messagebox.showwarning("Input Error", "Please enter an IP address or Domain!")
        return

    # Pichla data clear karna (Refresh Logic)
    for i in results_table.get_children():
        results_table.delete(i)
    
    status_label.config(text=f"Scanning {target}... Please wait", fg="#E67E22")
    
    def run_threads():
        threads = []
        # Ports 1 se 1000 tak scan honge
        for port in range(1, 1001):
            t = threading.Thread(target=scan_port, args=(target, port, results_table))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        
        status_label.config(text="Scan Completed Successfully!", fg="#27AE60")

    threading.Thread(target=run_threads).start()

def clear_all():
    ip_entry.delete(0, tk.END)
    for i in results_table.get_children():
        results_table.delete(i)
    status_label.config(text="Ready to Scan", fg="black")

# --- Dashboard Design (GUI) ---
root = tk.Tk()
root.title("Advanced Network Port Scanner")
root.geometry("700x550")
root.configure(bg="#F4F6F7")

# Header
header = tk.Label(root, text="PORT SCANNER DASHBOARD", font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="white", pady=15)
header.pack(fill="x")

# Input Area
input_frame = tk.Frame(root, bg="#F4F6F7", pady=20)
input_frame.pack()

tk.Label(input_frame, text="Target IP / Domain:", font=("Arial", 11), bg="#F4F6F7").grid(row=0, column=0, padx=5)
ip_entry = tk.Entry(input_frame, width=30, font=("Arial", 11), bd=2)
ip_entry.grid(row=0, column=1, padx=10)

# Buttons
scan_btn = tk.Button(input_frame, text="START SCAN", command=start_scanning, bg="#2980B9", fg="white", font=("Arial", 10, "bold"), padx=15)
scan_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(input_frame, text="CLEAR", command=clear_all, bg="#95A5A6", fg="white", font=("Arial", 10, "bold"), padx=15)
clear_btn.grid(row=0, column=3, padx=5)

# Status
status_label = tk.Label(root, text="Ready to Scan", font=("Arial", 10, "italic"), bg="#F4F6F7")
status_label.pack()

# Results Table
columns = ("Port", "Status", "Service")
results_table = ttk.Treeview(root, columns=columns, show="headings")

results_table.heading("Port", text="PORT NUMBER")
results_table.heading("Status", text="STATUS")
results_table.heading("Service", text="SERVICE NAME")

results_table.column("Port", anchor="center", width=150)
results_table.column("Status", anchor="center", width=150)
results_table.column("Service", anchor="center", width=250)

results_table.pack(pady=20, padx=30, fill="both", expand=True)

# Footer
footer = tk.Label(root, text="Semester Project - Network Security Tool", font=("Arial", 9), bg="#F4F6F7", fg="#7F8C8D")
footer.pack(side="bottom", pady=5)

root.mainloop()