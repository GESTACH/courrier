from django.urls import path

from courrier.views_courrier import courrier_sortant_list, courrier_sortant_create, courrier_sortant_delete, \
    courrier_sortant_detail, courrier_entrant_list, courrier_entrant_detail, courrier_entrant_delete, \
    courrier_special_list, courrier_special_create, courrier_special_delete, courrier_special_detail
from courrier.views_service import (
    direction_list,
    direction_detail,
    direction_create,
    direction_update,
    direction_delete,
    service_list,
    service_detail,
    service_create,
    service_update,
    service_delete,
    fonction_employer_list,
    fonction_employer_create,
    fonction_employer_update,
    fonction_employer_delete,

    affectation_employer
)

app_name = 'service'


urlpatterns = [

    path('direction/list/', direction_list, name='direction_list'),
    path('direction/<int:pk>/', direction_detail, name='direction_detail'),
    path('direction/create/', direction_create, name='direction_create'),
    path('direction/<int:pk>/update/', direction_update, name='direction_update'),
    path('direction/<int:pk>/delete/', direction_delete, name='direction_delete'),

    path('service/list/', service_list, name='service_list'),
    path('service/<int:pk>/', service_detail, name='service_detail'),
    path('service/create/', service_create, name='service_create'),
    path('service/<int:pk>/update/', service_update, name='service_update'),
    path('service/<int:pk>/delete/', service_delete, name='service_delete'),

    path('affectation/.<int:pk>/', affectation_employer, name='affectation_employer'),

    path('fonction_employers/', fonction_employer_list, name='fonction_employer_list'),
    path('fonction_employer/create/<int:pk>/', fonction_employer_create, name='fonction_employer_create'),
    path('fonction_employer/<int:pk>/update/', fonction_employer_update, name='fonction_employer_update'),
    path('fonction_employer/<int:pk>/delete/', fonction_employer_delete, name='fonction_employer_delete'),

    path('courriers-sortants/', courrier_sortant_list, name='courrier_sortant_list'),
    path('courriers-sortants/creer/', courrier_sortant_create, name='courrier_sortant_create'),
    path('courriers-sortants/<int:pk>/supprimer/', courrier_sortant_delete, name='courrier_sortant_delete'),
    path('courriers-sortant/<int:pk>/detail/', courrier_sortant_detail, name='courrier_sortant_detail'),

# Courriers entrants
    path('courriers-entrants/', courrier_entrant_list, name='courrier_entrant_list'),
    path('courriers-entrants/<int:pk>/', courrier_entrant_detail, name='courrier_entrant_detail'),
    path('courriers-entrants/<int:pk>/supprimer/', courrier_entrant_delete, name='courrier_entrant_delete'),
    path('courriers-entrants/<int:pk>/detail/', courrier_entrant_detail, name='courrier_entrant_detail'),

    # Courriers spéciaux
    path('courriers-speciaux/', courrier_special_list, name='courrier_special_list'),
    path('courriers-speciaux/creer/', courrier_special_create, name='courrier_special_create'),
    path('courriers-speciaux/<int:pk>/supprimer/', courrier_special_delete, name='courrier_special_delete'),
    path('courriers-speciaux/<int:pk>/detail/', courrier_special_detail, name='courrier_special_detail'),
]

