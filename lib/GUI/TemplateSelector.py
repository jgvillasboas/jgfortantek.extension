import clr
clr.AddReference("PresentationFramework", "WindowsBase", "PresentationCore")

from System.Windows import Window, Thickness, WindowStartupLocation, ResizeMode, HorizontalAlignment, VerticalAlignment
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock
from System.IO import StringReader
from System import EventHandler
from System.Collections.Generic import List

class TemplateSelector(Window):
    def __init__(self, items):

        Window.__init__(self)


        self.Title = "Select a ViewTemplate"
        self.Width = 600
        self.Height = 800
        self.WindowStartupLocation = WindowStartupLocation.CenterScreen
        self.ResizeMode = ResizeMode.CanResize
        self.original_items = list(items)
        dock = DockPanel()
        self.Content = dock

        #---Search Panel---
        search_panel = StackPanel()
        search_panel.Orientation = Orientation.Horizontal
        search_panel.HorizontalAlignment = HorizontalAlignment.Left
        DockPanel.SetDock(search_panel, Dock.Top)
        dock.Children.Add(search_panel)
        
        search_label = TextBlock()
        search_label.Text = "Search:"
        search_label.Margin = Thickness(5, 7 , 5, 5)
        search_panel.VerticalAlignment = VerticalAlignment.Center
        search_panel.Children.Add(search_label)

        self.search_box = TextBox()
        self.search_box.Margin = Thickness(10) 
        self.search_box.Width = 517
        self.search_box.HorizontalAlignment = HorizontalAlignment.Left
        self.search_box.TextChanged += self.on_search_text_changed #changes always user start writing
        search_panel.Children.Add(self.search_box)

        #OK Button
        self.ok_button = Button()
        self.ok_button.Height = 30
        self.ok_button.Content = "OK"
        DockPanel.SetDock(self.ok_button, Dock.Bottom)
        dock.Children.Add(self.ok_button)

        #List
        self.listbox = ListBox()
        self.listbox.SelectionMode = SelectionMode.Single
        self.listbox.Margin = Thickness (5)
        self.listbox.ItemsSource = items

        DockPanel.SetDock(self.listbox, Dock.Top)
        dock.Children.Add(self.listbox)
     
        self.ok_button.Click += self.ok_clicked

    def ok_clicked(self, sender, args):
        self.DialogResult = True
        self.Close()

    def on_search_text_changed(self, sender, args):
            search_term = self.search_box.Text.lower()
            filtered = [item for item in self.original_items if search_term in str(item).lower()]
            self.listbox.ItemsSource = filtered




