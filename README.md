## Rasa Milk Tea Chatbot  (chinese)

a milk tea waiter chatbot for chinese, if you don't know rasa yet, refer to `mini rasa tutorial` below 

or read the [rasa offical docs](https://rasa.com/docs/rasa/1.1.8/)

- ### installation

  you need to **download** bert_chinese_model **and unzip it** first:  [chinese_L-12_H-768_A-12](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)

  ~~~shell
  git clone https://github.com/BI4O/rasa_milktea_chatbot.git
  cd rasa_milktea_chatbot
  pip install -r requirements.txt -i https://pypi.tuan.tsinghua.edu.cn/simple
  ~~~

- ### quick start

  1. start bert server

     `bert-serving-start -model_dir path/to/chinese_L-12_H-768_A-12/ -num_worker=1`

  2. jump to milktea

     `cd milktea`

  3. start action server

     `rasa run actions`

  4. train a model

     `rasa train`

  5. talk to your chatbot

     `rasa shell`

     you can order 3 different products，more can be added to model yourself

     - 奶茶
     - 咖啡
     - 卡布奇诺

     and choose 3 sizes

     - 中
     - 大
     - 特大

- ### mini rasa tutorial

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

     | \_\_init\_\_.py            | 空文件用于定位                     |
     | -------------------------- | ---------------------------------- |
     | actions.py                 | 用于定义动作（自定义脚本代码）     |
     | config.yml                 | 配置NLU和core模型                  |
     | credentials.yml            | 连接到其他服务器的细节（不常用）   |
     | data/nlu.md                | 我的自定义NLU训练数据              |
     | data/stories.md            | 我的自定义故事stories              |
     | domain.yml                 | 助手的定义域domian                 |
     | endpoints.yml              | 连接到fb message等的轨道（不常用） |
     | models/\<timestamp>.tar.gz | 模型及其参数文件                   |

  2. #### 自定义NLU训练数据

     `cat data/nlu.md`

     显示如下

     ~~~shell
     ## intent:order
     - [奶茶](type)
     - [咖啡](type)
     - 我想要一杯[奶茶](type)
     - 要杯[奶茶](type)
     - 有[奶茶](type)吗
     - 有[奶茶](type)卖吗
     - 想要一杯[咖啡](type)
     - 要杯[咖啡](type)
     - 有[咖啡](type)吗
     - 我想要一杯[卡布奇诺](type)
     - 要杯[卡布奇诺](type)
     - [卡布奇诺](type)
     
     ## intent:inform_size
     - [中](size)
     - [中](size)的
     - [中](size)杯
     - [中](size)杯吧
     - 要[中](size)杯
     - [大](size)
     - [大](size)的
     - [大](size)杯
     - [大](size)杯吧
     - 要[大](size)杯
     - [特大](size)
     - [特大](size)的 
     - [特大](size)杯
     - [特大](size)杯吧
     - 要[特大](size)杯
     ~~~
     
     - intent
       表示意图，需要以##开头，以换行结尾。比如说这里显示的是两个意图1. 下单，2. 告知奶茶的规格，所有客户可能会用的说辞都应该放在这里，用于nlu模型学习怎么去理解一个人说的话
     
     - `[value](entity)`
       entity表示实体，value表示实体具体的值，经过训练后，nlu模型就可以给core模型返回类似这样的变量：`{"type":"奶茶","size":"大"}`，这样core模型就可以根据`type`和`size`这两个参数做出相应的回应
     
  3. #### 定义模型配置
  
     1. 配置文件`config.yml`将定义前面的NLU模块和你的模型会用到的Core元素，本次使用的是来自大神写好的组件，这里也强烈推荐大家前往学习https://github.com/GaoQ1/rasa_nlu_gq
     2. NLU的配置属于决定了使用的语言和管道，Core的policies的关键词决定了模型见会使用到的策略policies
     3. note: 如果你只是想建立一个chatbot而不想了解太多关于算法的细节，config.yml可以不用改，直接用

  4. #### 自定义故事
  
     查看写好的故事
  
     `cat data/stories.md`
  
     ~~~shell
     ## order naicha
     - order{"type": "奶茶"}
       - slot{"type": "奶茶"}
       - utter_ask_size
     - inform_size{"size": "大"}
       - slot{"size": "大"}
       - utter_affirm
       - confirm
       - action_charge
       - utter_goodbye
     ~~~

     **故事的组成**
  
     1. `##`开头表示的是这个**故事的名称**，一个描述性的名字
     2. 故事以换行结束，下一个故事`##`开头
     3. `*`开头的表示为**用户意图**
        `intent{"entity1": "value", "entity2": "value"}`
     4. `-`开头的表示为机器人执行的**动作**actions
        
  
     **用户信息**
  
     1. 在定义故事的时候，不需要知道用户具体说了什么，而是根据NLU pipeline中输出的意图intent和实体entity的组合来猜测用户的所有可能的需求
     2. 实体entity是很重要的，因为助手学习动作的时候，需要同时结合这两者
        
  
     **动作acitons**
  
     ​	actions有两种类型
  
     1. utter_xxx 可以直接返回要回复的话术，只需要在domain.yml中说明就可以用了
  
     2. action_xxx 可以执行你想要的自定义操作，除了需要在domain.yml中说明外，还需要在aciton.py文件中添加。比如你想有一个自定义动作`action_HelloWorld`
  
        - 首先把这个自定义动作添加到domain.yml的acitons下
        
          ~~~
          actions:
          - aciton_HelloWorld
          ~~~
        
        - 然后在acitons.py文件中添加新的类
        
          ~~~python
          class YourCustomAction(Action):
              def name(self):
                  # 这个返回的值必须和stories.md和domain.yml中说明的一致
                  return "action_HelloWorld"
              def run(self,dispatcher,tracker,domain):
                  # 定义这个动作要执行的你想要的操作
                  # 比如我想在对话中返回给用户的是HellowWorld!
                  dispatcher.utter_message('HelloWorld!')
                  return []
  
  5. #### 定义域domain
  
     `cat domain.yml`
  
       ~~~shell
       intents:  
         - greet:
           triggers: utter_greet
         - goodbye:
           triggers: utter_goodbye
         - confirm
         - deny
         - order
         - thanks
         - inform_size
         - unknown_intent
          
       actions: 
         - utter_greet
         - utter_ask_order_what
         - utter_ask_size
          
       entities:
         - type
         - size
       
       slots:
         type:
           type: text
         size:
           type: text
          
       templates:
         utter_greet:
           - text: "你好"
         utter_ask_order_what:
           - text: "想要喝点什么？"
         utter_ask_size:
           - text: "想要什么规格的呢？我们有中/大/特大杯"
     ~~~
  
     其中
  
       1. intents：用户意图
       2. entities：实体
       3. slots：槽
       4. actions：助手说和做的事情
       5. templates：助手根据actions具体要做的事情

       因为在这种情况下，我们的动作action只是向用户发送话语作为回复，这些简单的actions都是`utter_`开头的动作actions，这种动作需要助手在templates中选择语句进行回复，实际上还可以定义更多的动作见`Custom Actions`

    6. #### 训练模型
  
     使用下面的命令，会自动检查domain/stories/NLU中的不同而重新对模型进行训练，训练好的模型将会被打上时间戳time stamp作为新的模型
         `rasa train`
  
    7. #### 启动助手进行对话

          `rasa shell`

  
  
  
