from Autodesk.Revit.DB import FilteredElementCollector, View

class NewNameHelper:
    def __init__(self, doc):
        self.existing_names = {v.Name for v in FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType()}
        
    def get_unique_name(self, base_name):
        if base_name not in self.existing_names:
            self.existing_names.add(base_name)
            return base_name
        
        i = 1

        new_name = "{}_{}".format(base_name, i)
        while new_name in self.existing_names:
            i += 1
            new_name = "{}_{}".format(base_name, i)
            
        self.existing_names.add(new_name)
        return new_name