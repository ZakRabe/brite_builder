import json
from django import forms
from talents.models import Talent

from django.core.exceptions import ValidationError

class BuildForm(forms.Form):
    id          = forms.IntegerField(required=False)
    title       = forms.CharField(max_length=200,required=False)
    description = forms.CharField(max_length=200,required=False)
    build_hash  = forms.CharField(max_length=200,required=False)
    talent_0_id = forms.IntegerField(required=False)
    talent_1_id = forms.IntegerField(required=False)
    talent_2_id = forms.IntegerField(required=False)
    talent_3_id = forms.IntegerField(required=False)
    talent_4_id = forms.IntegerField(required=False)

    champ_name = forms.CharField(max_length=200,required=True)

    def clean(self):
        cleaned_data = super(BuildForm, self).clean()
        champ_name = cleaned_data.get("champ_name")

        # make sure talents belong to the champ
        talent_0_id = cleaned_data.get('talent_0_id')
        talent_1_id = cleaned_data.get('talent_1_id')
        talent_2_id = cleaned_data.get('talent_2_id')
        talent_3_id = cleaned_data.get('talent_3_id')
        talent_4_id = cleaned_data.get('talent_4_id')
        talent_ids = sorted([talent_0_id,talent_1_id, talent_2_id, talent_3_id, talent_4_id]);

        for talent_id in talent_ids:
            if talent_id is None:
                self._errors["valid"] = ['Loadout must have 5 Battlerites']
                return cleaned_data
            if talent_ids.count(talent_id) > 1:
                self._errors["valid"] = ['You cant fool me, dummy...']
                return cleaned_data


        talents = Talent.objects.filter(id__in=talent_ids, spell__champ__title__iexact=champ_name).count()

        if talents < 5:
            self._errors["valid"] = ["Talents don't belong to the right champ"]
            return cleaned_data

        build_hash = json.dumps(talent_ids)
        cleaned_hash = cleaned_data.get('build_hash', "")

        if cleaned_hash == "":
            # self._errors["valid"] = build_hash
            cleaned_data['build_hash'] = build_hash

        if cleaned_data.get("title", "") =="":
            cleaned_data['title'] = "Unnamed Build"

        # incase we're sent null
        cleaned_data['description'] = cleaned_data.get('description', "")

        return cleaned_data





