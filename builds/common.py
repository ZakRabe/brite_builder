from .models import Loadout, Build
from champs.models import Champ
from .forms import BuildForm
from brite_builder.templatetags.html_filters import champName
from django.shortcuts import render, get_object_or_404

def create_loadout(data, request):
        for attr in ['talent_0','talent_1','talent_2','talent_3', 'talent_4']:
            if data['loadout'][attr] is not None:
                data[attr+"_id"] = data['loadout'][attr]['id']
        data.update(data.get('build'))
        data.update(data.get('loadout'))

        referer = request.META.get('HTTP_REFERER')
        champ_name = referer.split('/')[3]
        champ = get_object_or_404(Champ,title__iexact=champName(champ_name))
        data['champ_name'] = champ_name
        build_data = data.get('build', {});
        data['title'] = build_data.get('title', "Unnamed Loadout")
        data['description'] = build_data.get('description', "")
        data['id'] = build_data.get('id', None)
        form = BuildForm(data)


        if not form.is_valid():
            return {"errors":form.errors, "data":data}

        clean = form.cleaned_data


        # look up if there's an existing loadout for this build_hash
        loadout = Loadout.objects.filter(build_hash=clean.get('build_hash'))
        if loadout.count() == 0:
            # strip our validation values
            del clean['champ_name']
            title = clean['title']
            description = clean['description']
            del clean['title']
            del clean['description']
            # create new loadout for the build
            loadout = Loadout(**clean)
            loadout.save()
            clean['title'] = title
            clean['description'] = description
        else:
            loadout = loadout[0]


        return {'loadout':loadout, "clean":clean}