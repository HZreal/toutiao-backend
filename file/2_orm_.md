
### 使用ORM的方式选择

先创建模型类，再迁移到数据库中

    优点：简单快捷，定义一次模型类即可，不用写sql
    缺点：不能尽善尽美的控制创建表的所有细节问题，表结构发生变化的时候，也会难免发生迁移错误
先用原生SQL创建数据库表，再编写模型类作映射

    优点：可以很好的控制数据库表结构的任何细节，避免发生迁移错误
    缺点：可能编写工作多（编写sql与模型类，似乎有些牵强）

### 基于python语言的orm软件SQLAlchemy

SQLAlchemy是Python实现的开源软件。提供了SQL工具包及对象关系映射（ORM）工具

SQLAlchemy“采用简单的Python语言，为高效和高性能的数据库访问设计，实现了完整的企业级持久模型”。

Flask-SQLAlchemy是在Flask框架的一个扩展，其对SQLAlchemy进行了封装，目的于简化在 Flask 中 SQLAlchemy 的 使用，提供了有用的默认值和额外的助手来更简单地完成日常任务。

安装Flask-SQLAlchemy，还需要安装MySQL的Python客户端库即驱动

    pip install flask-sqlalchemy
    

数据库连接配置，如mysql

    SQLALCHEMY_DATABASE_URI 数据库的连接信息
    mysql://user:password@localhost/mydatabase
    SQLALCHEMY_TRACK_MODIFICATIONS 在Flask中是否追踪数据修改
    SQLALCHEMY_ECHO 显示生成的SQL语句，可用于调试

这些配置参数需要放在Flask的应用配置（app.config）中

模型类字段与选项

构建模型类映射






