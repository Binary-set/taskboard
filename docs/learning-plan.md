
# Python Web 全栈学习计划与进度

> 本文件是主线导航。每次学习：先看「进度追踪」确认走到哪，再看对应阶段详情执行，最后更新进度。
> 排错细节见同目录 `env-checklist.md`。

## 主线技术栈（锁定，不改）

Python 3.11.9 + uv + FastAPI + Pydantic v2 + SQLAlchemy 2.1（同步 Session）+ Alembic + SQLite→PostgreSQL 17 + Docker Compose + Nginx + certbot + GitHub Actions。

贯穿项目：`taskboard`（任务看板：注册登录、多看板、任务 CRUD 与状态流转、评论、附件上传、统计图表）。

---

## 阶段总览

| 阶段 | 目标 | 关键内容 | 工时 | 验收里程碑 |
|---|---|---|---|---|
| 1 环境与工具链 | 可复现的 Python 环境 | PowerShell、uv、IDE 绑定、Git、路径与编码 | 1周/12h | 新机 60 分钟跑通装工具→恢复→起服务→推送 |
| 2 语言核心 | 纯标准库写出带类型注解的程序 | 类型、函数、模块、异常、类、pathlib/datetime/json/logging | 3周/40h | 闭卷 30 分钟写一个命令行程序 |
| 3 工程习惯 | 代码可被接手、可自动检查 | Git 分支流、src 布局、ruff、pytest、类型检查、.env、pre-commit | 2周/26h | 25 分钟搭出含 lint/测试/CI 的骨架 |
| 4 HTTP 与数据库 | 讲清请求链路与数据落库 | HTTP、curl/DevTools、SQL、索引事务、SQLite、PostgreSQL、SQLAlchemy、Alembic | 3周/38h | 只改连接串切换 SQLite↔PostgreSQL |
| 5 后端框架 | 交付带鉴权与测试的 REST API | FastAPI、Pydantic、依赖注入、JWT、分层、测试 | 5周/65h | 闭卷 3 小时搭出登录+CRUD+迁移+测试 |
| 6 前后端联调 | 用现有 JS 能力做前端并定契约 | OpenAPI、fetch、Token、CORS、XSS/CSRF、静态托管 | 3周/38h | 陌生人完成注册到上传闭环，控制台零报错 |
| 7 容器化 | 一条命令复现整套服务 | WSL2、Docker 镜像/容器/卷/网络、多阶段构建、compose | 3周/38h | 新机 10 分钟 up 全站且数据不丢 |
| 8 部署上线 | 公网可访问、HTTPS、自动发布可回滚 | Linux、VPS、DNS、Nginx 反代、certbot、CI/CD、备份与故障演练 | 4周/50h | 30 分钟内完成回滚/恢复/定位 502 |
| 9 长期深化 | 从能跑到能撑住 | 异步、SQL 性能、缓存队列、安全扫描、可观测性 | 4周/50h+持续 | 1 小时内给出性能/安全问题的证据链 |

---

## 各阶段详情

### 阶段 1｜环境与工具链（已完成）
- 知识点：PowerShell 基础、uv 工作流、虚拟环境本质、Git 安装、路径与编码、IDE 解释器绑定。
- 交付物：`SETUP.md`、`env-checklist.md`、可复现的 taskboard 骨架 + GitHub 仓库。
- 典型坑：解释器不一致（用 uv run 绕开）；PowerShell 执行策略/编码/UTF-8 BOM（见 env-checklist 8）。
- **验收：新机 60 分钟内完成装工具→恢复→起服务→推送。**

### 阶段 2｜语言核心（进行中）
- 知识点（按序）：变量与类型/不可变/f-string → list/dict/set/tuple 与推导式 → 控制流 → 函数(默认参数/可变默认值坑/*args/**kwargs) → 模块与 import 搜索路径/`__name__` → 异常与 traceback → 类/dataclass/Enum → 生成器/with/pathlib/datetime/json/logging/类型注解。
- 动手练习：W1 命令行打卡工具 `daily.py`(argparse add/list/stats, JSON 存用户目录, 7 天完成率柱状图)；W2 看板领域模型(dataclass)+Markdown 周报；W3 CSV 清洗(UTF-8/异常/日志/类型注解)。
- 典型坑：可变默认参数与浅拷贝；`True/False` 大小写、`str` vs `bytes` 编码、`python 脚本.py` 与 `python -m` 的 import 差异。
- 复习：D+1/D+2/D+4/D+8/D+21 卡片；每周一闭卷重写上周函数；第6、12周回炉。
- **验收：闭卷 30 分钟写出带类型注解、支持 --help、读写 UTF-8 文件、异常有提示的命令行程序，不用第三方库。**

### 阶段 3｜工程习惯
- 知识点：Git 心智模型与分支流、src 布局、pyproject 全貌、ruff、mypy/pyright、pytest 与 fixture、.env+pydantic-settings、logging 规范、README/CHANGELOG/ADR、pre-commit。
- 交付物：迁移旧练习目录进规范仓库；给阶段2代码补 ≥25 个测试(领域层覆盖≥85%)；`skeleton/` 新项目模板 + 一次闭卷搭骨架计时。
- 典型坑：src 布局未安装导致 pytest 收集失败；`.venv/.env/__pycache__` 误提交。
- **验收：任意项目 25 分钟搭出含 venv/lint/类型/测试/覆盖率/pre-commit/README/CI 的骨架，pytest 与 ruff 全绿。**

### 阶段 4｜HTTP 与数据库
- 知识点：HTTP 报文/方法/状态码/Header/同源；curl.exe 与 DevTools；REST 契约；关系模型与 SQL(增删改查/JOIN/聚合/窗口/索引/事务/隔离)；SQLite；SQLAlchemy 2.1 声明式与 select；Alembic 迁移；PostgreSQL 17 与 psql/角色/编码。
- 交付物：W1 http-lab.md(10 组 curl 请求+响应)；W2 ER图+schema.sql+exercises.sql(≥40条)+索引笔记；W3 ORM 重写模型+seed 1000 行+两次可回滚迁移+SQLite↔PG 对比证据。
- 典型坑：SQLite 相对路径随 cwd 变；PG 服务/端口/pg_hba；SQLAlchemy 2.1 用 psycopg 3(postgresql+psycopg://)；Alembic autogenerate 需导入模型。
- **验收：口述一次请求全链路；40 分钟设计两表关系+写 6 条 JOIN/聚合 SQL+跑通迁移升级与回滚。**

### 阶段 5｜后端框架
- 知识点：ASGI/uvicorn/fastapi dev；路径/查询/请求体/表单/文件；Pydantic DTO 分离；依赖注入；错误处理与统一响应；分层(api/services/repositories/db/core)；密码哈希与 JWT 认证与所有权授权；分页过滤排序；CORS；BackgroundTasks/lifespan；OpenAPI 文档；TestClient 测试；同步/异步端点选择。
- 交付物：W1 CRUD+health+接口清单；W2 分页过滤+统一错误码表；W3 注册登录鉴权+auth-flow.md；W4 附件上传+统计+服务层覆盖≥80%；W5 闭卷重写+架构文档。
- 典型坑：ModuleNotFoundError/端口占用；CORS 预检与 401 死循环排查顺序。
- **验收：闭卷 3 小时搭出分层骨架+CRUD+登录+迁移+10 个通过的接口测试。**

### 阶段 6｜前后端联调
- 知识点：读 openapi.json 契约；fetch 封装(超时/错误规范/Token/401)；ES Modules 组织；localStorage vs httpOnly Cookie 与 XSS/CSRF；CORS 全貌；静态资源与缓存；日期时区对齐；四态 UI；DevTools 定位法。
- 交付物：W1 认证前端+network-forensics.md(6 张截图)；W2 看板主界面+返工记录；W3 上传+统计图+Lighthouse+架构决策。
- 典型坑：`file://` 打开导致模块/fetch 失败(必须起 HTTP 服务)；401 刷新死循环；时区差 8 小时。
- **验收：陌生人手机完成注册→上传闭环，控制台零报错；能用 DevTools 判定失败原因归属。**

### 阶段 7｜容器化
- 知识点：WSL2 与 Docker 引擎；镜像/容器/卷/网络；Dockerfile(多阶段/uv sync --frozen/非root/HEALTHCHECK/.dockerignore)；compose(services/env/volumes/ports/restart/healthcheck/profiles)；镜像瘦身；时区与编码。
- 交付物：W1 CLI 镜像+PG 起容器；W2 后端+PG 的 compose(删容器不丢数据)；W3 加 Nginx 本地全站+体积/内存实测。
- 典型坑：Docker 起不来(虚拟化/虚拟机平台)；容器里 `localhost` 指自己(用服务名)；postgres:18 数据目录变更(本项目锁 17-alpine)。
- **验收：新机 10 分钟 `docker compose up -d` 起全站且数据保留；能说出容器启动失败的三条排查命令。**

### 阶段 8｜部署上线
- 知识点：Linux 与 SSH(密钥登录/权限/systemctl/journalctl/ufw/fail2ban)；VPS 选型与备案；DNS A 记录；Nginx 反代与静态托管；certbot HTTPS 与自动续签；systemd/重启策略；生产 PG 与 pg_dump/restore；GitHub Actions 全流程 CI/CD(含回滚)；可观测与故障演练 runbook。
- 交付物：W1 干净服务器+域名解析；W2 公网 HTTPS 站点;W3 CI/CD+备份恢复演练;W4 七类故障演练报告+runbook+作品集。
- 典型坑：502 排查四步法；改 sshd/ufw 把自己关门外(先 allow OpenSSH、留会话、控制台兜底)；certbot 失败(解析/80端口/时钟)。
- **验收：发域名给陌生人可用；30 分钟内完成一次回滚、一次从备份恢复、一次定位并解释一条 502。**

### 阶段 9｜长期深化
- 知识点：asyncio 与异步 SQLAlchemy；SQL 性能与索引/连接池/PgBouncer；Redis 缓存与任务队列；契约/属性/性能测试；OWASP 与依赖扫描；结构化日志/指标/追踪；架构演进与在线迁移。
- 节奏：每月一个上线增量 + 一页纸文档 + 前后对比数据；每季度闭卷重做整套。
- 典型坑：无证据地上微服务；异步改造混用同步阻塞事件循环。
- **验收：任一线上性能/安全问题 1 小时内给出证据→假设→验证→修复→回滚的书面回答。**

---

## 进度追踪

图例：`[x]` 完成 `[~]` 进行中 `[ ]` 未开始

- [x] 阶段 1 环境与工具链
  - [x] 检查点1 安装 uv 并验证
  - [x] 检查点2 uv init --package 建 taskboard 锁定 3.11.9
  - [x] 检查点3 加 FastAPI 并跑起 dev 服务
  - [x] 检查点4 首次提交 + SSH key + 推送 GitHub（走 443）
  - [x] 检查点5 重装演练（删 .venv → uv sync 复原）
  - [x] 检查点6 写 env-checklist.md
  - [x] 检查点7 十题闭卷自测（改为逐题讲解）
  - [x] PyCharm 解释器绑定到 taskboard/.venv
- [~] 阶段 2 语言核心
  - [x] W1 命令行打卡工具 daily.py
    - [x] Day1 第一个脚本：变量/类型/f-string/datetime
    - [x] Day2 列表与字典：存打卡记录
    - [x] Day3 pathlib + json：持久化到用户目录
    - [x] Day4 argparse 三个子命令 add/list/stats
    - [x] Day5 stats 文本柱状图 + 产出 samples/daily-output.txt
    - [x] 复习 D+1/D+2 闭卷默写 load_records / save_records
  - [~] W2 看板领域模型(dataclass/Enum) + Markdown 周报
    - [x] Day6 Enum：TaskStatus / TaskPriority + status_to_chinese + domain 包骨架
    - [~] Day7 dataclass：Task 对象 + 可变默认值陷阱 + python -m 运行方式
      - [x] Step1 D+3 闭卷复习：重写枚举与 status_to_chinese、Note dataclass（练功区 recall_enum_dataclass.py）
      - [ ] Step2 写 Task 的 6 个字段（title/status/priority/minutes/created_at/tags）
      - [ ] Step3 运行观察 __repr__ 自动生成（python -m taskboard.domain.task）
      - [ ] Step4 加实例方法 is_done / finish
      - [ ] Step5 亲手踩可变默认值陷阱（= [] 与 default_factory 对照）
    - [ ] Day8 对象行为与关系：Board 持有 Task 列表（一对多）与实例方法
    - [ ] Day9 对象 ↔ 字典 ↔ JSON：asdict 落盘与从 JSON 重建对象
    - [ ] Day10 Markdown 周报生成器 + 产出 samples/weekly-report.md
  - [ ] W3 CSV 清洗 + 类型注解 + logging + 异常处理
- [ ] 阶段 3 工程习惯
- [ ] 阶段 4 HTTP 与数据库
- [ ] 阶段 5 后端框架
- [ ] 阶段 6 前后端联调
- [ ] 阶段 7 容器化
- [ ] 阶段 8 部署上线
- [ ] 阶段 9 长期深化

## 学习日志（倒序追加）

- 阶段2 Day7 Step1：完成 D+3 闭卷复习，新建练功区 exercises/recall_enum_dataclass.py（主题命名，不按天）。踩坑：① 在枚举类体内定义方法、且参数注解引用自身类名 → 类定义时 NameError（注解在定义时求值，而类名要到 class 语句结束才绑定）；② else 兜底分支吞掉 DONE，非法值被误显示为"已完成"；③ 字段顺序颠倒 → TypeError: non-default argument 'text' follows default argument。认知修正：Python 3.11 的 dataclass 已直接拒绝 list/dict/set 可变默认值，但普通函数默认值与其它可变对象仍会共享同一实例。

- 阶段2 Day6：建 domain 包，写 TaskStatus / TaskPriority 两个枚举与 status_to_chinese；掌握 Enum 混入 str 的意义、.value 与 .name、按值(圆括号)/按名(方括号)反查；练习结论——裸字符串拼错**不会**抛异常（错误静默漂移到远处才暴露），枚举把失败点提前到边界。
- 阶段2 Day5：stats 增加最近 7 天柱状图，产出 samples/daily-output.txt。踩坑：替换函数时误删 cmd_add 引发 NameError，并遗留同名 cmd_stats 被后定义覆盖——教训：改完必须 git diff 复核，且"能跑就立刻提交"。
- 阶段2 Day4：argparse 三子命令 add/list/stats，掌握 set_defaults(func=...) 分发模式。
- 阶段2 Day3：pathlib + json 持久化到用户目录；记住 ensure_ascii=False 与 encoding="utf-8" 两个中文坑。
- 阶段2 Day2：list + dict 存打卡记录并统计。
- 阶段2 Day1：创建 src/taskboard/cli/daily.py，跑通变量/f-string/datetime。
- 阶段1 全部通过：uv 环境、src 布局、FastAPI Hello World、GitHub 推送(SSH over 443)、可复现演练、排错手册。踩坑已沉淀至 env-checklist.md（含 winget 需重开终端、uv run 需在项目根、main.py 需在 src 包内、PowerShell UTF-8 BOM、GitHub 22 端口、PSReadLine 粘贴崩溃等）。

## 复习节点提醒（间隔重复）

- 阶段1：D+4 遮盖 SETUP 重做初始化；D+8 念 env-checklist；D+22 阶段3 时回答"为何 lock 提交、venv 不提交"。
- 阶段2 已排定的节点：
  - D+3（明天）：闭卷重写 TaskStatus 枚举与 status_to_chinese；再闭卷写一个含 2 个字段的 dataclass。
  - D+4：给 daily.py 加一个 `clear` 子命令练手 argparse。
  - D+8：生成器表达式、条件表达式、dict.get 默认值、f-string 对齐与 .1f 各写 3 个例子。
  - D+21：从头默写 daily.py 核心骨架与 domain 模型。
- 阶段2 通用：每晚 D+1 写 3 张卡；D+2/4/8/21 各 20 分钟只复习到期卡；每周一闭卷重写上周函数。
