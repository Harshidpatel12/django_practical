from django.core.exceptions import ValidationError

def validate_password_length(value):
    if len(value) < 5:
        raise ValidationError("Password must be at least 5 characters long.") 