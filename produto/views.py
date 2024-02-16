from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models

from pprint import pprint

# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = "produto/lista.html"
    context_object_name = "produtos"
    paginate_by = 10

class DetalheProdutos(DetailView):
    model = models.Produto
    template_name = "produto/detalhe.html"
    context_object_name = "produto"
    slug_url_kwarg = "slug"


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        # TODO: Remover linhas abaixo
        # if self.request.session.get("carrinho"):
        #     del self.request.session["carrinho"]
        #     self.request.session.save()
        
        http_referer = self.request.META.get(
            "HTTP_REFERER",
            reverse("produto:lista")
            )
        vid = self.request.GET.get("vid")
        
        if not vid:
            messages.error(
                self.request,
                "Produto inexistente!"
            )
            return redirect(http_referer)
        
        variacao = get_object_or_404(models.Variacao, id=vid)
        variacao_estoque = variacao.estoque
        produto = variacao.produto
        
        produto_id = produto.id
        produto_nome = produto.nome 
        variacao_nome = variacao.nome or ""
        variacao_id = variacao.id
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem
        
        if imagem:
            imagem = imagem.name
        else:
            imagem = ""
        
        if variacao.estoque < 1:
            messages.error(
                self.request,
                "Sem produto no estoque!"
            )
            return redirect(http_referer)
        
        if not self.request.session.get("carrinho"):
            self.request.session["carrinho"] = {}
            self.request.session.save()
        
        carrinho = self.request.session["carrinho"]
        
        if vid in carrinho:
            quantidade_carrinho = carrinho[vid]["quantidade"]
            quantidade_carrinho += 1
            
            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f"Estoque insuficiente para {quantidade_carrinho}x no produto {produto.nome}. "
                    f"Adicionamos {variacao_estoque}x no seu carrinho."
                )
                quantidade_carrinho = variacao_estoque
                
            carrinho[vid]["quantidade"] = quantidade_carrinho
            carrinho[vid]["preco_quantitativo"] = preco_unitario * quantidade_carrinho
            carrinho[vid]["preco_quantitativo_promocional"] = preco_unitario_promocional * quantidade_carrinho
        else:
            carrinho[vid] = {
                "produto_id": produto_id,
                "produto_nome": produto_nome,
                "variacao_nome": variacao_nome,
                "preco_unitario": preco_unitario,
                "preco_unitario_promocional": preco_unitario_promocional,
                "preco_quantitativo": preco_unitario,
                "preco_quantitativo_promocional": preco_unitario_promocional,
                "quantidade": 1,
                "slug": slug,
                "imagem": imagem,
            }
        
        self.request.session.save()
        messages.success(
            self.request,
            f"{produto_nome} {variacao_nome} adicionado ao seu "
            f"carrinho {carrinho[vid]['quantidade']}x"
        )
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("RemoverCarrinho")


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Carrinho")


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Finalizar")
