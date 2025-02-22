from src.common.log import log_method




class MyClass:
    def __init__(self, name):
        self.name = name

    @log_method  # 控制台输出日志
    def say_hello(self, greeting):
        return f"{greeting}, {self.name}!"
    
    @log_method  # 文件输出日志
    def divide(self, a, b):
        return a / b

# 示例调用
obj = MyClass("Alice")

# 控制台输出日志
obj.say_hello("Hi")

# 文件输出日志
obj.divide(10)
