# trains the model according to the CNN specifications provided

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras import optimizers

img_folder = 'training_data'
# batches = {16:1024, 32:512, 64:256, 128:128}
batches = {16:4096}
total_classes = 5

for batch in batches:

    train_datagen = ImageDataGenerator(
        width_shift_range=0.2, height_shift_range=0.2, horizontal_flip=True,
        rotation_range=20, brightness_range=[0.5, 1.5], zoom_range=0.2,
        shear_range=0.2, validation_split=0.2,
        rescale=1/255
    )

    train_generator = train_datagen.flow_from_directory(
        img_folder, color_mode='rgb', target_size=(150, 150), batch_size=batch, subset='training',
        shuffle=True
    )

    test_generator = train_datagen.flow_from_directory(
        img_folder, color_mode='rgb', target_size=(150, 150), batch_size=batch, subset='validation',
        shuffle=True
    )

    # load model without classifier layers
    model = VGG16(include_top=False, input_shape=(150, 150, 3))

    # for layer in model.layers:
    # 	layer.trainable = False

    # add new classifier layers
    flat1 = Flatten()(model.output)
    class1 = Dense(1024, activation='relu')(flat1)
    class1 = Dense(512, activation='relu')(flat1)
    output = Dense(total_classes, activation='softmax')(class1)
    # define new model
    model = Model(inputs=model.inputs, outputs=output)

    # custom optimizer
    sgd = optimizers.SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)

    # compile model using accuracy to measure model performance
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    epoch_steps = batches[batch]

    # train the model
    model.fit_generator(train_generator, steps_per_epoch=epoch_steps,
                        validation_data=test_generator, validation_steps=epoch_steps,
                        epochs=256)

    # model.save('vgg_batch_{}.h5'.format(batch))
    model.save('cnn_aug_256.h5'.format(batch))

