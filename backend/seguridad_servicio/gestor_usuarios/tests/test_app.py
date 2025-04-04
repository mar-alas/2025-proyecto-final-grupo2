from gestor_usuarios.app import app

def test_app_routes_registradas():
    rutas = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/api/v1/seguridad/gestor_usuarios/ping' in rutas
    assert '/api/v1/seguridad/gestor_usuarios/w/signup' in rutas
    assert '/api/v1/seguridad/gestor_usuarios/r/auth/login' in rutas
    assert '/' in rutas
