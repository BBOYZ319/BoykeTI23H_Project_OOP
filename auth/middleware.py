def auth_required(func):
    def wrapper(user, *args, **kwargs):
        if not user:
            print("[SERVER] AKSES DITOLAK: User belum login.")
            return
        return func(user, *args, **kwargs)
    return wrapper
