from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Testimonial, ContactMessage
from .forms import TestimonialForm, ContactForm

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def testimonials(request):
    testimonials_list = Testimonial.objects.filter(is_approved=True).select_related('user')
    form = None
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TestimonialForm(request.POST)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.user = request.user
                testimonial.save()
                messages.success(request, 'Merci pour votre témoignage ! Il a été publié avec succès.')
                return redirect('core:testimonials')
        else:
            form = TestimonialForm()
    
    context = {
        'testimonials': testimonials_list,
        'form': form
    }
    return render(request, 'core/testimonials.html', context)

def help_page(request):
    return render(request, 'core/help.html')

