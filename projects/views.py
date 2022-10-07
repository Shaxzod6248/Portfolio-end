from django.shortcuts import redirect, render
from .models import *
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.contrib import messages
from .forms import *
from .utils import *


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    for project in projects:
        print("project.user", project.user, project.title)
    context = {'projects': projects,'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, id):
    project = Project.objects.get(id=id)
    tags = project.tag.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.user = request.user.profil
        review.save()
        project.getVoteCount

        messages.success(request, 'Review successfull!')
        return redirect('project', id=project.id)
    context = {
        "project": project,
        "tags": tags,
        "form": form,
    }

    return render(request, "projects/project.html", context)


@login_required(login_url='login')
def project_add(request):
    profile =request.user.profil
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = profile
            project.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, "projects/project_add.html", context)


@login_required(login_url='login')
def project_edit(request, id):
    profile = request.user.profil
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')    
    
    context = {
        "form": form
    }
    return render(request, "projects/project_add.html", context)


@login_required(login_url='login')
def project_delete(request, id):
    profile = request.user.profil
    project = profile.project_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
