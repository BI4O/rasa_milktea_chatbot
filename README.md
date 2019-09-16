## Rasa使用指南

- ### 安装

  ~~~python
  pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
  ~~~

- ### 教程

  > 1. 创建一个新的项目
  > 2. 查看NLU培训数据
  > 3. 定义模型配置，写下第一个故事Story
  > 4. 定义这个故事story的作用域domain
  > 5. 训练模型
  > 6. 测试你写好的助手

  1. #### 创建新项目

     路径指向一个新的空文件夹
     `cd path/to/a/blank/folder`

     在这个文件夹里面创建新的rasa项目
     `rasa init --no-prompt`

     文件夹中将会生成以下的文件：

     | \_\_init\_\_.py            | 空文件用于定位                 |
     | -------------------------- | ------------------------------ |
     | actions.py                 | 用于定义动作（自定义脚本代码） |
     | config.yml                 | 配置NLU和core模型              |
     | credentials.yml            | 连接到其他服务器的细节         |
     | data/nlu.md                | 我的自定义NLU训练数据          |
     | data/stories.md            | 我的自定义故事stories          |
     | domain.yml                 | 助手的定义域domian             |
     | endpoints.yml              | 连接到fb message等的轨道       |
     | models/\<timestame>.tar.gz | 模型及其参数文件               |

  2. #### 查看NLU训练数据

     `cat data/nlu.md`

     显示如下

     ~~~shell
     ## intent:check_balance
     - what is my balance <!-- no entity -->
     - how much do I have on my [savings](source_account) <!-- entity "source_account" has value "savings" -->
     - how much do I have on my [savings account](source_account:savings) <!-- synonyms, method 1-->
     - Could I pay in [yen](currency)?  <!-- entity matched by lookup table -->
     
     ## intent:greet
     - hey
     - hello
     
     ## synonym:savings   <!-- synonyms, method 2 -->
     - pink pig
     
     ## regex:zipcode
     - [0-9]{5}
     
     ## lookup:currencies   <!-- lookup table list -->
     - Yen
     - USD
     - Euro
     
     ## lookup:additional_currencies  <!-- no list to specify lookup table file -->
     path/to/currencies.txt
     ~~~

     也就是说，训练数据可以有不同的几个部分构成

     - 常见的例子（写死的回复语句）

       常见的例子intent是比较固定的回复语句

     - 根据同义词匹配synonyms

       同义词synonyms将intent中提取的实体映射到享用的名称，比如将提取出来的实体`my savings acount`映射到`savings`

     - 正则匹配regex

     - 查询表lookup tables

  3. #### 定义模型配置

     配置文件`config.yml`将定义前面的NLU模块和你的模型会用到的Core元素，本次将会使用supervise_embeddings管道pipline
     `cat config.yml`

     ~~~~python
     # Configuration for Rasa NLU.
     # https://rasa.com/docs/rasa/nlu/components/
     language: en
     pipeline: supervised_embeddings
     
     # Configuration for Rasa Core.
     # https://rasa.com/docs/rasa/core/policies/
     policies:
       - name: MemoizationPolicy
       - name: KerasPolicy
       - name: MappingPolicy
     ~~~~

     NLU的配置属于决定了使用的语言和管道，Core的policies的关键词决定了模型见会使用到的策略policies

  4. #### 写下第一个故事

     查看写好的故事

     `cat data/stories.md`

     ~~~shell
     ## happy path
     * greet
       - utter_greet
     * mood_great
       - utter_happy
     
     ## sad path 1
     * greet
       - utter_greet
     * mood_unhappy
       - utter_cheer_up
       - utter_did_that_help
     * affirm
       - utter_happy
     
     ## sad path 2
     * greet
       - utter_greet
     * mood_unhappy
       - utter_cheer_up
       - utter_did_that_help
     * deny
       - utter_goodbye
     ~~~

     在以上的例子中，助手都是直接回复文字作为回应，但是实际上还可以有其他的动作，包括call api

     **故事的组成**

     1. `##`开头表示的是这个**故事的名称**，一个描述性的名字
     2. 故事以换行结束，下一个故事`##`开头
     3. `*`开头的表示为**用户意图**
        `intent{"entity1": "value", "entity2": "value"}`
     4. `-`开头的表示为机器人执行的**动作**

     **用户信息**

     1. 在定义故事的时候，不需要知道用户具体说了什么，而是根据NLU pipeline中输出的意图intent和实体entity的组合来猜测用户的所有可能的需求
     2. 实体entity是很重要的，因为助手学习动作的时候，需要同时结合这两者

     ##### 动作atcions

  5. #### 定义域domain

     `cat domain.yml`

     ~~~shell
     intents:
       - greet
       - goodbye
       - affirm
       - deny
       - mood_great
       - mood_unhappy
     
     actions:
     - utter_greet
     - utter_cheer_up
     - utter_did_that_help
     - utter_happy
     - utter_goodbye
     
     templates:
       utter_greet:
       - text: "Hey! How are you?"
     
       utter_cheer_up:
       - text: "Here is something to cheer you up:"
         image: "https://i.imgur.com/nGF1K8f.jpg"
     
       utter_did_that_help:
       - text: "Did that help you?"
     
       utter_happy:
       - text: "Great carry on!"
     
       utter_goodbye:
       - text: "Bye"
     ~~~

     其中

     1. intents：用户意图
     2. entities：实体
     3. slots：槽
     4. actions：助手说和做的事情
     5. templates：助手根据actions具体要做的事情

     因为在这种情况下，我们的动作action只是向用户发送话语作为回复，这些简单的actions都是`utter_`开头的动作actions，这种动作需要助手在templates中选择语句进行回复，实际上还可以定义更多的动作见`Custom Actions`

  6. #### 训练模型

     因为随着业务的发展，我们需要对NLU和Core Data进行更新，使用下面的命令，会自动检查domain/stories/NLU中的不同而重新对模型进行训练，训练好的模型将会被打伤时间戳time stamp作为新的模型
     `rasa train`

  7. #### 启动助手进行对话

     `rasa shell`

     