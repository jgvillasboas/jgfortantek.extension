import clr, re
clr.AddReference("PresentationFramework", "WindowsBase", "PresentationCore", "System.Xml")

from System.Windows import Window, Thickness, WindowStartupLocation, ResizeMode, HorizontalAlignment, VerticalAlignment
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock
from System.Windows.Markup import XamlReader
from System.IO import StringReader
from System.Xml import XmlReader
from System import EventHandler
from System.Collections.Generic import List

class ViewSelection(Window):
    def __init__(self, items):

        Window.__init__(self)

        self.Title = "Select Views"
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
        self.search_box.TextChanged += self.on_search_text_changed #changes alwats user start writing
        search_panel.Children.Add(self.search_box)

        #---Bottom Pannel (All Buttons)---
        bottom_panel = StackPanel()
        bottom_panel.Orientation = Orientation.Vertical
        bottom_panel.HorizontalAlignment = HorizontalAlignment.Stretch
        bottom_panel.Margin = Thickness(10)
        DockPanel.SetDock(bottom_panel, Dock.Bottom)
        dock.Children.Add(bottom_panel)

        #---Check/Uncheck/Toggle Panel---
        top_button_panel = StackPanel()
        top_button_panel.Orientation = Orientation.Horizontal
        top_button_panel.HorizontalAlignment = HorizontalAlignment.Center
        top_button_panel.Margin = Thickness(5)
                
        #Check/Uncheck/Toggle Buttons
        self.check_button = Button()
        self.check_button.Content = "Check All"
        self.check_button.Margin = Thickness(5)
        self.check_button.Width = 150
        self.check_button.Height = 25
        self.check_button.Click += self.check_all

        self.uncheck_button = Button()
        self.uncheck_button.Content = "Uncheck All"
        self.uncheck_button.Margin = Thickness(5)
        self.uncheck_button.Width = 150
        self.uncheck_button.Height = 25
        self.uncheck_button.Click += self.uncheck_all

        self.toggle_button = Button()
        self.toggle_button.Content = "Toggle All"
        self.toggle_button.Margin = Thickness(5)
        self.toggle_button.Width = 150
        self.toggle_button.Height = 25
        self.toggle_button.Click += self.toggle_all
        
        top_button_panel.Children.Add(self.check_button)
        top_button_panel.Children.Add(self.uncheck_button)
        top_button_panel.Children.Add(self.toggle_button)    

        #---Select Sheets Panel---
        bot_button_panel = StackPanel()
        bot_button_panel.Orientation = Orientation.Horizontal
        bot_button_panel.HorizontalAlignment = HorizontalAlignment.Center
        bot_button_panel.Margin = Thickness(5)

        #---Select Views Button---
        self.ok_button = Button()
        self.ok_button.Content = "Select Views"
        self.ok_button.Click += self.ok_clicked
        self.ok_button.Width = 200
        self.ok_button.Height = 25
        self.ok_button.Margin = Thickness(0, 0, 0, 0)

        bot_button_panel.Children.Add(self.ok_button)

        #Add Buttons Panel in Bottom Panel
        bottom_panel.Children.Add(top_button_panel)
        bottom_panel.Children.Add(bot_button_panel)
        
        #ListBox
        self.listbox = ListBox()
        self.listbox.SelectionMode = SelectionMode.Multiple
        self.listbox.Margin = Thickness (10)
        self.listbox.ItemsSource = items

        #CheckBox with Xaml
        xaml = """
        <DataTemplate xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
            <CheckBox Content="{Binding Display}" IsChecked="{Binding IsSelected}" />
        </DataTemplate>
        """
        reader = XmlReader.Create(StringReader(xaml))
        template = XamlReader.Load(reader)
        self.listbox.ItemTemplate = template

        dock.Children.Add(self.listbox)
     
    def ok_clicked(self, sender, args):
        self.DialogResult = True
        self.Close()

    def check_all(self, sender, args):
        for item in self.original_items:
            item.IsSelected = True
        self.refresh_list()

    def uncheck_all(self, sender, args):
        for item in self.original_items:
            item.IsSelected = False
        self.refresh_list()

    def toggle_all(self, sender, args):
        for item in self.original_items:
            item.IsSelected = not item.IsSelected
        self.refresh_list()

    def refresh_list(self):
        self.listbox.ItemsSource = None
        self.listbox.ItemsSource = [item for item in self.original_items if self.search_box.Text.lower() in str(item).lower()]

    def on_search_text_changed(self, sender, args):
        search_term = self.search_box.Text.lower()
        filtered = [item for item in self.original_items if search_term in str(item).lower()]
        self.listbox.ItemsSource = filtered

    def get_selected_items(self):
        selected_wrappers = [item for item in self.original_items if item.IsSelected]
        selected_views = [vw.views for vw in selected_wrappers]
        
        return selected_wrappers, selected_views
class ViewWrapper(object):
    def __init__(self, views):
        self.views = views
        self.Display = "{}".format(self.views.Name)
        self.IsSelected = False

    def __str__(self):
        return self.Display
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def alphanum_key(s):
        parts = re.split('(\d+)', s)
        return [int (p) if p.isdigit() else p.lower() for p in parts]
    




