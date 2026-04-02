from django import template

register = template.Library()

@register.filter
def tag_color(tag):
    colors = {
        'VERT': 'green',
        'JAUNE': 'amber',
        'ROUGE': 'red',
    }
    return colors.get(tag, 'gray')  # gris par défaut



###
###utilistation {% load colors %}
"""
 <td class="border px-4 py-2 text-center font-bold bg-{{ boite.tag|tag_color }}-100 text-{{ boite.tag|tag_color }}-800 border-{{ boite.tag|tag_color }}-300">
    {{ boite.get_tag_display }}
 </td>

"""