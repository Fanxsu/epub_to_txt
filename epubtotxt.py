# coding:utf-8
# Editor : Ellen Fan
# 2024/12/4 6:10


from ebooklib import epub
from bs4 import BeautifulSoup
import zipfile
import os


 # 第一步，解压epub文件

def set_file():
    while True:
        epub_path = input("请输入epub文件的路径： ")
        if os.path.exists(epub_path):
            break
        print("文件不存在，请重新输入。")

    while True:
        output_dir = input("请输入输出目录： ")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        break
    return epub_path, output_dir


def extract_epub(epub_path, output_dir):
    # 检查文件是否为ZIP格式
    if not zipfile.is_zipfile(epub_path):
        print(f"{epub_path} 不是一个有效的epub文件！")
        return

    # 解压epub文件到指定目录
    with zipfile.ZipFile(epub_path, 'r') as epub_zip:
        epub_zip.extractall(output_dir)
        print(f"epub文件已解压到: {output_dir}")



# 第二步 提取文本文件内容及目录
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def get_toc_structure(output_dir):
    """从 toc.ncx 或 nav.xhtml 中获取目录结构"""
    toc_file = None
    # 查找目录文件
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file == 'toc.ncx' or file == 'nav.xhtml':
                toc_file = os.path.join(root, file)
                break
        if toc_file:
            break
    
    if not toc_file:
        return None
    
    # 解析目录文件获取章节结构
    chapters = {}
    if toc_file.endswith('.ncx'):
        # 处理 NCX 格式目录
        tree = ET.parse(toc_file)
        root = tree.getroot()
        for navPoint in root.findall('.//{http://www.daisy.org/z3986/2005/ncx/}navPoint'):
            title = navPoint.find('.//{http://www.daisy.org/z3986/2005/ncx/}text').text
            content = navPoint.find('.//{http://www.daisy.org/z3986/2005/ncx/}content').get('src')
            chapters[content] = {'title': title, 'level': len(navPoint.findall('./'))}
    
    return chapters

def find_html_files(output_dir):
    """查找所有 HTML 文件并按目录结构排序"""
    html_files = []
    chapters = get_toc_structure(output_dir)
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.html') or file.endswith('.xhtml'):
                full_path = os.path.join(root, file)
                html_files.append(full_path)
    
    # 如果有目录结构，按目录顺序排序
    if chapters:
        html_files.sort(key=lambda x: list(chapters.keys()).index(os.path.basename(x)) 
                       if os.path.basename(x) in chapters else float('inf'))
    
    return html_files, chapters


def extract_html_content(html_files, chapters):
    """提取 HTML 内容并保持章节格式"""
    content = []
    book_title_added = False    # 用于标记书名是否已添加

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            chapter_name = os.path.basename(html_file)

            # 提取并清理文本内容
            text = soup.get_text().strip()  #去除首尾空白

            # 只在第一个文件添加书名
            if not book_title_added and text:
                content.append(text.split('\n')[0]) #添加第一行作为书名
                content.append('\n\n')            # 书名后添加空行
                book_title_added = True
            
            # 添加章节标题（如果存在）
            if chapters and chapter_name in chapters:
                level = chapters[chapter_name]['level']
                title = chapters[chapter_name]['title']
                # 添加明显的分隔
                content.append('    ' * level + f'**{title}**')
                content.append('\n\n')  #章节标题后添加空行
            
            # 提取并清理文本内容(跳过第一行，因为通常是重复的书名)
            if text:
                chapter_content = '\n'.join(text.split('\n')[1:])   #跳过第一行
                if chapter_content.strip(): #确保还有内容
                    content.append(chapter_content)
                    content.append('\n\n')  #章节内容后添加空行
  
    return content

if __name__ == "__main__":
    import sys

    # 使用set_file()获取路径
    if len(sys.argv) != 3:
        epub_path, output_dir = set_file()
    else:  
        epub_path = sys.argv[1]
        output_dir = sys.argv[2]   
    print(f"开始处理epub文件: {epub_path}") 

    # 解压epub文件
    try:
        extract_epub(epub_path, output_dir)
    except Exception as e:
        print(f"解压epub文件时出错: {str(e)}")
        sys.exit(1)

    # 查找HTML文件
    print(f"开始查找HTML文件...")
    try:
        html_files, chapters = find_html_files(output_dir)
        if not html_files:
            print("未找到HTML文件！")
            sys.exit(1)
        
        print(f"找到{len(html_files)} 个HTML文件")
        content = extract_html_content(html_files, chapters)

        output_file = os.path.join(output_dir, 'output.txt')
        print(f"正在保存到文件: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"文本已提取并保存到 {output_file}")

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        sys.exit(1)