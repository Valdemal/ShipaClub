from django.contrib import admin
from .models import Post, Rubric, Estimation


class EstimationAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'value')
    list_display_links = ('post', 'user')
    search_fields = ('post__name', 'user__username')


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'published', 'rubric')
    list_display_links = ('name', 'info')
    search_fields = ('name', 'rubric__name', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)

        form.base_fields['author'].initial = request.user

        if not request.user.is_superuser:
            form.base_fields['author'].disabled = request.user

        return form


admin.site.register(Post, PostAdmin)
admin.site.register(Rubric)
admin.site.register(Estimation, EstimationAdmin)
