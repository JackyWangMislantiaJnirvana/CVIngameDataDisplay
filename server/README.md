### 在自己的服务器部署 / 参与开发

安装要求：

- Python 3.6.5+
- virtualenv

```bash
cd /var/www/
git clone https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay.git
cd CVIngameDataDisplay
git checkout server
vi server/config.py # 更改 SECRET_KEY 和 SALT
cd server
# 建立virtualenv并激活
virtualenv -p python3 venv
. venv/bin/activate
# 安装依赖
pip install -r requirements.txt
nohup gunicorn -w 4 main:app &
# 后续操作，如设置 Nginx 转发、supervisor等省略
```

若需改变语言，参考 main.py 第 10-11 行。（一个语言对应一个模板目录）

### 开发注意事项

- `server`  为包名称，不要改变
- 文档注意事项：
  1. 文档需要先用 Typora 写成 Markdown 存储在 `模板目录/docs/markdown` 下，并且使用 Typora 的导出 HTML 导出到 `模板目录/docs/`
  2. 运行 `tools/html_doc_transformer.py 模板HTML`，以调整模板格式，适应 CVDD 排版