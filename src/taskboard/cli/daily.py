from datetime import date

#python不用let、var，直接赋值
habit_name = "每天写代码"
streak_days = 3
done_today = True
today = date.today()
print(f"习惯名称：{habit_name}")
print(f"当前 streak 天数：{streak_days}")
print(f"今天是否完成：{done_today}")
print(f"今天日期：{today}")
