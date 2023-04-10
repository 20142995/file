from lanzou.api import LanZouCloud
import os
import json
lzy = LanZouCloud()
cookie = {}
if lzy.login_by_cookie(cookie) == LanZouCloud.SUCCESS:
    print('登录 ok')
data = {}
# 读取历史记录
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pentest_lzy.json')
if os.path.exists(data_file):
    try:
        data = json.loads(open(data_file,'r',encoding='utf8').read())
    except:
        with open(data_file, 'w',encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False,indent = 4)
else:
    with open(data_file, 'w',encoding='utf-8') as f:
        json.dump(data, f,ensure_ascii=False,indent = 4)

def show_progress(file_name, total_size, now_size):
    """显示进度的回调函数"""
    global file_name1,share_url1 
    file_name1 = file_name
    percent = now_size / total_size
    bar_len = 40  # 进度条长总度
    bar_str = '>' * round(bar_len * percent) + '=' * round(bar_len * (1 - percent))
    print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB | {} '.format(
        percent * 100, bar_str, now_size / 1048576, total_size / 1048576, file_name), end='')
    if total_size == now_size:
        print('')  # 下载完成换行

def handler(fid, is_file):
    global file_name1,share_url1 
    if is_file:
        # lzy.set_desc(fid, '这是文件的描述', is_file=True)
        info = lzy.get_share_info(fid)
        share_url1 = info.url

global file_name1,share_url1 
file_name1,share_url1  ='',''

base_path = r'.'
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file in data:
            continue
        file_path = os.path.join(root,file)
        file_size = os.path.getsize(file_path)
        
        # 将文件大小转换为MB
        file_size_mb = file_size / (1024 * 1024)
        
        # 判断文件大小是否小于100MB
        if file_size_mb < 100:
            code = lzy.upload_file(file_path, -1, callback=show_progress, uploaded_handler=handler)
            if code == LanZouCloud.SUCCESS:
                data[file_name1] = share_url1
                print(file_name1,share_url1)
# 写入历史
with open(data_file, 'w',encoding='utf-8') as f:
    json.dump(data, f,ensure_ascii=False,indent = 4)