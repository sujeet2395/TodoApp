from django.shortcuts import HttpResponseRedirect, redirect, render, reverse
from .models import Task, TasksList
from account.models import User
from sharedtodos.models import SharedTasksList
from datetime import datetime
# Create your views here.
def home(request):
    if 'sessionuser_id' not in request.session:
        return redirect('account:login')
    sessionuser = User.objects.get(pk=int(request.session['sessionuser_id']))
    taskslists=list()
    for taskslist in TasksList.objects.filter(user=User.objects.get(pk=sessionuser.id)):
        tasksandtaskslist=list()
        tasks=list()
        for task in Task.objects.filter(taskslist=taskslist):
            tasks.append(task)
        tasksandtaskslist.append(taskslist)
        tasksandtaskslist.append(tasks)
        taskslists.append(tasksandtaskslist)

    sharedtaskslists=list()
    #print('Shared')
    for sharedtaskslist in SharedTasksList.objects.filter(withuser=User.objects.get(pk=sessionuser.id)):
        #print(sharedtaskslist.id,'s')
        for taskslist_ref in TasksList.objects.filter(id=sharedtaskslist.sharedtaskslist.id):
            sharedtasksandtaskslist=list()
            sharedtasks=list()
            #print(taskslist_ref,'sp')
            for task in Task.objects.filter(taskslist=taskslist_ref):
                sharedtasks.append(task)
            sharedtasksandtaskslist.append(taskslist_ref)
            sharedtasksandtaskslist.append(sharedtasks)
            sharedtaskslists.append(sharedtasksandtaskslist)
            #print(sharedtaskslists,'sq')
    #print('end')
    context=dict()
    if taskslists:
        context['taskslists']=taskslists
    else:
        context['taskslists']=[]
    
    '''
    if tasks:
        context['tasks']=tasks
    else:
        context['sharedtaskslists':'No tasks']
    '''
    if sharedtaskslists:
        context['sharedtaskslists']=sharedtaskslists
    else:
        context['sharedtaskslists']=[]
    '''
    if sharedtasks:
        context['sharedtasks']=sharedtasks
    else:
        context['sharedtasks':'No sharedtasks']
    '''
    return render(request, 'todos.html',context)

def addtaskinnewlist(request):
    if 'sessionuser_id' not in request.session:
        return redirect('account:login')
    
    sessionuser = User.objects.get(pk=int(request.session['sessionuser_id']))
    if request.method=='POST':
        newtaskslist=TasksList()
        newtask=Task()
        if request.POST['listname']!="":
            newtaskslist.list_name=request.POST['listname']
        if request.POST['taskslistdesc']!="":
            newtaskslist.descriptions=request.POST['taskslistdesc']
        newtaskslist.status="NEW"
        newtaskslist.user=User.objects.get(pk=sessionuser.id)
        if request.POST['tasktitle']!="":
            newtask.title=request.POST['tasktitle']
        if request.POST['taskdesc']!="":
            newtask.descriptions=request.POST['taskdesc']
            newtask.status="NEW"
            newtask.created=datetime.now()
        newtask.taskslist=newtaskslist

        newtaskslist.save()
        newtask.save()
        return redirect('todos:home')
    return redirect('todos:home')

def addtaskinexistedlist(request):
    if 'sessionuser_id' not in request.session:
        return redirect('account:login')
    sessionuser = User.objects.get(pk=int(request.session['sessionuser_id']))
    if request.method=='POST':
        newtask=Task()
        taskslist=None
        if request.POST['taskslistid']!="":
            taskslistid=int(request.POST['taskslistid'])

            #print(taskslistid)
            taskslist=TasksList.objects.get(pk=taskslistid)
            newtask.taskslist=taskslist
            newtask.created=datetime.now()
            newtask.status="NEW"
            #print(newtask)
        if request.POST['tasktitle']!="":
            newtask.title=request.POST['tasktitle']
        if request.POST['taskdesc']!="":
            newtask.descriptions=request.POST['taskdesc']
        if taskslist!=None and taskslist.user.id==sessionuser.id:
            newtask.save()
        else:
            print('newtask is not saved.')
        
        return redirect('todos:home')
    return redirect('todos:home')

def edittask(request):
    if 'sessionuser_id' not in request.session:
        return redirect('account:login')
    sessionuser = User.objects.get(pk=int(request.session['sessionuser_id']))
    if request.method=='POST':
        task=None
        
        if request.POST['taskid']!="":
            #taskslistid=int(request.POST['taskslistid'])
            task=Task.objects.get(pk=int(request.POST['taskid']))
            #print(taskslistid)
            #taskslist=TasksList.objects.get(pk=taskslistid)
            #newtask.taskslist=taskslist
            #task.created=datetime.now()
            #task.status="NEW"
            #print(newtask)
        if request.POST['tasktitle']!="":
            task.title=request.POST['tasktitle']
        if request.POST['taskstatus']!="":
            task.status=request.POST['taskstatus']
        if request.POST['taskdesc']!="":
            task.descriptions=request.POST['taskdesc']
        if task!=None and task.taskslist.user.id==sessionuser.id:
            task.save()
        else:
            print('task is not edited.')
        
        return redirect('todos:home')
    return redirect('todos:home')
        

def editsharedtask(request):
    if 'sessionuser_id' not in request.session:
        return redirect('account:login')
    sessionuser = User.objects.get(pk=int(request.session['sessionuser_id']))
    if request.method=='POST':
        task=None
        
        if request.POST['taskid']!="":
            #taskslistid=int(request.POST['taskslistid'])
            task=Task.objects.get(pk=int(request.POST['taskid']))
            #print(taskslistid)
            #taskslist=TasksList.objects.get(pk=taskslistid)
            #newtask.taskslist=taskslist
            #task.created=datetime.now()
            #task.status="NEW"
            #print(newtask)
        
        if request.POST['taskstatus']!="":
            task.status=request.POST['taskstatus']
        
        if task!=None:
            task.save()
        else:
            print('task is not edited.')
        
        return redirect('todos:home')
    return redirect('todos:home')

def sharetasklist(request):
    if 'sessionuser_id' not in request.session:
        return redirect('account:login')
    sessionuser = User.objects.get(pk=int(request.session['sessionuser_id']))
    if request.method=='POST':
        taskslist=None
        sharedtaskslist=SharedTasksList()
        sharewithuser=None
        if request.POST['taskslistid']!="":
            taskslistid=int(request.POST['taskslistid'])
            taskslist=TasksList.objects.get(pk=taskslistid)
            #print(taskslistid)
            #taskslist=TasksList.objects.get(pk=taskslistid)
            #newtask.taskslist=taskslist
            #task.created=datetime.now()
            #task.status="NEW"
            #print(newtask)
        
        if request.POST['userid']!="":
            userid=int(request.POST['userid'])
            sharewithuser=User.objects.get(pk=userid)
        if taskslist!=None and sharewithuser!=None:
            sharedtaskslist.sharedtaskslist=taskslist
            sharedtaskslist.withuser=sharewithuser
            sharedtaskslist.save()
        else:
            print('sharing taskslist is not done.')
        return redirect('todos:home')
    return redirect('todos:home')