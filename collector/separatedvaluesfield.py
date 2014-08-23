from django.forms.fields import MultipleChoiceField
from django.core import validators
from django.db import models
from django.core import exceptions
from django.utils.text import capfirst
from django.utils.six import with_metaclass


class SeparatedValuesField(with_metaclass(models.SubfieldBase, models.CharField)):
    #__metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self._choices and value:
            choices = []

            for option_key, option_value in self.choices:
                if isinstance(option_value, (list, tuple)):
                    # This is an optgroup, so look inside the group for
                    # options.
                    for optgroup_key, optgroup_value in option_value:
                        choices.append(optgroup_key)
                else:
                    choices.append(option_key)

            for val in value:
                if val and not val in choices:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % val)

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])

    def to_python(self, value):
        if not value:
            return

        if isinstance(value, list):
            return value

        return value.split(self.token)

    def get_db_prep_value(self, value, **kwargs):
        if not value:
            return

        assert(isinstance(value, list) or isinstance(value, tuple))

        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        return self.token.join([str(s) for s in value])
        value = self._get_val_from_obj(obj)

        return self.get_db_prep_value(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^collector\.separatedvaluesfield\.SeparatedValuesField"])
except ImportError:
    pass
