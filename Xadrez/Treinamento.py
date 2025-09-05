import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from dataset import load_dataset

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "análises", "analises.txt")

(X_planes, X_extras), y = load_dataset(DATA_PATH)

N = X_planes.shape[0]
idx = tf.random.shuffle(tf.range(N))
train_cut = int(0.85 * N)
tr_idx = idx[:train_cut]
va_idx = idx[train_cut:]

def take(data, idx):
    return tf.gather(data, idx)

Xtr_planes = take(X_planes, tr_idx)
Xva_planes = take(X_planes, va_idx)
Xtr_extras = take(X_extras, tr_idx)
Xva_extras = take(X_extras, va_idx)
ytr = take(y, tr_idx)
yva = take(y, va_idx)

inp_planes = keras.Input(shape=(8,8,12), name='planes')
x = layers.Conv2D(64, 3, padding='same', activation='relu')(inp_planes)
x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)
x = layers.Flatten()(x)

inp_extra = keras.Input(shape=(5,), name='extras')
e = layers.Dense(16, activation='relu')(inp_extra)

h = layers.Concatenate()([x, e])
h = layers.Dense(128, activation='relu')(h)
h = layers.Dense(64, activation='relu')(h)
out = layers.Dense(1, activation='tanh')(h) 

model = keras.Model([inp_planes, inp_extra], out)
model.compile(optimizer=keras.optimizers.Adam(1e-3),
              loss='mse',
              metrics=[keras.metrics.MeanAbsoluteError()])

model.summary()

callbacks = [
    keras.callbacks.ReduceLROnPlateau(patience=3, factor=0.5, verbose=1),
    keras.callbacks.EarlyStopping(patience=8, restore_best_weights=True, verbose=1)
]

history = model.fit(
    (Xtr_planes, Xtr_extras), ytr,
    validation_data=((Xva_planes, Xva_extras), yva),
    epochs=50,
    batch_size=256,
    verbose=2,
    callbacks=callbacks
)

model.save(os.path.join(os.path.dirname(DATA_PATH), "chess_eval_tf.keras")) 

from dataset import fen_to_input

model = keras.models.load_model(os.path.join(BASE_DIR, "análises", "chess_eval_tf.keras"))

fen = "rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b - - 0 1"

X_planes, X_extras = fen_to_input(fen)

X_planes = X_planes[None, ...]
X_extras = X_extras[None, ...]

pred = model.predict({"planes": X_planes, "extras": X_extras}, verbose=0)

score_cp = pred[0][0] * 1000

print("Avaliação normalizada:", pred[0][0])
print("Avaliação em centipawns:", score_cp)