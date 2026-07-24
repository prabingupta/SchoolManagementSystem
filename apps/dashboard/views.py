from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_home(request):
    """
    Placeholder for a future custom-branded staff dashboard.

    Today, all real content management happens through Django Admin
    (fully functional — see core, home, about, admissions, services,
    gallery, blog, contact, testimonials apps). This view exists so
    the URL/app structure is ready for a future dashboard UI once
    there's an actual reason to build one — e.g. when the Student/
    Teacher/Parent Portal exists and staff need a role-specific view
    that Django Admin doesn't provide (attendance entry, grade entry,
    etc.). Building that UI now, with no portal data to display,
    would be premature — this route just reserves the architecture.
    """
    return render(request, 'dashboard/home.html', {
        'user': request.user,
        'role': request.user.profile.get_role_display(),
    })
