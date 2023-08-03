from django.contrib.admin import ModelAdmin
from django.contrib.gis.db import models
from django.contrib.gis.forms import OSMWidget


class GeoModelAdminMixin:
    gis_widget = OSMWidget
    gis_widget_kwargs = {}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if (
            not isinstance(db_field, models.GeometryField)
            or db_field.dim >= 3
            and not self.gis_widget.supports_3d
        ):
            return super().formfield_for_dbfield(db_field, request, **kwargs)
        kwargs["widget"] = self.gis_widget(**self.gis_widget_kwargs)
        return db_field.formfield(**kwargs)


class GISModelAdmin(GeoModelAdminMixin, ModelAdmin):
    pass
