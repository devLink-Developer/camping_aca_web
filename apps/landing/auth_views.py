from __future__ import annotations

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods


def _safe_redirect(request: HttpRequest, url: str | None, fallback: str) -> HttpResponse:
    if url and url_has_allowed_host_and_scheme(url=url, allowed_hosts={request.get_host()}):
        return redirect(url)
    return redirect(fallback)


@require_http_methods(["GET", "POST"])
def acceso(request: HttpRequest) -> HttpResponse:
    """Pantalla de inicio de sesión (Acceso)."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("dashboard:statistics")
        return redirect("landing:home")

    form = AuthenticationForm(request, data=request.POST or None)

    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Al loguear, por defecto el admin entra en modo admin.
            request.session["client_mode"] = False

            if getattr(user, "is_staff", False):
                return redirect("dashboard:statistics")

            fallback = "dashboard:statistics" if getattr(user, "is_staff", False) else "landing:home"
            return _safe_redirect(request, next_url, fallback)
        messages.error(request, "Usuario o contraseña incorrectos")

        # Si el login fue disparado desde un modal (en una página pública),
        # volvemos a la pantalla anterior y pedimos abrir el modal.
        if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
            separator = "&" if "?" in next_url else "?"
            return redirect(f"{next_url}{separator}login=1")

    return render(
        request,
        "auth/acceso.html",
        {
            "form": form,
            "next": next_url or "",
        },
    )


@require_http_methods(["POST", "GET"])
def salir(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


@require_http_methods(["GET"])
def toggle_client_mode(request: HttpRequest) -> HttpResponse:
    """Activa/desactiva el modo cliente para usuarios admin (staff).

    Se guarda en sesión como `client_mode` para que el navbar y los botones
    flotantes se rendericen como cliente.
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("landing:home")

    next_url = request.GET.get("next")

    current = bool(request.session.get("client_mode", False))
    request.session["client_mode"] = not current

    if request.session["client_mode"]:
        # Guardar la última pantalla admin para poder volver luego.
        if next_url and (next_url.startswith("/dashboard") or next_url.startswith("/vouchers") or next_url.startswith("/admin")):
            request.session["last_admin_path"] = next_url
            next_url = None
        return _safe_redirect(request, next_url, "landing:home")

    # Al volver a admin, intentamos volver a la última pantalla admin usada.
    if not next_url or not (next_url.startswith("/dashboard") or next_url.startswith("/vouchers") or next_url.startswith("/admin")):
        next_url = request.session.get("last_admin_path")

    return _safe_redirect(request, next_url, "dashboard:settings")
