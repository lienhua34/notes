# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf

# 加载 matplotlib 工具包，使用该工具可以对预测的 sin 函数曲线进行绘图
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt

learn = tf.contrib.learn

HIDDEN_SIZE = 30               # LSTM 中隐藏节点的个数
NUM_LAYERS = 2                 # LSTM 的层数
TIMESTEPS = 10                 # 循环神经网络的截断长度
TRAINING_STEPS = 10000         # 训练轮数
BATCH_SIZE = 32                # batch 大小

TRAINING_EXAMPLES = 10000      # 训练数据个数
TESTING_EXAMPLES = 1000        # 测试数据个数
SAMPLE_GAP = 0.01              # 采样间隔

def generate_data(seq):
    X = []
    y = []

    # 序列的第 i 项和后面的 TIMESTEPS-1 项合在一起做为输入；第 i + TIMESTEPS 项作为输出。
    # 即用 sin 函数前面的 TIMESTEPS 个点的信息，预测第 i + TIMESTEPS 个点的函数值。
    for i in range(len(seq) - TIMESTEPS - 1):
        X.append([seq[i: i + TIMESTEPS]])
        y.append([seq[i + TIMESTEPS]])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

def lstm_model(X, y):
    # 使用多层 LSTM 结构。
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(HIDDEN_SIZE)
    cell = tf.contrib.rnn.MultiRNNCell([lstm_cell] * NUM_LAYERS)
    x_ = tf.unstack(X, axis=1)

    # 使用 TensorFlow 接口将多层的 LSTM 结构连接成 RNN 网络并计算其前向传播结果。
    output, _ = tf.contrib.rnn.static_rnn(cell, x_, dtype=tf.float32)
    # 在本问题中只关注最后一个时刻的输出结果，该结果为下一时刻的预测值。
    output = output[-1]

    # 对 LSTM 网络的输出再做加一层全连接层并计算损失。注意这里默认的损失为平均平方差
    # 损失函数。
    prediction, loss = learn.models.linear_regression(output, y)

    train_op = tf.contrib.layers.optimize_loss(
        loss, tf.contrib.framework.get_global_step(),
        optimizer="Adagrad", learning_rate=0.1)

    return prediction, loss, train_op

# 建立深层循环网络模型。
regressor = learn.Estimator(model_fn=lstm_model)

# 用正弦函数生成训练和测试数据集合。
# numpy.linspace 函数可以创建一个等差序列的数组，它常用的参数有三个参数，第一个参数
# 表示起始值，第二个参数表示终止值，第三个参数表示训练的长度。例如，linspace(1, 10, 10)
# 产生的数组是 array([1,2,3,4,5,6,7,8,9,10])。
test_start = TRAINING_EXAMPLES * SAMPLE_GAP
test_end = (TRAINING_EXAMPLES + TESTING_EXAMPLES) * SAMPLE_GAP
train_X, train_y = generate_data(np.sin(np.linspace(
    0, test_start, TRAINING_EXAMPLES, dtype=np.float32)))
test_X, test_y = generate_data(np.sin(np.linspace(
    test_start, test_end, TESTING_EXAMPLES, dtype=np.float32)))

# 调用 fit 函数训练模型。
regressor.fit(train_X, train_y, batch_size=BATCH_SIZE, steps=TRAINING_STEPS)

# 使用训练好的模型对测试数据进行预测。
predicted = [[pred] for pred in regressor.predict(test_X)]
# 计算 rmse 作为评价指标。
rmse = np.sqrt(((predicted - test_y) ** 2).mean(axis=0))
print("Mean Square Error is: {0}".format(rmse[0]))

# 对预测的 sin 函数曲线进行绘图，并存储到运行目录下的 sin.png
fig = plt.figure()
plot_predicted = plt.plot(predicted, label='predicted')
plot_test = plt.plot(test_y, label='real_sin')
plt.legend([plot_predicted, plot_test], ['predicted', 'real_sin'])
fig.savefig('sin.png')

