from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel

app = FastAPI()

ENGINE = create_engine("sqlite:///./test.db", echo=True)
Base = declarative_base()
mksess = sessionmaker(bind=ENGINE)

# Раскидка по банкам
member_association = Table(
    "member_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("chunk_id", ForeignKey("chunks.id"), primary_key=True),
)

post_association = Table(
    "post_association",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("chunk_id", ForeignKey("chunks.id"), primary_key=True),
)

# ===============================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    admin_profile = relationship("AdminProfile", uselist=False, back_populates="user", cascade="all, delete, delete-orphan")
    owned_chunks = relationship("Chunk", back_populates="owner", cascade="all, delete, delete-orphan")
    chunks = relationship("Chunk", secondary=member_association, back_populates="members")

class AdminProfile(Base):
    __tablename__ = "admin_profiles"
    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="admin_profile")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_users = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="owned_chunks")
    members = relationship("User", secondary=member_association, back_populates="chunks", cascade="save-update, merge")
    posts = relationship("Post", secondary=post_association, back_populates="chunks")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    chunks = relationship("Chunk", secondary=post_association, back_populates="posts", cascade="save-update, merge")

Base.metadata.create_all(ENGINE)

# Pydantic schemas
class ProfileCreate(BaseModel):
    level: int

class ProfileResponse(BaseModel):
    id: int
    level: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class UserWithProfileCreate(BaseModel):
    user: UserCreate
    admin_profile: ProfileCreate

class UserWithProfileResponse(BaseModel):
    user: UserResponse
    admin_profile: ProfileResponse

class ChunkCreate(BaseModel):
    name: str
    max_users: int

class ChunkResponse(BaseModel):
    id: int
    name: str
    max_users: int
    owner: UserResponse
    members: List[UserResponse] = []
    posts: List["PostResponse"] = []

    class Config:
        from_attributes = True

class UserWithChunksCreate(BaseModel):
    user: UserCreate
    chunks: List[ChunkCreate]

class UserWithChunksResponse(BaseModel):
    user: UserResponse
    owned_chunks: List[ChunkResponse]

class PostCreate(BaseModel):
    content: str
    chunk_ids: List[int]

class PostResponse(BaseModel):
    id: int
    content: str
    chunks: List[ChunkResponse]

    class Config:
        from_attributes = True

class MemberAdd(BaseModel):
    user_id: int

# DB dependency
def get_db():
    db = mksess()
    try:
        yield db
    finally:
        db.close()

# Создавать нормисов
@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Одмены
@app.post("/one_to_one", response_model=UserWithProfileResponse)
def create_user_profile(data: UserWithProfileCreate, db: Session = Depends(get_db)):
    user_data = data.user.model_dump()
    user = User(**user_data)
    profile_data = data.admin_profile.model_dump()
    profile = AdminProfile(**profile_data)
    user.admin_profile = profile
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserWithProfileResponse(user=user, admin_profile=user.admin_profile)

@app.get("/one_to_one/{user_id}", response_model=UserWithProfileResponse)
def read_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.admin_profile:
        raise HTTPException(status_code=404, detail="No admin profile")
    return UserWithProfileResponse(user=user, admin_profile=user.admin_profile)

@app.put("/one_to_one/{user_id}", response_model=UserWithProfileResponse)
def update_user_profile(user_id: int, data: UserWithProfileCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = data.user.model_dump()
    for key, value in user_data.items():
        setattr(user, key, value)
    if user.admin_profile:
        profile_data = data.admin_profile.model_dump()
        for key, value in profile_data.items():
            setattr(user.admin_profile, key, value)
    else:
        profile_data = data.admin_profile.model_dump()
        profile = AdminProfile(**profile_data)
        user.admin_profile = profile
    db.commit()
    db.refresh(user)
    return UserWithProfileResponse(user=user, admin_profile=user.admin_profile)

@app.delete("/one_to_one/{user_id}")
def delete_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

# Pair 2: 1-M (User and Chunk for ownership)
@app.post("/one_to_many", response_model=UserWithChunksResponse)
def create_user_chunks(data: UserWithChunksCreate, db: Session = Depends(get_db)):
    user_data = data.user.model_dump()
    user = User(**user_data)
    for chunk_data in data.chunks:
        chunk_dict = chunk_data.model_dump()
        chunk = Chunk(**chunk_dict)
        user.owned_chunks.append(chunk)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserWithChunksResponse(user=user, owned_chunks=user.owned_chunks)

@app.get("/one_to_many/{user_id}", response_model=UserWithChunksResponse)
def read_user_chunks(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserWithChunksResponse(user=user, owned_chunks=user.owned_chunks)

@app.put("/one_to_many/{user_id}", response_model=UserWithChunksResponse)
def update_user_chunks(user_id: int, data: UserWithChunksCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = data.user.model_dump()
    for key, value in user_data.items():
        setattr(user, key, value)
    # Replace chunks for simplicity
    for chunk in user.owned_chunks[:]:
        db.delete(chunk)
    user.owned_chunks = []
    for chunk_data in data.chunks:
        chunk_dict = chunk_data.model_dump()
        chunk = Chunk(**chunk_dict)
        user.owned_chunks.append(chunk)
    db.commit()
    db.refresh(user)
    return UserWithChunksResponse(user=user, owned_chunks=user.owned_chunks)

@app.delete("/one_to_many/{user_id}")
def delete_user_chunks(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

# Посты в банках
@app.post("/many_to_many", response_model=PostResponse)
def create_post_chunks(data: PostCreate, db: Session = Depends(get_db)):
    post = Post(content=data.content)
    for chunk_id in data.chunk_ids:
        chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
        if not chunk:
            raise HTTPException(status_code=404, detail=f"Chunk {chunk_id} not found")
        post.chunks.append(chunk)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/many_to_many/{post_id}", response_model=PostResponse)
def read_post_chunks(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/many_to_many/{post_id}", response_model=PostResponse)
def update_post_chunks(post_id: int, data: PostCreate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.content = data.content
    post.chunks = []
    for chunk_id in data.chunk_ids:
        chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
        if not chunk:
            raise HTTPException(status_code=404, detail=f"Chunk {chunk_id} not found")
        post.chunks.append(chunk)
    db.commit()
    db.refresh(post)
    return post

@app.delete("/many_to_many/{post_id}")
def delete_post_chunks(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"ok": True}

# Membership management (M-M User and Chunk) with limit check
@app.post("/chunks/{chunk_id}/members")
def add_member(chunk_id: int, data: MemberAdd, db: Session = Depends(get_db)):
    chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if len(chunk.members) >= chunk.max_users:
        raise HTTPException(status_code=400, detail="Chunk has reached maximum users")
    if user in chunk.members:
        raise HTTPException(status_code=400, detail="User already a member")
    chunk.members.append(user)
    db.commit()
    return {"ok": True}

@app.delete("/chunks/{chunk_id}/members/{user_id}")
def remove_member(chunk_id: int, user_id: int, db: Session = Depends(get_db)):
    chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user in chunk.members:
        chunk.members.remove(user)
        db.commit()
    return {"ok": True}

# Admin view of chunks as channels
@app.get("/admins/{admin_id}/channels", response_model=List[ChunkResponse])
def get_admin_channels(admin_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == admin_id).first()
    if not user or not user.admin_profile:
        raise HTTPException(status_code=404, detail="Admin not found")
    return user.owned_chunks