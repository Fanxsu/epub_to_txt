# epub_to_txt
This is a simple tool that converts an EPUB file to a TXT file.
几点说明：
1. 使用时需要创建两个文件夹：
第一个文件夹(文件夹1)里放原始的epub文件(最好把这个文件改成英文名字), 第二个文件夹(文件夹2)是空的，用来放中间过程文件以及最后生成的txt文件。
2. 双击exe文件运行。
第一步输入epub文件的路径，这个路径是含刚才建立的“文件夹1”+文件名.epub 的完整路径；
第二步，输入输出目录，这个目录是文件夹2，这个文件夹应该是空的，用于放中间过程文件及最后产生的txt文件。
3. 最后产生的txt文件，文件名是 "output.txt"
4. 不同原始epub文件转成的txt ，因为原始格式的差异，转出txt 细节格式会有变化。
5. 如果要改变输出txt格式，更改extract_html_content(html_files, chapters)模块。
6. epub原始文件中的图片及超链接等，没有保留。
