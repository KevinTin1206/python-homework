# Assignment 5: OO, inheritance, encapsulation: SimpleBank

第五次 Python 作业：用普通账户和学生账户练习类、继承、封装与信息隐藏。

## 文件

- [oo_inheritance.py](oo_inheritance.py)：完整实现，含详细中文注释和题目演示。
- [题目解析.md](题目解析.md)：中文题意、实现思路、重要知识点和预期结果。
- [tests/test_oo_inheritance.py](tests/test_oo_inheritance.py)：根据题意编写的行为测试，不是老师提供的测试。

所有账户功能都实现在 `oo_inheritance.py` 中。运行仅需 Python 3 标准库。

## 运行

在本目录执行：

```sh
python3 oo_inheritance.py
```

运行测试：

```sh
python3 -B -m unittest discover -s tests -v
```

## 账户规则

| 功能 | Account | StudentAccount |
| --- | --- | --- |
| 初始余额 | `0.0` | `0.0` |
| 存款 | 允许 | 继承父类功能 |
| 取款导致负余额 | 允许 | 抛出 `ValueError`，余额不变 |
| 直接赋值 `balance` | 不允许 | 不允许 |
| 参与转账 | 允许 | 允许，仍遵守学生账户的取款限制 |

余额内部为私有 `__balance`，通过只读 `@property` 读取。学生账户继承 `Account` 并重写 `withdraw`。转账方法使用 `@staticmethod`，接口为 `Account.transfer(amount, fromAccount, toAccount)`。

## 题目未明确处的约定

- 金额接受有限、非负的 `int` 或 `float`，允许 `0`；不接受 `bool`、字符串、NaN 或无穷大。
- 错误类型抛出 `TypeError`；负金额、学生账户余额不足等无效操作抛出 `ValueError`。
- 存款、取款和转账正常结束时返回 `None`，余额通过 `.balance` 查询。
- 转账双方必须是不同的账户实例。所有本题账户的预期校验失败均发生在修改余额之前。
- 不增加业务上的普通账户透支限额；超出有限浮点数的表示范围时拒绝操作。
- 余额按题目要求使用 `float`，不额外规定只能输入两位小数；显示格式保留两位小数。

提交前请填写代码开头的实际学号和姓氏。
