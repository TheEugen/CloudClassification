#   USAGE: classifyImage.py <model.h5> <image.jpg>

import sys
import os.path
import numpy


def validateInput():
    if len(sys.argv) < 3:
        print("\nNot enough arguments provided\n"
        "Try classifyImage.py <model.h5> <image.jpg>")
        return False

    if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print()
        if not os.path.isfile(sys.argv[1]):
            print("%s doesnt exist" % sys.argv[1])
        if not os.path.isfile(sys.argv[2]):
            print("%s doesnt exist" % sys.argv[2])
        return False

    return True

def main():
    if not validateInput():
        return

    import tensorflow as tf
    from tensorflow import keras

    image_size = (180, 180)
    batch_size = 32

    model = tf.keras.models.load_model(sys.argv[1])

    callbacks = [
        keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
    ]
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    #model.fit(
    #    train_ds, epochs=1, callbacks=callbacks, validation_data=val_ds,
    #)

    img = keras.preprocessing.image.load_img(
        sys.argv[2], target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    # Create batch axis
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    # custom dataset
    directory = os.fsencode(os.getcwd() + "/mergedDataset")
    list_classes = os.listdir(directory)
    for i in range(len(list_classes)):
        print("%s %.2f" % (os.fsdecode(list_classes[i]), predictions[0][i] * 100))

    print()
    maxPred = numpy.amax(predictions)
    maxPredIndex = numpy.where(predictions == numpy.amax(predictions))
    #print(maxPredIndex[1][0])
    print('Winner: %s with %.2f' % (os.fsdecode(list_classes[maxPredIndex[1][0]]), maxPred * 100))

main()
