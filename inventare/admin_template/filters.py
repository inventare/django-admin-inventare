from django.db import models
from django.contrib.admin import filters
from django.contrib.admin.exceptions import NotRegistered
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import (
    build_q_object_from_lookup_parameters,
    get_last_value_from_parameters,
    get_model_from_relation,
)
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IncorrectLookupParameters

class SelectBooleanFilter(filters.FieldListFilter):
    template = "admin/filters/boolean_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = "%s__exact" % field_path
        self.lookup_kwarg2 = "%s__isnull" % field_path
        
        self.lookup_val = get_last_value_from_parameters(params, self.lookup_kwarg)
        self.lookup_val2 = ""

        if self.lookup_val == "null":
            self.lookup_val = "0"
            self.lookup_val2 = "True"

        if not self.lookup_val and self.lookup_kwarg in params:
            params.pop(self.lookup_kwarg)

        super().__init__(field, request, params, model, model_admin, field_path)
        
        if (
            self.used_parameters
            and self.lookup_kwarg in self.used_parameters
            and self.used_parameters[self.lookup_kwarg] in ("1", "0")
        ):
            self.used_parameters[self.lookup_kwarg] = bool(
                int(self.used_parameters[self.lookup_kwarg])
            )
        
    def expected_parameters(self):
        return [self.lookup_kwarg]

    def queryset(self, request, queryset):
        try:
            if self.lookup_val2 == "True":
                q_object = build_q_object_from_lookup_parameters({ self.lookup_kwarg2: [True] })
            else:
                q_object = build_q_object_from_lookup_parameters(self.used_parameters)
            return queryset.filter(q_object)
        except (ValueError, ValidationError) as e:
            # Fields may raise a ValueError or ValidationError when converting
            # the parameters to the correct type.
            raise IncorrectLookupParameters(e)

    def get_facet_counts(self, pk_attname, filtered_qs):
        return {
            "true__c": models.Count(
                pk_attname, filter=models.Q(**{self.field_path: True})
            ),
            "false__c": models.Count(
                pk_attname, filter=models.Q(**{self.field_path: False})
            ),
            "null__c": models.Count(
                pk_attname, filter=models.Q(**{self.lookup_kwarg2: True})
            ),
        }
    
    def choices(self, changelist):
        # FIXME: remove the query_string property

        field_choices = dict(self.field.flatchoices)
        for lookup, title, count_field in (
            (None, _("All"), None),
            ("1", field_choices.get(True, _("Yes")), "true__c"),
            ("0", field_choices.get(False, _("No")), "false__c"),
        ):
            yield {
                "selected": self.lookup_val == lookup and not self.lookup_val2,
                "value": lookup or "",
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg: lookup}, [self.lookup_kwarg2]
                ),
                "display": title,
                'inline_display': title if lookup else self.title,
            }
        #FIXME: continue here!!!!!!!!!
        if self.field.null:
            display = field_choices.get(None, _("Unknown"))
            yield {
                "selected": self.lookup_val2 == "True",
                "value": "null",
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg: "null"}, [self.lookup_kwarg2]
                ),
                "display": display,
                'inline_display': display,
            }

filters.FieldListFilter.register(
    lambda f: isinstance(f, models.BooleanField),
    SelectBooleanFilter,
    True
)

class RelatedFieldListFilter(filters.FieldListFilter):
    template = "admin/filters/related_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.request = request
        self.model_admin = model_admin

        self.other_model = get_model_from_relation(field)
        self.lookup_kwarg = "%s__%s__exact" % (field_path, field.target_field.name)
        self.lookup_val = params.get(self.lookup_kwarg)
        
        self.lookup_val_isnull = False
        if self.lookup_val == "null":
            self.lookup_val_isnull = True
            self.lookup_val = []
        
        super().__init__(field, request, params, model, model_admin, field_path)
        #self.lookup_choices = self.field_choices(field, request, model_admin)
        if hasattr(field, "verbose_name"):
            self.lookup_title = field.verbose_name
        else:
            self.lookup_title = self.other_model._meta.verbose_name
        self.title = self.lookup_title
        self.empty_value_display = model_admin.get_empty_value_display()
    
    def expected_parameters(self):
        return [self.lookup_kwarg]
    
    @property
    def include_empty_choice(self):
        """
        Return True if a "(None)" choice should be included, which filters
        out everything except empty relationships.
        """
        return self.field.null or (self.field.is_relation and self.field.many_to_many)

    def choices(self, changelist):
        if self.lookup_val:
            try:
                instance = self.other_model._default_manager.get(pk=self.lookup_val[0])
            except self.other_model.DoesNotExist as e:
                # TODO: make some action here?
                raise e
            return [
                {
                    "selected": True,
                    "query_string": changelist.get_query_string({self.lookup_kwarg: instance.pk}),
                    "display": str(instance),
                }
            ]
        return []

filters.FieldListFilter.register(
    lambda f: f.remote_field,
    RelatedFieldListFilter,
    True
)
