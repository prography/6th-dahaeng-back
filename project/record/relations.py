from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework.relations import RelatedField


class QuestionRelatedField(RelatedField):
    def __init__(self, slug_field=None, **kwargs):
        assert slug_field is not None, 'The `slug_field` argument is required.'
        self.slug_field = slug_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return str(value)
