import os
import tensorflow as tf

tf.app.flags.DEFINE_string('model_dir', '', 'Saved Model Directory')
FLAGS = tf.app.flags.FLAGS

def main(_):
    is_saved_model = tf.saved_model.loader.maybe_saved_model_directory(FLAGS.model_dir)
    if not is_saved_model:
        print('"{0}" is not a saved_model directory'.format(FLAGS.model_dir))
        sys.exit(-1)

    sess = tf.Session()
    mymodel = tf.saved_model.loader.load(sess,
                                         [tf.saved_model.tag_constants.SERVING],
                                         FLAGS.model_dir)
    serving_sig = mymodel.signature_def[tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY]

    print('Model Inputs:')
    ind = 1
    for key in serving_sig.inputs:
        print('  Input {0}:'.format(ind))
        print('    Name: {0}'.format(key))
        input_tmp = serving_sig.inputs[key]
        print('    Dtype: {0}'.format(tf.DType(input_tmp.dtype).name))

        ts = tf.TensorShape(input_tmp.tensor_shape)
        if ts.dims is None:
            print('    Shape: {0}'.format(ts.dims))
        else:
            print('    Shape: {0}'.format(ts.as_list()))
        ind = ind + 1
    

    print('Model Outputs:')
    ind = 1
    for key in serving_sig.outputs:
        print('  Output {0}:'.format(ind))
        print('    Name: {0}'.format(key))
        output_tmp = serving_sig.outputs[key]
        print('    Dtype: {0}'.format(tf.DType(output_tmp.dtype).name))

        ts = tf.TensorShape(output_tmp.tensor_shape)
        if ts.dims is None:
            print('    Shape: {0}'.format(ts.dims))
        else:
            print('    Shape: {0}'.format(ts.as_list()))
        ind = ind + 1

if __name__ == '__main__':
    tf.app.run()
