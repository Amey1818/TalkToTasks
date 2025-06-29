import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from nltk.tokenize import sent_tokenize
from src.summarize import summarize_text
from src.extract_actions import extract_action_items
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
import csv
from fpdf import FPDF
import nltk
nltk.data.path.append(r"C:\\Users\\Amey\\AppData\\Roaming\\nltk_data")

# Initialize main window
root = tk.Tk()
root.title("TalkToTasks – Smart Meeting Summarizer")
root.geometry("1024x750")
root.configure(bg="#e6f7ff")  # Updated from white to blue tint

# Global variable
latest_actions = []
is_dark = False

# GUI widgets (defined before usage)
title = tk.Label(root, text="TalkToTasks", font=("Segoe UI", 20, "bold"), bg="#e6f7ff", fg="#003366")
title.pack(pady=10)

upload_btn = tk.Button(root, text="\U0001F4C2 Upload Transcript", bg="#007acc", fg="white", font=("Segoe UI", 10, "bold"))
upload_btn.pack()

text_area_label = tk.Label(root, text="Transcript Preview", font=("Segoe UI", 12, "bold"), bg="#e6f7ff", fg="#003366")
text_area_label.pack(pady=(15, 0))

text_area = scrolledtext.ScrolledText(root, height=8, wrap=tk.WORD, font=("Segoe UI", 10), bg="#f0fbff")
text_area.pack(fill=tk.X, padx=20)

summary_label = tk.Label(root, text="Auto-Generated Summary", font=("Segoe UI", 12, "bold"), bg="#e6f7ff", fg="#003366")
summary_label.pack(pady=(15, 0))

summary_area = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD, font=("Segoe UI", 10), bg="#f0fbff")
summary_area.pack(fill=tk.X, padx=20)

action_label = tk.Label(root, text="Action Items", font=("Segoe UI", 12, "bold"), bg="#e6f7ff", fg="#003366")
action_label.pack(pady=(15, 0))

filter_frame = tk.Frame(root, bg="#e6f7ff")
filter_frame.pack(pady=5)
tk.Label(filter_frame, text="\U0001F50D Filter by keyword:", bg="#e6f7ff", fg="#003366").pack(side=tk.LEFT, padx=5)
keyword_entry = tk.Entry(filter_frame)
keyword_entry.pack(side=tk.LEFT, padx=5)

parent_frame = tk.Frame(root)
parent_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
action_tree = ttk.Treeview(parent_frame, columns=("Type", "Action"), show='headings', height=8)
action_tree.heading("Type", text="Type")
action_tree.heading("Action", text="Action")
action_tree.column("Type", width=100, anchor="center")
action_tree.column("Action", width=800, anchor="w")
action_tree.pack(fill=tk.BOTH, expand=True)

# Functional logic
def update_action_table(data):
    for row in action_tree.get_children():
        action_tree.delete(row)
    for item in data:
        action_tree.insert("", "end", values=(item['type'].title(), item['action'][:100]))

def draw_freq_chart(text):
    words = [w.lower() for w in text.split() if w.isalpha()]
    counter = Counter(words)
    top_words = counter.most_common(10)
    if not top_words:
        return
    labels, values = zip(*top_words)
    fig = plt.Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(labels, values, color='#3399ff')
    ax.set_title("Top 10 Frequent Words")
    ax.tick_params(axis='x', labelrotation=45)
    chart_window = tk.Toplevel(root)
    chart_window.title("Word Frequency Chart")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def export_to_csv():
    if not latest_actions:
        messagebox.showinfo("No Actions", "No action items to export.")
        return
    export_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not export_path:
        return
    with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["type", "action"])
        writer.writeheader()
        writer.writerows(latest_actions)
    messagebox.showinfo("Exported", f"Action items exported to:\n{export_path}")

def export_summary_to_pdf():
    summary_text = summary_area.get("1.0", tk.END).strip()
    if not summary_text:
        messagebox.showinfo("No Summary", "No summary to export.")
        return
    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary_text)
    pdf.output(pdf_path)
    messagebox.showinfo("Exported", f"Summary exported to:\n{pdf_path}")

def filter_keywords():
    keyword = keyword_entry.get().strip().lower()
    if not keyword:
        update_action_table(latest_actions)
        return
    filtered = [item for item in latest_actions if keyword and keyword in item['action'].lower()]
    update_action_table(filtered)

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    theme = "#1e1e1e" if is_dark else "#e6f7ff"
    fg = "#f5f5f5" if is_dark else "#003366"
    text_bg = "#2b2b2b" if is_dark else "#f0fbff"
    root.config(bg=theme)
    for widget in [title, upload_btn, text_area_label, summary_label, action_label, filter_frame]:
        widget.config(bg=theme, fg=fg)
    text_area.config(bg=text_bg, fg=fg, insertbackground=fg)
    summary_area.config(bg=text_bg, fg=fg, insertbackground=fg)
    parent_frame.config(bg=theme)

def browse_transcript():
    global latest_actions
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return
    with open(filepath, "r", encoding="utf-8") as f:
        transcript = f.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, transcript)

    # Summary
    summary_area.delete(1.0, tk.END)
    try:
        summary = summarize_text(transcript, method='extractive')
        if not summary or not isinstance(summary, list):
            summary = sent_tokenize(transcript.strip())[:5]
        formatted = "\n\n".join(f"• {s.strip()}" for s in summary if s.strip())
        summary_area.insert(tk.END, formatted if formatted else "No summary generated.")
    except Exception as e:
        summary_area.insert(tk.END, f"[Error generating summary]\n{e}")

    # Actions
    latest_actions = extract_action_items(transcript)
    update_action_table(latest_actions)
    draw_freq_chart(transcript)

# Button actions
tk.Button(filter_frame, text="Filter", command=filter_keywords, bg="#007acc", fg="white").pack(side=tk.LEFT)
tk.Button(root, text="\u2B73 Export Actions to CSV", command=export_to_csv, bg="#007acc", fg="white").pack(pady=5)
tk.Button(root, text="\U0001F4C4 Export Summary to PDF", command=export_summary_to_pdf, bg="#007acc", fg="white").pack(pady=5)
tk.Button(root, text="\U0001F319 Toggle Dark Mode", command=toggle_theme, bg="#007acc", fg="white").pack(pady=5)

# Connect upload button to function
upload_btn.config(command=browse_transcript)

root.mainloop()
