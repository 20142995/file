from github import Github
import os

# 1. 获取GitHub API令牌
token = os.environ.get('GITHUB_TOKEN')
g = Github(token)

# 2. 找到你要上传文件的发布
repo = g.get_repo('1')
release = repo.create_git_release(
    tag='1',
    name='1',
    message='1'
)
# repo.create_git_tag('1')
# release = repo.get_release('1')

# 3. 上传文件
file_path = r'1'
file_name = '1'
asset = release.upload_asset(file_path, label=file_name)

# 4. 打印已上传文件的URL
print(asset.browser_download_url)
