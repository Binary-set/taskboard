# 从 dataclasses 模块导入 dataclass 装饰器与 field 辅助函数
# dataclass：类装饰器，自动生成 __init__ / __repr__ / __eq__，省去手写样板代码
# field：辅助函数，用于指定"每次新建实例都要重新计算"的默认值
from dataclasses import dataclass, field

# 从 datetime 模块导入 date 类
# 用 date 而不是 datetime：任务看板只关心"哪一天创建的"，不关心具体时分秒
from datetime import date

# 绝对导入：从包的根开始写完整路径 taskboard.domain.status
# 这样写不受文件在包内位置的影响，一看就知道来源
from taskboard.domain.status import TaskPriority, TaskStatus


@dataclass
class Task:
    # @dataclass 会根据下面的"字段名 + 类型注解"自动生成 __init__ 等样板方法，
    # 所以这里只声明字段，不需要自己手写构造函数

    title: str
    # 任务标题：必填字段，没有默认值
    # 必须排在所有有默认值的字段之前，否则 dataclass 生成 __init__ 时会报
    # TypeError: non-default argument 'title' follows default argument

    status: TaskStatus = TaskStatus.TODO
    # 任务状态：默认"待办"
    # 类型注解写 TaskStatus 而不是 str：让 IDE 能提示、让类型检查器能拦截，
    # 也让"状态拼错"这种错误在写代码时就暴露，而不是留到线上

    priority: TaskPriority = TaskPriority.MEDIUM
    # 任务优先级：默认"中优先级"
    # 同样用枚举而不是裸字符串，理由与 status 一致

    minutes: int = 0
    # 已投入的分钟数：默认 0
    # 用 0 而不是 None：0 能直接参与求和与统计，None 会让聚合逻辑到处要判空

    created_at: date = field(default_factory=date.today)
    # 创建日期：默认是"创建这个任务的那天"
    # 必须用 default_factory=date.today：默认值只在类定义时求值一次，
    # 若写成 = date.today()，所有任务都会拿到"模块被导入那天"的日期
    # default_factory 是工厂函数，每次新建任务都调用一次 date.today()，拿到当天日期

    tags: list[str] = field(default_factory=list)
    # 标签列表：默认为空列表
    # 必须用 default_factory=list：list 是可变对象，
    # 若写成 = []，Python 3.11 会直接报错
    # ValueError: mutable default <class 'list'> ... use default_factory
    # （3.10 及以前不报错，但所有实例会共享同一个列表，是个隐蔽的线上 bug）

    # 方法：判断这个任务是否已完成
    # 放在类里，是为了让"怎么才算完成"这件事跟着对象走，而不是散落在各个调用处
    def is_done(self) -> bool:
        """判断任务是否完成"""
        # 用 is 而不是 == 比较枚举：枚举成员是全局唯一对象，is 才是"确实是这个成员"的严格判断
        # 而 == 因为混入了 str，裸字符串 "done" == TaskStatus.DONE 同样成立，
        # 会把"数据里混进了字符串"这个污染问题悄悄掩盖掉
        return self.status is TaskStatus.DONE

    # 方法：把任务标记为完成，并记录投入的分钟数
    def finish(self, minutes: int = 0) -> None:
        """将任务标记为完成"""
        # 修改的是实例自己的属性，self 就是调用这个方法的那个任务对象
        self.status = TaskStatus.DONE
        # 直接覆盖原有的 minutes（不是累加）：finish 接收的是"本次总共投入了多少分钟"
        self.minutes = minutes


if __name__ == "__main__":
    # 只有以模块方式直接运行本文件时才执行下面这段（被 import 时不执行）

    task_1 = Task(
        title="学dataclass",
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
        minutes=60,
        created_at=date(2023, 1, 1),  # 手动指定创建日期，演示与自动取值的区别
        tags=["tag1", "tag2"],
    )
    # 关键字参数传参：以后增删字段不会让位置错位，读代码也能直接看懂每个值的含义

    print(task_1)
    # 打印第一个任务：dataclass 自动生成的 __repr__ 会展示所有字段

    task_2 = Task(title="学datetime")
    # 只给必填字段 title，其余 5 个字段全部走默认值

    print(task_2)
    # 打印第二个任务，和第一个对比差别

    done_flag = task_1.is_done()
    # 调用实例方法，判断任务当前是否已完成；结果存进变量再打印，代码更易读

    print(done_flag)
    # 输出 False：任务刚创建，状态还是 TODO

    task_1.finish(minutes=120)
    # 标记为完成，并记录投入 120 分钟

    print(task_1)
    # 再打印一次：status 变成 DONE，minutes 从 60 被覆盖成 120

    print(task_1.is_done())
    # 输出 True：状态已经改成完成
