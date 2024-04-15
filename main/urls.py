from django.urls import path
from .views import getUsers, getUser, addUser, updateUser, deleteUser, getAdmin, getTrainer, getClient, login
from .views import getTrainerNames, addSchedule, getClientsInfo, getScheduleTrainer, getScheduleClient, getAllSchedules
urlpatterns = [
    path('', getUsers),
    path('<int:pk>/', getUser),
    path('register', addUser),
    path('update/<int:pk>', updateUser),
    path('delete/<int:pk>', deleteUser),
    path('admin', getAdmin),
    path('trainer', getTrainer),
    path('client', getClient),
    path('login', login),
    path('getTrainerInfo', getTrainerNames),
    path('getClientsInfo', getClientsInfo),
    path('getScheduleTrainer/<int:pk>', getScheduleTrainer),
    path('getAllSchedules', getAllSchedules),
    path('getScheduleClient/<int:pk>', getScheduleClient),
    path('addSchedule', addSchedule)
]