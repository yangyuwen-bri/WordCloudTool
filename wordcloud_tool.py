import os
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tkinter import Tk, Label, filedialog, messagebox, Frame, IntVar, Canvas, Toplevel
from tkinter.ttk import Progressbar
import random

# 忽略 Tkinter 警告
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# --- 全局变量初始化 ---
input_path = ""
output_path = ""
stopwords_file = None

# --- "咩咩仓库" 品牌设计语言 ---
COLORS = {
    "bg": "#f8fafc",
    "card": "#ffffff",
    "text_primary": "#1f2937",
    "text_secondary": "#6b7280",
    "text_status": "#9ca3af",
    "accent_light": "#2dd4bf", 
    "accent": "#14b8a6",       
    "accent_hover": "#0f766e", 
    "success": "#22c55e",
    "white": "#ffffff"
}

# ###############################################################
#                                                               #
#           核心功能函数                                          #
#                                                               #
# ###############################################################
def load_stopwords(file_path=None):
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    return set(['的', '了', '和', '是', '就', '都', '而', '及', '与', '着', '或', '一个', '没有', '我们', '你们', '他们', '有', '在', '也', '这', '那', '这个', '那个', '不', '很', '这样', '那样', '到', '等', '把', '吗', '啊', '呢', '哦', '吧', '啦', '嗯'])

def generate_files(progress_var, progress_label, popup):
    """实际执行文件生成，并更新UI"""
    stopwords = load_stopwords(stopwords_file)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # --- 字体路径处理 (跨平台兼容) ---
    font_file_name = 'SimHei.ttf'
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, font_file_name)
    except NameError:
        font_path = font_file_name
    
    if not os.path.exists(font_path):
        popup.destroy()
        messagebox.showerror("字体错误", f"关键字体文件 '{font_file_name}' 未找到！\n请确保它和程序在同一个文件夹下。")
        return
    # --- 字体处理结束 ---

    xlsx_files = [f for f in os.listdir(input_path) if f.endswith('.xlsx')]
    if not xlsx_files:
        popup.destroy()
        messagebox.showwarning("警告", "输入文件夹中没有找到任何 Excel 文件！")
        return

    total_files = len(xlsx_files)
    progress_var.set(0)
    
    for i, xlsx_file in enumerate(xlsx_files):
        progress_label.config(text=f"正在处理: {xlsx_file} ({i+1}/{total_files})")
        
        file_path = os.path.join(input_path, xlsx_file)
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            text = ' '.join(df['content'].astype(str).values)
            words = [word for word in jieba.cut(text) if word.strip() and word not in stopwords]
            filtered_text = ' '.join(words)

            wc = WordCloud(
                font_path=font_path, width=800, height=400,
                background_color='white', max_words=100
            ).generate(filtered_text)

            freq_df = pd.DataFrame({'词语': list(wc.words_.keys()), '频次': list(wc.words_.values())})
            freq_output_file = os.path.join(output_path, f"{os.path.splitext(xlsx_file)[0]}_词频统计.xlsx")
            freq_df.to_excel(freq_output_file, index=False)
            
            wordcloud_output_file = os.path.join(output_path, f"{os.path.splitext(xlsx_file)[0]}.png")
            wc.to_file(wordcloud_output_file)

        except Exception as e:
            messagebox.showerror("错误", f"处理文件 {xlsx_file} 时出错: {e}")
        
        progress_var.set(i + 1)
        popup.update_idletasks()

    popup.destroy()
    messagebox.showinfo("完成", f"词云已生成，保存在：{output_path}")

# ###############################################################
#                                                               #
#                UI界面构建                                       #
#                                                               #
# ###############################################################
def select_input_folder():
    global input_path; path = filedialog.askdirectory();
    if path: input_path = path; status_labels['input'].config(text=f"✅ {os.path.basename(path)}", fg=COLORS['success'])

def select_output_folder():
    global output_path; path = filedialog.askdirectory();
    if path: output_path = path; status_labels['output'].config(text=f"✅ {os.path.basename(path)}", fg=COLORS['success'])

def select_stopwords_file():
    global stopwords_file; path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")]);
    if path: stopwords_file = path; status_labels['stopwords'].config(text=f"✅ {os.path.basename(path)}", fg=COLORS['success'])

def start_processing():
    if not input_path or not output_path:
        messagebox.showerror("错误", "请选择输入和输出文件夹！")
        return
    
    popup = Toplevel(root)
    popup.geometry("400x120")
    popup.resizable(False, False)
    popup.title("正在处理")
    popup.config(bg=COLORS['card'])
    
    x = root.winfo_x() + (root.winfo_width() // 2) - 200
    y = root.winfo_y() + (root.winfo_height() // 2) - 60
    popup.geometry(f'+{x}+{y}')

    popup.grab_set()
    
    def on_close():
        popup.grab_release()
        popup.destroy()
    popup.protocol("WM_DELETE_WINDOW", on_close)

    progress_label = Label(popup, text="准备开始...", font=("Microsoft YaHei", 10), bg=COLORS['card'], fg=COLORS['text_primary'])
    progress_label.pack(pady=(20, 5))
    
    progress_var = IntVar()
    progress_bar = Progressbar(popup, length=350, mode="determinate", variable=progress_var)
    progress_bar.pack(pady=5)
    
    popup.update()
    generate_files(progress_var, progress_label, popup)
    
class Particle:
    def __init__(self, canvas, width, height):
        self.canvas, self.x, self.y = canvas, random.uniform(0, width), random.uniform(0, height)
        self.vx, self.vy = random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)
        self.radius = random.uniform(1, 3)
        self.color = random.choice(["#5eead4", "#2dd4bf", "#14b8a6", "#a7f3d0"])
        self.id = self.canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color, outline="")
    def move(self, width, height):
        self.x += self.vx; self.y += self.vy
        if not (self.radius < self.x < width - self.radius): self.vx *= -1
        if not (self.radius < self.y < height - self.radius): self.vy *= -1
        self.canvas.coords(self.id, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
particles, all_buttons = [], []

def update_particles():
    for p in particles: p.move(header_canvas.winfo_width(), header_canvas.winfo_height())
    root.after(20, update_particles)

def create_gradient(canvas, w, h, c1, c2):
    r1,g1,b1 = canvas.winfo_rgb(c1); r2,g2,b2 = canvas.winfo_rgb(c2)
    for i in range(w):
        nr,ng,nb = r1+(r2-r1)*i//w, g1+(g2-g1)*i//w, b1+(b2-b1)*i//w
        canvas.create_line(i,0,i,h, fill=f'#{nr:04x}{ng:04x}{nb:04x}', tags="gradient")

def create_hover_button(parent, text, command, width=None):
    btn = Label(parent, text=text, font=("Microsoft YaHei",10,"bold"), fg=COLORS['white'], bg=COLORS['accent'], cursor="hand2", pady=8, padx=20, width=width)
    btn.command = lambda e: command(); btn.bind("<Button-1>", btn.command)
    btn.bind("<Enter>", lambda e: e.widget.config(bg=COLORS['accent_hover'])); btn.bind("<Leave>", lambda e: e.widget.config(bg=COLORS['accent']))
    all_buttons.append(btn); return btn

root = Tk(); root.title("咩咩仓库 - 词云球"); root.geometry("600x550"); root.resizable(False, False); root.configure(bg=COLORS['bg'])
header_canvas = Canvas(root, height=120, highlightthickness=0); header_canvas.pack(fill="x")

def on_resize_and_init(e):
    w,h = e.width, e.height; header_canvas.delete("all"); create_gradient(header_canvas, w, h, COLORS['accent_light'], COLORS['accent'])
    if not particles:
        for _ in range(50): particles.append(Particle(header_canvas, w, h))
    new_title = "咩～词云球"
    header_canvas.create_text(w/2, 65, text=new_title, font=("Microsoft YaHei",28,"bold"), fill=COLORS['white'], anchor="center", tags="text")
header_canvas.bind("<Configure>", on_resize_and_init)

main_frame = Frame(root, bg=COLORS['bg']); main_frame.place(x=30, y=105, width=540, height=430)
card_frame = Frame(main_frame, bg=COLORS['card'], bd=0, highlightbackground="#e2e8f0", highlightthickness=1); card_frame.pack(fill="both", expand=True)
card_content = Frame(card_frame, bg=COLORS['card'], padx=30, pady=25); card_content.pack(fill="both", expand=True)

section_title = Label(card_content, text="⚙️ 基础配置", font=("Microsoft YaHei",18,"bold"), fg=COLORS['text_primary'], bg=COLORS['card']); section_title.pack(anchor="w", pady=(0, 20))
status_labels = {}

def create_function_row(parent, icon, title, initial_text, command, selection_key):
    row = Frame(parent, bg=COLORS['card']); row.pack(fill="x", pady=12)
    Label(row, text=icon, font=("Microsoft YaHei",22), fg=COLORS['accent'], bg=COLORS['card'], width=3).pack(side="left", padx=(0,10))
    tf = Frame(row, bg=COLORS['card']); tf.pack(side="left", fill="x", expand=True)
    Label(tf, text=title, font=("Microsoft YaHei",12,"bold"), fg=COLORS['text_primary'], bg=COLORS['card']).pack(anchor="w")
    sl = Label(tf, text=initial_text, font=("Microsoft YaHei",9), fg=COLORS['text_status'], bg=COLORS['card']); sl.pack(anchor="w")
    status_labels[selection_key] = sl; create_hover_button(row, "选择", command).pack(side="right")

create_function_row(card_content, "📁", "输入文件夹", "从本地选择...", select_input_folder, 'input')
create_function_row(card_content, "💾", "输出位置", "选择保存位置...", select_output_folder, 'output')
create_function_row(card_content, "🚫", "停用词文件", "可选，自定义词库...", select_stopwords_file, 'stopwords')

sbf = Frame(card_content, bg=COLORS['card']); sbf.pack(fill="x", pady=(25,0))
sb = create_hover_button(sbf, "🚀 开始生成", start_processing); sb.config(font=("Microsoft YaHei",14,"bold"), pady=12); sb.pack(fill="x")

footer_area = Frame(card_frame, bg=COLORS['card']); footer_area.pack(side="bottom", fill="x", padx=30, pady=(15,10))
separator = Frame(footer_area, height=1, bg="#e5e7eb"); separator.pack(fill="x", pady=(0,10))
Label(footer_area, text="✨ Designed by阿羊@咩咩仓库", font=("Microsoft YaHei",9), fg=COLORS['text_secondary'], bg=COLORS['card']).pack()

update_particles()
root.mainloop()