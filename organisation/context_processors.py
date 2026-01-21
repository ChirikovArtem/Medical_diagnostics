def user_groups(request):
    """Определение пользователей по группам"""
    user = request.user
    if user.is_authenticated:
        return {
            "is_admin": user.groups.filter(name="Администратор").exists(),
            "is_manager": user.groups.filter(name="Менеджер").exists(),
        }
    return {
        "is_admin": False,
        "is_manager": False,
    }
