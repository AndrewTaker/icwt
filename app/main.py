from app import create_app


def print_routes(app):
    for rule in app.url_map.iter_rules():
        print(rule, rule.methods)


if __name__ == "__main__":
    app = create_app()
    print_routes(app)
    app.run(debug=True)
