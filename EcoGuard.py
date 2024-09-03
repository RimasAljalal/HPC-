# -*- coding: utf-8 -*-
"""Welcome To Colab

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
"""

from google.colab import drive
import os
import pandas as pd

# ربط Google Colab بحساب Google Drive
drive.mount('/content/drive')


# مسارات المجلدين في Google Drive
deforestation_dir = '/content/drive/My Drive/Dataset/deforestation/'  # مسار مجلد صور deforestation
no_deforestation_dir = '/content/drive/My Drive/Dataset/no_deforestation/'  # مسار مجلد صور no_deforestation

from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

# دالة لتحميل الصور مع التحقق من الامتداد
def load_and_preprocess_image(image_path):
    try:
        img = load_img(image_path, target_size=(224, 224))  # تحديد حجم الصورة
        img_array = img_to_array(img)
        return img_array
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None

# قائمة لتخزين الصور والفئات
images = []
labels = []

# تحميل الصور من مجلد deforestation
for filename in os.listdir(deforestation_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # التحقق من الامتداد
        img_path = os.path.join(deforestation_dir, filename)
        img_array = load_and_preprocess_image(img_path)
        if img_array is not None:  # إضافة الصورة إذا تم تحميلها بنجاح
            images.append(img_array)
            labels.append(1)  # الفئة 1 لـ deforestation

# تحميل الصور من مجلد no_deforestation
for filename in os.listdir(no_deforestation_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # التحقق من الامتداد
        img_path = os.path.join(no_deforestation_dir, filename)
        img_array = load_and_preprocess_image(img_path)
        if img_array is not None:  # إضافة الصورة إذا تم تحميلها بنجاح
            images.append(img_array)
            labels.append(0)  # الفئة 0 لـ no_deforestation

# تحويل القوائم إلى مصفوفات numpy
X = np.array(images)
y = np.array(labels)

# طباعة الأشكال للتأكد
print(f'Images shape: {X.shape}')
print(f'Labels shape: {y.shape}')

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = X_train / 255.0
X_test = X_test / 255.0

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_acc}")
print(f"Test loss: {test_loss}")

model.save('final_deforestation_model.h5')

model.save('final_deforestation_model.keras')

import matplotlib.pyplot as plt

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# أولاً، نربط Google Drive بجوجل كولاب
from google.colab import drive
drive.mount('/content/drive')

import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# مسار مجلد الصور الجديدة في Google Drive
new_images_dir = '/content/drive/My Drive/DataTest/'  # استبدل المسار بمسار المجلد الخاص بك في Google Drive

# دالة لتحضير الصورة
def preprocess_new_image(image_path):
    img = load_img(image_path, target_size=(224, 224))  # تغيير حجم الصورة إلى 224x224 بكسل
    img_array = img_to_array(img)  # تحويل الصورة إلى مصفوفة أرقام
    img_array = np.expand_dims(img_array, axis=0)  # إضافة بعد جديد لتناسب متطلبات النموذج
    img_array /= 255.0  # تطبيع الصورة لتكون القيم بين 0 و 1
    return img_array

# قائمة لتخزين النتائج
results = []

# حلقة لتحميل الصور الجديدة ومعالجتها
for filename in os.listdir(new_images_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # التحقق من أن الملف هو صورة
        image_path = os.path.join(new_images_dir, filename)
        processed_image = preprocess_new_image(image_path)  # معالجة الصورة

        # التنبؤ باستخدام النموذج المدرب
        prediction = model.predict(processed_image)

        # تحديد الفئة بناءً على التنبؤ
        if prediction[0][0] > 0.5:
            result = (filename, "Deforestation")
        else:
            result = (filename, "No Deforestation")

        # إضافة النتيجة إلى القائمة
        results.append(result)
        print(f"Image: {filename}, Prediction: {result[1]}")

# عرض جميع النتائج
print("All predictions completed.")
for res in results:
    print(f"Image: {res[0]}, Prediction: {res[1]}")

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# إعداد مولد البيانات مع تعزيز البيانات
train_datagen = ImageDataGenerator(
    rescale=1./255,          # تطبيع الصور
    rotation_range=20,       # تدوير الصور بزاوية تصل إلى 20 درجة
    width_shift_range=0.2,   # تغيير العرض بنسبة تصل إلى 20%
    height_shift_range=0.2,  # تغيير الارتفاع بنسبة تصل إلى 20%
    shear_range=0.2,         # إمالة الصور
    zoom_range=0.2,          # تكبير/تصغير الصور
    horizontal_flip=True,    # عكس الصور أفقياً
    fill_mode='nearest'      # كيفية ملء البكسلات التي تم إزالتها بعد التحويل
)

test_datagen = ImageDataGenerator(rescale=1./255)

# استخدام مولد البيانات لتدريب النموذج
train_generator = train_datagen.flow(X_train, y_train, batch_size=32)
validation_generator = test_datagen.flow(X_test, y_test, batch_size=32)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# إعادة بناء النموذج مع تحسينات
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(256, (3, 3), activation='relu'))  # إضافة طبقة إضافية
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))  # زيادة عدد الخلايا العصبية
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

from tensorflow.keras.callbacks import EarlyStopping

# إعداد التوقف المبكر
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# تدريب النموذج مع التوقف المبكر
history = model.fit(
    train_generator,
    steps_per_epoch=len(X_train) // 32,
    epochs=50,  # يمكنك تجربة زيادة عدد الدورات (Epochs)
    validation_data=validation_generator,
    validation_steps=len(X_test) // 32,
    callbacks=[early_stop]  # إضافة التوقف المبكر هنا
)

import matplotlib.pyplot as plt

# رسم دقة التدريب والتحقق
plt.figure(figsize=(8, 5))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy After Improvements')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

# رسم خسارة التدريب والتحقق
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss After Improvements')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

from tensorflow.keras.optimizers import Adam

model.compile(optimizer=Adam(learning_rate=0.00001), loss='binary_crossentropy', metrics=['accuracy'])

from tensorflow.keras.callbacks import EarlyStopping

# إعداد التوقف المبكر (اختياري)
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# إعادة تدريب النموذج
history = model.fit(
    X_train, y_train,  # استخدم نفس بيانات التدريب
    epochs=50,  # يمكنك ضبط عدد الدورات (Epochs) حسب الحاجة
    batch_size=32,
    validation_data=(X_test, y_test),  # استخدم نفس بيانات التحقق (الاختبار)
    callbacks=[early_stop]  # إضافة التوقف المبكر إذا كان ذلك مفيدًا
)

pip install twilio

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_alert(subject, body):
    # Email settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'rimasaljalal.2003@gmail.com'  # Replace with your email address
    sender_password = 'kqtn lhsj ugol vgqw'  # Replace with your App Password
    recipient_email = 'bawared988.rr@gmail.com'  # Replace with recipient's email address

    # Set up the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Add the body content to the email
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS for security
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Example usage
send_email_alert('Deforestation Alert', 'Deforestation detected with high confidence!')

from google.colab import files
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# تحميل الصور من جهازك إلى Google Colab
uploaded = files.upload()

image_arrays = []

# معالجة كل صورة تم تحميلها
for image_name in uploaded.keys():
    # تحميل الصورة وتحويلها إلى مصفوفة
    img = load_img(image_name, target_size=(224, 224))  # ضبط الحجم بما يتناسب مع النموذج
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # إضافة بعد إضافي لتتناسب مع توقعات النموذج (batch size)
    img_array /= 255.0  # تطبيع البيانات
    image_arrays.append((image_name, img_array))  # إضافة الصورة المعالجة إلى القائمة

# نفترض أن لديك نموذج تم تدريبه مسبقاً وتسميه 'model'
threshold = 0.5  # يمكنك تعديل العتبة بناءً على متطلباتك

for image_name, img_array in image_arrays:
    # تنفيذ التنبؤ باستخدام النموذج
    prediction = model.predict(img_array)

    # التحقق من النتيجة وإرسال التنبيه إذا تم الكشف عن إزالة الغابات
    if prediction[0][0] > threshold:
        print(f"Deforestation detected in {image_name}")
        send_email_alert('Deforestation Alert', f"Deforestation detected in the image {image_name} with a confidence level of {prediction[0][0] * 100:.2f}%.")
    else:
        print(f"No deforestation detected in {image_name}")
        send_email_alert('No Deforestation Detected', f"No deforestation detected in the image {image_name}. Confidence level: {prediction[0][0] * 100:.2f}%.")