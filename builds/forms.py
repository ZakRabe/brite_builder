import json
from django import forms
from talents.models import Talent, SpecialTalent
from django.db.models import Q
from django.core.exceptions import ValidationError

class BuildForm(forms.Form):
    title       = forms.CharField(max_length=150,required=False)
    description = forms.CharField(max_length=500,required=False)
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
                self._errors["valid"] = ['A Loadout must have 5 Battlerites to Title it. You can still share an incomplete Loadout using the link below']
                return cleaned_data
            if talent_ids.count(talent_id) > 1:
                self._errors["valid"] = ['You cant fool me, dummy...']
                return cleaned_data

        special = SpecialTalent.objects.filter(champ__title__iexact=champ_name, talent_id__in=talent_ids).count()
        talents = Talent.objects.filter(spell__champ__title__iexact=champ_name,id__in=talent_ids).count()

        if talents + special < 5:
            self._errors["valid"] = ["Talents don't belong to the right champ"]
            # self._errors["debug"] = [special, talents]
            return cleaned_data

        build_hash = json.dumps(talent_ids)
        cleaned_hash = cleaned_data.get('build_hash', "")

        if cleaned_hash == "":
            # self._errors["valid"] = build_hash
            cleaned_data['build_hash'] = build_hash
        title = cleaned_data.get("title", "")
        if title  == "" or title == "New Loadout":
            cleaned_data['title'] = "Unnamed Loadout"

        # incase we're sent null
        cleaned_data['description'] = cleaned_data.get('description', "")

        return cleaned_data





