from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from monitoring.models import *


@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Variant)
class VariantTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Exercise)
class ExerciseTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ('text',)


# @register(MainResult)
# class MainResultTranslationOptions(TranslationOptions):
#     fields = ('subject_name', 'subject_variant')
#
#
# @register(InfoResult)
# class InfoResultTranslationOptions(TranslationOptions):
#     fields = ('subject_name', 'subject_variant', 'exercise_text',)
