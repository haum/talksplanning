# -*- coding:utf8 -*-

from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory

from talksplanning.models import Talk, Hacker, HackerBatch

class HackerForm(forms.ModelForm):

    class Meta:
        model = Hacker

    def save(self):

        return Hacker.objects.get_or_create(
            pseudo=self.cleaned_data['pseudo'],
            mail=self.cleaned_data['mail'],
            haum=self.cleaned_data.get('haum') # can be blank
        )[0] # indice comme pour le TalkProposalForm


class TalkProposalForm(forms.ModelForm):
    """ Form to propose a talk """

    class Meta:
        model = Talk
        fields = ['titre', 'url', 'description']


    def save(self, batch, speaker):

        # shorter is better
        cd = self.cleaned_data

        # == Talk ==
        talk = Talk()
        talk.titre = cd['titre']
        talk.description = cd['description']
        talk.url = cd.get('url') # may be None
        talk.approved = True # TODO: change that when moderation will be set
        talk.speaker = speaker
        talk.batch = batch
        talk.save()

        return talk

class ListenerForm(HackerForm):
    """ Form to register as a litener """

    def save(self, batch):

        listener = super(HackerForm, self).save()
        HackerBatch(batch=batch, hacker=listener).save()
        return listener
