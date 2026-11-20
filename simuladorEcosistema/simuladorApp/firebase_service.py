import base64
import json
import os
from functools import lru_cache

from django.conf import settings

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:  # Permite ejecutar tests sin Firebase instalado.
    firebase_admin = None
    credentials = None
    firestore = None


def _service_account():
    if settings.FIREBASE_SERVICE_ACCOUNT_B64:
        raw = base64.b64decode(settings.FIREBASE_SERVICE_ACCOUNT_B64).decode("utf-8")
        return json.loads(raw)

    if settings.FIREBASE_SERVICE_ACCOUNT_JSON:
        value = settings.FIREBASE_SERVICE_ACCOUNT_JSON
        if os.path.exists(value):
            with open(value, "r", encoding="utf-8") as fh:
                return json.load(fh)
        return json.loads(value)

    return None


@lru_cache(maxsize=1)
def firebase_client():
    if not settings.FIREBASE_ENABLED or firebase_admin is None:
        return None

    try:
        if not firebase_admin._apps:
            account = _service_account()
            if account:
                cred = credentials.Certificate(account)
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(
                cred,
                {"projectId": settings.FIREBASE_PROJECT_ID} if settings.FIREBASE_PROJECT_ID else None,
            )
        return firestore.client()
    except Exception:
        # La aplicación puede seguir ejecutándose localmente sin Firebase configurado.
        return None


def firestore_available():
    return firebase_client() is not None


def save_simulation(data):
    db = firebase_client()
    if not db:
        return None
    ref = db.collection("simulaciones").document()
    data = dict(data)
    data["id"] = ref.id
    ref.set(data)
    return ref.id


def list_simulations(uid=None, role="estudiante"):
    db = firebase_client()
    if not db:
        return []

    collection = db.collection("simulaciones")
    if role == "estudiante":
        query = collection.where("usuarioId", "==", uid)
    else:
        query = collection

    docs = query.stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)

    result.sort(key=lambda x: str(x.get("fecha", "")), reverse=True)
    return result


def get_simulation(simulation_id, uid=None, role="estudiante"):
    db = firebase_client()
    if not db:
        return None

    doc = db.collection("simulaciones").document(simulation_id).get()
    if not doc.exists:
        return None

    data = doc.to_dict()
    if role == "estudiante" and data.get("usuarioId") != uid:
        return None

    data["id"] = doc.id
    return data


def save_user_profile(uid, email, nombre, role="estudiante"):
    db = firebase_client()
    if not db:
        return
    db.collection("usuarios").document(uid).set(
        {
            "uid": uid,
            "email": email,
            "nombre": nombre,
            "rol": role,
        },
        merge=True,
    )


def get_user_profile(uid, email=""):
    db = firebase_client()
    if not db:
        return {"uid": uid, "email": email, "nombre": email.split("@")[0], "rol": "estudiante"}

    doc = db.collection("usuarios").document(uid).get()
    if doc.exists:
        return doc.to_dict()

    profile = {"uid": uid, "email": email, "nombre": email.split("@")[0], "rol": "estudiante"}
    db.collection("usuarios").document(uid).set(profile)
    return profile
