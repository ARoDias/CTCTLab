# backend/ctct_api/users/validators.py
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, UserAttributeSimilarityValidator,
    CommonPasswordValidator, NumericPasswordValidator)

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return _(
            "A sua palavra-passe deve conter pelo menos %(min_length)d caracteres."
            % {'min_length': self.min_length}
        )

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def get_help_text(self):
        return _("A sua palavra-passe não pode ser semelhante às suas outras informações pessoais.")

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def get_help_text(self):
        return _("A sua palavra-passe não pode ser uma palavra-passe comumente usada.")

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_help_text(self):
        return _("A sua palavra-passe não pode ser inteiramente numérica.")

