import json
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .firebase_service import firebase_client, get_user_profile, save_user_profile

try:
    from firebase_admin import auth as firebase_auth
except ImportError:
    firebase_auth = None


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("uid"):
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper


def _firebase_web_config():
    return {
        "apiKey": settings.FIREBASE_WEB_API_KEY,
        "authDomain": settings.FIREBASE_WEB_AUTH_DOMAIN,
        "projectId": settings.FIREBASE_WEB_PROJECT_ID,
        "storageBucket": settings.FIREBASE_WEB_STORAGE_BUCKET,
        "messagingSenderId": settings.FIREBASE_WEB_MESSAGING_SENDER_ID,
        "appId": settings.FIREBASE_WEB_APP_ID,
    }


def login_view(request):
    if request.session.get("uid"):
        return redirect("dashboard")

    return render(
        request,
        "simuladorApp/login.html",
        {
            "firebase_config": _firebase_web_config(),
            "firebase_enabled": settings.FIREBASE_ENABLED,
        },
    )


@require_POST
def firebase_login(request):
    if firebase_auth is None or not firebase_client():
        return JsonResponse(
            {"ok": False, "message": "Firebase no está configurado en el servidor."},
            status=503,
        )

    try:
        body = json.loads(request.body.decode("utf-8"))
        id_token = body.get("idToken", "")
        if not id_token:
            return JsonResponse(
                {"ok": False, "message": "Token de acceso no recibido."},
                status=400,
            )

        decoded = firebase_auth.verify_id_token(id_token)
        uid = decoded["uid"]
        email = decoded.get("email", "")
        profile = get_user_profile(uid, email)

        request.session.cycle_key()
        request.session["uid"] = uid
        request.session["email"] = email
        request.session["nombre"] = (
            profile.get("nombre") or decoded.get("name") or email.split("@")[0]
        )
        request.session["rol"] = profile.get("rol", "estudiante")

        return JsonResponse({"ok": True, "redirect": "/dashboard/"})
    except Exception:
        return JsonResponse(
            {"ok": False, "message": "No fue posible validar las credenciales."},
            status=401,
        )


def register_view(request):
    if request.session.get("uid"):
        return redirect("dashboard")

    return render(
        request,
        "simuladorApp/register.html",
        {"firebase_config": _firebase_web_config()},
    )


@require_POST
def firebase_register(request):
    """Registro alternativo desde backend; el frontend usa Firebase Web SDK."""
    if firebase_auth is None or not firebase_client():
        return JsonResponse(
            {"ok": False, "message": "Firebase no está configurado en el servidor."},
            status=503,
        )

    try:
        body = json.loads(request.body.decode("utf-8"))
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        nombre = body.get("nombre", "").strip()

        if len(nombre) < 2 or "@" not in email or len(password) < 6:
            return JsonResponse(
                {"ok": False, "message": "Completa los datos con un formato válido."},
                status=400,
            )

        user = firebase_auth.create_user(
            email=email,
            password=password,
            display_name=nombre,
        )
        save_user_profile(user.uid, email, nombre, "estudiante")

        return JsonResponse(
            {"ok": True, "message": "Cuenta creada correctamente. Ahora inicia sesión."}
        )
    except Exception:
        return JsonResponse(
            {
                "ok": False,
                "message": "No se pudo crear la cuenta. Verifica si el correo ya está registrado.",
            },
            status=400,
        )


@require_POST
def firebase_profile(request):
    """Guarda el perfil creado desde Firebase Authentication."""
    if firebase_auth is None or not firebase_client():
        return JsonResponse(
            {"ok": False, "message": "Firebase no está configurado en el servidor."},
            status=503,
        )

    try:
        body = json.loads(request.body.decode("utf-8"))
        id_token = body.get("idToken", "")
        nombre = body.get("nombre", "").strip()

        if not id_token or len(nombre) < 2:
            return JsonResponse(
                {"ok": False, "message": "Datos de perfil inválidos."},
                status=400,
            )

        decoded = firebase_auth.verify_id_token(id_token)
        uid = decoded["uid"]
        email = decoded.get("email", "")
        save_user_profile(uid, email, nombre, "estudiante")

        return JsonResponse({"ok": True})
    except Exception:
        return JsonResponse(
            {"ok": False, "message": "No fue posible guardar el perfil."},
            status=401,
        )


def logout_view(request):
    request.session.flush()
    return redirect("login")
