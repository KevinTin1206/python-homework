# 牛顿法原始程序：中文注释对照版
# 保留 Downloads/newton.py 的六个函数、参数和计算逻辑。
# 它用于理解原算法；作业任务 1、2 的改写位于 hop_decorator.py。
#
# 原文件说明：本程序根据 Abelson/Sussman 的
# Structure and Interpretation of Computer Programs（书本页码 28）
# 中的 LISP 平方根算法改写为 Python。
# 原文件给出的来源：https://web.mit.edu/6.001/6.037/sicp.pdf
#
# 目标：给定 x，找一个数 guess，使 guess * guess 足够接近 x。
# 比如 x = 9 时，我们希望最后得到接近 3 的结果。
# 方法：从 1.0 开始，不断使用 (guess + x / guess) / 2 改进猜测值。


def square(x):
    """计算平方。"""
    # 例如 square(3) 返回 9；return 返回结果，不负责打印。
    return x * x


def average(x, y):
    """计算两个数的平均值。"""
    # 先计算括号中的和，再除以 2。
    return (x + y) / 2


def isGoodEnough(guess, x):
    """检查猜测值的平方是否已经足够接近目标 x。"""
    # guess 是当前猜测值；x 是要求平方根的目标数。
    # abs 取绝对值；比较表达式的结果为 True 或 False。
    # 注意：误差标准针对 guess 的平方，不保证平方根的小数位数。
    return abs(square(guess) - x) < 0.001


def improve(guess, x):
    """根据当前猜测值计算一个更好的猜测值。"""
    # 对正数 x 和正的 guess：
    # guess 小于平方根时，x / guess 大于平方根；反过来也成立。
    # 将这两个值取平均，可以逐渐得到更准确的猜测。
    # 例如 x = 9、guess = 1 时，下一次猜测是 (1 + 9) / 2 = 5。
    # guess 不能为 0，否则 x / guess 会产生除零错误。
    return average(guess, x / guess)


def sqrtIter(guess, x):
    """通过递归不断检查和改进猜测值。"""
    # 每次调用都先检查是否满足停止条件。
    if isGoodEnough(guess, x):
        # 满足条件：返回答案，不再继续递归。
        return guess
    else:
        # 不满足条件：先算 improve(guess, x)，再递归调用 sqrtIter。
        # 下一层调用接收新的 guess，但目标 x 始终不变。
        # return 把下一层得到的答案传回本层，再逐层传给最初的调用者。
        return sqrtIter(improve(guess, x), x)


def newton(x):
    """从猜测值 1.0 开始，求 x 的近似平方根。"""
    # 调用者只需要提供 x，不必自己选择初值或调用其他辅助函数。
    return sqrtIter(1.0, x)


# 执行 newton(9) 时的调用顺序：
# newton(9)
#   -> sqrtIter(1.0, 9)
#   -> sqrtIter(5.0, 9)
#   -> sqrtIter(3.4, 9)
#   -> sqrtIter(3.023529411764706, 9)
#   -> sqrtIter(3.00009155413138, 9)
# 最后一个猜测值的平方与 9 的差的绝对值小于 0.001，因此停止。
#
# 与任务 1 对照：
# 原程序每次都把 x 传给辅助函数；任务 1 把它们移入 newton，
# 使它们直接读取外层的 x，从而省去重复的 x 参数。
#
# 原算法边界：普通正数是本题的预期输入。
# 输入 0 会返回 0.03125；负数没有实数平方根，也未做输入检查。
# 接近 0 或非常大的输入可能受到误差标准、浮点精度和递归深度限制。
# 这里保留原算法，不额外改变这些行为。

# 与原文件一样，演示默认注释掉；取消下面三行的注释即可直接运行。
# if __name__ == "__main__":
#     print(newton(4))
#     print(newton(9))
