import re
class Validator:
    __valid_dict = {
        "email" : r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    }
    def __init__(self):
        return
        
    def validate(self, type, input):
        """Validates `input` for `type`"""
        pattern = self.__valid_dict[type]
        input = self.clean(input)
        return re.match(pattern, input) is not None
    
    def clean(self, s):
        return s.strip().lower()
    


# Test for validate()
# email = "example@email.com"
# if Validator().validate("email", email):
#     print("Valid email address")
# else:
#     print("Invalid email address")


# Test for clean()
# email = " ExAmplE@gmail.coM         "
# print(Validator().clean(email))

    
    
    