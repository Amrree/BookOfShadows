"""
Mobile-optimized UI components for Book of Shadows - The Crone
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.metrics import dp
from kivy.core.window import Window

class MobileButton(Button):
    """Mobile-optimized button with touch-friendly sizing."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        kwargs.setdefault('font_size', dp(16))
        super().__init__(**kwargs)

class MobileTextInput(TextInput):
    """Mobile-optimized text input."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        kwargs.setdefault('font_size', dp(16))
        kwargs.setdefault('multiline', False)
        super().__init__(**kwargs)

class MobileLabel(Label):
    """Mobile-optimized label."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', dp(16))
        kwargs.setdefault('text_size', (None, None))
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'middle')
        super().__init__(**kwargs)

class MobileHeader(Label):
    """Mobile-optimized header label."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', dp(20))
        kwargs.setdefault('bold', True)
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(56))
        super().__init__(**kwargs)

class MobileSpinner(Spinner):
    """Mobile-optimized spinner."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        kwargs.setdefault('font_size', dp(16))
        super().__init__(**kwargs)

class MobileCheckBox(CheckBox):
    """Mobile-optimized checkbox."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(48), dp(48)))
        super().__init__(**kwargs)

class MobileSwitch(Switch):
    """Mobile-optimized switch."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(80), dp(40)))
        super().__init__(**kwargs)

class MobileSlider(Slider):
    """Mobile-optimized slider."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        super().__init__(**kwargs)

class MobileCard(BoxLayout):
    """Mobile card component."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('padding', dp(16))
        kwargs.setdefault('spacing', dp(8))
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(120))
        super().__init__(**kwargs)
        
        # Add card styling
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.2, 0.2, 0.2, 1)  # Dark background
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8)]
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MobileList(ScrollView):
    """Mobile-optimized list component."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.list_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        
        self.add_widget(self.list_layout)
    
    def add_item(self, widget):
        """Add an item to the list."""
        self.list_layout.add_widget(widget)
    
    def clear_items(self):
        """Clear all items from the list."""
        self.list_layout.clear_widgets()

class MobileForm(BoxLayout):
    """Mobile-optimized form component."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('spacing', dp(16))
        kwargs.setdefault('padding', dp(16))
        super().__init__(**kwargs)
    
    def add_field(self, label_text, widget, required=False):
        """Add a form field."""
        field_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(4)
        )
        
        label = MobileLabel(text=label_text)
        if required:
            label.text += " *"
            label.color = (1, 0.5, 0.5, 1)  # Red for required fields
        
        field_layout.add_widget(label)
        field_layout.add_widget(widget)
        
        self.add_widget(field_layout)

class MobileDialog(Popup):
    """Mobile-optimized dialog."""
    
    def __init__(self, title="", content=None, **kwargs):
        kwargs.setdefault('size_hint', (0.9, 0.8))
        kwargs.setdefault('auto_dismiss', True)
        super().__init__(title=title, content=content, **kwargs)

class MobileActionSheet(Popup):
    """Mobile action sheet."""
    
    def __init__(self, title="", actions=None, **kwargs):
        kwargs.setdefault('size_hint', (0.9, 0.6))
        kwargs.setdefault('auto_dismiss', True)
        
        content = BoxLayout(orientation='vertical', spacing=dp(8))
        
        if title:
            header = MobileHeader(text=title)
            content.add_widget(header)
        
        if actions:
            for action_text, action_callback in actions:
                btn = MobileButton(text=action_text)
                btn.bind(on_press=lambda x, callback=action_callback: self.dismiss() or callback())
                content.add_widget(btn)
        
        super().__init__(content=content, **kwargs)

class MobileNavigation(BoxLayout):
    """Mobile navigation component."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'horizontal')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(56))
        kwargs.setdefault('spacing', dp(4))
        super().__init__(**kwargs)
    
    def add_tab(self, text, callback):
        """Add a navigation tab."""
        btn = MobileButton(text=text)
        btn.bind(on_press=callback)
        self.add_widget(btn)

class MobileSearchBar(BoxLayout):
    """Mobile search bar component."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'horizontal')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(56))
        kwargs.setdefault('spacing', dp(8))
        super().__init__(**kwargs)
        
        self.search_input = MobileTextInput(hint_text="Search...")
        self.add_widget(self.search_input)
        
        self.search_button = MobileButton(text="Search", size_hint_x=None, width=dp(80))
        self.add_widget(self.search_button)
    
    def bind_search(self, callback):
        """Bind search callback."""
        self.search_button.bind(on_press=lambda x: callback(self.search_input.text))

class MobileFloatingActionButton(Button):
    """Mobile floating action button."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(56), dp(56)))
        kwargs.setdefault('font_size', dp(24))
        super().__init__(**kwargs)
        
        # Position at bottom right
        self.pos_hint = {'right': 1, 'bottom': 1}
        
        # Style as FAB
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, Ellipse
            Color(0.2, 0.6, 1, 1)  # Blue background
            self.circle = Ellipse(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_circle, size=self.update_circle)
    
    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size