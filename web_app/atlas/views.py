from datetime import datetime
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views import View
import random

from atlas.models import Exercises, ExercisesPlan, DayName, Plan, Page

class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class HomePage(View):

    def get(self,request):
        exercises_all = Exercises.objects.all()

        exercises = list(exercises_all)
        random.shuffle(exercises)

        if len(exercises) == 0:
            exercises = "Nie ma zaplanowanego treningu"
        else:
            random.shuffle(exercises)

        return render(request, "index.html", context = {"exercises": exercises})

class Dashboard(View):

    def get(self, request):
        exercises_count = Exercises.objects.count()
        plan_count = Plan.objects.count()
        recent_plan = Plan.objects.order_by('-created').first()
        plan_dict = {}
        for day in ExercisesPlan.objects.filter(plan__name=recent_plan.name):
            if day.day_name.name not in plan_dict.keys():
                plan_dict[day.day_name.name] = []
            plan_dict[day.day_name.name].append((day.exercises.name, day.exercises_id))

        context = {
            'exercises_count': exercises_count,
            'plan_count': plan_count,
            'recent_plan': recent_plan,
            'exercises_plan': plan_dict,
        }
        return render(request, "dashboard.html", context)


class ExercisesDetails(View):
    def get(self, request, exercises_id):
        exercises = Exercises.object.get(id=exercises_id)


        context = {
            "exercises": exercises,
        }
        return render(request, 'app-exercises-details.html')

    def post(self, request, exercises_id):
        exercises = Exercises.objects.get(id=exercises_id)
        sel_button = request.POST.get('button')
        if sel_button == 'button1':
            exercises.votes += 1
            exercises.save()
        elif sel_button == 'button2':
            exercises.votes -+1
            exercises.save()
        return redirect(f'/exercises/{exercises_id}/')


class ExercisesList(View):

    def get(self, request):
        exercises_list = Exercises.objects.all()
        paginator = Paginator(exercises_list, 25)
        page = request.GET.get('page')

        try:
            exercises = paginator.page(page)
        except PageNotAnInteger:
            exercises = paginator.page(1)
        except EmptyPage:
            exercises = paginator.page(paginator.num_pages)

        return render (request, "app-exercises.html", context={'page':page, 'exercises': exercises})


class ExercisesAdd(View):
    def get(self, request):
        return render(request, 'app-add-exercises.html')

    def post(self, request):
        name = request.POST.get('name-exercises')
        description = request.POST.get('description')
        exercises_time = request.POST.get('exercises_time')
        detalis = request.POST.get('detalis')
        if all([name,description]):
            Exercises.objects.create(name=name, description=description, exercises_time=exercises_time, detalis=detalis)

            context = { 
                "message": "dodano ćwiczenie"
            }
            return render(request, "app-add-exercises.html", context)
        else:
            context = {
                'error': ' Nie uzupełniłeś wszyskich danych '
            }
            return render(request, "app-add-exercises.html", context)


class ExercisesModify(View):

    def get(self, request, exercises_id):

        try:
            recent_exercises = Exercises.objects.get(id=exercises_id)
        except Exercises.DoesNotExist:
            raise Http404('<h1>Page not found</h1>')
        return render(request, 'app-edit-exercises.html', context={'recent_exercises': recent_exercises})

    def post(self, request, recipe_id):
        name = request.POST.get('name-exercises')
        description = request.POST.get('description')
        exercises_time = request.POST.get('exercises_time')
        detalis = request.POST.get('detalis')

        Exercises.objects.create(name=name, description=description,
            exercises_time=exercises_time, detalis=detalis)

        return redirect('/exercises/list/')


class PlanDetails(View):
    def get(self, request, plan_id):

        recent_plan = Plan.objects.get(id=plan_id)

        plan_dict = {}

        for day in Plan.objects.filter(plan__name=recent_plan.name):
            plan_dict[day.day_name.name] = []
            plan_dict[day.day_name.name].append([day.plan_name, day.exercises.name, day.exercises_id])

        context = {
            'recent_plan': recent_plan,
            'exercises_plan': plan_dict,
        }
        return render(request, "app-details-schedules.html", context)

class PlanList(View):
    
    def get(self, request):
        plan_list = Plan.objects.all()
        paginator = Paginator(plan_list, 2)
        page = request.GET.get('page')

        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)

        context = {
            'page': page,
            'plans': plans,
        }

        return render(request, 'app-schedules.html', context)

        

class PlanAdd(View):    
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        new_plan_name = request.POST.get('planName', 'nie ma')
        new_plan_description = request.POST.get('planDescription')

        if all([new_plan_name, new_plan_description]):
            new_plan = Plan()
            new_plan.name = new_plan_name
            new_plan.description = new_plan_description
            new_plan.save()

        return render(request, 'app-add-schedules.html')


class PlanModify(View):
    def get(self, request, plan_id):
        return HttpResponse('')


class PlanAddExercises(View):
    def get(self, request):
        plans = Plan.objects.all()
        exercises = Exercises.objects.all()
        days = DayName.objects.all()

        context = {
            'plans': plans,
            'exercises': exercises,
            'days': days,
        }
        return render(request, 'app-schedules-exercise.html', context)