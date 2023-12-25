from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from monitoring.models import Subject, Variant, Exercise, Answer, User, Teacher


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    pass



# @admin.register(Variant)
# class VariantAdmin(TranslationAdmin):
#     list_display = ('title',)
#     # list_filter = ["subject"]
#     group_fieldsets = True
#
#     def get_queryset(self, request):
#         # Foydalanuvchiga faqat o'zi yaratgan postlarni o'zgartirish va o'chirishga ruxsat berish
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             return qs.filter(teacher__user=request.user)
#         return qs
#
#     def render_change_form(self, request, context, *args, **kwargs):
#         context['adminform'].form.fields['teacher'].queryset = Teacher.objects.filter(user=request.user)
#         context['adminform'].form.fields['subject'].queryset = Subject.objects.filter(teacher__user=request.user)
#         return super(VariantAdmin, self).render_change_form(request, context, *args, **kwargs)


class AnswerAdmin(admin.TabularInline):
    model = Answer
    extra = 4

#
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]



# @admin.register(Exercise)
# class ExerciseAdmin(TranslationAdmin):
#     list_filter = ["variant"]
#     group_fieldsets = True
#
#     def get_object(self, request, *args, **kwargs):
#         request._admin_obj = super(ExerciseAdmin, self).get_object(*args, **kwargs)
#         return request._admin_obj
#
#     def get_queryset(self, request):
#         # Foydalanuvchiga faqat o'zi yaratgan postlarni o'zgartirish va o'chirishga ruxsat berish
#         qs = super().get_queryset(request)
#         return qs.filter(variant__teacher__user=request.user)
#
#     def render_change_form(self, request, context, *args, **kwargs):
#         context['adminform'].form.fields['variant'].queryset = Variant.objects.filter(
#             subject__teacher__user=request.user)
#         return super(ExerciseAdmin, self).render_change_form(request, context, *args, **kwargs)

# @admin.register(Answer)
# class PostAdmin(admin.ModelAdmin):
#     pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass