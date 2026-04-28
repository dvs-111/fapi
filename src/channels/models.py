from models import BaseORM, Mapped, mapped_column, ForeignKey, relationship, intpk, str_100

class Post(BaseORM):
	__tablename__ = "posts"

	id: Mapped[intpk]
	title: Mapped[str_100]
	text: Mapped[str]
	author: Mapped[int] = mapped_column(ForeignKey("users.id"))
	channel: Mapped[int] = mapped_column(ForeignKey("channels.id"))

	# rel_author: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[author_id])
	# rel_channel: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[channel_id])

class Channel(BaseORM):
	__tablename__ = "channels"

	id: Mapped[intpk]
	name: Mapped[str]

	rel_subs: Mapped["User"] = relationship(back_populates="rel_channels")

class Chunk(BaseORM):
	__tablename__ = "chunks"

	id: Mapped[intpk]
	name: Mapped[str]