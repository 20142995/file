from github import Github
import os
import json

data = {}
# 读取历史记录
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pentest_git.json')
if os.path.exists(data_file):
    try:
        data = json.loads(open(data_file,'r',encoding='utf8').read())
    except:
        with open(data_file, 'w',encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False,indent = 4)
else:
    with open(data_file, 'w',encoding='utf-8') as f:
        json.dump(data, f,ensure_ascii=False,indent = 4)
# 初始化
token = os.environ.get('GITHUB_TOKEN')

g = Github(token)
repo = g.get_repo('20142995/file')
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
            try:
                release = repo.get_release(file)
                print(f'[*] tag {file} 已存在')
                try:
                    for asset in release.get_assets():
                        data[file] = asset.browser_download_url
                except:
                    pass
            except:
                
                try:
                    release = repo.create_git_release(tag=file,name=file,message=file)
                    print(f'[*] 新建 tag {file}')
                    asset = release.upload_asset(file_path, label=file)
                    print(f'[*] 上传 {file}')
                    data[file] = asset.browser_download_url
                except:
                    pass
        else:
            print(file_path)

# 写入历史
with open(data_file, 'w',encoding='utf-8') as f:
    json.dump(data, f,ensure_ascii=False,indent = 4)
