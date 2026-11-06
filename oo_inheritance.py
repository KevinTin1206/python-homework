### Assignment oo_inheritance ###

# s123456_s56789, YourLastname1_YourLastname2
# 提交前请把上一行替换为实际提交者的学号和姓氏。
#
# 本次作业：用类、继承、封装、信息隐藏实现一个简易银行账户系统。
# 所有实现都在本文件中；直接运行可查看题目中的演示。
# 只使用 Python 标准库，不需要安装第三方依赖。
#
# 对题目未明确之处，采用以下约定：
# 1. 金额接受 int 或 float，但不接受 bool、字符串、负数、无穷大和 NaN。
# 2. 金额类型错误抛出 TypeError；负金额等无效数值抛出 ValueError。
# 3. 学生账户余额不足时抛出 ValueError，余额不变。
# 4. 零金额合法；成功的存款、取款、转账不返回新余额，即返回 None。
# 5. 转账双方必须是 Account 或其子类的实例，且必须是两个不同的账户。
# 6. 余额按题目要求使用 float；超出有限 float 表示范围时拒绝操作。
# 这些是本实现的约定，不是额外引用的老师要求。

import math


class Account:
    """普通银行账户：允许余额为负，也允许在已透支时继续取款。"""

    def __init__(self, owner):
        """创建账户，保存户主姓名，并将余额初始化为 0.0。"""
        # self 表示“当前这个账户对象”。
        # Account("A") 和 Account("B") 会创建两个独立的对象。
        self.owner = owner

        # 双下划线 __balance 表示私有属性，满足题目 PRIVATE 的要求。
        # 不要写成类变量，否则可能错误地让所有账户共享一份状态。
        # 这里为每个对象分别初始化余额，0.0 也明确表示浮点数。
        self.__balance = 0.0

    @property
    def balance(self):
        """允许通过 account.balance 读取余额，但不允许直接赋值。"""
        # @property 把这个方法变成可以像属性一样读取的接口。
        # 外部写 account.balance，而不是 account.balance()。
        # 这里只提供 getter，没有 @balance.setter，所以：
        # account.balance = 999 会抛出 AttributeError。
        # 正常修改余额必须通过 deposit 或 withdraw。
        return self.__balance

    @staticmethod
    def _validate_amount(amount):
        """内部辅助方法：检查金额，并返回统一的 float 表示。"""
        # 这个辅助方法不依赖某个具体账户，所以不需要 self。
        # 单下划线表示供类内部和子类使用的辅助接口；余额本身仍是私有的。
        # isinstance(True, int) 为 True，因此需要单独排除 bool。
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("Amount must be an int or float, not bool.")

        # 统一成 float，使所有余额更新都保持题目要求的浮点数类型。
        # 极大的整数可能无法转换为 float；将其作为无效金额处理。
        try:
            amount = float(amount)
        except OverflowError:
            raise ValueError("Amount is outside the finite float range.") from None

        # NaN 表示“不是一个数”；只判断 amount < 0 无法排除 NaN。
        # math.isfinite 排除 NaN 和正负无穷大，避免余额被这些值污染。
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("Amount must be finite and non-negative.")

        return amount

    def deposit(self, amount):
        """存款：增加余额，拒绝负金额。"""
        # 必须先检查，再修改。输入不合法时，下面的余额更新不会执行。
        amount = self._validate_amount(amount)
        new_balance = self.__balance + amount

        # 两个有限浮点数相加仍可能超出 float 范围。
        # 在真正赋值之前检查，失败时保留原余额。
        if not math.isfinite(new_balance):
            raise ValueError("The resulting balance is outside the finite float range.")

        self.__balance = new_balance
        # 没有显式 return 的方法正常结束时会返回 None。
        # 调用者通过 account.balance 查询更新后的余额。

    def withdraw(self, amount):
        """取款：减少余额；普通账户不设置业务上的透支额度。"""
        amount = self._validate_amount(amount)
        new_balance = self.__balance - amount

        # 这里只检查计算机浮点数的表示范围，不设置银行业务上的透支限额。
        # 普通账户从 0 取 100 后是 -100，还可以继续取 600 变成 -700。
        if not math.isfinite(new_balance):
            raise ValueError("The resulting balance is outside the finite float range.")

        self.__balance = new_balance

    @staticmethod
    def transfer(amount, fromAccount, toAccount):
        """从 fromAccount 向 toAccount 转账，支持普通账户和学生账户。"""
        # 静态方法不会自动接收 self。调用方式严格按题目给定的顺序：
        # Account.transfer(金额, 转出账户, 转入账户)。
        # isinstance 也认可子类，因此 StudentAccount 可以通过此检查。
        if not isinstance(fromAccount, Account) or not isinstance(toAccount, Account):
            raise TypeError("Both transfer endpoints must be Account instances.")

        amount = Account._validate_amount(amount)

        # is 比较是否为同一个对象；两个同名户主仍然可以有不同的账户。
        if fromAccount is toAccount:
            raise ValueError("A transfer requires two different accounts.")

        # 在任何余额发生变化前，先排除接收方入账会溢出的情况。
        # 否则可能出现转出已扣钱、转入却因无法存储结果而失败的问题。
        if not math.isfinite(toAccount.balance + amount):
            raise ValueError("The receiving balance would exceed the finite float range.")

        # 关键：先扣款成功，再入账；如果 withdraw 抛异常，后一句不会执行。
        # 这样学生账户余额不足时，双方余额都保持不变。
        #
        # 这里通过对象调用 withdraw，不能写 Account.withdraw(fromAccount, amount)。
        # 对象是 StudentAccount 时，会自动选中子类重写的 withdraw。
        # 这体现了多态：相同的方法调用，根据实际对象使用不同实现。
        fromAccount.withdraw(amount)
        toAccount.deposit(amount)

    def __str__(self):
        """让 print(account) 显示账户类型、户主和余额。"""
        # print(account) 会调用 __str__，而不是只显示对象的内存信息。
        # type(self).__name__ 可区分 Account 和 StudentAccount。
        # :.2f 只控制显示两位小数，不会把实际保存的余额四舍五入。
        return f"{type(self).__name__}(owner={self.owner}, balance={self.balance:.2f})"


class StudentAccount(Account):
    """学生账户：继承普通账户，但不允许透支。"""
    # 括号中的 Account 表示父类；StudentAccount 是子类。
    # 没有重写 __init__，所以会继承父类的构造方法，初始余额也是 0.0。
    # deposit、balance、transfer、__str__ 都可以直接继承，不必重复编写。

    def withdraw(self, amount):
        """在父类取款功能前增加余额不足检查。"""
        # 先检查金额类型和数值，避免拿字符串等无效金额去比较余额。
        amount = self._validate_amount(amount)

        # 只有“金额大于余额”才拒绝；恰好取完所有钱是允许的。
        # 检查发生在扣款之前，因此拒绝后余额不会变化。
        if amount > self.balance:
            raise ValueError("Insufficient funds: a student account cannot be overdrawn.")

        # 子类通过父类的只读属性读取余额，不另建 self.__balance。
        # Python 会对双下划线属性做名称改写：
        # 父类的 __balance 是 _Account__balance；
        # 子类若再写 __balance，会成为另一个 _StudentAccount__balance。
        # 所以通过 super 调用父类方法，复用同一份余额和更新规则。
        # 父类会再次校验金额，这是复用父类方法时保留的统一检查。
        super().withdraw(amount)


# =====================================================================
# 题目演示：直接运行本文件时执行，import 时不会自动创建账户或打印。
# =====================================================================
if __name__ == "__main__":
    a1 = Account("A")
    a2 = Account("B")
    a1.deposit(100)
    a2.withdraw(100)                 # 普通账户可透支，a2 的余额变成 -100。
    print(a1)
    print(a2)

    Account.transfer(600, a1, a2)     # a1 变成 -500，a2 变成 500。
    print(a1)
    print(a2)

    print(a1.owner)                  # 读取户主姓名 A。
    print(a1.balance)                # 读取余额 -500.0，不需要调用括号。

    # a1.balance = 999               # 禁止直接赋值，取消注释会产生 AttributeError。

    s1 = StudentAccount("S")
    s1.deposit(100)

    try:
        Account.transfer(500000, s1, a1)
    except ValueError as error:
        # withdraw 抛出异常并提供原因；演示代码捕获后负责显示错误。
        # 不使用空的 except，避免把无关程序错误也当成余额不足。
        print(f"Fehler: {error}")

    print(s1)                        # 转账失败，仍然是 100。
    print(a1)                        # 接收方没有被错误入账，仍然是 -500。
