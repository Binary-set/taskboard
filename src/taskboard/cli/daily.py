from datetime import date

# 一条打卡记录 = 一个字典（对应 JS 的对象 {}）
# records = 列表（对应 JS 的数组 []），里面装了很多字典
records = [
    {"habit": "每天写代码", "date": "2026-11-19", "done": True, "minutes": 45},
    {"habit": "每天写代码", "date": "2026-11-20", "done": False, "minutes": 0},
    {"habit": "每天写代码", "date": "2026-11-21", "done": True, "minutes": 30},
    {"habit": "背单词", "date": "2026-11-21", "done": True, "minutes": 15},
]

# 遍历：for 元素 in 列表（相当于 JS 的 for...of）
for r in records:
    status = "完成" if r["done"] else "缺卡"   # 三元表达式，见下
    print(f"{r['date']} {r['habit']:<8} {status}  {r['minutes']:>3} 分钟")# f-string，格式化字符串

# 统计
total = len(records)          # len() = 列表长度，相当于 JS 的 .length
done_count = 0
for r in records:
    if r["done"]:
        done_count += 1       # += 和 JS 一样
print(f"总计 {total} 条，完成 {done_count} 条")