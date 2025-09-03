from pymongo import MongoClient

client = MongoClient("mongodb+srv://glouloudorra7:2VMbnEHFf1uiwvLU@cluster0.z6ezz9f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["pawmatch"]
pets_collection = db["pets"]


pets_collection.delete_many({})

pets = [
    # 🐶 Dogs (12)
    {"name": "Loulou", "type": "Dog", "breed": "Golden Retriever", "age": "2 years",
     "size": "Large", "activity": "high", "temperament": "Friendly, Loyal",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "images/golden_retriever.jpg",
     "description": "Golden fur, affectionate and playful."},

    {"name": "Max", "type": "Dog", "breed": "Beagle", "age": "1 year",
     "size": "Medium", "activity": "moderate", "temperament": "Curious, Energetic",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "images/beagle.jpeg",
     "description": "Adventurous scent hound."},

    {"name": "Bella", "type": "Dog", "breed": "Bulldog", "age": "4 years",
     "size": "Medium", "activity": "low", "temperament": "Calm, Affectionate",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "images/bella.jpg",
     "description": "Gentle bulldog, perfect for indoors."},

    {"name": "Simba", "type": "Dog", "breed": "German Shepherd", "age": "3 years",
     "size": "Large", "activity": "high", "temperament": "Protective, Brave",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": True,
     "image": "https://images.pexels.com/photos/333083/pexels-photo-333083.jpeg",
     "description": "Loyal guardian, needs active family."},

    {"name": "Snowball", "type": "Dog", "breed": "Poodle", "age": "5 years",
     "size": "Small", "activity": "high", "temperament": "Smart, Playful",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "https://images.pexels.com/photos/191353/pexels-photo-191353.jpeg",
     "description": "Fluffy, hypoallergenic, and clever."},

    {"name": "Chams", "type": "Dog", "breed": "Siberian Husky", "age": "3 years",
     "size": "Large", "activity": "high", "temperament": "Energetic, Independent",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": True,
     "image": "images/Siberian_Husky.jpg",
     "description": "High-energy sled dog, loves outdoors."},

    {"name": "Daisy", "type": "Dog", "breed": "Labrador", "age": "2 years",
     "size": "Large", "activity": "high", "temperament": "Gentle, Friendly",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "https://images.pexels.com/photos/8700/wall-animal-dog-pet.jpg",
     "description": "Classic family dog, very playful."},

    {"name": "Zina", "type": "Dog", "breed": "Maltese", "age": "1 year",
     "size": "Small", "activity": "moderate", "temperament": "Affectionate, Gentle",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Maltese.jpg",
     "description": "Tiny and adorable lapdog."},

    {"name": "Rocky", "type": "Dog", "breed": "Rottweiler", "age": "4 years",
     "size": "Large", "activity": "high", "temperament": "Confident, Protective",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": True,
     "image": "images/Rottweiler.jpg",
     "description": "Strong protector, best for experienced owners."},

    {"name": "Misk", "type": "Dog", "breed": "Shih Tzu", "age": "3 years",
     "size": "Small", "activity": "low", "temperament": "Gentle, Calm",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Shih_Tzu.webp",
     "description": "Loving and hypoallergenic companion."},

    {"name": "Balha", "type": "Dog", "breed": "Chihuahua", "age": "2 years",
     "size": "Small", "activity": "moderate", "temperament": "Alert, Bold",
     "hypoallergenic": False, "good_with_children": False, "needs_experience": False,
     "image": "https://images.pexels.com/photos/39317/chihuahua-dog-puppy-cute-39317.jpeg",
     "description": "Tiny but fearless dog."},

    {"name": "Charlie", "type": "Dog", "breed": "Dachshund", "age": "2 years",
     "size": "Small", "activity": "moderate", "temperament": "Curious, Brave",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "images/Dachshund.jpg",
     "description": "Small but adventurous sausage dog."},

    # 🐱 Cats (8)
    {"name": "Simba Jr.", "type": "Cat", "breed": "Maine Coon", "age": "3 years",
     "size": "Large", "activity": "moderate", "temperament": "Gentle, Intelligent",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "https://images.pexels.com/photos/617278/pexels-photo-617278.jpeg",
     "description": "Big fluffy cat with gentle nature."},

    {"name": "Kiwi", "type": "Cat", "breed": "Persian", "age": "4 years",
     "size": "Small", "activity": "low", "temperament": "Sweet, Quiet",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "https://images.pexels.com/photos/20787/pexels-photo.jpg",
     "description": "Fluffy indoor lap cat."},

    {"name": "Maya", "type": "Cat", "breed": "Siamese", "age": "1 year",
     "size": "Medium", "activity": "high", "temperament": "Talkative, Social",
     "hypoallergenic": False, "good_with_children": False, "needs_experience": False,
     "image": "https://images.pexels.com/photos/45170/kittens-cat-cat-puppy-rush-45170.jpeg",
     "description": "Chatty and affectionate Siamese."},

    {"name": "Tiger", "type": "Cat", "breed": "Bengal", "age": "2 years",
     "size": "Medium", "activity": "high", "temperament": "Active, Playful",
     "hypoallergenic": False, "good_with_children": False, "needs_experience": True,
     "image": "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg",
     "description": "Athletic and playful Bengal."},

    {"name": "Zitouna", "type": "Cat", "breed": "British Shorthair", "age": "2 years",
     "size": "Medium", "activity": "low", "temperament": "Calm, Independent",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "images/British_Shorthair.jpeg",
     "description": "Calm and plush-coated kitty."},

    {"name": "Luna", "type": "Cat", "breed": "Ragdoll", "age": "2 years",
     "size": "Medium", "activity": "low", "temperament": "Gentle, Relaxed",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "images/Ragdoll.jpg",
     "description": "Soft and affectionate cat."},

    {"name": "Milo", "type": "Cat", "breed": "Abyssinian", "age": "2 years",
     "size": "Medium", "activity": "high", "temperament": "Energetic, Curious",
     "hypoallergenic": False, "good_with_children": True, "needs_experience": False,
     "image": "https://images.pexels.com/photos/979247/pexels-photo-979247.jpeg",
     "description": "Curious cat, loves climbing."},

    {"name": "Safi", "type": "Cat", "breed": "Sphynx", "age": "3 years",
     "size": "Small", "activity": "moderate", "temperament": "Affectionate, Curious",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": True,
     "image": "images/Sphynx.jpg",
     "description": "Hairless hypoallergenic cat."},

    # 🐰 Rabbits (3)
    {"name": "Snowy", "type": "Rabbit", "breed": "Mini Lop", "age": "1 year",
     "size": "Small", "activity": "moderate", "temperament": "Gentle, Playful",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Mini_Lop.jpg",
     "description": "Cute and fluffy rabbit."},

    {"name": "Caramel", "type": "Rabbit", "breed": "Angora", "age": "2 years",
     "size": "Small", "activity": "low", "temperament": "Calm, Gentle",
     "hypoallergenic": False, "good_with_children": False, "needs_experience": True,
     "image": "images/Angora.jpg",
     "description": "Fluffy rabbit, needs grooming."},

    {"name": "Coco", "type": "Rabbit", "breed": "Rex", "age": "2 years",
     "size": "Small", "activity": "moderate", "temperament": "Friendly, Active",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Rex.jpeg",
     "description": "Playful bunny with soft fur."},

    # 🐦 Birds (3)
    {"name": "Kiwi", "type": "Bird", "breed": "Parrot", "age": "5 years",
     "size": "Small", "activity": "high", "temperament": "Talkative, Social",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": True,
     "image": "images/Parrot.jpg",
     "description": "Talkative parrot, loves music."},

    {"name": "Sunny", "type": "Bird", "breed": "Canary", "age": "1 year",
     "size": "Small", "activity": "moderate", "temperament": "Cheerful, Musical",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Canary.JPG",
     "description": "Cheerful canary, bright song."},

    {"name": "Peach", "type": "Bird", "breed": "Cockatiel", "age": "2 years",
     "size": "Small", "activity": "moderate", "temperament": "Friendly, Curious",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Cockatiel.jpg",
     "description": "Sweet cockatiel, whistles tunes."},

    # 🐹 Small Pets (4)
    {"name": "Doudou", "type": "Hamster", "breed": "Syrian Hamster", "age": "6 months",
     "size": "Small", "activity": "high", "temperament": "Curious, Independent",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Syrian_Hamster.JPG",
     "description": "Tiny curious hamster."},

    
    {"name": "Sammy", "type": "Turtle", "breed": "Greek Tortoise", "age": "12 years",
     "size": "Small", "activity": "low", "temperament": "Calm, Quiet",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": True,
     "image": "images/Greek_Tortoise.jpeg",
     "description": "Slow but steady companion."},

    {"name": "Choco", "type": "Hamster", "breed": "Dwarf Hamster", "age": "8 months",
     "size": "Small", "activity": "high", "temperament": "Energetic, Playful",
     "hypoallergenic": True, "good_with_children": True, "needs_experience": False,
     "image": "images/Dwarf_Hamster.jpg",
     "description": "Energetic hamster, loves tunnels."},
]

pets_collection.insert_many(pets)
print(f"Inserted {len(pets)} pets into MongoDB!")
