
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from courrier.forms_courrier import MissionForm
from courrier.models import Employer, Notification, Mission, Missionnaire


def create_mission(request):
        if request.method == 'POST':
            form = MissionForm(request.POST)
            if form.is_valid():
                mission = form.save(commit=False)
                mission.valide_mission = False  # Par défaut, la mission n'est pas validée

                # Traiter les champs supplémentaires transport, hebergement et repas_fourni
                mission.transport = form.cleaned_data['transport']
                mission.hebergement = form.cleaned_data['hebergement']
                mission.repas_fourni = form.cleaned_data['repas_fourni']

                mission.save()

                # Récupérer les missionnaires sélectionnés dans le formulaire
                missionnaire_ids = request.POST.getlist('missionnaires')

                # Créer des objets Missionnaire pour chaque missionnaire sélectionné
                for missionnaire_id in missionnaire_ids:
                    Missionnaire.objects.create(mission=mission, missionnaire_id=missionnaire_id)
                    Missionnaire.objects.create(
                        mission=mission,
                        missionnaire=missionnaire_ids
                    )

                return redirect('courrier:list_mission')  # Rediriger vers la liste des missions après création
        else:
            form = MissionForm()

        # Récupérer tous les employés, ordonnés par service
        employers = Employer.objects.all().order_by('service__nom_service', 'user__last_name')

        context = {
             'mission_form': form,
                'employers': employers,
        }

        return render(request, 'mission/form_mission.html', {'form': form})



def read_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    return render(request, 'mission/detail_mission.html', {'mission': mission})


def list_mission(request):
    mission_form = MissionForm(request.POST)
    missions = Mission.objects.all()
    return render(request, 'mission/list_mission.html', {'missions': missions, 'mission_form': mission_form})



def update_mission(request, mission_id):
    if request.method == 'POST':
        mission = get_object_or_404(Mission, pk=mission_id)
        # Mettre à jour les champs de la mission
        mission.reference = request.POST.get('reference')
        mission.date_mission = request.POST.get('date_mission')
        mission.date_fin_mission = request.POST.get('date_fin_mission')
        mission.objet_mission = request.POST.get('objet_mission')
        mission.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def delete_mission(request, pk):
    if request.method == 'DELETE':
        mission = get_object_or_404(Mission, pk=pk)
        # Supprimer la mission
        mission.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def detail_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    return render(request, 'mission/detail_mission.html', {'mission': mission})


def print_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="mission_{pk.id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, f'Mission ID: {mission.id}')
    p.drawString(100, 730, f'Ordonnateur ID: {mission.ordonnateur_id}')
    p.drawString(100, 710, f'Reference: {mission.reference}')
    p.drawString(100, 690, f'Date Mission: {mission.date_mission}')
    p.drawString(100, 670, f'Date Fin Mission: {mission.date_fin_mission}')
    p.drawString(100, 650, f'Objet Mission: {mission.objet_mission}')

    p.save()

    return response
