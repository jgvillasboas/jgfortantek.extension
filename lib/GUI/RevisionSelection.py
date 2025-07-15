import clr
clr.AddReference("PresentationFramework", "WindowsBase", "PresentationCore")

from System.Windows import Window, Thickness, WindowStartupLocation, ResizeMode, HorizontalAlignment, VerticalAlignment
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock
from System.Windows.Markup import XamlReader
from System.IO import StringReader
from System.Xml import XmlReader
from System import EventHandler
from System.Collections.Generic import List

class RevisionSelection(Window):
    def __init__(self, revisions):

        Window.__init__(self)

        self.Title = "Select Revisions"
        self.Width = 600
        self.Height = 800
        self.WindowStartupLocation = WindowStartupLocation.CenterScreen
        self.ResizeMode = ResizeMode.NoResize
        self.original_items = list(revisions)
        dock = DockPanel()
        self.Content = dock

        #OK Button
        self.ok_button = Button()
        self.ok_button.Width = 200
        self.ok_button.Height = 25
        self.ok_button.Content = "Select Revisions"
        self.ok_button.Margin = Thickness(5)
        DockPanel.SetDock(self.ok_button, Dock.Bottom)
        dock.Children.Add(self.ok_button)

        #List
        self.listbox = ListBox()
        self.listbox.SelectionMode = SelectionMode.Multiple
        self.listbox.Margin = Thickness (5)
        self.listbox.ItemsSource = revisions
        
        #CheckBox with Xaml
        xaml = """
        <DataTemplate xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
            <CheckBox Content="{Binding Display}" IsChecked="{Binding IsSelected}" />
        </DataTemplate>
        """
        reader = XmlReader.Create(StringReader(xaml))
        template = XamlReader.Load(reader)
        self.listbox.ItemTemplate = template

        DockPanel.SetDock(self.listbox, Dock.Top)
        dock.Children.Add(self.listbox)

        self.ok_button.Click += self.ok_clicked

    def ok_clicked(self, sender, args):
        self.DialogResult = True
        self.Close()

    def get_selected_revisions(self):
        return [item for item in self.original_items if item.IsSelected]

class RevisionWrapper(object):
    def __init__(self, revision):
        self.revision = revision
        self.Id = revision.Id
        self.Display =  "Seq: {} | Date: {} | Description: {}".format(self.revision.SequenceNumber, self.revision.RevisionDate, self.revision.Description)
        self.IsSelected = False

    def __str__(self):
        return self.Display
    
    def __repr__(self):
        return self.__str__()





