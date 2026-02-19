from hotels.models import Hotel


def build_context():
    hotels = Hotel.objects.all()

    hotels_data = [
        {
            "nom": h.nom,
            "adresse": h.adresse,
            "email": h.email,
            "telephone": h.telephone,
            "prix_par_nuit": str(h.prix_par_nuit),
            "devise": h.devise,
        }
        for h in hotels
    ]

    return {
        "hotelsCount": hotels.count(),
        "hotels": hotels_data
    }