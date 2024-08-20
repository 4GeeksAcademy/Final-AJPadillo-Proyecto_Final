from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único
    password = db.Column(db.String(80), nullable=False)  # Contraseña encriptada
    is_active = db.Column(db.Boolean, nullable=False, default=True)  # Estado activo/inactivo
    # Relación uno a muchos: un usuario puede escribir muchas reseñas
    reviews = db.relationship('Review', backref='author', lazy=True)
    # Relación uno a muchos: un usuario puede crear varios posts
    posts = db.relationship('Post', backref='author', lazy=True)
    # Relación uno a muchos: un usuario puede crear varios comentarios
    comments = db.relationship('Comment', backref='author', lazy=True)
    # Relación muchos a muchos: usuarios pueden asistir a varios eventos
    events = db.relationship('Event', secondary='user_events', back_populates='attendees')
    # Preferencias de géneros de videojuegos
    preferred_genres = db.Column(db.String(200))  # Almacena géneros preferidos como una cadena separada por comas

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "preferred_genres": self.preferred_genres,
            "events": [event.serialize() for event in self.events],
            "posts": [post.serialize() for post in self.posts],
            "reviews": [review.serialize() for review in self.reviews]
        }

# Modelo de Videojuego
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)  # ID único del videojuego
    name = db.Column(db.String(120), nullable=False)  # Nombre del videojuego
    genres = db.Column(db.String(200), nullable=False)  # Géneros del videojuego
    about = db.Column(db.Text, nullable=False)  # Descripción del videojuego
    # Relación uno a muchos: un videojuego puede tener muchas reseñas
    reviews = db.relationship('Review', backref='game', lazy=True)

    def __repr__(self):
        return f'<Game {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "about": self.about,
            "reviews": [review.serialize() for review in self.reviews]
        }

# Modelo de Reseña
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)  # ID único de la reseña
    content = db.Column(db.Text, nullable=False)  # Contenido de la reseña
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID del usuario que escribió la reseña
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)  # ID del videojuego reseñado

    def __repr__(self):
        return f'<Review {self.id} for Game {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "game_id": self.game_id
        }

# Modelo de Evento
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)  # ID único del evento
    name = db.Column(db.String(120), nullable=False)  # Nombre del evento
    description = db.Column(db.Text, nullable=False)  # Descripción del evento
    date = db.Column(db.DateTime, nullable=False)  # Fecha del evento
    # Relación muchos a muchos con usuarios
    attendees = db.relationship('User', secondary='user_events', back_populates='events')

    def __repr__(self):
        return f'<Event {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "attendees": [user.serialize() for user in self.attendees]
        }

# Tabla de asociación para la relación muchos a muchos entre User y Event
user_events = db.Table('user_events',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)
)

# Modelo de Post
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)  # ID único del post
    title = db.Column(db.String(120), nullable=False)  # Título del post
    content = db.Column(db.Text, nullable=False)  # Contenido del post
    image_url = db.Column(db.String(255))  # URL de la imagen (opcional)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID del usuario que creó el post
    # Relación uno a muchos: un post puede tener muchos comentarios
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "image_url": self.image_url,
            "user_id": self.user_id,
            "comments": [comment.serialize() for comment in self.comments]
        }

# Modelo de Comentario
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)  # ID único del comentario
    content = db.Column(db.Text, nullable=False)  # Contenido del comentario
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID del usuario que escribió el comentario
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # ID del post al que pertenece el comentario

    def __repr__(self):
        return f'<Comment {self.id} for Post {self.post_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
