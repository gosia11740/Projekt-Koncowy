"""web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from atlas.views import (
    IndexView,
    HomePage,
    Dashboard,
    ExercisesDetails,
    ExercisesList,
    ExercisesAdd,
    ExercisesModify,
    PlanDetails,
    PlanList,
    PlanAdd,
    PlanModify,
    PlanAddExercises,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view(), name='index'),
    path('', HomePage.as_view(), name='home-page'),
    path('main/', Dashboard.as_view(), name='dashboard'),
    path('exercises/list/', ExercisesList.as_view(), name='exercises-list'),
    path('exercises/add/', ExercisesAdd.as_view(), name='exercise-add'),
    path('exercises/<int:exercises_id>/', ExercisesDetails.as_view(), name='exercises-details'),
    path('exercises/modify/<int:exercises_id>/', ExercisesModify.as_view(), name='exercises-modify'),
    path('plan/details/', PlanDetails.as_view(), name='plan-details'),
    path('plan/list/', PlanList.as_view(), name='plan-list'),
    path('plan/add/', PlanAdd.as_view(), name='plan-add'),
    path('plan/add-exercises/', PlanAddExercises.as_view(), name='plan-add-exercises'),
    path('plan/modify/<int:plan_id>/', PlanModify.as_view(), name='plan-modify'),
    path('plan/<int:plan_id>/', PlanDetails.as_view(), name='plan-details'),

]
