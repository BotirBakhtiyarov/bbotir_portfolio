"""
Portfolio views: home, case studies, contact, CV download.
"""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import ContactForm
from .models import CaseStudy


def home(request):
    """Landing page: hero, skills, projects preview, experience, contact."""
    case_studies = CaseStudy.objects.filter(is_published=True)[:6]
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        body = f"From: {name} <{email}>\n\n{message}"
        try:
            send_mail(
                subject=f'[bbotir.xyz] Contact from {name}',
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Message sent. I\'ll get back to you soon.')
            return redirect('portfolio:home')
        except TimeoutError:
            if settings.DEBUG:
                print('Email error: SMTP connection timed out (check network/firewall or use console backend for local dev).')
            messages.error(
                request,
                'The mail server did not respond in time. Please try again later or email directly at hello@bbotir.xyz',
            )
        except OSError as e:
            if settings.DEBUG:
                print(f'Email error: {e}')
            messages.error(
                request,
                'Sorry, the message could not be sent. Please try emailing directly at hello@bbotir.xyz',
            )
        except Exception as e:
            if settings.DEBUG:
                import traceback
                print(f'Email error: {e}')
                traceback.print_exc()
            messages.error(
                request,
                'Sorry, the message could not be sent. Please try emailing directly at hello@bbotir.xyz',
            )
    context = {
        'case_studies': case_studies,
        'contact_form': form,
    }
    return render(request, 'portfolio/home.html', context)


class CaseStudyListView(ListView):
    """List all published case studies."""
    model = CaseStudy
    context_object_name = 'case_studies'
    template_name = 'portfolio/casestudy_list.html'
    queryset = CaseStudy.objects.filter(is_published=True)


class CaseStudyDetailView(DetailView):
    """Single case study detail page."""
    model = CaseStudy
    context_object_name = 'case_study'
    template_name = 'portfolio/casestudy_detail.html'
    slug_url_kwarg = 'slug'
    queryset = CaseStudy.objects.filter(is_published=True)


def cv_download(request):
    """Serve CV PDF for download."""
    from pathlib import Path
    cv_path = Path(settings.BASE_DIR) / 'static' / 'cv' / 'Botir_Bakhtiyarov_CV.pdf'
    if not cv_path.exists():
        raise Http404('CV not found. Add your PDF to static/cv/Botir_Bakhtiyarov_CV.pdf')
    return FileResponse(
        open(cv_path, 'rb'),
        as_attachment=True,
        filename='Botir_Bakhtiyarov_CV.pdf',
        content_type='application/pdf',
    )
