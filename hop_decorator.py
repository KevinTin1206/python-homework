### Assignment hop_decorator ###

# s123456_s56789, YourLastname1_YourLastname2
# 提交前：将上一行替换为实际提交者的学号和姓氏。
#
# 本文件完成题目中的五个任务。建议对照同目录的“题目解析.md”阅读。
# newton.py 是老师提供的原始算法的中文注释版，用来和任务 1、2 对照。
# 本文件独立运行，不需要导入 newton.py，也不需要安装第三方库。

import time
from functools import wraps

# time：任务 4 用它获取时间戳。
# wraps：让包装后的函数保留原函数的名称、说明文字等信息。
# 例如，装饰 helperfunction 后，它的 __name__ 仍然是 "helperfunction"。


# =====================================================================
# Task 1：内部函数版牛顿法
# 要求：保留 square、average；把另外三个辅助函数移入 newton。
# =====================================================================

def square(x):
    """返回 x 的平方。"""
    # square(3) 的结果是 3 * 3，也就是 9。
    return x * x


def average(x, y):
    """返回 x 和 y 的算术平均值。"""
    # 括号保证先相加，再除以 2。例如 average(1, 9) 返回 5.0。
    return (x + y) / 2


def newton(x):
    """保留原始递归算法，通过内部函数近似计算 x 的平方根。"""
    # 调用 newton(9) 时，这一次调用中的局部变量 x 就是 9。
    # 下面三个函数定义在 newton 的内部，因此可以直接读取外层的 x。
    # 原来辅助函数需要接收 (guess, x)，现在只需接收 (guess)。
    # 这里没有给 x 重新赋值，所以不需要 global 或 nonlocal。

    def isGoodEnough(guess):
        # guess：当前猜测的平方根。
        # square(guess) - x：猜测值的平方与目标数之间的差。
        # abs(...)：取绝对值，消除正负号的影响。
        # < 0.001：误差足够小时返回 True，否则返回 False。
        # 注意：比较的是“guess 的平方”和 x，不是 guess 与真实平方根。
        # 因而这里不能理解为“平方根一定精确到小数点后三位”。
        return abs(square(guess) - x) < 0.001

    def improve(guess):
        # 用牛顿法的更新公式改进猜测值：(guess + x / guess) / 2。
        # 当 x = 9、guess = 1.0 时：average(1.0, 9 / 1.0) = 5.0。
        # 这一题要求保留 average，因此仍然通过它计算平均值。
        return average(guess, x / guess)

    def sqrtIter(guess):
        # 递归的终止情况：猜测值已足够准确，直接返回。
        if isGoodEnough(guess):
            return guess
        else:
            # Python 先执行 improve(guess)，得到下一次猜测值，
            # 再把新值交给 sqrtIter，重复检查。
            # 例如 x = 9 时，猜测值依次约为 1、5、3.4、3.0235、3.00009。
            # 外面的 return 必须保留，它把更深一层递归的结果传回来。
            # 只有调用、没有 return，会使当前这一层最后返回 None。
            return sqrtIter(improve(guess))

    # 前面的 def 只是定义内部函数，尚未执行这些函数的计算过程。
    # 走到这里才真正开始计算，初始猜测值固定为原程序中的 1.0。
    return sqrtIter(1.0)


# =====================================================================
# Task 2：用更简洁的 Python 写法实现牛顿法
# 要求：仍然逐次改进猜测值；不能直接使用 math.sqrt 或 x ** 0.5。
# =====================================================================

def newtonPy(x):
    """用 while 循环代替递归，近似计算 x 的平方根。"""
    # 保留与原程序相同的起点。
    guess = 1.0

    # 只要误差还不满足要求，就继续循环。
    # 原程序的停止条件是误差 < 0.001，因此继续条件是误差 >= 0.001。
    while abs(guess * guess - x) >= 0.001:
        # 先用旧的 guess 计算等号右边，再把计算结果存回 guess。
        # 每轮循环都用新猜测值替换旧猜测值。
        guess = (guess + x / guess) / 2

    # 循环结束说明误差已满足停止条件，将最终猜测值交给调用者。
    return guess


# 两个版本都保留老师原算法的初值、更新公式和误差标准。
# 本题按普通正数输入理解，不额外加入通用数值库的输入检查。
# 原方法在接近 0 时相对精度较差；例如输入 0 会返回 0.03125。
# 原方法不支持负数的实数平方根，极端大数也可能遇到浮点数限制。
# 这些是原教学算法的边界；任务 1 要求不做其他简化，因此保留其行为。


# =====================================================================
# Task 3：log 装饰器——记录函数名、参数和返回值
# =====================================================================
# 函数也可以作为参数传给另一个函数，并作为返回值返回。
# 装饰器 log(func) 接收原函数，返回一个增加了日志功能的新函数。
#
# 写法：
#     @log
#     def helperfunction(a, b):
#         return a + b
#
# 等价于先定义 helperfunction，再执行：
#     helperfunction = log(helperfunction)
#
# 注意两个时刻：
# 1. 执行带 @log 的函数定义时，调用 log，得到 wrapper。
# 2. 以后调用 helperfunction(1, 2) 时，实际执行 wrapper(1, 2)。

def log(func):
    """打印一次正常结束的函数调用，并保留原函数的返回值。"""

    @wraps(func)
    def wrapper(*args):
        # 在形参中，*args 把任意数量的位置参数收集成一个元组。
        # 调用 helperfunction(1, 2) 时，args 就是 (1, 2)。
        # 没有参数时，args 是空元组 ()。
        # 在调用表达式 func(*args) 中，星号表示反过来“拆开”元组。
        # 因此 func 接收到两个独立参数 1、2，而不是一个元组参数。
        result = func(*args)

        # repr 把每个参数转换为便于阅读的文字表示。
        # 整数 1、2 变成字符串 "1"、"2"；字符串参数会保留引号。
        # 这行是列表推导式：依次处理 args 中的每一个 arg。
        argument_texts = [repr(arg) for arg in args]

        # 用逗号连接字符串，不加多余空格，以匹配题目示例的 (1,2)。
        # 例如 ["1", "2"] 经过 join 后得到 "1,2"。
        arguments = ",".join(argument_texts)

        # func.__name__ 获取原函数名；f 字符串把大括号中的值嵌入文本。
        print(f"@log: {func.__name__}({arguments}) -> {result}")

        # print 只负责显示；return 才负责把结果交给调用者。
        # 如果漏掉这一行，helperfunction(1, 2) 就会返回 None，而不是 3。
        return result

    # 返回函数本身，供之后调用；这里不能写成 wrapper()。
    # wrapper() 会立刻执行函数，而不是把函数交出去。
    return wrapper


# =====================================================================
# Task 4：timeMe 装饰器——记录函数执行时间
# 要求：使用 time.time()，支持任意数量的位置参数，不要求关键字参数。
# =====================================================================

def timeMe(func):
    """以毫秒打印一次正常调用的耗时，同时返回原函数结果。"""

    @wraps(func)
    def wrapper(*args):
        # 时间戳的单位是秒；先记录函数开始执行前的时间。
        start = time.time()

        # 原函数只执行一次，*args 将接收到的位置参数原样转交给它。
        # 比如 f()、f(1)、f(1, 2, 3) 都可以使用这个包装函数。
        result = func(*args)

        # 当前时间减开始时间，得到经过的秒数；乘 1000 转换为毫秒。
        # 测量范围包括函数内部的计算和 time.sleep 等等待过程。
        elapsed_milliseconds = (time.time() - start) * 1000

        # :.2f 表示以定点数形式保留小数点后两位。
        # 实际时间因电脑和运行情况而异，不需要等于题目示例的具体数值。
        print(f"@timeMe: {elapsed_milliseconds:.2f} milliseconds")

        # 保留原函数返回值；原函数没有显式 return 时，结果就是 None。
        return result

    return wrapper


# =====================================================================
# Task 5：memo 装饰器——缓存已经计算过的结果
# =====================================================================
# Memoization（记忆化）：同一组参数再次出现时，直接使用之前的结果。
# 对 fib 这类由输入决定结果的函数很合适。
# 缓存命中时不会再次执行原函数，所以它并不适合所有有副作用的函数。

def memo(func):
    """为参数可哈希的位置参数调用缓存结果。"""
    # 装饰函数时创建字典；不是每次调用 wrapper 都重新创建。
    # wrapper 通过外层作用域持续使用同一个 cache，这就是闭包的应用。
    # 如果把 cache = {} 放进 wrapper，每次调用都会清空，无法记住结果。
    # 不同函数分别使用 @memo 时，会各自获得一个独立字典。
    cache = {}

    @wraps(func)
    def wrapper(*args):
        # 使用整个参数元组作为键，返回值作为对应的值。
        # fib(5) 的键是 (5,)，双参数函数 f(2, 3) 的键是 (2, 3)。
        # (5,) 中的逗号说明它是单元素元组；(5) 仍然只是数字 5。
        # 字典的键必须可哈希；整数可以，含有列表的参数元组不可以。
        if args not in cache:
            # 没有缓存：真正执行原函数，并保存计算结果。
            cache[args] = func(*args)

        # 已有缓存：跳过上面的计算，直接返回之前存下的结果。
        # 不使用 if cache.get(args)，因为结果 0、False、None 也要缓存。
        return cache[args]

    return wrapper


# 先定义 memo，再使用 @memo；此后名称 fib 指向带缓存的包装函数。
@memo
def fib(n):
    """返回第 n 个斐波那契数；本题约定 n 是非负整数。"""
    # 两个递归出口：fib(0) = 0，fib(1) = 1。
    if n < 2:
        return n
    else:
        # 后一个数等于前两个数之和，例如 fib(5) = fib(4) + fib(3)。
        # 这里通过名称 fib 递归调用，因此递归的子问题也会经过缓存。
        return fib(n - 1) + fib(n - 2)


# 为什么不用缓存时 fib(35) 很慢？
# fib(5) 会计算 fib(4) 和 fib(3)，而 fib(4) 又会计算 fib(3) 和 fib(2)。
# 因此同一个 fib(3) 被重复计算，下面还有更多重复的子问题。
# 输入增大时，普通递归的调用次数呈指数级增长。
# 使用 @memo 后，从空缓存开始算 fib(35)，只需要计算 0 到 35 这 36 种输入。
# 每种输入的结果计算一次，后续调用直接复用，因此避免了大量重复工作。
# 按每次数值运算视为常数耗时的常见分析，首次计算从指数级降为 O(n)，
# 同时需要 O(n) 的缓存和递归栈空间；缓存并没有消除递归本身。


# =====================================================================
# 运行示例：直接执行本文件时才运行；被其他程序 import 时不会运行。
# =====================================================================
# 以下保留题目中的计时示例，会分别等待 1 秒、6 秒，合计约 7 秒。
# __name__ == "__main__" 是“直接运行本文件”的判断条件。

if __name__ == "__main__":
    print("Task 1: Newton's method with inner functions")
    print(newton(4))
    print(newton(9))

    print("\nTask 2: Newton's method with a while loop")
    print(newtonPy(4))
    print(newtonPy(9))

    print("\nTask 3: Logging a function call")

    @log
    def helperfunction(a, b):
        return a + b

    # 第一行日志应为：@log: helperfunction(1,2) -> 3
    # 再显示 helper_result，验证装饰器确实把 3 返回给了调用者。
    helper_result = helperfunction(1, 2)
    print(f"Returned value: {helper_result}")

    print("\nTask 4: Timing functions with different numbers of arguments")

    @timeMe
    def testFunctionTime():
        # 用 total 命名，避免遮住 Python 内置的 sum 函数。
        total = 0
        for i in range(10000):
            total += i

    @timeMe
    def testFunctionTime2(t):
        # 暂停 t 秒，因此计时结果应接近 t * 1000 毫秒。
        time.sleep(t)

    @timeMe
    def testFunctionTime3(*args):
        total = 0
        for a in args:
            total += a
        time.sleep(total)

    testFunctionTime()
    testFunctionTime2(1)
    testFunctionTime3(1, 2, 3)

    print("\nTask 5: Memoized Fibonacci numbers")
    print(f"fib(5) = {fib(5)}")       # 应为 5。
    print(f"fib(35) = {fib(35)}")     # 应为 9227465。
    # map 把 fib 依次应用到 0 至 19；list 收集这些返回值。
    print(list(map(fib, range(20))))
