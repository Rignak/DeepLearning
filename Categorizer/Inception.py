import os
import sys

from keras.applications.inception_v3 import InceptionV3
from keras.optimizers import SGD, rmsprop
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model

from Rignak_DeepLearning.Categorizer.flat import WEIGHT_ROOT, SUMMARY_ROOT

# nohup python3.6 train.py inceptionV3 chen --IMAGENET=transfer --INPUT_SHAPE="(299,299,1)" > nohup_inception.out &
LOAD = False
IMAGENET = False
DEFAULT_LOSS = 'categorical_crossentropy'
DEFAULT_METRICS = ['accuracy']
LAST_ACTIVATION = 'softmax'

def import_model_v3(input_shape, output_shape, name, weight_root=WEIGHT_ROOT, summary_root=SUMMARY_ROOT, load=LOAD,
                    imagenet=IMAGENET, loss=DEFAULT_LOSS, metrics=DEFAULT_METRICS, last_activation=LAST_ACTIVATION):
    if imagenet:
        print('Will load imagenet weights')
        weights = "imagenet"
    else:
        weights = None

    base_model = InceptionV3(weights=weights, input_shape=input_shape, classes=output_shape, include_top=False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(output_shape, activation=last_activation)(x)
    model = Model(base_model.input, outputs=x)

    if imagenet == "fine-tuning":
        for layer in model.layers[:-1]:
            layer.trainable = False
    model.compile(optimizer='adam', loss=loss, metrics=metrics)


    if weights is None:
        model.name = f"{name}_False"
    else:
        model.name = f"{name}_{weights}"

    model.weight_filename = os.path.join(weight_root, f"{model.name}.h5")
    model.summary_filename = os.path.join(summary_root, f"{model.name}.txt")

    if load:
        print('load weights')
        model.load_weights(model.weight_filename)

    with open(model.summary_filename, 'w') as file:
        old = sys.stdout
        sys.stdout = file
        model.summary()
        sys.stdout = old
    return model
