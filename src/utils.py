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
    

def format_headers(input_str):
    words = []
    current_word = ''

    for char in input_str:
        if char.isalpha():
            current_word += char
        elif current_word:
            words.append(current_word)
            current_word = ''

    if current_word:
        words.append(current_word)

    formatted_str = ' '.join(word.capitalize() for word in words)
    return formatted_str

# Test the function with examples
# print(format_headers("student_id"))            # Output: Student Id
# print(format_headers("Avg_Test_score"))        # Output: Avg Test Score
# print(format_headers("stUdy_hours-Per_Week"))  # Output: Study Hours Per Week





    
    
    