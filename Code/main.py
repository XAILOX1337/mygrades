from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import sqlite3
import random
from functools import partial

Config.set('graphics', 'resizeble', 1)

class Application(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marks_gl = GridLayout(cols=15, rows=10, padding=10, spacing=10,)
    
    def on_mainpage(self,instance):
        self.bl.clear_widgets()  # Очищаем содержимое BoxLayout
        self.boxl.clear_widgets()
        self.al.clear_widgets()
        self.marks_gl.clear_widgets()
        # Добавляем кнопки на главную страницу
        self.bl.add_widget(Button(text='ПРОСМОТР ОЦЕНОК',
                                font_size=50,
                                background_color=[0.25, 0.96, 0.7, 1],
                                background_normal='',
                                size_hint_y=None,
                                size = (900,500),
                                on_press=self.look_marks))
        self.add_marks_button = Button(text='ДОБАВЛЕНИЕ ОЦЕНОК',
                               font_size=50,
                               background_color=[0.25, 0.96, 0.7, 1],
                               background_normal='',
                               size_hint_y=None,
                               size = (900,500),
                               on_press=self.add_marks)
        self.bl.add_widget(self.add_marks_button)
        self.bl.add_widget(Button(text='ИЗМЕНЕНИЕ ОЦЕНОК',
                                font_size=50,
                                background_color=[0.25, 0.96, 0.7, 1],
                                background_normal='',
                                size_hint_y=None,
                                size = (900,500),
                                on_press=self.change_marks))


    def look_subject(self, instance):
        name_sub = instance.text
        self.al.add_widget(Button(text='На главную',
                                font_size=30,
                                background_color=[0.25, 0.96, 0.7, 1],
                                background_normal='',
                                size_hint=(1,1),
                                on_press = self.on_mainpage))
        self.add_marks_button.disabled = False
        self.bl.clear_widgets()
        self.boxl.clear_widgets() # Очищаем содержимое BoxLayout
        con = sqlite3.connect('first_db.db')
        c = con.cursor()
        
        c.execute(f"SELECT grade FROM final WHERE subject = '{name_sub}';")
        records = c.fetchall()
        lab = Label(text = f'Ваши оценки по предмету {instance.text}',font_size=40, 
                    size_hint=(1, None), 
                    height=80,
                    padding=10,
                    )
        self.boxl.add_widget(lab)
        self.marks_gl= GridLayout(cols=15,rows = 10, padding=10, spacing=10)
        for record in records:
            
            if record is not None:
                marks = Label(text=f'{record[0]}', 
                            font_size=40, 
                            size_hint=(1, None), 
                            height=80,
                            color = [0,0,0])
            else:
                marks = Label(text=f'По предмету {instance.text} вы не получили ни одной оценки', 
                            font_size=20, 
                            size_hint=(1, None), 
                            height=40,color = [0,0,0])
            self.marks_gl.add_widget(marks)
        self.boxl.add_widget(self.marks_gl)
        
        con.commit()
        con.close()


    def look_marks(self, instance):
        
        self.al.add_widget(Button(text='На главную',
                                font_size=30,
                                background_color=[0.25, 0.96, 0.7, 1],
                                background_normal='',
                                size_hint=(1,1),
                                on_press = self.on_mainpage))
        
        self.bl.clear_widgets()  # Очищаем содержимое BoxLayout
        sub = ['Математика', 'Русский язык', 'Литература', 'Физика', 'История', 'ОБЖ', 'Обществознание', 'Физ-ра', 'Химия', 'Английский язык', 'Информатика', 'ОПД']  
        
        for i in sub:
            but = Button(text=i,
                        font_size=45,
                        background_color=[0.25, 0.96, 0.7, 1],
                        background_normal='',
                        size_hint_y=None,
                        size = (900,350),
                        on_press = self.look_subject)
            self.bl.add_widget(but)
        
        self.label.text = 'По какому предмету хотите посмотреть оценки?'
       
        

        self.boxl.add_widget(self.label)

    
    def add_marks(self, *args):
        def add_mark_popup(instance):
            
            # Save the mark to the database or whatever data storage you're using
            self.mark_subject = subject.text
            self.mark_grade = grade.text
            self.id_of_grade = id_mark 
            # Save the mark to the database or whatever data storage you're using
            con = sqlite3.connect('first_db.db')
            c = con.cursor()
            
            c.execute('INSERT INTO final VALUES (:subject, :grade, :id_of_grade)', 
                 {'subject': self.mark_subject, 'grade': self.mark_grade, 'id_of_grade': self.id_of_grade})
            
            con.commit()
            con.close()
        con = sqlite3.connect('first_db.db')
        c = con.cursor()
        layout = GridLayout(cols=2, padding=10, spacing=10)
        lab=Label(text='Предмет:')
        layout.add_widget(lab)
        subject = TextInput(multiline=False)
        layout.add_widget(subject)
        nofreeid = []
        id_mark =  random.randint(1,99999)
        if id_mark in nofreeid:
            id_mark =  random.randint(1,99999)
            nofreeid.append(id_mark)
        else:
            nofreeid.append(id_mark)
        layout.add_widget(Label(text='Оценка:'))
        grade = TextInput(multiline=False)
        layout.add_widget(grade)

        popup = Popup(title='Добавление оценки', content=layout, size_hint=(0.7, 0.4)) #добавить сохранение
        popup.bind(on_dismiss=add_mark_popup)
        popup.open()
        con.commit()
        con.close()
    def change_marks(self, instance):
        self.al.add_widget(Button(text='На главную',
                                font_size=30,
                                background_color=[0.25, 0.96, 0.7, 1],
                                background_normal='',
                                size_hint=(1,1),
                                on_press=self.on_mainpage))
        
        sub = ['Математика', 'Русский язык', 'Литература', 'Физика', 'История', 'ОБЖ', 'Обществознание', 'Физ-ра', 'Химия', 'Английский язык', 'Информатика', 'ОПД']
        self.bl.clear_widgets()  # очистка контейнера
        Text = Label(text='По какому предмету хотите исправить оценку?',
                     font_size=40,
                     size_hint=(1, None), 
                    height=80,
                    padding=20)
        self.boxl.add_widget(Text)
        for i in sub:
            but = Button(text=i,
                        font_size=45,
                        background_color=[0.25, 0.96, 0.7, 1],
                        background_normal='',
                        size_hint_y=None,
                        size = (900,350),
                        on_press=self.change_marks_real)
            self.bl.add_widget(but)
    
    def change_marks_real(self,instance):
        self.bl.clear_widgets()
        self.boxl.clear_widgets()
        
        self.al.add_widget(Button(text='На главную',
                                font_size=30,
                                background_color=[0.25, 0.96, 0.7, 1],
                                background_normal='',
                                size_hint=(1, 1),
                                on_press=self.on_mainpage))
        con = sqlite3.connect('first_db.db')
        name_sub = instance.text
        c = con.cursor()
        c.execute(f"SELECT id_of_grade, grade FROM final WHERE subject = '{name_sub}';")
        records = c.fetchall()
        lab = Label(text=f'Ваши оценки по предмету {instance.text}', font_size=45,
                    size_hint=(1, None),
                    height=80,
                    padding=10,
                    )
        
        self.boxl.add_widget(lab)
        
        for record in records:
            id_of_grade, grade = record
            marks = Button(
                text=f'{grade}',
                font_size=55,
                size_hint=(None, None),
                size=(250, 250),
                
                background_color=[0.25, 0.96, 0.7, 1],
                background_normal='',
                on_press=partial(self.on_change_grade, subject=name_sub, id_of_grade=id_of_grade)
            )
            
            self.bl.add_widget(marks)
            
        
        con.commit()
        con.close()

    def on_change_grade(self, instance, subject, id_of_grade):
        popup = Popup(title='Изменить оценку', size_hint=(0.7, 0.4))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(text='Введите новую оценку:',font_size = 40)
        layout.add_widget(label)
        con = sqlite3.connect('first_db.db')
        c = con.cursor()
        grade_input = TextInput(multiline=False)
        layout.add_widget(grade_input)
        id_of_grade = id_of_grade
        button = Button(
            text='Изменить',
            on_press=lambda instance, id_of_grade=id_of_grade: self.update_grade(instance, popup, subject, grade_input, id_of_grade)
                        )
        layout.add_widget(button)
        
        popup.content = layout
        popup.open()
        con.commit()
        con.close()

    def update_grade(self, instance, popup, subject, new_grade, id_of_grade):
        con = sqlite3.connect('first_db.db')
        c = con.cursor()
        c.execute(f"UPDATE final SET grade = '{new_grade.text}' WHERE subject = '{subject}' and id_of_grade = '{id_of_grade}';")

        con.commit()
        con.close()
        
        
        # Отправка пользователя на главное меню
        self.on_mainpage
        popup.dismiss()

    def build(self):

        Window.clearcolor= (0.3, 0.52, 0.95,1)

        self.al = AnchorLayout(anchor_x='left', anchor_y='top', padding = 10,size_hint=(0.17,0.1))
        self.boxl= BoxLayout(orientation='vertical',  padding=10, size_hint = (1,0.05))
        self.label=Label(text='', font_size=35,size_hint=(1,0.12))
        self.blmain= BoxLayout(orientation='vertical', spacing=10, padding=2)
        self.bl = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=30)
        
        self.scroll_view = ScrollView(size_hint=(1, 1))  # do not touch!!!
        self.bl.bind(minimum_height=self.bl.setter('height'))

        con = sqlite3.connect('first_db.db')
        c = con.cursor()
        c.execute('''CREATE TABLE if not exists final(
              subject text,
              grade text,
              id_of_grade INTEGER
                 )
                  
        
                 ''')
        
        con.commit()
        con.close()



        self.bl.add_widget(Button(text='ПРОСМОТР ОЦЕНОК',
                                    font_size=50,
                                    background_color=[0.25, 0.96, 0.7, 1],
                                    background_normal='',
                                    size_hint_y=None,
                                    size = (900,500),
                                    on_press=self.look_marks))
        
        self.add_marks_button = Button(text='ДОБАВЛЕНИЕ ОЦЕНОК',
                               font_size=50,
                               background_color=[0.25, 0.96, 0.7, 1],
                               background_normal='',
                               size_hint_y=None,
                               size = (900,500),
                               on_press=self.add_marks)
        self.bl.add_widget(self.add_marks_button)
        self.change_marks_button = Button(text='ИЗМЕНЕНИЕ ОЦЕНОК',
                                       font_size=50,
                                       background_color=[0.25, 0.96, 0.7, 1],
                                       background_normal='',
                                       size_hint_y=None,
                                       size = (900,500),
                                       on_press=self.change_marks)
        self.bl.add_widget(self.change_marks_button)
        self.blmain.add_widget(self.al)
        self.blmain.add_widget(self.boxl)
        self.scroll_view.add_widget(self.bl)
        self.blmain.add_widget(self.scroll_view)
        
        return self.blmain

if __name__ == "__main__":
    Application().run()