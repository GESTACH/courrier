from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from courrier.models import Direction, Service, FonctionEmployer
from courrier.forms_service import DirectionForm, ServiceForm, FonctionEmployerForm, \
    AffectationEmployerForm


def direction_list(request):
    search_query = request.GET.get('search', '')
    directions = Direction.objects.all()

    if search_query:
        directions = directions.filter(
            Q(direction__icontains=search_query) |
            Q(sigle__icontains=search_query)
        )

    directions = directions.order_by('-direction')  # Trier la liste par ordre alphabétique

    # Pagination
    paginator = Paginator(directions, 15)  # 15 éléments par page
    page = request.GET.get('page')
    try:
        directions = paginator.page(page)
    except PageNotAnInteger:
        directions = paginator.page(1)
    except EmptyPage:
        directions = paginator.page(paginator.num_pages)

    context = {
        'directions': directions,
        'search_query': search_query,
    }
    return render(request, 'service/direction_list.html', context)


def direction_detail(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    return render(request, 'service/direction_detail.html', {'direction': direction})


def direction_create(request):
    if request.method == 'POST':
        form = DirectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Direction créé avec succès.")
            return redirect('service:direction_list')
    else:
        form = DirectionForm()
    return render(request, 'service/direction_form.html', {'form': form})


def direction_update(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        form = DirectionForm(request.POST, instance=direction)
        if form.is_valid():
            form.save()
            messages.success(request, "Modification effectuée avec succès.")
            return redirect('service:direction_list')
    else:
        form = DirectionForm(instance=direction)
    return render(request, 'service/direction_form.html', {'form': form})


def direction_delete(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        direction.delete()
        messages.success(request, "Direction supprimé créé avec succès.")
        return redirect('service:direction_list')
    return render(request, 'service/direction_list.html', {'direction': direction})


def service_list(request):
    search_query = request.GET.get('search', '')
    services = Service.objects.all()

    if search_query:
        services = services.filter(
            Q(nom_service__icontains=search_query) |
            Q(sigle__icontains=search_query)
        )

    services = services.order_by('-nom_service')  # Trier la liste par ordre alphabétique

    # Pagination
    paginator = Paginator(services, 15)  # 15 éléments par page
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)

    context = {
        'services': services,
        'search_query': search_query,
    }
    return render(request, 'service/service_list.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service/service_detail.html', {'service': service})


def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service créé avec succès.")
            return redirect('service:service_list')
    else:
        form = ServiceForm()
    return render(request, 'service/service_form.html', {'form': form})



def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Modification effectuée avec succès.")
            return redirect('service:service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service/service_form.html', {'form': form})


def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service supprimé créé avec succès.")
        return redirect('service:service_list')
    return render(request, 'service/service_list.html', {'service': service})



def fonction_employer_list(request):
    fonctions = FonctionEmployer.objects.all()
    return render(request, 'service/fonction_employer_list.html', {'fonctions': fonctions})


def fonction_employer_create(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        form = FonctionEmployerForm(request.POST)
        if form.is_valid():
            fonction_employer = form.save(commit=False)
            fonction_employer.service = service
            fonction_employer.save()
            messages.success(request, "Fonction d'employé créée avec succès.")
            return redirect('service:affectation_employer', pk=service.pk)
    else:
        form = FonctionEmployerForm()

    return render(request, 'service/fonction_employer_form.html', {'form': form, 'service': service})


def fonction_employer_update(request, pk):
    fonction = get_object_or_404(FonctionEmployer, pk=pk)
    if request.method == 'POST':
        form = FonctionEmployerForm(request.POST, instance=fonction)
        if form.is_valid():
            form.save()

            return redirect('fonction_employer_list')
    else:
        form = FonctionEmployerForm(instance=fonction)
    return render(request, 'service/fonction_employer_form.html', {'form': form})


def fonction_employer_delete(request, pk):
    fonction = get_object_or_404(FonctionEmployer, pk=pk)
    if request.method == 'POST':
        fonction.delete()
        return redirect('fonction_employer_list')
    return render(request, 'service/fonction_employer_list.html', {'fonction': fonction})


def affectation_employer(request, pk):
    # Récupérer le service correspondant au pk fourni
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        # Si le formulaire est soumis, le traiter
        form= AffectationEmployerForm(request.POST)
        if form.is_valid():
            # Créer une instance Employer avec les données du formulaire
            employer_instance = form.save(commit=False)
            employer_instance.service = service
            employer_instance.save()
            messages.success(request, "Employé affecté avec succès.")
            return redirect('service:service_list')  # Rediriger vers la page de confirmation
    else:
        # Si la méthode est GET, afficher le formulaire vide
        form = AffectationEmployerForm()

    return render(request, 'service/affectation_employer.html', {'form': form, 'service': service})

