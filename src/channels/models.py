from models import BaseORM, Mapped, mapped_column, ForeignKey, relationship, intpk, str_100
from sqlalchemy import Table, Column, Integer, String, UniqueConstraint

class Post(BaseORM):
	__tablename__ = "posts"

	id: Mapped[intpk]
	title: Mapped[str_100]
	text: Mapped[str]
	author: Mapped[int] = mapped_column(ForeignKey("users.id"))
	channel: Mapped[int] = mapped_column(ForeignKey("channels.id"))

	# rel_author: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[author_id])
	rel_channel: Mapped["Channel"] = relationship(
		"Channel",
		back_populates="rel_posts",
		foreign_keys=[channel],
	)

class Channel(BaseORM):
	__tablename__ = "channels"

	id: Mapped[intpk]
	owner: Mapped[int] = mapped_column(ForeignKey("users.id"))
	name: Mapped[str]

	rel_subs: Mapped[list["User"]] = relationship(
		"User",
		# back_populates="rel_channels",
		secondary="user_channel_subs",
		lazy="selectin"
	)
	rel_posts: Mapped[list["Post"]] = relationship(
		"Post",
		back_populates="rel_channel",
		cascade="all, delete-orphan",
		single_parent=True,
		lazy="selectin",
	)
	rel_chunk: Mapped["Chunk"] = relationship(
		"Chunk",
		secondary="channel_chunk_association",
		back_populates="rel_channels",
		lazy="selectin",
	)

class Chunk(BaseORM):
	__tablename__ = "chunks"

	id: Mapped[intpk]
	name: Mapped[str]

	rel_channels: Mapped[list["Channel"]] = relationship(
		"Channel",
		secondary="channel_chunk_association",
		back_populates="rel_chunk",
		# cascade="all, delete-orphan",
		lazy="selectin",
	)

user_channel_subs = Table(
	"user_channel_subs",
	BaseORM.metadata,
	Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
	Column("channel_id", ForeignKey("channels.id", ondelete="CASCADE"), primary_key=True),
)

channel_chunk_association = Table(
	"channel_chunk_association",
	BaseORM.metadata,
	Column("channel_id", ForeignKey("channels.id", ondelete="CASCADE"), primary_key=True),
	Column("chunk_id", ForeignKey("chunks.id", ondelete="CASCADE"), primary_key=True),

	UniqueConstraint("channel_id", name="uq_channel_in_chunk")
)