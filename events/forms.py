from django import forms
from events.models import Event,Catagory



class StyledFormMixin():

    def __init__(self,*args,**kargs):
            super().__init__(*args,**kargs)
            self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300  w-[100%] rounded-lg shadow-sm focus:outine-none focus:border-rose-500 focus:ring-rose-300"
    otherwise = "border-2 border-gray-300  rounded-lg shadow-sm focus:outine-none focus:border-rose-500 focus:ring-rose-300"
    iamge = "border-2 border-gray-300 rounded-lg shadow-sm p-2 w-full file:bg-rose-500 file:text-white file:px-4 file:py-2 file:rounded-lg file:border-none file:cursor-pointer hover:file:bg-rose-600"
   
    
    def apply_styled_widgets(self):
          
          for field_name,field in self.fields.items():
                if isinstance(field.widget,forms.TextInput):
                      field.widget.attrs.update({
                            "class":self.default_classes,
                            "placeholder": f"Enter {field.label.lower()}"
                      })
     
                elif isinstance(field.widget, forms.EmailInput):
                  # EmailField
                  field.widget.attrs.update({
                            "class":self.default_classes,
                            "placeholder": f"Enter {field.label.lower()}"
                      })
                  
                elif isinstance(field.widget, forms.Textarea):
                  # TextField
                  field.widget.attrs.update({
                            "class":self.default_classes,
                            "placeholder": f"Enter {field.label.lower()}"
                      })
      
           
                elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                  # CheckboxSelectMultiple (for MultipleChoiceField)
                    field.widget.attrs.update({
                    "class": "space-y-2"
                   })
                    

                elif isinstance(field.widget, forms.SelectDateWidget) or isinstance(field.widget, forms.TimeInput):
                  #Date or Time fields
                  field.widget.attrs.update({
                  "class": self.otherwise
                  })


                elif isinstance(field.widget, forms.ClearableFileInput):
                     field.widget.attrs.update({
                          "class":self.iamge,
                          "placeholder": f"Upload {field.label.lower()}",
                     })
                  
                elif isinstance(field.widget, forms.PasswordInput):
                        # Password field styling
                        field.widget.attrs.update({
                              "class": self.default_classes,
                              "placeholder": f"Enter {field.label.lower()}"
                        })
               

                else:
                     field.widget.attrs.update({
                            "class":self.otherwise
                      })
                     
               




             

             
             


class CatagoryModelForm(StyledFormMixin,forms.ModelForm):
      class Meta:
            model = Catagory
            fields = ["catagoryName","catagoryDescription"]
      

                


class EventModelForm(StyledFormMixin,forms.ModelForm):
      class Meta:
            model = Event
            fields = ["eventName","eventDate","eventTime","eventLocation","catagory", "participants","eventImage"]

            widgets = {
                 "participants":forms.CheckboxSelectMultiple,
                 "catagory": forms.Select,
                 "eventDate": forms.SelectDateWidget,
                 "eventTime": forms.TimeInput(attrs={'type': 'time'}),
            }



""" 



  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>


 """
