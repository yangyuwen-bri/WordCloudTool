import os
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame, IntVar
from tkinter.ttk import Progressbar, Separator

# 忽略 Tkinter 警告
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# 全局变量初始化
input_path = ""
output_path = ""
stopwords_file = None  # 初始化为 None

def load_stopwords(file_path=None):
    """加载停用词"""
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    # 返回默认停用词
    return set(['的', '了', '和', '是', '就', '都', '而', '及', '与', '着', '或', '一个',
                '没有', '我们', '你们', '他们', '有', '在', '也', '这', '那', '这个', 
                '那个', '不', '很', '这样', '那样', '到', '等', '把', '吗', '啊', 
                '呢', '哦', '吧', '啦', '嗯'])

def create_wordcloud(input_path, output_path, stopwords_path=None):
    """生成词云和词频统计"""
    stopwords = load_stopwords(stopwords_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    xlsx_files = [f for f in os.listdir(input_path) if f.endswith('.xlsx')]

    if not xlsx_files:
        messagebox.showwarning("警告", "输入文件夹中没有找到任何 Excel 文件！")
        return

    total_files = len(xlsx_files)
    progress_var.set(0)  # 重置进度条
    progress_bar["maximum"] = total_files

    for i, xlsx_file in enumerate(xlsx_files):
        file_path = os.path.join(input_path, xlsx_file)
        try:
            df = pd.read_excel(file_path, engine='openpyxl')  # 显式指定 openpyxl 引擎
            text = ' '.join(df['content'].astype(str).values)

            # 分词和过滤停用词
            words = [word for word in jieba.cut(text) if word.strip() and word not in stopwords]
            filtered_text = ' '.join(words)

            # 统计词频
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

            freq_df = pd.DataFrame({'词语': list(word_freq.keys()), '频次': list(word_freq.values())})
            freq_df = freq_df.sort_values(by='频次', ascending=False)

            # 保存词频统计表
            freq_output_file = os.path.join(output_path, f"{os.path.splitext(xlsx_file)[0]}_词频统计.xlsx")
            freq_df.to_excel(freq_output_file, index=False)

            # 生成词云
            wc = WordCloud(
                font_path='SimHei.ttf',
                width=800,
                height=400,
                background_color='white',
                max_words=100
            ).generate(filtered_text)

            wordcloud_output_file = os.path.join(output_path, f"{os.path.splitext(xlsx_file)[0]}.png")
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(wordcloud_output_file)
            plt.close()

        except Exception as e:
            messagebox.showerror("错误", f"处理文件 {xlsx_file} 时出错: {e}")

        # 更新进度条
        progress_var.set(i + 1)
        root.update_idletasks()

    messagebox.showinfo("完成", f"词云和词频统计已生成，结果保存在：{output_path}")


def select_input_folder():
    """选择输入文件夹"""
    global input_path
    input_path = filedialog.askdirectory(title="请选择输入文件夹")
    if input_path:
        input_label.config(text=f"输入文件夹：{input_path}")


def select_output_folder():
    """选择输出文件夹"""
    global output_path
    output_path = filedialog.askdirectory(title="请选择输出文件夹")
    if output_path:
        output_label.config(text=f"输出文件夹：{output_path}")


def select_stopwords_file():
    """选择停用词文件"""
    global stopwords_file
    stopwords_file = filedialog.askopenfilename(title="请选择停用词文件（可选）", filetypes=[("Text Files", "*.txt")])
    if stopwords_file:
        stopwords_label.config(text=f"停用词文件：{stopwords_file}")


def start_processing():
    """开始处理"""
    if not input_path or not output_path:
        messagebox.showerror("错误", "请输入正确的输入和输出路径！")
        return

    create_wordcloud(input_path, output_path, stopwords_file)


# 创建 Tkinter 窗口
root = Tk()
root.title("词云生成工具")
root.geometry("600x500")
root.iconbitmap("icon.ico")  # 添加窗口图标

# 应用标题
title_label = Label(root, text="词云生成工具", font=("Arial", 20, "bold"), fg="blue")
title_label.pack(pady=10)

# 使用说明
instruction_label = Label(
    root,
    text="选择输入文件夹、输出文件夹，以及停用词文件（可选），点击生成词云。",
    font=("Arial", 12),
    fg="gray"
)
instruction_label.pack(pady=5)

# 添加分隔线
Separator(root, orient="horizontal").pack(fill="x", pady=10)

# 主功能区域
frame = Frame(root)
frame.pack(pady=10)

input_label = Label(frame, text="未选择输入文件夹", font=("Arial", 10), fg="black")
input_label.grid(row=0, column=0, padx=5, pady=5)

input_button = Button(frame, text="选择输入文件夹", command=select_input_folder, bg="lightblue", width=20)
input_button.grid(row=0, column=1, padx=5, pady=5)

output_label = Label(frame, text="未选择输出文件夹", font=("Arial", 10), fg="black")
output_label.grid(row=1, column=0, padx=5, pady=5)

output_button = Button(frame, text="选择输出文件夹", command=select_output_folder, bg="lightblue", width=20)
output_button.grid(row=1, column=1, padx=5, pady=5)

stopwords_label = Label(frame, text="未选择停用词文件（可选）", font=("Arial", 10), fg="black")
stopwords_label.grid(row=2, column=0, padx=5, pady=5)

stopwords_button = Button(frame, text="选择停用词文件", command=select_stopwords_file, bg="lightblue", width=20)
stopwords_button.grid(row=2, column=1, padx=5, pady=5)

# 开始按钮
start_button = Button(root, text="生成词云", command=start_processing, bg="green", fg="red", font=("Arial", 12), width=20)
start_button.pack(pady=20)

# 进度条
progress_var = IntVar()
progress_bar = Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.pack(pady=20)

# 主循环
root.mainloop()
