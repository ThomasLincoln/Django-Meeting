# accounts/views.py
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Compromisso
from django.db.models import Q
from django.contrib.auth.decorators import login_required


from .forms import CompromissoForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def dashboard(request):
    user = request.user
    compromissos = Compromisso.objects.filter(
        (Q(estado='Agendado') | Q(estado='Concluído')) & Q(participantes=user)
    )

    # Obtém a data escolhida pelo usuário da solicitação GET
    data_escolhida = request.GET.get('data_escolhida')

    # Se a data_escolhida foi fornecida, filtre os compromissos com base nela
    if data_escolhida:
        compromissos = compromissos.filter(data=data_escolhida)

    return render(request, 'home.html', {
        'compromissos': compromissos,
    })

@login_required
def compromisso_detail(request, pk):
    compromisso = get_object_or_404(Compromisso, pk=pk)
    return render(request, 'compromisso/compromisso.html', {'compromisso': compromisso})


@login_required
def new(request):
    if request.method == 'POST':
        form = CompromissoForm(request.POST)
        if form.is_valid():
            compromisso = form.save(commit=False)
            compromisso.criador = request.user 

            compromisso.save()
            data = form.cleaned_data['data']

            participants = [participant.id for participant in form.cleaned_data['participantes']]

            for participant_id in participants:
                participant = User.objects.get(id=participant_id)
                if Compromisso.objects.filter(data=data, participantes=participant).exclude(pk=compromisso.pk).exists():
                    print(f"{participant.username} já está em outro compromisso no mesmo dia.") 

            compromisso.participantes.set(participants)

            return redirect('home')

    else:
        form = CompromissoForm()

    return render(request, 'compromisso/form.html', {'form': form})

@login_required
def cancelar(request, pk):
    compromisso = get_object_or_404(Compromisso, pk=pk)
    if compromisso.criador == request.user:
        compromisso.estado = 'Cancelado'
        compromisso.save()
    return redirect('home')

@login_required
def editar(request, pk):
    compromisso = get_object_or_404(Compromisso, pk=pk)

    # Verifique se o usuário logado é o criador do compromisso
    if compromisso.criador != request.user:
        # Adicione uma lógica para lidar com permissões, como redirecionar para uma página de erro
        pass

    if request.method == 'POST':
        form = CompromissoForm(request.POST, instance=compromisso)
        if form.is_valid():
            form.save()
            # Redirecione para a página de detalhes do compromisso ou para onde você desejar
            return redirect(reverse('compromisso:detail', args=(compromisso.id,)))
    else:
        form = CompromissoForm(instance=compromisso)

    return render(request, 'compromisso/edit.html', {'form': form})
