# 环境排错手册（阶段 1 实战踩坑记录）

> 每条格式：现象 → 原因 → 解决。命令均在 Windows PowerShell 5.1 下。

## 1. 装完 uv 后 `uv` 命令找不到
- 现象：`uv : 无法将"uv"项识别为 cmdlet...`
- 原因：winget 改了用户 PATH，但旧终端进程没刷新。
- 解决：**关掉整个终端（必要时重启 PyCharm）重开**，再 `uv --version`。

## 2. 本机有 4 个 python，到底用哪个
- 现象：`where.exe python` 列出 D:\program、anaconda、Python312、WindowsApps 四个。
- 原因：多个安装抢 PATH。
- 解决：不手动管理它们，一律用 `uv run`，让 uv 决定解释器（本项目锁定 3.11.9）。

## 3. `uv run` 报 `Failed to spawn: fastapi / program not found`
- 原因：当前目录不是项目根（外层没有 pyproject.toml）。
- 解决：先 `cd taskboard` 再运行。凡 uv 命令都在含 `pyproject.toml` 的目录执行。

## 4. `fastapi dev` 报 `Path does not exist src\taskboard\main.py`
- 原因：src 布局下代码必须放 `src/taskboard/` 包内，不能放项目根。
- 解决：把 `main.py` 移到 `src/taskboard/main.py`。

## 5. 项目根出现多余的 `__init__.py`
- 现象：GitHub 根目录多了 `__init__.py`。
- 原因：早期把脚本建在根目录残留。
- 解决：删除根目录 `__init__.py` 和 `__pycache__`；包内 `src/taskboard/__init__.py` 保留。

## 6. `git add.` 报 `'add.' is not a git command`
- 原因：`add` 与 `.` 之间漏了空格。
- 解决：`git add .`（有空格）。`.` 表示当前目录。

## 7. git 命令报 `not a git repository`
- 原因：在仓库外（外层 PythonProject 目录）执行。
- 解决：`cd taskboard`（含 `.git` 的目录）再操作。

## 8. ssh config 报 `Bad configuration option: \357\273\277host`
- 原因：PowerShell 5.1 的 `Out-File -Encoding utf8` 会写入 UTF-8 **BOM**（EF BB BF），OpenSSH 不认。
- 解决：生成给 CLI 工具读的配置文件一律用 `-Encoding ascii`（或 PowerShell 7 的 `utf8NoBOM`）。

## 9. `ssh -T git@github.com` 报 `port 22: Connection refused`
- 原因：网络屏蔽 GitHub 22 端口。
- 解决：`~/.ssh/config` 里让 SSH 走 443：
- ## 10. 粘贴多行命令时 PowerShell 崩（PSReadLine top -2 异常）
- 原因：PSReadLine 渲染多行 here-string 的已知 bug。
- 解决：改用单行写法，例如：
  `@('Host github.com','  Hostname ssh.github.com','  Port 443','  User git') | Set-Content "$env:USERPROFILE\.ssh\config" -Encoding ascii`

## 11. PyCharm 解释器与项目环境不一致
- 现象：IDE 显示解释器为 `D:/tang/.venv`，非 `taskboard/.venv`。
- 解决：命令行统一 `uv run`；日后用 PyCharm 运行按钮时再把解释器绑到 `taskboard/.venv`（阶段 3 处理）。