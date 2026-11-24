# 练习文件：D+3 闭卷复习 —— 枚举与 dataclass
# 用途：脱离主项目独立重建"任务状态枚举 + 状态转中文函数"，检验记忆是否牢固
# 目的：巩固 Enum 的定义方式、.value/.name 的区别、模块级函数与类方法的区别

# 从标准库 enum 模块导入 Enum 基类：用于定义"一组固定的、有名字的常量"
from enum import Enum
# 从标准库 dataclasses 模块导入 dataclass 装饰器：用于定义数据类，
# 它会自动生成 __init__ / __repr__ / __eq__ 等样板方法，省去手写重复代码
from dataclasses import dataclass


# 任务状态枚举：表示一个任务当前处在哪个阶段
# 继承 (str, Enum)：让每个成员"既是枚举成员、又是字符串"，
# 这样写入 JSON 时能直接当字符串序列化，比较时也兼容普通字符串
class TaskStatus(str, Enum):
    TODO = "todo"      # 待办：任务已创建但尚未开始
    DOING = "doing"    # 进行中：任务正在处理
    DONE = "done"      # 已完成：任务已结束


# 定义一个数据类 Note，表示一个便签
@dataclass
class Note:
    text: str             # 便签内容
    pinned: bool = False  # 是否置顶

note_1 = Note(text="这是一个便签", pinned=True)     # 创建一个便签对象
note_2 = Note(text="这是另一个便签", pinned=False)  # 创建另一个便签对象


# 函数：把任务状态翻译成中文标签
# 注意它是"模块级函数"而不是"方法"——定义在类体之外，因此没有 self 参数
# 参数 s 期望传入一个 TaskStatus 成员；返回对应的中文描述字符串
def status_to_chinese(s: TaskStatus) -> str:
    # 逐个枚举成员显式判断，每个分支对应一种状态
    if s == TaskStatus.TODO:
        # 等于"待办"状态时返回对应标签
        return "待办"
    elif s == TaskStatus.DOING:
        # 等于"进行中"状态时返回对应标签
        return "进行中"
    elif s == TaskStatus.DONE:
        # 等于"已完成"状态时返回对应标签
        return "已完成"
    else:
        # 兜底分支：传入的不是合法枚举成员时走这里
        # 必须单独写 DONE 的分支，否则非法值会被误显示成"已完成"
        return "未知状态"


# 只有直接运行本文件时才执行下面的自测代码（被 import 时不执行）
if __name__ == "__main__":
    # 遍历枚举，逐个验证三种合法状态的中文标签
    for status in TaskStatus:
        # status.value 取成员背后的字符串值；status_to_chinese 把它翻译成中文
        print(f"{status.value}: {status_to_chinese(status)}")

    # 故意传入一个非法值（整数 1），验证兜底分支是否生效
    # 注意：这违反类型注解 s: TaskStatus，阶段 3 接入 mypy 后会报类型错误，
    # 那时可在行尾追加 "# type: ignore" 显式豁免
    print(f"不合法的值: {status_to_chinese(1)}")
    print(note_1)  # 打印便签对象
    print(note_2)  # 打印另一个便签对象
