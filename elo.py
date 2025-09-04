from main import create_app

app = create_app()
app.app_context().push()

print("Registered endpoints:")
for rule in app.url_map.iter_rules():
    print(rule.endpoint)
