from django.urls import path

from courrier.views_courrier import courrier_sortant_list, courrier_sortant_create, courrier_sortant_delete, \
    courrier_entrant_list, courrier_entrant_detail, courrier_entrant_delete, courrier_special_list, \
    courrier_special_create, courrier_special_delete, courrier_sortant_detail, courrier_special_detail

app_name = 'courriers'

urlpatterns = [
    # Courriers sortants
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