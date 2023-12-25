from django.urls import path, reverse_lazy

from monitoring.views import index_view, show_subject_view, show_subject_variants_view, show_question, \
    SelectedVariant, create_main_result_record, show_result, show_result_2, show_result_3, show_temp_confirm_to_exit, \
    absolute_confirm_view, ProfileView, EditProdileView, DeleteProfileView, VariantCreateView, ChangePasswordView

urlpatterns = [
    path('', index_view, name='home'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('edit_profile/<int:pk>/', EditProdileView.as_view(), name="edit_profile"),
    path('delete_profile/<int:pk>/', DeleteProfileView.as_view(), name="delete_profile"),
    path('test_ishlash/', show_subject_view, name='solve_test'),
    path('test_ishlash/<int:subject_id>', show_subject_variants_view, name='solve_test'),
    path('test_ishlash/<int:subject_id>/<int:variant_id>/<int:exercise_id>', show_question, name='solve_test'),
    path('natijalar/<slug:username>', show_result, name='show_result'),
    path('natijalar/<slug:username>/<int:subject_id>', show_result_2, name='show_result'),
    path('natijalar/<slug:username>/<int:subject_id>/<int:sub_variant_id>', show_result_3, name='show_result'),
    path('select_var/<int:subject_id>/<int:subject_variant_id>/<int:exercise_id>', SelectedVariant, name='test'),
    path('create_info_table/<int:subject_id>/<int:variant_id>', create_main_result_record, name='create_main_info'),
    path('confirm_to_exit/<int:subject_id>/<int:subject_var_id>/<int:user_id>/<slug:url>', show_temp_confirm_to_exit,
         name="confirm_to_exit"),
    path('absolute_confirm/<int:subject_id>/<int:subject_var_id>/<int:user_id>/<slug:url>', absolute_confirm_view,
         name="absolute_confirm"),
    path('variant/create/', VariantCreateView.as_view(), name='variant_create'),
    path('password-change/123', ChangePasswordView.as_view(), name='password_change')

]
