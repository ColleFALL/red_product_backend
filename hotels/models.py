from django.db import models

class Hotel(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=30)
    prix_par_nuit = models.DecimalField(max_digits=12, decimal_places=2)
    devise = models.CharField(max_length=10)
    
    # Stockage local du fichier
    photo = models.ImageField(upload_to='hotels/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
