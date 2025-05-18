import os
import sys
from bs4 import BeautifulSoup

def extract_title_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    h1 = soup.find('h1')
    if h1:
        return h1.get_text().strip()
    return None

def generate_html(template_path, content_path, output_path):
    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 读取内容
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 如果内容是完整的HTML文件，只提取article标签内的内容
        if '<article>' in content:
            start = content.index('<article>') + len('<article>')
            end = content.index('</article>')
            content = content[start:end].strip()
    
    # 从内容中提取标题
    title = extract_title_from_content(content)
    if not title:
        title = "Untitled"  # 如果没有找到标题，使用默认值
    
    # 替换模板中的标记
    html = template.replace('{{title}}', title).replace('{{content}}', content)
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def process_all_content():
    template_file = 'template.html'
    content_dir = 'content'
    
    if not os.path.exists(template_file):
        print(f"错误：模板文件 {template_file} 不存在")
        sys.exit(1)
    
    if not os.path.exists(content_dir):
        print(f"错误：content 目录不存在")
        sys.exit(1)
    
    # 遍历content目录下的所有html文件
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.html'):
                content_path = os.path.join(root, file)
                # 输出文件将直接放在主目录下
                output_path = os.path.join(os.path.dirname(content_dir), file)
                
                try:
                    generate_html(template_file, content_path, output_path)
                    print(f"成功生成文件：{output_path}")
                except Exception as e:
                    print(f"处理文件 {content_path} 时出错：{str(e)}")

if __name__ == '__main__':
    process_all_content()
