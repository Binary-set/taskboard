# mutable_default_experiment.py：亲手验证"默认值只在定义时求值一次"会怎样
# 目的：亲眼看到可变默认值被所有实例共享，以及 default_factory 如何解决它
# 运行方式：uv run python src/taskboard/exercises/mutable_default_experiment.py

# 从 dataclasses 模块导入 dataclass 装饰器与 field 辅助函数
from dataclasses import dataclass, field


# 普通类：实例内部装着一个可变列表
# 关键：它不是 list/dict/set，所以 dataclass 的"可变默认值自动检查"抓不到它
class Bag:
    # 作用：创建一个"包"，用来装 items 列表
    def __init__(self) -> None:
        # 每次 __init__ 被调用都会新建一个空列表，所以每个 Bag 各自独立
        # （这里的写法是对的：它在"方法体内"，不是默认值位置）
        self.items: list[str] = []


# 正确写法：用工厂函数产生默认值
@dataclass
class WithFactory:
    # 每次 WithFactory() 都会调用一次 Bag()，得到一个全新的 Bag 实例
    bag: Bag = field(default_factory=Bag)


# 危险写法：把一个已经造好的实例直接当默认值
# 注意必须有 @dataclass 装饰器，否则测的就不是"dataclass 的默认值共享"，
# 而是"普通类的类属性共享"——两者现象一样，但机制和结论完全不同
@dataclass
class DangerousDefault:
    # Bag() 在"类定义那一刻"被调用一次，这个实例随后被所有实例共享
    # Python 3.11 的 dataclass 只检查 list/dict/set 这三种，抓不到 Bag，所以这里不报错
    bag: Bag = Bag()


# 普通函数的危险写法：默认值是列表，函数定义时求值一次，所有调用共用
def create_bag(items: list[str] = []) -> list[str]:
    # 最经典的陷阱：两次调用返回的是同一个列表，内容会不断累积
    items.append("tag")
    return items


# 普通函数的正确写法：用 None 当"哨兵"，进入函数体后再创建真正的对象
def create_bag_safe(items: list[str] | None = None) -> list[str]:
    # 用 None 表示"调用者没传"，而不是把空列表当默认值
    if items is None:
        # 只有真的没传时，才在这一刻新建一个列表
        items = []
    items.append("tag")
    return items


if __name__ == "__main__":
    # 只有直接运行本文件时才执行下面这段（被 import 时不执行）

    # ---------- 实验一：default_factory（正确写法）----------
    f1 = WithFactory()
    # 创建第一个实例
    f2 = WithFactory()
    # 创建第二个实例

    f1.bag.items.append("放进f1")
    # 只往 f1 的 bag 里放一个东西

    print("WithFactory(正确写法):")
    print(f"f1.bag.items: {f1.bag.items}")
    print(f"f2.bag.items: {f2.bag.items}")
    # 预期 f2 是空列表：两个实例各自拥有独立的 Bag
    print("f1.bag is f2.bag = ", f1.bag is f2.bag)
    # 预期 False：两个 Bag 是不同的对象

    # ---------- 实验二：直接用实例当默认值（危险写法）----------
    d1 = DangerousDefault()
    # 创建第一个实例
    d2 = DangerousDefault()
    # 创建第二个实例

    d1.bag.items.append("放进d1")
    # 只往 d1 的 bag 里放一个东西

    print("DangerousDefault(危险写法):")
    print(f"d1.bag.items: {d1.bag.items}")
    print(f"d2.bag.items: {d2.bag.items}")
    # 预期 d2 也变了！一个实例的操作污染了另一个
    print("d1.bag is d2.bag = ", d1.bag is d2.bag)
    # 预期 True：两个实例共用同一个 Bag 对象

    # ---------- 实验三：普通函数的默认参数（危险写法）----------
    c1 = create_bag()
    # 第一次调用

    c2 = create_bag()
    # 第二次调用

    print("create_bag(危险写法):")
    print(f"c1: {c1}")
    print(f"c2: {c2}")
    # 预期 c2 变成两个 tag：两次调用共用同一个列表
    print("c1 is c2 = ", c1 is c2)
    # 预期 True：返回的是同一个列表对象

    # ---------- 实验四：普通函数的正确写法（None 哨兵）----------
    s1 = create_bag_safe()
    # 第一次调用

    s2 = create_bag_safe()
    # 第二次调用

    print("create_bag_safe(正确写法):")
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    # 预期两个都只有一个 tag：每次调用都新建列表
    print("s1 is s2 = ", s1 is s2)
    # 预期 False：两个不同的列表对象
