# As usual, a bit of setup
import matplotlib.pyplot as plt

from cs231n.fast_layers import *

plt.rcParams['figure.figsize'] = (10.0, 8.0)  # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


# for auto-reloading external modules
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython

def rel_error(x, y):
    """ returns relative error """
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))


#############################################################################
# Load the (preprocessed) CIFAR10 data.

# data = get_CIFAR10_data()
# for k, v in data.iteritems():
#     print '%s: ' % k, v.shape

#############################################################################
# Convolution: Naive forward pass

# x_shape = (2, 3, 4, 4)  # [N x C x H x W]
# w_shape = (3, 3, 4, 4)  # (F, C, HH, WW)
# print "w_shape"
# print w_shape
# x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
# w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
# print "w"
# print w
# print "x"
# print x
# b = np.linspace(-0.1, 0.2, num=3)
#
# conv_param = {'stride': 2, 'pad': 1}
# out, _ = conv_forward_naive(x, w, b, conv_param)
# correct_out = np.array([[[[[-0.08759809, -0.10987781],
#                            [-0.18387192, -0.2109216]],
#                           [[0.21027089, 0.21661097],
#                            [0.22847626, 0.23004637]],
#                           [[0.50813986, 0.54309974],
#                            [0.64082444, 0.67101435]]],
#                          [[[-0.98053589, -1.03143541],
#                            [-1.19128892, -1.24695841]],
#                           [[0.69108355, 0.66880383],
#                            [0.59480972, 0.56776003]],
#                           [[2.36270298, 2.36904306],
#                            [2.38090835, 2.38247847]]]]])
#
# # Compare your output to ours; difference should be around 1e-8
# print 'Testing conv_forward_naive'
# print 'difference: ', rel_error(out, correct_out)
#############################################################################
# Aside: Image processing via convolutions

# from scipy.misc import imread, imresize
#
# kitten, puppy = imread('kitten.jpg'), imread('puppy.jpg')
# print "kitten"
# print kitten.shape
# print "puppy"
# print puppy.shape
#
# # kitten is wide, and puppy is already square
# d = kitten.shape[1] - kitten.shape[0]
# kitten_cropped = kitten[:, d/2:-d/2, :]
#
# img_size = 200   # Make this smaller if it runs too slow
# x = np.zeros((2, 3, img_size, img_size))
# x[0, :, :, :] = imresize(puppy, (img_size, img_size)).transpose((2, 0, 1))
# x[1, :, :, :] = imresize(kitten_cropped, (img_size, img_size)).transpose((2, 0, 1))
#
# # Set up a convolutional weights holding 2 filters, each 3x3
# w = np.zeros((2, 3, 3, 3))
#
# # The first filter converts the image to grayscale.
# # Set up the red, green, and blue channels of the filter.
# w[0, 0, :, :] = [[0, 0, 0], [0, 0.3, 0], [0, 0, 0]]
# w[0, 1, :, :] = [[0, 0, 0], [0, 0.6, 0], [0, 0, 0]]
# w[0, 2, :, :] = [[0, 0, 0], [0, 0.1, 0], [0, 0, 0]]
#
# # Second filter detects horizontal edges in the blue channel.
# w[1, 2, :, :] = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
#
# # Vector of biases. We don't need any bias for the grayscale
# # filter, but for the edge detection filter we want to add 128
# # to each output so that nothing is negative.
# b = np.array([0, 128])
#
# # Compute the result of convolving each input in x with each filter in w,
# # offsetting by b, and storing the results in out.
# out, _ = conv_forward_naive(x, w, b, {'stride': 1, 'pad': 1})
#
# def imshow_noax(img, normalize=True):
#     """ Tiny helper to show images as uint8 and remove axis labels """
#     if normalize:
#         img_max, img_min = np.max(img), np.min(img)
#         img = 255.0 * (img - img_min) / (img_max - img_min)
#     plt.imshow(img.astype('uint8'))
#     plt.gca().axis('off')
#
# # Show the original images and the results of the conv operation
# plt.subplot(2, 3, 1)
# imshow_noax(puppy, normalize=False)
# plt.title('Original image')
# plt.subplot(2, 3, 2)
# imshow_noax(out[0, 0])
# plt.title('Grayscale')
# plt.subplot(2, 3, 3)
# imshow_noax(out[0, 1])
# plt.title('Edges')
# plt.subplot(2, 3, 4)
# imshow_noax(kitten_cropped, normalize=False)
# plt.subplot(2, 3, 5)
# imshow_noax(out[1, 0])
# plt.subplot(2, 3, 6)
# imshow_noax(out[1, 1])
# plt.show()

#############################################################################
# Convolution: Naive backward pass

# x = np.random.randn(4, 3, 5, 5)
# w = np.random.randn(2, 3, 3, 3)
# b = np.random.randn(2,)
# dout = np.random.randn(4, 2, 5, 5)
# conv_param = {'stride': 1, 'pad': 1}
#
# dx_num = eval_numerical_gradient_array(lambda x: conv_forward_naive(x, w, b, conv_param)[0], x, dout)
# dw_num = eval_numerical_gradient_array(lambda w: conv_forward_naive(x, w, b, conv_param)[0], w, dout)
# db_num = eval_numerical_gradient_array(lambda b: conv_forward_naive(x, w, b, conv_param)[0], b, dout)
#
# out, cache = conv_forward_naive(x, w, b, conv_param)
# dx, dw, db = conv_backward_naive(dout, cache)
#
# # Your errors should be around 1e-9'
# print 'Testing conv_backward_naive function'
# print 'dx error: ', rel_error(dx, dx_num)
# print 'dw error: ', rel_error(dw, dw_num)
# print 'db error: ', rel_error(db, db_num)
#############################################################################
# Max pooling: Naive forward

# x_shape = (2, 3, 4, 4)
# x = np.linspace(-0.3, 0.4, num=np.prod(x_shape)).reshape(x_shape)
# pool_param = {'pool_width': 2, 'pool_height': 2, 'stride': 2}
#
# out, _ = max_pool_forward_naive(x, pool_param)
#
# # [2,3,2,2]
# correct_out = np.array([[[[-0.26315789, -0.24842105],
#                           [-0.20421053, -0.18947368]],
#                          [[-0.14526316, -0.13052632],
#                           [-0.08631579, -0.07157895]],
#                          [[-0.02736842, -0.01263158],
#                           [0.03157895, 0.04631579]]],
#                         [[[0.09052632, 0.10526316],
#                           [0.14947368, 0.16421053]],
#                          [[0.20842105, 0.22315789],
#                           [0.26736842, 0.28210526]],
#                          [[0.32631579, 0.34105263],
#                           [0.38526316, 0.4]]]])
#
# # Compare your output with ours. Difference should be around 1e-8.
# print 'Testing max_pool_forward_naive function:'
# print 'difference: ', rel_error(out, correct_out)

#############################################################################
# Max pooling: Naive backward

# x = np.random.randn(3, 2, 8, 8)
# dout = np.random.randn(3, 2, 4, 4)
# pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}
#
# dx_num = eval_numerical_gradient_array(lambda x: max_pool_forward_naive(x, pool_param)[0], x, dout)
#
# out, cache = max_pool_forward_naive(x, pool_param)
# dx = max_pool_backward_naive(dout, cache)
#
# # Your error should be around 1e-12
# print 'Testing max_pool_backward_naive function:'
# print 'dx error: ', rel_error(dx, dx_num)

#############################################################################
# Fast layers
from cs231n.layer_utils import *
from cs231n.fast_layers import conv_forward_fast
from time import time

x = np.random.randn(100, 1, 28, 28)
w1 = np.random.randn(32, 1, 5, 5)
b1 = np.random.randn(32,)
w2 = np.random.randn(64, 32, 5, 5)
b2 = np.random.randn(64,)
w3 = np.random.randn(64 *7 * 7, 1024)
b3 = np.random.randn(1024,)
w4 = np.random.randn(1024, 10)
b4 = np.random.randn(10,)
dout = np.random.randn(100, 32, 28, 28)
dscores = np.random.randn(100, 10)

conv_param = {'stride': 1, 'pad': 2}

# t0 = time()
# out_naive, cache_naive = conv_forward_naive(x, w, b, conv_param)
# print out_naive.shape
# print out_naive
# t1 = time()
# out_fast, cache_fast = conv_forward_fast(x, w, b, conv_param)
# print out_fast.shape
# print out_fast
# t2 = time()

# pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}
# out1, cache1 = conv_relu_pool_forward(x, w1, b1, conv_param, pool_param)
# print out1.shape
# # print out1
# print "#############################################################################"
# out2, cache2 = conv_relu_pool_forward(out1, w2, b2, conv_param, pool_param)
# print out2.shape
# # print out2
# affine_relu_out2, affine_relu_cache2 = affine_relu_forward(out2, w3, b3)
# print affine_relu_out2.shape
# # print affine_relu_out2
# affine2_out, affine2_cache = affine_forward(affine_relu_out2, w4, b4)
# print affine2_out.shape
# affine2_dx, affine2_dw, affine2_db = affine_backward(dscores, affine2_cache)
# print affine2_dw.shape
# dx = np.zeros_like(affine2_dw)
# dx[affine2_dw > 0] = 1
# print dx.sum()
# affine3_dx, affine3_dw, affine3_db = affine_relu_backward(affine2_dx, affine_relu_cache2)
# print "#############################################################################"
# print affine3_dw.shape
# dx = np.zeros_like(affine3_dw)
# dx[affine3_dw > 0] = 1
# print dx.sum()
# out1_dout, conv_dw, conv_db = conv_relu_pool_backward_naive(affine3_dx, cache2)
# print "#############################################################################"
# print conv_dw.shape
# dx = np.zeros_like(conv_dw)
# dx[conv_dw > 0] = 1
# print dx.sum()
# out_dout, w_dw, d_db = conv_relu_pool_backward_naive(out1_dout, cache1)
# print w_dw.shape
# dx = np.zeros_like(w_dw)
# dx[w_dw > 0] = 1
# print dx.sum()
#

# print 'Testing conv_forward_fast:'
# print 'Naive: %fs' % (t1 - t0)
# print 'Fast: %fs' % (t2 - t1)
# print 'Speedup: %fx' % ((t1 - t0) / (t2 - t1))
# print 'Difference: ', rel_error(out_naive, out_fast)
#
# t0 = time()
# dx_naive, dw_naive, db_naive = conv_backward_naive(dout, cache_naive)
# t1 = time()
# dx_fast, dw_fast, db_fast = conv_backward_fast(dout, cache_fast)
# t2 = time()
#
# print '\nTesting conv_backward_fast:'
# print 'Naive: %fs' % (t1 - t0)
# print 'Fast: %fs' % (t2 - t1)
# print 'Speedup: %fx' % ((t1 - t0) / (t2 - t1))
# print 'dx difference: ', rel_error(dx_naive, dx_fast)
# print 'dw difference: ', rel_error(dw_naive, dw_fast)
# print 'db difference: ', rel_error(db_naive, db_fast)

# x = np.random.randn(100, 3, 32, 32)
# dout = np.random.randn(100, 3, 16, 16)
# pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}
#
# t0 = time()
# out_naive, cache_naive = max_pool_forward_naive(x, pool_param)
# t1 = time()
# out_fast, cache_fast = max_pool_forward_fast(x, pool_param)
# t2 = time()
#
# print 'Testing pool_forward_fast:'
# print 'Naive: %fs' % (t1 - t0)
# print 'fast: %fs' % (t2 - t1)
# print 'speedup: %fx' % ((t1 - t0) / (t2 - t1))
# print 'difference: ', rel_error(out_naive, out_fast)
#
# t0 = time()
# dx_naive = max_pool_backward_naive(dout, cache_naive)
# t1 = time()
# dx_fast = max_pool_backward_fast(dout, cache_fast)
# t2 = time()
#
# print '\nTesting pool_backward_fast:'
# print 'Naive: %fs' % (t1 - t0)
# print 'speedup: %fx' % ((t1 - t0) / (t2 - t1))
# print 'dx difference: ', rel_error(dx_naive, dx_fast)

#############################################################################
# Convolutional "sandwich" layers

# from cs231n.layer_utils import conv_relu_pool_forward, conv_relu_pool_backward
#
# x = np.random.randn(2, 3, 16, 16)
# w = np.random.randn(3, 3, 3, 3)
# b = np.random.randn(3,)
# dout = np.random.randn(2, 3, 8, 8)
# conv_param = {'stride': 1, 'pad': 1}
# pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}
#
# out, cache = conv_relu_pool_forward(x, w, b, conv_param, pool_param)
# dx, dw, db = conv_relu_pool_backward_naive(dout, cache)  # fast method is just not fixxing well, try to set correct env for that
#
# dx_num = eval_numerical_gradient_array(lambda x: conv_relu_pool_forward(x, w, b, conv_param, pool_param)[0], x, dout)
# dw_num = eval_numerical_gradient_array(lambda w: conv_relu_pool_forward(x, w, b, conv_param, pool_param)[0], w, dout)
# db_num = eval_numerical_gradient_array(lambda b: conv_relu_pool_forward(x, w, b, conv_param, pool_param)[0], b, dout)
#
# print 'Testing conv_relu_pool'
# print 'dx error: ', rel_error(dx_num, dx)
# print 'dw error: ', rel_error(dw_num, dw)
# print 'db error: ', rel_error(db_num, db)
#
# from cs231n.layer_utils import conv_relu_forward, conv_relu_backward
#
# x = np.random.randn(2, 3, 8, 8)
# w = np.random.randn(3, 3, 3, 3)
# b = np.random.randn(3,)
# dout = np.random.randn(2, 3, 8, 8)
# conv_param = {'stride': 1, 'pad': 1}
#
# out, cache = conv_relu_forward(x, w, b, conv_param)
# dx, dw, db = conv_relu_backward_naive(dout, cache)
#
# dx_num = eval_numerical_gradient_array(lambda x: conv_relu_forward(x, w, b, conv_param)[0], x, dout)
# dw_num = eval_numerical_gradient_array(lambda w: conv_relu_forward(x, w, b, conv_param)[0], w, dout)
# db_num = eval_numerical_gradient_array(lambda b: conv_relu_forward(x, w, b, conv_param)[0], b, dout)
#
# print 'Testing conv_relu:'
# print 'dx error: ', rel_error(dx_num, dx)
# print 'dw error: ', rel_error(dw_num, dw)
# print 'db error: ', rel_error(db_num, db)
#############################################################################
# Three-layer ConvNet

# model = ThreeLayerConvNet()
#
# N = 50
# X = np.random.randn(N, 3, 32, 32)
# y = np.random.randint(10, size=N)
#
# loss, grads = model.loss(X, y)
# print 'Initial loss (no regularization): ', loss
#
# model.reg = 0.5
# loss, grads = model.loss(X, y)
# print 'Initial loss (with regularization): ', loss


#############################################################################
# Gradient check

# num_inputs = 2
# input_dim = (3, 16, 16)
# reg = 0.0
# num_classes = 10
# X = np.random.randn(num_inputs, *input_dim)
# y = np.random.randint(num_classes, size=num_inputs)
#
# model = ThreeLayerConvNet(num_filters=3, filter_size=3,
#                           input_dim=input_dim, hidden_dim=7,
#                           dtype=np.float64)
# loss, grads = model.loss(X, y)
# for param_name in sorted(grads):
#     f = lambda _: model.loss(X, y)[0]
#     param_grad_num = eval_numerical_gradient(f, model.params[param_name], verbose=False, h=1e-6)
#     e = rel_error(param_grad_num, grads[param_name])
#     print '%s max relative error: %e' % (param_name, rel_error(param_grad_num, grads[param_name]))

#############################################################################
# Overfit small data : A nice trick is to train your model with just a few training samples.
# You should be able to overfit small datasets, which will result in very high training accuracy and comparatively low validation accuracy.

# num_train = 100
# small_data = {
#   'X_train': data['X_train'][:num_train],
#   'y_train': data['y_train'][:num_train],
#   'X_val': data['X_val'],
#   'y_val': data['y_val'],
# }
#
# model = ThreeLayerConvNet(weight_scale=1e-2)
#
# solver = Solver(model, small_data,
#                 num_epochs=10, batch_size=50,
#                 update_rule='adam',
#                 optim_config={
#                   'learning_rate': 1e-3,
#                 },
#                 verbose=True, print_every=1)
# solver.train()
#
# # Plotting the loss, training accuracy, and validation accuracy should show clear overfitting:
# plt.subplot(2, 1, 1)
# plt.plot(solver.loss_history, 'o')
# plt.xlabel('iteration')
# plt.ylabel('loss')
#
# plt.subplot(2, 1, 2)
# plt.plot(solver.train_acc_history, '-o')
# plt.plot(solver.val_acc_history, '-o')
# plt.legend(['train', 'val'], loc='upper left')
# plt.xlabel('epoch')
# plt.ylabel('accuracy')
# plt.show()
#############################################################################
# Train the net: By training the three-layer convolutional network for one epoch, you should achieve greater than 40% accuracy on the training set:

# model = ThreeLayerConvNet(weight_scale=0.001, hidden_dim=500, reg=0.001)
#
# solver = Solver(model, data,
#                 num_epochs=1, batch_size=50,
#                 update_rule='adam',
#                 optim_config={
#                   'learning_rate': 1e-3,
#                 },
#                 verbose=True, print_every=20)
# solver.train()

# Visualize Filters :
# from cs231n.vis_utils import visualize_grid
#
# grid = visualize_grid(model.params['W1'].transpose(0, 2, 3, 1))
# plt.imshow(grid.astype('uint8'))
# plt.axis('off')
# plt.gcf().set_size_inches(5, 5)
# plt.show()
#############################################################################
# Spatial Batch Normalization  # need practice

# We already saw that batch normalization is a very useful technique for training deep fully-connected networks. Batch normalization can also be used for convolutional networks,
# but we need to tweak it a bit; the modification will be called "spatial batch normalization."
# Normally batch-normalization accepts inputs of shape (N, D) and produces outputs of shape (N, D), where we normalize across the minibatch dimension N. For data coming from convolutional layers,
# batch normalization needs to accept inputs of shape (N, C, H, W) and produce outputs of shape (N, C, H, W) where the N dimension gives the minibatch size and the (H, W) dimensions give the spatial size of the feature map.
# If the feature map was produced using convolutions, then we expect the statistics of each feature channel to be relatively consistent both between different imagesand different locations within the same image.
# Therefore spatial batch normalization computes a mean and variance for each of the C feature channels by computing statistics over both the minibatch dimension N and the spatial dimensions H and W.
# Spatial batch normalization: forward
# Check the training-time forward pass by checking means and variances
# of features both before and after spatial batch normalization

# small_data = data['X_train'][:10]
# N, C, H, W = small_data.shape
# print small_data.shape
#
# x_tr = small_data.transpose(0, 3, 2, 1)
# print x_tr.shape
#
# x_reshape = x_tr.reshape((N * H * W, C))
# print x_reshape.shape

# N, C, H, W = 2, 3, 4, 5
# x = 4 * np.random.randn(N, C, H, W) + 10
#
# print 'Before spatial batch normalization:'
# print '  Shape: ', x.shape
# print '  Means: ', x.mean(axis=(0, 2, 3))
# print '  Stds: ', x.std(axis=(0, 2, 3))
#
# # Means should be close to zero and stds close to one
# gamma, beta = np.ones(C), np.zeros(C)
# bn_param = {'mode': 'train'}
# out, _ = spatial_batchnorm_forward(x, gamma, beta, bn_param)
# print 'After spatial batch normalization:'
# print '  Shape: ', out.shape
# print '  Means: ', out.mean(axis=(0, 2, 3))
# print '  Stds: ', out.std(axis=(0, 2, 3))
#
# # Means should be close to beta and stds close to gamma
# gamma, beta = np.asarray([3, 4, 5]), np.asarray([6, 7, 8])
# out, _ = spatial_batchnorm_forward(x, gamma, beta, bn_param)
# print 'After spatial batch normalization (nontrivial gamma, beta):'
# print '  Shape: ', out.shape
# print '  Means: ', out.mean(axis=(0, 2, 3))
# print '  Stds: ', out.std(axis=(0, 2, 3))
#
# # Check the test-time forward pass by running the training-time
# # forward pass many times to warm up the running averages, and then
# # checking the means and variances of activations after a test-time
# # forward pass.
#
# N, C, H, W = 10, 4, 11, 12
#
# bn_param = {'mode': 'train'}
# gamma = np.ones(C)
# beta = np.zeros(C)
# for t in xrange(50):
#     x = 2.3 * np.random.randn(N, C, H, W) + 13
#     spatial_batchnorm_forward(x, gamma, beta, bn_param)
# bn_param['mode'] = 'test'
# x = 2.3 * np.random.randn(N, C, H, W) + 13
# a_norm, _ = spatial_batchnorm_forward(x, gamma, beta, bn_param)
#
# # Means should be close to zero and stds close to one, but will be
# # noisier than training-time forward passes.
# print 'After spatial batch normalization (test-time):'
# print '  means: ', a_norm.mean(axis=(0, 2, 3))
# print '  stds: ', a_norm.std(axis=(0, 2, 3))

#############################################################################
# Spatial batch normalization: backward

# N, C, H, W = 2, 3, 4, 5
# x = 5 * np.random.randn(N, C, H, W) + 12
# gamma = np.random.randn(C)
# beta = np.random.randn(C)
# dout = np.random.randn(N, C, H, W)
#
# bn_param = {'mode': 'train'}
# fx = lambda x: spatial_batchnorm_forward(x, gamma, beta, bn_param)[0]
# fg = lambda a: spatial_batchnorm_forward(x, gamma, beta, bn_param)[0]
# fb = lambda b: spatial_batchnorm_forward(x, gamma, beta, bn_param)[0]
#
# dx_num = eval_numerical_gradient_array(fx, x, dout)
# da_num = eval_numerical_gradient_array(fg, gamma, dout)
# db_num = eval_numerical_gradient_array(fb, beta, dout)
#
# _, cache = spatial_batchnorm_forward(x, gamma, beta, bn_param)
# dx, dgamma, dbeta = spatial_batchnorm_backward(dout, cache)
# print 'dx error: ', rel_error(dx_num, dx)
# print 'dgamma error: ', rel_error(da_num, dgamma)
# print 'dbeta error: ', rel_error(db_num, dbeta)

#############################################################################
# Experiment!
# [conv-relu-pool]xN - conv - relu - [affine]xM - [softmax or SVM]
# [conv-relu-pool]xN - [affine]xM - [softmax or SVM]
# [conv-relu-conv-relu-pool]xN - [affine]xM - [softmax or SVM]


# model = CustomLayerConvNet(weight_scale=0.001, hidden_dim=500, reg=0.001)
#
# solver = Solver(model, data,
#                 num_epochs=100, batch_size=50,
#                 update_rule='adam',
#                 optim_config={
#                   'learning_rate': 1e-3,
#                 },
#                 verbose=True, print_every=100)
#
# solver.train()
#
# # get the best_params
# param = solver.best_params





#############################################################################

