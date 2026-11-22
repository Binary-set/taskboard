# argparse：Python 标准库，负责解析命令行参数、自动生成 --help、校验必填项
import argparse
# json：标准库，把 Python 对象与 JSON 文本互相转换（写入/读取磁盘文件用）
import json
# 从标准库 datetime 模块只导入 date 类，用于获取“今天”的日期
from datetime import date, timedelta
# 从标准库 pathlib 模块只导入 Path 类，用面向对象方式安全地拼路径、读写文件
from pathlib import Path

# DATA_DIR：数据存放目录，用 Path.home() 取当前用户主目录，再“/”拼接子目录名
# 不写死盘符（如 C:\），换机器也能自动定位，这是 pathlib 的惯用法
DATA_DIR = Path.home() / ".taskboard"
# DATA_FILE：打卡数据文件名，同样是 Path 对象，指向 .taskboard/daily.json
DATA_FILE = DATA_DIR / "daily.json"


def load_records() -> list[dict]:
    # 作用：从磁盘读取所有打卡记录
    # 返回类型注解 -> list[dict] 表示“返回一个列表，列表每个元素是字典”（仅提示，不强制）
    if not DATA_FILE.exists():
        # exists() 判断文件是否真实存在；不存在则……
        return []
        # ……返回空列表作为“还没有数据”的边界处理，避免下一步读取时抛 FileNotFoundError
    # 读取文件文本，显式指定 encoding="utf-8" 防止中文乱码（Windows 默认编码可能非 UTF-8）
    text = DATA_FILE.read_text(encoding="utf-8")
    # json.loads 把 JSON 字符串解析回 Python 的 list/dict 结构，随后返回给调用方
    return json.loads(text)


def save_records(records: list[dict]) -> None:
    # 作用：把记录列表写回磁盘
    # 参数注解 records: list[dict] 说明传入应是“字典组成的列表”
    # -> None 表示该函数只执行副作用（写文件），不返回任何值
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # 确保目录存在：parents=True 连父目录一并创建；exist_ok=True 目录已存在时不报错
    text = json.dumps(records, ensure_ascii=False, indent=2)
    # json.dumps 把 Python 对象序列化成 JSON 文本
    # ensure_ascii=False 让中文按原样写入，而不是被转义成 \uXXXX
    # indent=2 每层缩进两个空格，便于人直接打开文件阅读
    DATA_FILE.write_text(text, encoding="utf-8")
    # 将 JSON 文本写入文件，同样显式 encoding="utf-8"；write_text 会覆盖旧内容


def cmd_stats(args: argparse.Namespace) -> None:
    # 作用：处理 `stats` 子命令——先打印总体完成率，再打印最近 7 天的打卡次数柱状图
    records = load_records()
    # 从磁盘读出全部打卡记录

    total = len(records)
    # 记录总条数
    done = sum(1 for r in records if r["done"])
    # 生成器表达式：对每条 done 为真的记录产出 1 再求和，得到"完成"的条数
    rate = (done / total * 100) if total else 0
    # 完成率；用 `if total else 0` 防止 total 为 0 时除以零（边界情况）
    print(f"总计 {total} 条，完成 {done} 条，完成率 {rate:.1f}%")
    # 输出总体统计；{rate:.1f} 把浮点数格式化成保留 1 位小数

    print("\n最近 7 天打卡次数：")
    # 空一行后打印图表标题（\n 是换行符）

    counts: dict[str, int] = {}
    # counts 用来存"日期 -> 当天打卡次数"的映射
    # 变量也带类型注解：dict[str, int] 表示键是日期字符串、值是整数（仅提示用途）
    for r in records:
        # 遍历每条记录，累加它所属日期的次数
        counts[r["date"]] = counts.get(r["date"], 0) + 1
        # dict.get(键, 默认值)：键不存在时返回默认 0，避免 KeyError
        # 整体含义：该日期已有计数 + 本次的 1

    today = date.today()
    # 取"今天"作为 7 天窗口的最后一天

    for i in range(6, -1, -1):
        # range(6, -1, -1) 产生 6,5,4,3,2,1,0（步长 -1 递减）
        # 即"从今天往前数 6 天，一直到今天"，共 7 天，且按时间先后顺序输出
        d = (today - timedelta(days=i)).isoformat()
        # today - timedelta(days=i) 得到 i 天前的日期对象
        # .isoformat() 转成 'YYYY-MM-DD' 字符串，才能和 counts 里的键对上
        n = counts.get(d, 0)
        # 取该天的打卡次数；那天没有记录则默认 0
        bar = "█" * n
        # 用 n 个方块字符拼成条形（次数越多条越长）
        print(f"{d} | {bar} {n}")
        # 输出：日期 | 柱状条 次数


def cmd_list(args: argparse.Namespace) -> None:
    # 作用：处理 `list` 子命令——列出全部打卡记录
    records = load_records()
    # 读取所有记录
    if not records:
        # 空列表在布尔上下文中等价 False，即“没有任何记录”
        print("还没有任何打卡记录")
        return
        # 提前返回，跳过下面的循环（卫语句写法，减少嵌套）
    for r in records:
        # 遍历列表，r 依次代表每一条记录字典
        status = "完成" if r["done"] else "缺卡"
        # 条件表达式（Python 的三元）：条件为真取“完成”，否则取“缺卡”
        # r["done"] 用键 "done" 从字典取值
        print(f"{r['date']} {r['habit']:<8} {status}  {r['minutes']} 分钟")
        # f-string 输出；{r['habit']:<8} 表示左对齐、占 8 个字符宽，让列对齐更整齐
        # 注意：外层用双引号，内层取键用单引号，避免引号冲突


def cmd_add(args: argparse.Namespace) -> None:
    # 作用：处理 `add` 子命令——新增一条打卡记录
    # args 是 argparse 解析后存放各参数的对象（Namespace），字段名与 add_argument 对应
    records = load_records()
    # 先读出已有记录，才能在其基础上追加（否则直接覆盖会丢历史数据）
    records.append({
        "habit": args.habit,
        # args.habit 来自 add 的位置参数 habit
        "date": args.date or date.today().isoformat(),
        # 若用户传了 --date 就用它；否则用“今天”
        # date.today() 取当天对象，.isoformat() 转成 'YYYY-MM-DD' 字符串
        # 用 or 实现“左边为空/None 则取右边”的默认值逻辑
        "done": True,
        # add 语义即“完成打卡”，故 done 固定为 True（注意首字母大写的 True）
        "minutes": args.minutes,
        # args.minutes 来自 --minutes，未提供时默认 0（在 add_argument 里设的 default）
    })
    save_records(records)
    # 把追加后的完整列表写回磁盘
    print(f"已记录：{args.habit} {args.minutes} 分钟")
    # 给用户一行确认反馈


def build_parser() -> argparse.ArgumentParser:
    # 作用：搭建并返回命令行的解析器（把“定义命令结构”单独成函数，便于测试与阅读）
    parser = argparse.ArgumentParser(prog="daily", description="命令行打卡工具")
    # prog 指定帮助信息里显示的程序名；description 是 --help 顶部的说明文字
    sub = parser.add_subparsers(dest="command", required=True)
    # 注册子命令集合；dest="command" 表示把用户选的子命令名存进 args.command
    # required=True 强制必须给一个子命令，否则报错退出
    p_add = sub.add_parser("add", help="添加一条打卡记录")
    # 定义名为 add 的子命令；help 出现在父级 --help 列表里
    p_add.add_argument("habit", help="习惯名称")
    # 位置参数（无 -- 前缀）：调用时直接跟在 add 后面，如 daily add 每天写代码
    p_add.add_argument("--minutes", type=int, default=0, help="用时（分钟）")
    # 选项参数：需写 --minutes 45；type=int 把字符串转成整数；不写则默认 0
    p_add.add_argument("--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    # 选项参数 --date，默认 None（表示“未提供”，在 cmd_add 里再回退到今天）
    p_add.set_defaults(func=cmd_add)
    # 给 add 绑定处理函数：解析出 add 时，args.func 就是 cmd_add
    p_list = sub.add_parser("list", help="列出所有打卡记录")
    # 定义 list 子命令
    p_list.set_defaults(func=cmd_list)
    # list 绑定到 cmd_list
    p_stats = sub.add_parser("stats", help="统计完成率")
    # 定义 stats 子命令
    p_stats.set_defaults(func=cmd_stats)
    # stats 绑定到 cmd_stats
    return parser
    # 返回配置好的解析器


def main() -> None:
    # 作用：程序主流程入口
    parser = build_parser()
    # 构建解析器
    args = parser.parse_args()
    # 解析实际传入的命令行参数，得到 Namespace 对象 args
    # 若缺少必填子命令/参数，parse_args 会自动打印错误并以非零状态退出
    args.func(args)
    # 根据 args.func（由 set_defaults 决定）调用对应处理函数，并把 args 传进去
    # 这是 argparse 推荐的“分发”写法，省去手写 if args.command == ... 分支


if __name__ == "__main__":
    # 只有当该文件被“直接运行”时，__name__ 才等于 "__main__"
    # 若被别的模块 import，这里为假，下面的 main() 不会自动执行
    main()
    # 作为脚本运行时才启动主流程