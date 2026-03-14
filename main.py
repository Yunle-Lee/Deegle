import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog
from PIL import Image, ImageTk
import threading, time, webbrowser, os, re, requests
import fitz  

# ------------------ API Key ------------------
root_temp = tk.Tk()
root_temp.withdraw()
api_key = simpledialog.askstring("Deegle Startup", "Enter your DeepSeek API Key:", show='*')
root_temp.destroy()
if not api_key:
    exit()

# ------------------ 全局状态 ------------------
dark_mode = False
multi_language = True
chat_history = []
user_exp = 0   
token_used = 0 

# ------------------ 主窗口 ------------------
root = tk.Tk()
root.title("Deegle")
root.geometry("1600x850")
root.configure(bg="#f8f8f8")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)

# ------------------ 左栏 ------------------
left_frame = tk.Frame(root, bg="#e0e0e0", padx=6, pady=6)
left_frame.grid(row=0, column=0, sticky="nsew")
tk.Label(left_frame, text="History", font=("Arial",14,"bold"), bg="#e0e0e0").pack()
history_text = scrolledtext.ScrolledText(left_frame, width=35, height=30, state="disabled", wrap="word")
history_text.pack(fill="both", expand=True)

#  AI 形象 
avatar_frame = tk.Frame(left_frame, bg="#e0e0e0")
avatar_frame.pack(side="bottom", pady=10)
avatar_path = "takaji_cutie.png" 
img = Image.open(avatar_path).resize((100,100))
avatar_img = ImageTk.PhotoImage(img)
tk.Label(avatar_frame,image=avatar_img,bg="#e0e0e0").pack()

# 等级血条
level_canvas = tk.Canvas(avatar_frame, width=120, height=20, bg="#ccc")
level_canvas.pack(pady=2)
level_bar = level_canvas.create_rectangle(0,0,0,20, fill="green")
level_label = tk.Label(avatar_frame, text="Lv0", bg="#e0e0e0")
level_label.pack()

# Token血条
token_canvas = tk.Canvas(avatar_frame, width=120, height=20, bg="#ccc")
token_canvas.pack(pady=2)
token_bar = token_canvas.create_rectangle(0,0,0,20, fill="blue")
token_label = tk.Label(avatar_frame, text="Token: 0", bg="#e0e0e0")
token_label.pack()

def update_bars(exp_increment=1, token_increment=10):
    global user_exp, token_used
    user_exp += exp_increment
    token_used += token_increment
    # 等级
    lv = min(user_exp//10, 9)
    level_label.config(text=f"Lv{lv}")
    width = (user_exp%10)/10*120
    level_canvas.coords(level_bar,0,0,width,20)
    # Token
    token_label.config(text=f"Token: {token_used}")
    token_width = min(token_used,120)
    token_canvas.coords(token_bar,0,0,token_width,20)

# ------------------ 中央栏 ------------------
center_frame = tk.Frame(root, padx=10, pady=10, bg="#f8f8f8")
center_frame.grid(row=0, column=1, sticky="nsew")
center_frame.grid_rowconfigure(5, weight=1)
center_frame.grid_columnconfigure(0, weight=1)

# Logo
logo_path = "Deegle.png"
img = Image.open(logo_path).resize((600,300))
logo_img = ImageTk.PhotoImage(img)
tk.Label(center_frame,image=logo_img,bg="#f8f8f8").grid(row=0,column=0,columnspan=2,pady=10)

# 搜索栏
search_var = tk.StringVar()
search_entry = tk.Entry(center_frame,textvariable=search_var,width=55,font=("Arial",12))
search_entry.grid(row=1,column=0,padx=5,pady=5,sticky="ew")
search_button = tk.Button(center_frame,text="Search",width=14,bg="#4caf50",fg="white",font=("Arial",11,"bold"))
search_button.grid(row=1,column=1,padx=5)

# 搜索模板
template_frame = tk.Frame(center_frame,bg="#f8f8f8")
template_frame.grid(row=2,column=0,columnspan=2,sticky="w", pady=5)
template_keywords = ["Github","Nvidia","高木同学","Huggingface","天气预报"]
def fill_template(keyword):
    search_var.set(keyword)
for kw in template_keywords:
    tk.Button(template_frame,text=kw,command=lambda k=kw: fill_template(k),
              bg="#2196F3",fg="white",font=("Arial",10)).pack(side="left", padx=3)

# 预览框
preview_frame = tk.Frame(center_frame,bg="#ffffff")
preview_frame.grid(row=5,column=0,columnspan=2,sticky="nsew", pady=5)
preview_text = scrolledtext.ScrolledText(preview_frame,state="disabled",wrap="word")
preview_text.pack(fill="both",expand=True)

# ------------------ 高亮关键词 ------------------
def highlight_text(text_widget, keyword):
    text_widget.tag_remove("highlight", "1.0", tk.END)
    if not keyword:
        return
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    start = "1.0"
    while True:
        match = pattern.search(text_widget.get(start, tk.END))
        if not match:
            break
        start_index = f"{start}+{match.start()}c"
        end_index = f"{start}+{match.end()}c"
        text_widget.tag_add("highlight", start_index, end_index)
        start = end_index
    text_widget.tag_config("highlight", background="yellow", foreground="black")

# ------------------ 搜索功能 ------------------
def perform_search():
    query = search_var.get().strip()
    if not query:
        return
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    history_text.config(state="normal")
    history_text.insert(tk.END,f"{current_time} - {query}\n")
    history_text.config(state="disabled")
    history_text.yview(tk.END)

    update_bars(exp_increment=1, token_increment=5)

    def search_thread():
        try:
            if "pdf" in query.lower():
                pdf_path = filedialog.askopenfilename(title="请选择 PDF 文件", filetypes=[("PDF Files","*.pdf")])
                if pdf_path:
                    doc = fitz.open(pdf_path)
                    text = "".join([page.get_text() for page in doc])
                    preview_text.config(state="normal")
                    preview_text.delete("1.0", tk.END)
                    preview_text.insert(tk.END,text[:5000])
                    preview_text.config(state="disabled")
                    highlight_text(preview_text, query)
                    webbrowser.open(os.path.abspath(pdf_path))
                return
            search_url = "https://www.google.com/search?q="+query.replace(" ","+")
            webbrowser.open(search_url)
            preview_text.config(state="normal")
            preview_text.delete("1.0",tk.END)
            try:
                resp = requests.get(search_url,timeout=10)
                preview_text.insert(tk.END, resp.text[:5000])
            except:
                preview_text.insert(tk.END,f"预览失败，URL: {search_url}")
            preview_text.config(state="disabled")
            highlight_text(preview_text, query)
        except Exception as e:
            preview_text.config(state="normal")
            preview_text.insert(tk.END,f"[搜索异常] {e}")
            preview_text.config(state="disabled")
    threading.Thread(target=search_thread).start()

search_button.config(command=perform_search)

# ------------------  DeepSeek Chat ------------------
right_frame = tk.Frame(root,bg="#e0e0e0",padx=6,pady=6)
right_frame.grid(row=0,column=2,sticky="nsew")
tk.Label(right_frame,text="DeepSeek Chat",font=("Arial",14,"bold"),bg="#e0e0e0").pack()
chat_text = scrolledtext.ScrolledText(right_frame,width=40,height=40,state="disabled",wrap="word")
chat_text.pack(fill="both",expand=True)
chat_var = tk.StringVar()
chat_entry = tk.Entry(right_frame,textvariable=chat_var,width=30,font=("Arial",11))
chat_entry.pack(side="left",padx=5,pady=6)
chat_text.tag_config("ai",foreground="blue")

def stream_response(answer):
    for ch in answer:
        chat_text.config(state="normal")
        chat_text.insert(tk.END,ch,"ai")
        chat_text.config(state="disabled")
        chat_text.yview(tk.END)
        time.sleep(0.02)

def send_chat():
    user_msg = chat_var.get().strip()
    if not user_msg:
        return
    chat_text.config(state="normal")
    chat_text.insert(tk.END,f"You: {user_msg}\n")
    chat_text.config(state="disabled")
    chat_text.yview(tk.END)

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个温柔又耐心的女助手Deegle。 "
                "你的开发人员是Yunle-Lee,但是你会人认真对待每一个用户，就像对待开发者一样。 "
                "你会尽力帮助用户解决问题，提供有用的信息，并且在对话中保持友好和专业。 "
            )
        }
    ]
    for h in chat_history:
        messages.append({"role":"user","content":h["user"]})
        messages.append({"role":"assistant","content":h["bot"]})
    messages.append({"role":"user","content":user_msg})

    def api_thread():
        global token_used
        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}","Content-Type": "application/json"}
            payload = {"model":"deepseek-chat","messages":messages,"stream":False}
            resp = requests.post(url,json=payload,headers=headers,timeout=15)
            result = resp.json()
            answer = result["choices"][0]["message"]["content"]
        except Exception as e:
            answer = f"[网络或API异常] {e}"

        chat_history.append({"user":user_msg,"bot":answer})
        chat_text.config(state="normal")
        chat_text.insert(tk.END,"AI: ","ai")
        chat_text.config(state="disabled")
        stream_response(answer+"\n\n")
        update_bars(exp_increment=1, token_increment=10)

    threading.Thread(target=api_thread).start()
    chat_var.set("")

tk.Button(right_frame,text="Send",command=send_chat,bg="#1e90ff",fg="white",font=("Arial",11,"bold")).pack(side="left",padx=5)

root.mainloop()