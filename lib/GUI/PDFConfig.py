import clr
clr.AddReference("PresentationFramework", "WindowsBase", "PresentationCore", "System.Xml")

from System.Windows import Window, Thickness, WindowStartupLocation, ResizeMode, HorizontalAlignment, VerticalAlignment
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock, ComboBox
from System.Windows.Markup import XamlReader
from System.IO import StringReader
from System.Xml import XmlReader
from System import EventHandler
from System.Collections.Generic import List

class PDFConfig(Window):
    def __init__(self, items):
        Window.__init__(self)

        self.Title = "PDF Configuration"
        self.Width, self.Height = 800, 800
        self.WindowStartupLocation = WindowStartupLocation.CenterScreen
        self.ResizeMode = ResizeMode.CanResize
        self.original_items = list(items)
        dock = DockPanel()
        self.Content = dock

        #StackPanel for Buttons
        button_panel = StackPanel(Orientation = Orientation.Vertical, HorizontalAlignment = HorizontalAlignment.Stretch, 
                                  Margin = Thickness(10))
        DockPanel.SetDock(button_panel, Dock.Bottom)
        dock.Children.Add(button_panel)

        #OK and Cancel Buttons
        self.ok_button = Button(Content = "OK", Width = 100, Height = 25, Margin = Thickness(5))
        self.cancel_button = Button(Content = "Cancel", Width = 100, Height = 25, Margin = Thickness(5))
        button_panel.Children.Add(self.ok_button)
        button_panel.Children.Add(self.cancel_button)

        #---File Location---
        location_group = StackPanel(Orientation=Orientation.Vertical, HorizontalAlignment = HorizontalAlignment.Left, Margin = Thickness(10))
        location_label = TextBlock(Text = "File Location", FontWeight = "Bold")
        location_group.Children.Add(location_label)

        location_panel = StackPanel(Orientation = Orientation.Horizontal)
        self.location_path = TextBox(Width = 300, Margin = Thickness(0, 0, 5, 0), IsReadOnly = True)

        browse_button = Button(Content = "Browse...", Width = 80)
        browse_button.Click += self.on_browse_click
        location_panel.Children.Add(self.location_path)
        location_panel.Children.Add(browse_button)
        location_group.Children.Add(location_panel)

        dock.Children.Add(location_group)

        #---Page Size---
        size_group = StackPanel(Orientation = Orientation.Vertical, HorizontalAlignment = HorizontalAlignment.Left, Margin = Thickness(10))
        size_label = TextBlock(Text = "Size", FontWeight = "Bold")
        size_group.Children.Add(size_label)

        page_size_panel = StackPanel(Orientation = Orientation.Horizontal)
        page_size_label = TextBlock(Text = "Page Size", Width = 100)
        self.page_size_combo = ComboBox(Items = ["A0", "A1", "A2", "A3", "A4"], SelectedIndex = 0, Width = 100)
        page_size_panel.Children.Add(page_size_label)
        page_size_panel.Children.Add(self.page_size_combo)
        size_group.Childre.Add(page_size_panel)

        #---Zoom---
        


        




