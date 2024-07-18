from django.contrib.auth.models import User
from django.db import models



# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Direction(models.Model):
    direction = models.CharField(max_length=255)
    sigle = models.CharField(max_length=10, blank=True)
    logo_dir = models.ImageField(upload_to='logo/', null=True, blank=True)
    bp_dir = models.CharField(max_length=255)
    adresse_dir = models.CharField(max_length=255)

    def __str__(self):
        return self.direction


class Service(models.Model):
    direction_service = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='services')
    nom_service = models.CharField(max_length=255)
    tutelle_service = models.ForeignKey('self', related_name='services_tutelle', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.nom_service


class FonctionEmployer(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='employers')
    fonction_employer = models.CharField(max_length=255)

    def __str__(self):
        return self.fonction_employer


class Permission(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom



class EmployerGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('Employer', related_name='employer_groups')

    def __str__(self):
        return self.name


class EmployerPermission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class GroupPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'permission')

    def __str__(self):
        return f"{self.group.name} - {self.permission.name}"


class EmployerGroupPermission(models.Model):
    employer_group = models.ForeignKey(EmployerGroup, on_delete=models.CASCADE, related_name='group_permissions')
    permission = models.ForeignKey(EmployerPermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employer_group', 'permission')

    def __str__(self):
        return f"{self.employer_group.name} - {self.permission.name}"


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='employers_services')
    fonction_employer = models.ForeignKey(FonctionEmployer, related_name='fonctions_employer', on_delete=models.CASCADE)
    photo_utilisateur = models.ImageField(upload_to='utilisateurs/', null=True, blank=True)
    sexe = models.CharField(max_length=2, choices=(('M', 'M'), ('F', 'F')), default='M.')
    contact = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, null=True)
    residence = models.CharField(max_length=50, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255)
    Nom_pere = models.CharField(max_length=255)
    nom_mere = models.CharField(max_length=255)
    matricule = models.CharField(max_length=20, null=True)
    num_cni = models.CharField(max_length=15)
    date_cni = models.DateField(null=True, blank=True)
    hors_service = models.BooleanField(default=False)
    vehicule = models.BooleanField(default=False)
    vehicule_immatriculation = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='employer_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='employer_set')
    employer_permissions = models.ManyToManyField(EmployerPermission, blank=True, related_name='employers')

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name



class Notification(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='notifications')
    type = models.TextField(max_length=50)
    objet_id = models.PositiveIntegerField()
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    lue = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.type} - {self.contenu[:20]}..."


class DestinataireNotification(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='destinataires_notification')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='destinataires')
    destinataire = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='notifications')

    class Meta:
        verbose_name = "Destinataire de Notification"
        verbose_name_plural = "Destinataires de Notifications"

    def __str__(self):
        return f"{self.notification.type} - {self.destinataire.user.username}"



class CourrierSortant(models.Model):
    expediteur = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='expediteurs')
    destinataire = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='destinataires')
    sujet = models.CharField(max_length=100)
    contenu = models.TextField()
    joint = models.FileField(upload_to='Courrier/')
    date_envoi = models.DateTimeField(auto_now_add=True)
    valide_courrier = models.BooleanField(default=False)
    observations_courrier = models.TextField(blank=True)
    superieur_validation = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='courriers_validation')



class CourrierEntrant(models.Model):
    expediteur = models.ForeignKey(Employer, on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='courriers_entrants')
    sujet = models.CharField(max_length=100)
    contenu = models.TextField()
    joint = models.FileField(upload_to='Courrier/')
    date_reception = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)


class Instruction(models.Model):
    nom_instruction = models.TextField(max_length=100)


class CourrierSpecial(models.Model):
    expediteur = models.CharField(max_length=100)
    destinataire = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='destinataires')
    date_reception = models.DateTimeField()
    date_envoie = models.DateTimeField(auto_now_add=True)
    num_origine = models.CharField(max_length=10)
    objet = models.TextField()
    joint = models.FileField(upload_to='Courrier/')
    note_1 = models.TextField()
    note_2 = models.TextField()
    lu = models.BooleanField(default=False)


class CourrierSpecialInstruction(models.Model):
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, related_name='instructions')
    courrier_specifique = models.ForeignKey(CourrierSpecial, on_delete=models.CASCADE,
                                            related_name='courriers_speciaux')
    directions_concernees = models.ManyToManyField(Direction, related_name='instructions_concernees')


class CourrierSpecialCopie(models.Model):
    courrier_special = models.ForeignKey(CourrierSpecialInstruction, on_delete=models.CASCADE, related_name='courriers_speciaux_copie')
    direction_concerne = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='direction_concernes')



class Mission(models.Model):
    ordonnateur = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="ordonateurs")
    reference = models.TextField(blank=True)
    date_mission = models.DateField()
    date_fin_mission = models.DateField()
    objet_mission = models.TextField()
    valide_mission = models.BooleanField(default=False)


class Missionnaire(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='missions')
    missionnaire = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='missionnaires')
    transport = models.TextField(blank=True)
    hebergement = models.BooleanField(default=False)
    repas_fourni = models.BooleanField(default=False)





