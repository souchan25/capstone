from datetime import datetime

def admin_context(request):
    """
    Context processor to add common variables needed in admin templates
    """
    return {
        'current_date': datetime.now(),
    } 