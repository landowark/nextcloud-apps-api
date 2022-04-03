import jinja2

notes_template = jinja2.Template(
    '''{% for key, value in params.items() %}{% if loop.first %}?{% endif %}{% if value is string or value is number %}{{key}}={{ value | replace(" ", "+") }}{% else %}{{key}}={% for v in value %}{{ v | replace(" ", "+") }}{% if not loop.last %},{% endif %}{% endfor %}{% endif %}{% if not loop.last %}&{% endif %}{% endfor %}'''
)

bookmarks_template = jinja2.Template(
    '''{% for key, value in params.items() %}{% if loop.first %}?{% endif %}{% if value is string or value is number %}{{key}}={{ value | replace(" ", "+") }}{% else %}{% for v in value %}{{key}}[]={{ v | replace(" ", "+") }}{% if not loop.last %}&{% endif %}{% endfor %}{% endif %}{% if not loop.last %}&{% endif %}{% endfor %}'''
)