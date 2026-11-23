# status.py：定义任务领域里的"状态"与"优先级"两组枚举，并提供状态转中文标签的辅助函数
# 本模块只依赖标准库 enum，可被其它模块安全 import（不会产生副作用）
from enum import Enum


# 任务状态枚举：描述一个任务当前处在哪个阶段
# 继承 (str, Enum) 表示"既是枚举成员、又是字符串"，
# 这样写入 JSON 时能直接当字符串序列化，比较时也兼容普通字符串
class TaskStatus(str, Enum):
    TODO = "todo"      # 待办：任务已创建但尚未开始
    DOING = "doing"    # 进行中：任务正在处理
    DONE = "done"      # 已完成：任务已结束


# 任务优先级枚举：描述任务的重要程度
# 同样混入 str，保持与 TaskStatus 一致的取值风格（统一用小写字符串）
class TaskPriority(str, Enum):
    LOW = "low"        # 低优先级
    MEDIUM = "medium"  # 中优先级
    HIGH = "high"      # 高优先级


def status_to_chinese(s: TaskStatus) -> str:
    # 作用：把一个任务状态翻译成中文标签，用于终端输出或周报展示
    # 参数 s 期望是 TaskStatus 成员；返回值是中文描述字符串
    if s == TaskStatus.TODO:
        # 等于"待办"状态时
        return "待办"
    elif s == TaskStatus.DOING:
        # 等于"进行中"状态时
        return "进行中"
    elif s == TaskStatus.DONE:
        # 等于"已完成"状态时
        return "已完成"
    else:
        # 兜底分支：理论上不会走到（类型注解已限定取值范围），
        # 但保留它可避免传入意外值时函数返回 None
        return "未知状态"


if __name__ == "__main__":
    # 只有直接运行本文件时才执行下面的演示代码

    status = TaskStatus.DONE
    # 取一个"已完成"状态作为演示对象

    print(status)
    # 输出 TaskStatus.DONE：Enum 重写了 __str__，显示"类名.成员名"

    print(status.value)
    # 输出 done：.value 取成员背后的实际字符串值（入库、存 JSON 用这个）

    print(status.name)
    # 输出 DONE：.name 取成员名本身

    print(status == "done")
    # 输出 True：因为混入了 str，枚举成员可以直接和普通字符串比较

    print(TaskStatus("done"))
    # 输出 TaskStatus.DONE：圆括号按"值"反查成员

    print(TaskStatus["DONE"])
    # 输出 TaskStatus.DONE：方括号按"名"反查成员

    for s in TaskStatus:
        # 遍历枚举，只会得到成员本身（不会遍历到类里的其它名字）
        print(s.name, s.value)
        # 输出每一对"成员名 + 值"：TODO todo / DOING doing / DONE done

    for p in TaskPriority:
        # 同理遍历优先级枚举，验证新枚举可用
        print(p.name, p.value)
        # 输出 LOW low / MEDIUM medium / HIGH high

    print(status_to_chinese(TaskStatus.TODO))
    # 输出 待办：演示 status_to_chinese 的调用方式

