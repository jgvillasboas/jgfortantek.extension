import clr
clr.AddReference("PresentationFramework", "WindowsBase", "PresentationCore")

from System.Windows import Window, Thickness, WindowStartupLocation, ResizeMode, HorizontalAlignment
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, StackPanel, Orientation

class LinkSelector(Window):
    def __init__(self, items):
        Window.__init__(self)

        self.Title = "Select Revit Links"
        self.Width = 600
        self.Height = 400
        self.WindowStartupLocation = WindowStartupLocation.CenterScreen
        self.ResizeMode = ResizeMode.CanResize if hasattr(ResizeMode, "CanResize") else ResizeMode.NoResize

        dock = DockPanel()
        self.Content = dock

        #Show and Hide Button
        button_panel = StackPanel()
        button_panel.Orientation = Orientation.Horizontal
        button_panel.HorizontalAlignment = HorizontalAlignment.Right
        button_panel.Margin = Thickness(5)

        self.show_button = Button()
        self.show_button.Height = 30
        self.show_button.Width = 120
        self.show_button.Content = "Show Selected"
        self.show_button.Margin = Thickness(5, 0, 5, 0)
        button_panel.Children.Add(self.show_button)

        self.hide_button = Button()
        self.hide_button.Height = 30
        self.hide_button.Width = 120
        self.hide_button.Content = "Hide Selected"
        self.hide_button.Margin = Thickness(5, 0, 0, 0)
        button_panel.Children.Add(self.hide_button)

        DockPanel.SetDock(button_panel, Dock.Bottom)
        dock.Children.Add(button_panel)

        self.action_result = None
        
        self.show_button.Click += self.show_clicked
        self.hide_button.Click += self.hide_clicked

        #List
        self.listbox = ListBox()
        self.listbox.SelectionMode = SelectionMode.Multiple
        self.listbox.Margin = Thickness (5)
        self.listbox.ItemsSource = items
        
        DockPanel.SetDock(self.listbox, Dock.Top)
        dock.Children.Add(self.listbox)



    def show_clicked(self, sender, args):
        self.action_result = True
        self.DialogResult = True
        self.Close()

    def hide_clicked(self, sender, args):
        self.action_result = False
        self.DialogResult = True
        self.Close()
        


        




