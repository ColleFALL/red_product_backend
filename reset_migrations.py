import os
import django
import psycopg2
from urllib.parse import urlparse

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'red_product.settings')
django.setup()

from django.conf import settings

# Récupérer l'URL de la base de données
db_url = os.environ.get('DATABASE_URL')

if db_url:
    result = urlparse(db_url)
    connection = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    
    cursor = connection.cursor()
    
    print("🔧 Nettoyage des migrations problématiques...")
    
    try:
        # Supprimer les migrations problématiques de django_migrations
        cursor.execute("""
            DELETE FROM django_migrations 
            WHERE app IN ('token_blacklist', 'admin', 'auth', 'contenttypes', 'sessions', 'accounts');
        """)
        
        # Supprimer les tables problématiques (pas hotels!)
        tables_to_drop = [
            'token_blacklist_outstandingtoken',
            'token_blacklist_blacklistedtoken',
            'django_admin_log',
            'auth_permission',
            'auth_group',
            'auth_group_permissions',
            'django_content_type',
            'django_session'
        ]
        
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                print(f"✅ Table {table} supprimée")
            except Exception as e:
                print(f"⚠️  Erreur sur {table}: {e}")
        
        connection.commit()
        print("✅ Nettoyage terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
else:
    print("❌ DATABASE_URL non trouvée")