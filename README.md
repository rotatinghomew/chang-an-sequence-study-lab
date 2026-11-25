# 讲演课程的顺序试验与跨校推广

本项目收录跨校讲演课程教务联报。资料按业务交换来源保存在 `data/`。所有记录均为合成数据。字段、口径来源和单位见[资料协议](资料协议.md)。

运行环境采用 Python 3.11。
按需先执行 `python3 -m pip install -r requirements.txt` 安装固定版本的数值依赖。

可使用以下命令核对一批交换文件的标识和各表记录数。

```sh
python3 catalog.py data
```

交换资料的测试覆盖标识、关键引用和依赖版本。执行测试时可直接使用随库资料。

```sh
python3 -m unittest discover -s tests -v
```
