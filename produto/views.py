from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View

# Create your views here.

class ListaProdutos(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse("Listar")


class DetalheProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Detalhe")


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("AdicionarCarrinho")


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("RemoverCarrinho")


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Carrinho")


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Finalizar")
