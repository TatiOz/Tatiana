
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import About, Skill, Project, Contact, SocialLink
from .forms import ContactForm

def home(request):
    """Home page view"""
    try:
        about = About.objects.first()
        featured_projects = Project.objects.filter(featured=True)[:3]
        skills = Skill.objects.all()[:6]
        social_links = SocialLink.objects.filter(active=True)
    except:
        about = None
        featured_projects = []
        skills = []
        social_links = []
    
    # Default data for Tatiana if no database content
    if not about:
        about = type('About', (), {
            'name': 'Tatiana Ozhgibesova',
            'title': 'Neurologist & Neuroscience Researcher',
            'bio': 'I am a medical doctor specializing in neurology with expertise in clinical EEG and computational neuroscience. I integrate neuroscience insights with data science techniques to solve real-world problems, focusing on brain-computer interfaces, cognitive technologies, and industry applications of neuroscience.',
            'email': 'tatiana.ozhgibesova@email.com',
            'location': 'Medical Research & Technology'
        })()
    
    # Default skills if none in database
    if not skills:
        skills = [
            type('Skill', (), {
                'name': 'Clinical Neurology',
                'category': 'medical',
                'icon': 'fas fa-brain'
            })(),
            type('Skill', (), {
                'name': 'Neuroscience Research',
                'category': 'research',
                'icon': 'fas fa-microscope'
            })(),
            type('Skill', (), {
                'name': 'Python (NumPy, Pandas, Matplotlib)',
                'category': 'programming',
                'icon': 'fab fa-python'
            })(),
            type('Skill', (), {
                'name': 'Data Analysis & Visualization',
                'category': 'tool',
                'icon': 'fas fa-chart-line'
            })(),
            type('Skill', (), {
                'name': 'EEG Interpretation',
                'category': 'medical',
                'icon': 'fas fa-wave-square'
            })(),
            type('Skill', (), {
                'name': 'Computational Modeling',
                'category': 'research',
                'icon': 'fas fa-cogs'
            })()
        ]
    
    # Default social links if none in database
    if not social_links:
        social_links = [
            type('SocialLink', (), {
                'name': 'Email',
                'url': 'mailto:tatiana.ozhgibesova@email.com',
                'icon': 'fas fa-envelope',
                'active': True
            })(),
            type('SocialLink', (), {
                'name': 'LinkedIn',
                'url': 'https://www.linkedin.com/in/tatiana-ozhgibesova',
                'icon': 'fab fa-linkedin',
                'active': True
            })()
        ]
    
    context = {
        'about': about,
        'featured_projects': featured_projects,
        'social_links': social_links,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """About page view"""
    try:
        about = About.objects.first()
        skills = Skill.objects.all()
        social_links = SocialLink.objects.filter(active=True)
    except:
        about = None
        skills = []
        social_links = []
    
    # Default data for Tatiana if no database content
    if not about:
        about = type('About', (), {
            'name': 'Tatiana Ozhgibesova',
            'title': 'Neurologist & Neuroscience Researcher',
            'bio': 'I am a medical doctor specializing in neurology with expertise in clinical EEG and computational neuroscience. I integrate neuroscience insights with data science techniques to solve real-world problems, focusing on brain-computer interfaces, cognitive technologies, and industry applications of neuroscience.',
            'email': 'tatiana.ozhgibesova@email.com',
            'location': 'Medical Research & Technology'
        })()
    
    if not skills:
        skills = [
            type('Skill', (), {
                'name': 'Clinical Neurology',
                'category': 'medical',
                'icon': 'fas fa-brain'
            })(),
            type('Skill', (), {
                'name': 'Neuroscience Research',
                'category': 'research',
                'icon': 'fas fa-microscope'
            })(),
            type('Skill', (), {
                'name': 'Python (NumPy, Pandas, Matplotlib)',
                'category': 'programming',
                'icon': 'fab fa-python'
            })(),
            type('Skill', (), {
                'name': 'Data Analysis & Visualization',
                'category': 'tool',
                'icon': 'fas fa-chart-line'
            })(),
            type('Skill', (), {
                'name': 'EEG Interpretation',
                'category': 'medical',
                'icon': 'fas fa-wave-square'
            })(),
            type('Skill', (), {
                'name': 'Computational Modeling',
                'category': 'research',
                'icon': 'fas fa-cogs'
            })()
        ]
    
    # Default social links if none in database
    if not social_links:
        social_links = [
            type('SocialLink', (), {
                'name': 'Email',
                'url': 'mailto:tatiana.ozhgibesova@email.com',
                'icon': 'fas fa-envelope',
                'active': True
            })(),
            type('SocialLink', (), {
                'name': 'LinkedIn',
                'url': 'https://www.linkedin.com/in/tatiana-ozhgibesova',
                'icon': 'fab fa-linkedin',
                'active': True
            })()
        ]
    
    # Add interests
    interests = [
        "Visual Neuroscience",
        "Brain-Computer Interfaces", 
        "Cognitive Technology",
        "German Language Learning"
    ]
    
    context = {
        'about': about,
        'social_links': social_links,
        'interests': interests,
    }
    return render(request, 'main/about.html', context)

def projects(request):
    """Projects page view"""
    try:
        projects = Project.objects.all()
        skills = Skill.objects.all()
        social_links = SocialLink.objects.filter(active=True)
    except:
        projects = []
        skills = []
        social_links = []
    
    # Default social links if none in database
    if not social_links:
        social_links = [
            type('SocialLink', (), {
                'name': 'Email',
                'url': 'mailto:tatiana.ozhgibesova@email.com',
                'icon': 'fas fa-envelope',
                'active': True
            })(),
            type('SocialLink', (), {
                'name': 'LinkedIn',
                'url': 'https://www.linkedin.com/in/tatiana-ozhgibesova',
                'icon': 'fab fa-linkedin',
                'active': True
            })()
        ]
    
    context = {
        'projects': projects,
        'social_links': social_links,
    }
    return render(request, 'main/projects.html', context)

def project_detail(request, pk):
    """Individual project detail view"""
    try:
        project = Project.objects.get(pk=pk)
        social_links = SocialLink.objects.filter(active=True)
    except Project.DoesNotExist:
        project = None
        social_links = []
    
    context = {
        'project': project,
        'social_links': social_links,
    }
    return render(request, 'main/project_detail.html', context)

def skills(request):
    """Skills page view"""
    try:
        skills = Skill.objects.all()
        social_links = SocialLink.objects.filter(active=True)
    except:
        skills = []
        social_links = []
    
    # Default skills for Tatiana if none in database
    if not skills:
        skills = [
            type('Skill', (), {
                'name': 'Clinical Neurology',
                'category': 'medical',
                'icon': 'fas fa-brain'
            })(),
            type('Skill', (), {
                'name': 'Neuroscience Research',
                'category': 'research',
                'icon': 'fas fa-microscope'
            })(),
            type('Skill', (), {
                'name': 'Python (NumPy, Pandas, Matplotlib)',
                'category': 'programming',
                'icon': 'fab fa-python'
            })(),
            type('Skill', (), {
                'name': 'Data Analysis & Visualization',
                'category': 'tool',
                'icon': 'fas fa-chart-line'
            })(),
            type('Skill', (), {
                'name': 'EEG Interpretation',
                'category': 'medical',
                'icon': 'fas fa-wave-square'
            })(),
            type('Skill', (), {
                'name': 'Computational Modeling',
                'category': 'research',
                'icon': 'fas fa-cogs'
            })()
        ]
    
    # Default social links if none in database
    if not social_links:
        social_links = [
            type('SocialLink', (), {
                'name': 'Email',
                'url': 'mailto:tatiana.ozhgibesova@email.com',
                'icon': 'fas fa-envelope',
                'active': True
            })(),
            type('SocialLink', (), {
                'name': 'LinkedIn',
                'url': 'https://www.linkedin.com/in/tatiana-ozhgibesova',
                'icon': 'fab fa-linkedin',
                'active': True
            })()
        ]
    
    context = {
        'skills': skills,
        'social_links': social_links,
    }
    return render(request, 'main/skills.html', context)

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification (optional)
            if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                try:
                    send_mail(
                        f'New Contact Form: {contact.subject}',
                        f'From: {contact.name} ({contact.email})\n\nMessage:\n{contact.message}',
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],
                        fail_silently=True,
                    )
                except:
                    pass
            
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    try:
        about = About.objects.first()
        social_links = SocialLink.objects.filter(active=True)
    except:
        about = None
        social_links = []
    
    # Default data for Tatiana if no database content
    if not about:
        about = type('About', (), {
            'name': 'Tatiana Ozhgibesova',
            'title': 'Neurologist & Neuroscience Researcher',
            'bio': 'I am a medical doctor specializing in neurology with expertise in clinical EEG and computational neuroscience.',
            'email': 'tatiana.ozhgibesova@email.com',
            'location': 'Medical Research & Technology'
        })()
    
    # Default social links if none in database
    if not social_links:
        social_links = [
            type('SocialLink', (), {
                'name': 'Email',
                'url': 'mailto:tatiana.ozhgibesova@email.com',
                'icon': 'fas fa-envelope',
                'active': True
            })(),
            type('SocialLink', (), {
                'name': 'LinkedIn',
                'url': 'https://www.linkedin.com/in/tatiana-ozhgibesova',
                'icon': 'fab fa-linkedin',
                'active': True
            })()
        ]
    
    context = {
        'form': form,
        'about': about,
        'social_links': social_links,
    }
    return render(request, 'main/contact.html', context)
