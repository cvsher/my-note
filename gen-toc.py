'''在README文件中生成目录，解析当前项目的目录结构
 生成  "* [常用单行命令.md](note/shell/常用单行命令.md)" 对应的链接文本
'''
import os

def gen_toc(f, index):
    '''根据文件目录结构，生成目录md格式字符串'''

    global toc_md_content
    if os.path.isdir(f):
        toc_md_content += ("  "*index + ("* [{0}]({1})".format(f.split("/")[-1], f.replace(base_dir, "")[1:])) + "\n")
        for cf in os.listdir(f):
            gen_toc(f+"/"+cf, index+1)
    elif os.path.isfile(f):
        toc_md_content += ("  "*index + ("* [{0}]({1})".format(f.split("/")[-1], f.replace(base_dir, "")[1:])) + "\n")

toc_str = "[TOC]"

global base_dir 
base_dir = os.getcwd()
toc_md_content = ""
gen_toc(base_dir+"/note", 0)
print(toc_md_content)
readme_file = open("README.md", "r+", encoding="utf-8")
readme_content = readme_file.read()
readme_content = readme_content.replace(toc_str, toc_md_content)
readme_file.seek(0)
readme_file.write(readme_content)
