from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from monitoring.forms import SignUpForm, MainResultForm, InfoResultForm, VariantForm, ExerciseFormSet, EditProfileForm
from monitoring.models import Subject, Variant, Exercise, Answer, MainResult, InfoResult, User


def index_view(request):
    # print(list(request.session.keys()))
    return render(request, 'pages/index.html')


@login_required(redirect_field_name=None)
def show_subject_view(request):
    subject = Subject.objects.all()
    return render(request, 'pages/choice_subject.html', {'subjects': subject})


@login_required(redirect_field_name=None)
def show_subject_variants_view(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    variants = Variant.objects.filter(subject_id=subject.id)
    # print(variants)
    context = {
        'variants': variants,
        'subject': subject,
        'return_back': request.META.get('HTTP_REFERER')
    }
    return render(request, 'pages/choice_subject_variant.html', context)


@login_required(redirect_field_name=None)
def show_question(request, subject_id, variant_id, exercise_id=1):
    subject = Subject.objects.get(id=subject_id)
    questions = Exercise.objects.filter(variant_id=variant_id)
    user_answers_info = InfoResult.objects.filter(user_id=request.user.id, subject_id=subject_id,
                                                  subject_variant_id=variant_id)
    if len(user_answers_info) < len(questions):
        couple_list = []
        for q in questions:
            data = [q, Answer.objects.filter(exercise=q.id), q.id]
            try:
                InfoResult.objects.get(user_id=request.user.id, exercise_id=q.id, subject_id=subject_id,
                                       subject_variant_id=variant_id)
                is_completed = True
            except:
                is_completed = False

            data.append(is_completed)
            couple_list.append(data)
            # print(q.id)

        variant_name = Variant.objects.get(id=variant_id).title
        completed_len = 0
        try:
            completed_len = len(
                InfoResult.objects.filter(user_id=request.user.id, subject_id=subject_id,
                                          subject_variant_id=variant_id))
        except:
            pass
        if len(couple_list) > 0:
            context = {
                'exercise': {
                    'question': couple_list[exercise_id - 1][0],
                    'variants': couple_list[exercise_id - 1][1],
                    'exercise_id': couple_list[exercise_id - 1][2],
                    'is_completed': couple_list[exercise_id - 1][3],
                },
                'variant': variant_name,
                'exercise_len': len(couple_list),
                'current_exercise_id': exercise_id,
                'subject': subject,
                'variant_id': variant_id,
                'completed_len': completed_len,
                'subject_id': subject_id
            }
            return render(request, 'pages/question.html', context)
    elif len(questions) < 1:
        context = {
            'message': _('Savollar holi yo\'q.'),
            'return_back': request.META.get('HTTP_REFERER')
        }
        return render(request, 'pages/question.html', context)
    return redirect('home')


def create_main_result_record(request, subject_id, variant_id):
    questions = Exercise.objects.filter(variant=variant_id)
    subject = Subject.objects.get(id=subject_id).name
    if len(questions):
        try:
            main_result = MainResult.objects.get(user_id=request.user.id, subject_id=subject_id,
                                                 subject_variant_id=variant_id)
            context = {
                'message': _("""Avval ishlagan!"""),
                'subject_id': subject_id,
                'subject_var_id': variant_id
            }
            return render(request, 'pages/message.html', context)
        except:
            print(222)
            data = {
                'user_id': request.user.id,
                'username': request.user,
                'subject_name': subject,
                'subject_id': subject_id,
                'subject_variant': Variant.objects.get(id=variant_id),
                'subject_variant_id': variant_id,
            }
            form = MainResultForm(data=data)
            if form.is_valid():
                data = form.cleaned_data
                new_record = MainResult(user_id=data['user_id'], username=data['username'],
                                        subject_name=data['subject_name'], subject_id=data['subject_id'],
                                        subject_variant=data['subject_variant'],
                                        subject_variant_id=data['subject_variant_id'])
                new_record.save()
    url = reverse('solve_test', args=(subject_id, variant_id, 1))
    return redirect(url)


@login_required(redirect_field_name=None)
def SelectedVariant(request, subject_id, subject_variant_id, exercise_id):
    if request.method == 'POST':
        selected_var_id = request.POST['option']
        option = Answer.objects.get(id=selected_var_id)
        is_true = option.is_True
        # is_true tepada

        subject_variant = Variant.objects.get(id=subject_variant_id)

        subject = Subject.objects.get(id=subject_id)

        subject_id = Subject.objects.get(name=subject).id

        data = {
            'user_id': request.user.id,
            'username': request.user,
            'subject_name': subject,
            'subject_id': subject_id,
            'subject_variant': subject_variant,
            'subject_variant_id': subject_variant_id,
            'exercise_id': exercise_id,
            'exercise_text': Exercise.objects.get(id=exercise_id),
            'is_resolved_true': is_true,
            'user_selected_variant_id': selected_var_id,
        }
        form = InfoResultForm(data=data)

        question_len = len(Exercise.objects.filter(variant=subject_variant_id))
        user_completed_exercise_len = len(
            InfoResult.objects.filter(user_id=request.user.id, subject_id=subject_id,
                                      subject_variant_id=subject_variant_id))

        if user_completed_exercise_len < question_len:
            if form.is_valid():
                data = form.cleaned_data
                main_result_model = MainResult.objects.get(user_id=data['user_id'],
                                                           subject_id=data['subject_id'],
                                                           subject_variant_id=data['subject_variant_id'], )
                if data['is_resolved_true']:
                    main_result_model.true_resolved_exercise_amount += 1
                    main_result_model.save()
                new_record = InfoResult(user_id=data['user_id'], username=data['username'],
                                        subject_name=data['subject_name'], subject_id=data['subject_id'],
                                        subject_variant=data['subject_variant'],
                                        subject_variant_id=data['subject_variant_id'],
                                        exercise_id=data['exercise_id'], exercise_text=data['exercise_text'],
                                        is_resolved_true=data['is_resolved_true'],
                                        user_selected_variant_id=data['user_selected_variant_id'])
                new_record.save()

            pre_url = request.META.get('HTTP_REFERER')
            next_url = pre_url.split('/')

            completed_exercise_query = InfoResult.objects.filter(user_id=request.user.id, subject_id=subject_id,
                                                                 subject_variant_id=subject_variant_id).values()
            question_query = Exercise.objects.filter(variant_id=subject_variant_id).values()
            question_list = list(question_query)
            not_completed_exercise_list = list(question_query)

            completed_exercise_list = []

            for completed_exercise in completed_exercise_query:
                completed_exer = {
                    'id': completed_exercise['exercise_id'],
                    'text': completed_exercise['exercise_text'],
                    'variant_id': completed_exercise['subject_variant_id']
                }
                completed_exercise_list.append(completed_exer)
            id = 0
            for cel in completed_exercise_list:
                try:
                    ind = not_completed_exercise_list.index(cel)
                    id = not_completed_exercise_list[-1]['id']
                    val = not_completed_exercise_list.pop(ind)
                except:
                    pass
            # print(not_completed_exercise_list[-1]['id'])

            print(data)
            print(id)
            if int(next_url[-1]) < len(Exercise.objects.filter(variant=subject_variant_id)) and data[
                'exercise_id'] != id:
                next_url[-1] = str(int(next_url[-1]) + 1)
                url = '/'.join(next_url)
                return redirect(url)
            else:
                try:
                    url = reverse('solve_test',
                                  args=(
                                      subject_id, subject_variant_id,
                                      question_list.index(not_completed_exercise_list[0]) + 1))
                    return redirect(url)
                except:
                    if len(not_completed_exercise_list) < 1:
                        url = reverse('show_result', args=(request.user, subject_id, subject_variant_id))
                        return redirect(url)
                    else:
                        url = reverse('solve_test',
                                      args=(
                                          subject_id, subject_variant_id,
                                          question_list.index(not_completed_exercise_list[0]) + 1))
                        return redirect(url)
    url = reverse('show_result', args=(request.user, subject_id, subject_variant_id))
    return redirect(url)


@login_required(redirect_field_name=None)
def show_result(request, username):
    # subjects = Subject.objects.all()
    subjects = MainResult.objects.filter(user_id=request.user.id).values()
    subject_list = []
    for subject in subjects:
        print(subject)
        data = {
            'subject_name': Subject.objects.get(id=subject['subject_id']),
            'subject_id': subject['subject_id']
        }
        if data not in subject_list:
            subject_list.append(data)

    context = {
        'subjects': subject_list,
        'user': username
    }
    return render(request, 'pages/result.html', context)


@login_required(redirect_field_name=None)
def show_result_2(request, username, subject_id):
    variants = MainResult.objects.filter(user_id=request.user.id, subject_id=subject_id).values()
    variant_list = []
    for variant in variants:
        print(variant['subject_id'], variant['subject_variant_id'],
              Variant.objects.get(id=variant['subject_variant_id']))
        data = {
            'subject_id': variant['subject_id'],
            'subject_variant_id': variant['subject_variant_id'],
            'sub_variant': Variant.objects.get(id=variant['subject_variant_id'])
        }
        variant_list.append(data)
    context = {
        'subject_variants': variant_list,
        'subject': Subject.objects.get(id=subject_id),
        'has_variant': bool(len(variants))
    }
    return render(request, 'pages/result.html', context)


@login_required(redirect_field_name=None)
def show_result_3(request, username, subject_id, sub_variant_id):
    subject = Subject.objects.get(id=subject_id)
    sub_variant = Variant.objects.get(id=sub_variant_id)
    try:
        main_result = MainResult.objects.get(user_id=request.user.id, subject_id=subject_id,
                                             subject_variant_id=sub_variant_id)
        info_result = InfoResult.objects.filter(user_id=request.user.id, subject_id=subject_id,
                                                subject_variant_id=sub_variant_id)
    except:
        context = {
            'message': _("""Bu variantni ishlamagansan garang!"""),
            'natijani_kurish': True
        }
        return render(request, 'pages/message.html', context)
    question_len = len(info_result)

    obj = {}
    exercises = Exercise.objects.filter(variant=sub_variant_id)
    if len(info_result) > 0:
        for info in info_result:
            obj[info.exercise_id] = info.is_resolved_true

    info_list = []
    son = 1
    for ex in exercises[:question_len]:
        user_select_var_id = InfoResult.objects.get(user_id=request.user.id, subject_id=subject_id,
                                                    subject_variant_id=sub_variant_id,
                                                    exercise_id=ex.id).user_selected_variant_id
        info_obj = {}
        info_obj['exer_text'] = ex.text
        try:
            info_obj['selected_var'] = Answer.objects.get(id=user_select_var_id).option
        except:
            info_obj['selected_var'] = '—'
        info_obj['true_variant'] = Answer.objects.get(exercise_id=ex.id, is_True=True)
        info_obj['son'] = son
        try:
            info_obj['is_true'] = '✓' if obj[ex.id] else '✕'
        except:
            info_obj['is_true'] = '✕'
        info_list.append(info_obj)
        son += 1

    context = {
        'ball': main_result.true_resolved_exercise_amount,
        'sub': subject,
        'sub_var': sub_variant,
        'question_len': question_len,
        'foiz': int(round(main_result.true_resolved_exercise_amount / (question_len / 100))),
        'info': info_list,
        'exercises': exercises,
    }
    return render(request, 'pages/result.html', context)


def show_temp_confirm_to_exit(request, subject_id, subject_var_id, user_id, url):
    previous_url = request.META.get('HTTP_REFERER')
    context = {
        'url': url,
        'pre_url': previous_url,
        'subject_id': subject_id,
        'variant_id': subject_var_id,
    }
    return render(request, 'pages/tochnami.html', context)


def absolute_confirm_view(request, subject_id, subject_var_id, user_id, url):
    subject = Subject.objects.get(id=subject_id)
    completed_exercise = InfoResult.objects.filter(user_id=user_id, subject_id=subject_id,
                                                   subject_variant_id=subject_var_id)
    completed_exercises_id_list = []
    for com_exer in completed_exercise:
        completed_exercises_id_list.append(com_exer.exercise_id)

    questions = Exercise.objects.filter(variant=subject_var_id)
    list = []
    for q in questions:
        if q.id not in completed_exercises_id_list:
            list.append(q)

    data = {
        'user_id': user_id,
        'username': request.user,
        'subject_name': subject,
        'subject_id': subject_id,
        'subject_variant': Variant.objects.get(id=subject_var_id),
        'subject_variant_id': subject_var_id,
        'is_resolved_true': False
    }

    for l in list:
        new_record = InfoResult(user_id=data['user_id'], username=data['username'],
                                subject_name=data['subject_name'], subject_id=data['subject_id'],
                                subject_variant=data['subject_variant'], subject_variant_id=data['subject_variant_id'],
                                exercise_id=l.id, exercise_text=l.text, user_selected_variant_id=-1,
                                is_resolved_true=data['is_resolved_true'])
        new_record.save()

    if url == 'show_result':
        url = reverse(url, args=(request.user,))
    elif 'profile' in url:
        url = reverse(url, args=(user_id,))
    else:
        url = reverse(url)
    return redirect(url)


# def edit_view(request):
#     return render(request, 'pages/edit.html')
#
#
# class AddSubjectView(View):
#     def get(self, request):
#         form = SubjectAddForm()
#         return render(request, 'pages/add_subject.html', {'form': form})
#
#     def post(self, request):
#         form = SubjectAddForm(data=request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             new_subject = Subject(subject_name=form.cleaned_data['subject_name'])
#             new_subject.save()
#             return redirect('home')
#
#
# class DeleteSubjectPageView(View):
#     def get(self, request):
#         subjects = Subject.objects.all()
#         return render(request, 'pages/delete_subject.html', {'subjects': subjects})
#
#
# class DeleteSubjectConfirmView(View):
#     def get(self, request, subject):
#         subject = Subject.objects.get(subject_name=subject)
#         subject.delete()
#         return redirect('home')
#
class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


class ProfileView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = MainResult.objects.filter(user_id=self.kwargs['pk']).values()
        variant_dict = {}
        for variant in variants:
            subject = Subject.objects.get(id=variant['subject_id']).name
            variant_title = Variant.objects.get(id=variant['subject_variant_id']).title
            data = {
                'subject_id': variant['subject_id'],
                'subject_variant_id': variant['subject_variant_id'],
                'sub_variant': Variant.objects.get(id=variant['subject_variant_id'])
            }
            try:
                variant_dict[f'{subject}'][f'{variant_title}'] = data
            except:
                variant_dict[f'{subject}'] = {}
                variant_dict[f'{subject}'][f'{variant_title}'] = data
        context['variants'] = variant_dict
        return context

    context_object_name = 'user'
    template_name = "pages/profile.html"


class EditProdileView(UpdateView):
    model = User
    # fields = ["username", "first_name", "last_name", "email", "avatar"]
    form_class = EditProfileForm
    template_name = "pages/edit_profile.html"

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"pk": self.object.pk})


class DeleteProfileView(DeleteView):
    model = User
    template_name = "pages/delete_profile.html"

    def get_success_url(self):
        return reverse_lazy("home")


class VariantCreateView(View):
    def get(self, request):
        context = {
            'variant_form': VariantForm(),
            'formset': ExerciseFormSet(instance=Variant())
        }

        return render(request, 'pages/variant_create.html', context=context)

    def post(self, request):
        variant_form = VariantForm(request.POST)
        formset = ExerciseFormSet(request.POST, instance=Variant())

        if variant_form.is_valid() and formset.is_valid():
            variant = variant_form.save()
            formset.instance = variant
            formset.save()
            return redirect('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_message = "Successfully Changed Your Password"
