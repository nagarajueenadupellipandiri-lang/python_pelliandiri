from django.http import JsonResponse
from django.shortcuts import render, redirect

def home(request):
    return redirect("http://localhost:5173/")

