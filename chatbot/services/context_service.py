from hotels.models import Hotel


def build_context():
    hotels_count = Hotel.objects.count()

    hotels = Hotel.objects.all()[:5]  # limiter

    hotels_data = [
        {
            "nom": h.nom,
            "prix": h.prix_par_nuit,
            "devise": h.devise
        }
        for h in hotels
    ]

    return {
        "hotelsCount": hotels_count,
        "hotelsPreview": hotels_data
    }
