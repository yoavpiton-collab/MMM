
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from PIL import Image as PILImage
import numpy as np
import os
try:
    import tensorflow as tf
    TFLITE_OK = True
except Exception:
    tf = None
    TFLITE_OK = False

class FruitCounterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.preview = Image(size_hint=(1, 0.6))
        self.add_widget(self.preview)
        self.status = Label(text='Pick or capture an image', size_hint=(1, 0.1))
        self.add_widget(self.status)
        row = BoxLayout(size_hint=(1, 0.15))
        btn_choose = Button(text='Choose Image')
        btn_choose.bind(on_release=self.open_chooser)
        btn_edit = Button(text='Edit Count')
        btn_edit.bind(on_release=self.edit_count)
        row.add_widget(btn_choose)
        row.add_widget(btn_edit)
        self.add_widget(row)
        self.count_value = 0
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        Clock.schedule_once(self._load_model, 0)

    def _load_model(self, *args):
        model_path = os.path.join(os.path.dirname(__file__), 'tflite_model', 'fruit_model.tflite')
        if TFLITE_OK and os.path.exists(model_path):
            try:
                self.interpreter = tf.lite.Interpreter(model_path=model_path)
                self.interpreter.allocate_tensors()
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
                self.status.text = 'Model loaded (offline)'
            except Exception as e:
                self.status.text = f'Model error: {e}'
        else:
            if not TFLITE_OK:
                self.status.text = 'TFLite not available; demo mode'
            else:
                self.status.text = 'Model not found; demo mode'

    def open_chooser(self, instance):
        chooser = FileChooserIconView(filters=['*.png','*.jpg','*.jpeg'])
        popup = Popup(title='Select Image', content=chooser, size_hint=(0.9,0.9))
        chooser.bind(on_submit=lambda fc, selection, touch: self._on_file_selected(selection, popup))
        popup.open()

    def _on_file_selected(self, selection, popup):
        if not selection: return
        path = selection[0]
        popup.dismiss()
        self._display_image(path)
        self.count_value = self.predict_count(path)
        self.status.text = f'Detected fruits: {self.count_value}'

    def _display_image(self, path):
        img = PILImage.open(path).convert('RGB')
        w, h = img.size
        img = img.resize((min(w, 640), min(h, 640)))
        data = img.tobytes()
        tex = Texture.create(size=img.size)
        tex.blit_buffer(data, colorfmt='rgb', bufferfmt='ubyte')
        self.preview.texture = tex

    def predict_count(self, path):
        if self.interpreter is None:
            return 3
        img = PILImage.open(path).convert('RGB').resize((224,224))
        input_data = np.expand_dims(np.array(img, dtype=np.float32)/255.0, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        out = self.interpreter.get_tensor(self.output_details[0]['index'])
        try:
            return int(round(float(out[0][0])))
        except Exception:
            return int(np.argmax(out))

    def edit_count(self, instance):
        popup = Popup(title='Edit Count', size_hint=(0.8,0.4))
        layout = BoxLayout(orientation='vertical')
        ti = TextInput(text=str(self.count_value), multiline=False, input_filter='int')
        layout.add_widget(ti)
        btn = Button(text='Save')
        btn.bind(on_release=lambda *_: self._save_manual(ti.text, popup))
        layout.add_widget(btn)
        popup.content = layout
        popup.open()

    def _save_manual(self, txt, popup):
        try:
            self.count_value = int(txt)
            self.status.text = f'Manual count: {self.count_value}'
        except:
            self.status.text = 'Invalid number'
        popup.dismiss()

class FruitCounterApp(App):
    def build(self):
        return FruitCounterLayout()

if __name__ == '__main__':
    FruitCounterApp().run()
