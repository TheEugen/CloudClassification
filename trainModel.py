#   USAGE: trainModel.py <model.h5> <dataset> <epochs>

import tensorflow as tf
from tensorflow import keras
import sys
import os.path


def validateInput():
    if len(sys.argv) < 4:
        print("\nNot enough arguments provided\n"
        "Try trainModel <model.h5> <dataset> <epochs>")
        return False

    if not os.path.isfile(sys.argv[1]):
        print("%s doesnt exist" % sys.argv[1])
        return False

    if not os.path.isdir(sys.argv[2]):
        print("%s doesnt exist" % sys.argv[2])
        return False

    try:
        int(sys.argv[3])
    except ValueError:
        print("Argument #2 is not an integer")
        return False

    return True

def scanForBrokenImages(dataset_path):
    num_skipped = 0
    for folder_name in ("Ac", "As", "Cb", "Cc",
    "Ci", "Cs", "Ct", "Cu", "Ns", "Sc", "St"):
        folder_path = os.path.join("customDataset", folder_name)
        for fname in os.listdir(folder_path):
            fpath = os.path.join(folder_path, fname)
            try:
                fobj = open(fpath, "rb")
                is_jfif = tf.compat.as_bytes("JFIF") in fobj.peek(10)
            finally:
                fobj.close()

            if not is_jfif:
                num_skipped += 1
            # Delete corrupted image
            os.remove(fpath)

    print("Deleted %d images" % num_skipped)

def main():
    if not validateInput():
        return

    model_path = sys.argv[1]
    dataset_path = sys.argv[2]
    epochs = int(sys.argv[3])

    image_size = (180, 180)
    batch_size = 32

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path,
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path,
        validation_split=0.2,
        subset="validation",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
    )

    train_ds = train_ds.prefetch(buffer_size=32)
    val_ds = val_ds.prefetch(buffer_size=32)

    model = tf.keras.models.load_model(model_path)

    callbacks = [
        keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
    ]
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(
        train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
    )


main()
