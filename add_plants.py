from database_setup import db, Plant, app

def add_plants():
    plants = [
        {
            "name": "Tulsi",
            "scientific_name": "Ocimum tenuiflorum",
            "common_names": "Holy Basil",
            "habitat": "Tropical and subtropical regions",
            "medicinal_uses": "Used for treating cough, cold, and fever",
            "cultivation": "Grows well in warm climates",
            "image": "https://example.com/tulsi.jpg",
            "wikipedia": "https://en.wikipedia.org/wiki/Ocimum_tenuiflorum",
            "model": "https://example.com/tulsi.glb"
        },
        {
            "name": "Aloe Vera",
            "scientific_name": "Aloe barbadensis miller",
            "common_names": "Ghritkumari",
            "habitat": "Dry, tropical climates",
            "medicinal_uses": "Used for skin treatment, burns, and digestion",
            "cultivation": "Grows well in sandy soil with minimal water",
            "image": "https://example.com/aloevera.jpg",
            "wikipedia": "https://en.wikipedia.org/wiki/Aloe_vera",
            "model": "https://example.com/aloevera.glb"
        }
    ]

    with app.app_context():
        for plant_data in plants:
            if not Plant.query.filter_by(name=plant_data["name"]).first():
                new_plant = Plant(**plant_data)
                db.session.add(new_plant)

        db.session.commit()
        print("Plants added successfully!")

if __name__ == '__main__':
    add_plants()
