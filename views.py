# -*- encoding:utf8 -*-
from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from talksplanning.models import Batch, Talk, Hacker
from talksplanning.forms import TalkProposalForm, ListenerForm, HackerForm

def home(request):
    """ Homepage """

    batches = Batch.objects.filter(published=True, interne=False)

    return render_to_response('home.html',
                              {'batches':batches},
                             context_instance=RequestContext(request))

def batch_detail(request, id):
    """ Details à propos d'un batch """

    batch = get_object_or_404(Batch, pk=id)
    talks = batch.talk_set.filter(approved=True)

    # hack en attendant mieux
    auditeurs = batch.participants.filter(hackerbatch__auditeur=True)
    auditeurs = list(set(map(lambda _:_.pseudo, auditeurs)))

    form = ListenerForm()

    return render_to_response('batch_detail.html',
                              {
                                  'batch':batch,
                                  'talks':talks,
                                  'auditeurs':auditeurs,
                                  'form':form},
                             context_instance=RequestContext(request))

def batch_form(request, batch_id):
    """ Formulaire inscription à un batch """

    batch = get_object_or_404(Batch, pk=batch_id)

    if request.method == 'POST':
        f = ListenerForm(request.POST)
        if not f.is_valid():
            return render_to_response('batch_detail.html', {'batch':batch, 'form': f}, context_instance=RequestContext(request))
        else:
            listener = f.save(batch)
            return HttpResponseRedirect(reverse('talksplanning:batch_detail', args=(batch.id,)))
    else:
        return HttpResponseRedirect(reverse('talksplanning:batch_detail', args=(batch.id,)))

def talk_form(request, batch_id):
    """ Formulaire proposition de talk pour un batch """

    batch = get_object_or_404(Batch, pk=batch_id)

    if request.method == 'POST':
        fT = TalkProposalForm(request.POST)
        fH = HackerForm(request.POST)
        if not (fT.is_valid() and fH.is_valid()):
            return render_to_response(
                'talk_form.html',
                {'batch':batch,
                 'formTalk': fT,
                 'formHacker': fH},
                context_instance=RequestContext(request))
        else:
            hacker = fH.save()
            talk = fT.save(batch, hacker)
            return HttpResponseRedirect(reverse('talksplanning:batch_detail', args=(batch.id,)))
    else:
        formTalk = TalkProposalForm()
        formHacker = HackerForm()
        return render_to_response(
            'talk_form.html',
            {'batch':batch,
             'formTalk': formTalk,
             'formHacker': formHacker},
            context_instance=RequestContext(request))

